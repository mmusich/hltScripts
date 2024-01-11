#!/usr/bin/env python3
import os
import argparse
import json
import fnmatch
import statistics

from omsapi import OMSAPI

def getOMSAPI_krb():
#    print("Calling  getOMSAPI_krb()")
    omsapi = OMSAPI("https://cmsoms.cern.ch/agg/api", "v1")
    omsapi.auth_krb()
    return omsapi

def getOMSAPI_oidc(appSecret):
#    print("Calling  getOMSAPI_oidc(appSecret)")
    omsapi = OMSAPI("https://cmsoms.cern.ch/agg/api", "v1", cert_verify=False)
    omsapi.auth_oidc("cms-tsg-oms-ntuple", appSecret)
    return omsapi

def getOMSAPI(appSecret=""):
    if appSecret == "":
#        print("### No CERN OpenID secret found. Trying using kerberos, but it will work only from lxplus! ( https://gitlab.cern.ch/cmsoms/oms-api-client#alternative-auth-option )")
        return getOMSAPI_krb()
    else:
        try:
            return getOMSAPI_oidc(appSecret)
        except:
#            print("### Problems with CERN OpenID secret found. Trying using kerberos, but it will work only from lxplus! ( https://gitlab.cern.ch/cmsoms/oms-api-client#alternative-auth-option )")
            return getOMSAPI_krb()

def getAppSecret(appSecret = "", appSecretLocation = "~/private/oms.sct"):
    if appSecret == "":
        fName = os.path.expanduser(appSecretLocation)
        if os.path.exists(fName):
            f = open(fName)
            return f.read()[:-1]
    return appSecret ## return "" if appSecret is not found

# Set up argument parser
parser = argparse.ArgumentParser(description='Script to get trigger-rate data of selected Fills from OMS')
parser.add_argument('-i', '--input-json', dest='input_json', default=None, help='Path to input .json file (alternative to fetching data from OMS)')
parser.add_argument('-y', '--years', dest='years', nargs='+', default=["2011", "2012", "2015", "2016", "2017", "2018", "2022", "2023"], help='List of data-taking years')
parser.add_argument('-f', '--fill', dest='fill', type=int, default=None, help='Fill number')
parser.add_argument('--fill-hours-min', type=int, default=None, help='Minimum number of hours in the Fill')
parser.add_argument('--fill-hours-max', type=int, default=None, help='Maximum number of hours in the Fill')
parser.add_argument('-n', '--fills-per-year', type=int, default=1, help='Number of Fills selected per year')
parser.add_argument('-s', '--sort-fills-by', dest='fill_sort', default="delivered_lumi", help='Attribute used to sort Fills')
parser.add_argument('-t', '--type', dest='rate_type', default="streams", choices=["streams", "datasetrates"], help='Attribute to extract HLT rates ("streams" or "datasetrates")')
parser.add_argument('-o', '--output', type=str, default='tmp.json', help='Output JSON file')
args = parser.parse_args()

ret = {}

# if input json file is specified, use that directly
if args.input_json != None:
  ret = json.load(open(args.input_json))
# otherwise, fetch data from OMS
else:
  # Initialize OMS API with secret
  omsapi = getOMSAPI(getAppSecret())

  for year in args.years:
   print(f'\nYear {year}')
   q_fills = omsapi.query("fills")
   q_fills.set_verbose(False)
   q_fills.filter("start_time", f"{year}-01-01T00:00:01Z", "GE")
   q_fills.filter("end_time", f"{year}-12-31T23:59:59Z", "LE")

   # select a single Fill by its number
   if args.fill != None:
     q_fills.filter("fill_number", args.fill)

   # sort all the selected Fill by args.fill_sort
   else:
     q_fills.filter("b_field", 3.6, "GE")
     q_fills.filter("energy", 3000, "GE")
     q_fills.filter("stable_beams", True)
     q_fills.filter("fill_type_runtime", "PROTONS")

     if args.fill_hours_min != None:
         q_fills.filter("duration", 3600*args.fill_hours_min, "GE")

     if args.fill_hours_max != None:
         q_fills.filter("duration", 3600*args.fill_hours_max, "LE")

     q_fills.sort(args.fill_sort, asc=False)

   q_fills.paginate(page=1, per_page=int(args.fills_per_year))

   data_fills = q_fills.data()
   data_fills_dict = data_fills.json()['data']

   ret[year] = []

   for fill_i in data_fills_dict:
    print(f'  Fill {fill_i["id"]}')
    fill_dict = {"fill_number": fill_i["id"]}
    for foo in [
      "bunches_colliding",
      "peak_lumi",
      "delivered_lumi",
      "duration",
      "energy",
      "start_time",
      "end_time",
    ]:
      fill_dict[foo] = fill_i["attributes"][foo]

    # convert "peak_lumi" to E34 cm^-2 s^-1
    try: fill_dict["peak_lumi"] /= 10**(34-int(fill_i['meta']['row']['peak_lumi']['units'][4:6]))
    except: pass

    q_runs = omsapi.query("runs")
    q_runs.set_verbose(False)
    q_runs.filter("fill_number", fill_i["id"])
    q_runs.sort("run_number", asc=True)
    q_runs.paginate(page=1, per_page=1)
    data_runs = q_runs.data()
    data_runs_dict = data_runs.json()
    ntot_runs = data_runs_dict["meta"]["totalResourceCount"]
    npages_runs = int(1+ntot_runs/1e5)
    runs = []
    for page_idx in range(1, 1+npages_runs):
      q_runs.paginate(page=page_idx, per_page=int(1e5))
      data_runs = q_runs.data()
      data_runs_dict = data_runs.json()['data']
      for run_i in data_runs_dict:
        hlt_key = run_i["attributes"]["hlt_key"]
        if not isinstance(hlt_key, str): hlt_key = ''
        if hlt_key.startswith("/cdaq/physics/"):
          runs.append(run_i["id"])
    runs = sorted(list(set(runs)))

    ntot_lumis = 0
    rate_Physics = 0.
    rate_Ephemeral = 0.
    rate_Parking = 0.
    rate_Scouting = 0.

    for run_i in runs:
      q_lumis = omsapi.query("lumisections")
      q_lumis.set_verbose(False)
      q_lumis.filter("run_number", run_i)
      q_lumis.paginate(page=1, per_page=1)
      data_lumis = q_lumis.data()
      data_lumis_dict = data_lumis.json()
      ntot_lumis_tmp = data_lumis_dict["meta"]["totalResourceCount"]
      npages_lumis = int(1+ntot_lumis/1e5)
      lumis = []
      for page_idx in range(1, 1+npages_lumis):
        q_lumis.paginate(page=page_idx, per_page=int(1e5))
        data_lumis_dict = q_lumis.data().json()['data']
        for lumi_i in data_lumis_dict:
          if not lumi_i["attributes"]["beams_stable"]:
            continue
          lumis.append(int(lumi_i["id"].split('_')[1]))

      print(f'    run {run_i} (selected LSs = {len(lumis)})')

      for lumi_i in lumis:
        q_streams = omsapi.query(args.rate_type)
        q_streams.set_verbose(False)
        q_streams.filter("run_number", run_i)
        q_streams.filter("last_lumisection_number", lumi_i)
        q_streams.paginate(page=1, per_page=1)
        data_streams = q_streams.data()
        data_streams_dict = data_streams.json()

        if "meta" not in data_streams_dict:
            print(f'      ERROR -- no stream-rate data (lumisection = {lumi_i})')
            rate_Physics = 0
            rate_Ephemeral = 0
            rate_Parking = 0
            rate_Scouting = 0
            break

        ntot_streams = data_streams_dict["meta"]["totalResourceCount"]

        if ntot_streams == 0:
            continue

        ntot_lumis += 1

        npages_streams = int(1+ntot_streams/1e5)
        for page_idx in range(1, 1+npages_streams):
          q_streams.paginate(page=page_idx, per_page=int(1e5))
          data_streams = q_streams.data()
          data_streams_dict = data_streams.json()['data']
          for stream_i in data_streams_dict:
            streamName_i = stream_i['attributes']['stream_name']
            streamRate_i = stream_i['attributes']['rate']

            if year != "2012":
              if streamName_i.startswith('Physics'):
                rate_Physics += streamRate_i

              if fnmatch.fnmatch(streamName_i, 'Physics*HLTPhysics*') or fnmatch.fnmatch(streamName_i, 'Physics*ZeroBias*'):
                rate_Ephemeral += streamRate_i

              elif streamName_i.startswith('Parking'):
                rate_Parking += streamRate_i

              elif streamName_i.startswith('Scouting'):
                rate_Scouting += streamRate_i

            else:
              if streamName_i == "A":
                rate_Physics += streamRate_i

              elif streamName_i.startswith('PhysicsDST'):
                rate_Scouting += streamRate_i

        if year != "2012":
          continue

        q_datasets = omsapi.query("datasetrates")
        q_datasets.set_verbose(False)
        q_datasets.filter("run_number", run_i)
        q_datasets.filter("last_lumisection_number", lumi_i)
        q_datasets.paginate(page=1, per_page=1)
        data_datasets = q_datasets.data()
        data_datasets_dict = data_datasets.json()

        if "meta" not in data_datasets_dict:
            print(f'      ERROR -- no dataset-rate data (lumisection = {lumi_i})')
            rate_Physics = 0
            rate_Ephemeral = 0
            rate_Parking = 0
            rate_Scouting = 0
            break

        ntot_datasets = data_datasets_dict["meta"]["totalResourceCount"]
        npages_datasets = int(1+ntot_datasets/1e5)
        for page_idx in range(1, 1+npages_datasets):
          q_datasets.paginate(page=page_idx, per_page=int(1e5))
          data_datasets = q_datasets.data()
          data_datasets_dict = data_datasets.json()['data']
          for dataset_i in data_datasets_dict:
            datasetName_i = dataset_i['attributes']['dataset_name']
            datasetRate_i = dataset_i['attributes']['rate']

            if datasetName_i.endswith("Parked"):
              rate_Parking += datasetRate_i
              rate_Physics -= datasetRate_i

    if ntot_lumis > 0:
      rate_Physics /= ntot_lumis
      rate_Ephemeral /= ntot_lumis
      rate_Parking /= ntot_lumis
      rate_Scouting /= ntot_lumis

    fill_dict["rate_Physics"] = rate_Physics
    fill_dict["rate_Ephemeral"] = rate_Ephemeral
    fill_dict["rate_Parking"] = rate_Parking
    fill_dict["rate_Scouting"] = rate_Scouting

    ret[year].append(fill_dict)

    # save intermediate results
    json.dump(ret, open(args.output, 'w'), sort_keys=True, indent=4)

  # save final results
  json.dump(ret, open(args.output, 'w'), sort_keys=True, indent=4)

# print results
for year_i in args.years:

  if year_i not in ret:
    print(f'\nERROR -- No data for year {year_i}\n')
    continue

  year_str = f'Year {year_i}'

  header_str = '\n|'
  header_str += f' {year_str:<10} |'
  header_str += f' {"Fill":<4} |'
  header_str += f' {"Date":<10} |'
  header_str += f' {"Num. of Bunches":<15} |'
  header_str += f' {"Fill Length [h]":<15} |'
  header_str += f' {"Peak Lumi [E34 cm^-2 s^-1]":<30} |'
  header_str += f' {"Delivered Lumi [pb^-1]":<30} |'
  header_str += f' {"Physics* [Hz]":<13} |'
  header_str += f' {"Ephemeral [Hz]":<15} |'
  header_str += f' {"Parking* [Hz]":<13} |'
  header_str += f' {"Scouting* [Hz]":<14} |'
  print(header_str)

  header_str = '|'
  header_str += '-'*11+':|'
  header_str += '-'* 5+':|'
  header_str += '-'*11+':|'
  header_str += '-'*16+':|'
  header_str += '-'*16+':|'
  header_str += '-'*31+':|'
  header_str += '-'*31+':|'
  header_str += '-'*14+':|'
  header_str += '-'*16+':|'
  header_str += '-'*14+':|'
  header_str += '-'*15+':|'
  print(header_str)

  rates_Physics = []
  rates_Ephemeral = []
  rates_Parking = []
  rates_Scouting = []

  for fill_i in ret[year_i]:
    fill_str = '|            |'
    fill_str += f' {fill_i["fill_number"]:>4} |'
    fill_str += f' {fill_i["start_time"].split("T")[0]:>10} |'
    fill_str += f' {fill_i["bunches_colliding"]:>15} |'
    fill_str += f' {fill_i["duration"]/3600:>15.1f} |'
    fill_str += f' {fill_i["peak_lumi"]:>30.2f} |'
    fill_str += f' {fill_i["delivered_lumi"]:>30.2f} |'
    fill_str += f' {fill_i["rate_Physics"]:>13.1f} |'
    fill_str += f' {fill_i["rate_Ephemeral"]:>15.1f} |'
    fill_str += f' {fill_i["rate_Parking"]:>13.1f} |'
    fill_str += f' {fill_i["rate_Scouting"]:>14.1f} |'
    print(fill_str)

    rates_Physics += [fill_i["rate_Physics"]]
    rates_Ephemeral += [fill_i["rate_Ephemeral"]]
    rates_Parking += [fill_i["rate_Parking"]]
    rates_Scouting += [fill_i["rate_Scouting"]]

  # mean and standard deviation of the Physics*, Ephemeral,
  # Parking* and Scouting* rates of the selected Fills
  # (if it is more than one Fill)
  if len(ret[year_i]) > 1:

    rates_Physics_mean = statistics.mean(rates_Physics)
    rates_Physics_sdev = statistics.stdev(rates_Physics)
    rates_Ephemeral_mean = statistics.mean(rates_Ephemeral)
    rates_Ephemeral_sdev = statistics.stdev(rates_Ephemeral)
    rates_Parking_mean = statistics.mean(rates_Parking)
    rates_Parking_sdev = statistics.stdev(rates_Parking)
    rates_Scouting_mean = statistics.mean(rates_Scouting)
    rates_Scouting_sdev = statistics.stdev(rates_Scouting)

    year_str = f'Year {year_i}'

    header_str = '\n|'
    header_str += f' {year_str:<18} |'
    header_str += f' {"Physics* [Hz]":<17} |'
    header_str += f' {"Ephemeral [Hz]":<17} |'
    header_str += f' {"Parking* [Hz]":<17} |'
    header_str += f' {"Scouting* [Hz]":<17} |'
    print(header_str)

    header_str = '|'
    header_str += '-'*19+':|'
    header_str += '-'*18+':|'
    header_str += '-'*18+':|'
    header_str += '-'*18+':|'
    header_str += '-'*18+':|'
    print(header_str)

    mean_str = f'| {"Mean +/- Std.Dev.":<18} |'
    mean_str += f' {rates_Physics_mean:>6.1f} +/- {rates_Physics_sdev:>6.1f} |'
    mean_str += f' {rates_Ephemeral_mean:>6.1f} +/- {rates_Ephemeral_sdev:>6.1f} |'
    mean_str += f' {rates_Parking_mean:>6.1f} +/- {rates_Parking_sdev:>6.1f} |'
    mean_str += f' {rates_Scouting_mean:>6.1f} +/- {rates_Scouting_sdev:>6.1f} |'
    print(mean_str)
