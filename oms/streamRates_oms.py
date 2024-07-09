#!/usr/bin/env python3
import os
import argparse
import json

from omsapi import OMSAPI

def get_omsapi():
    omsapi = OMSAPI('https://cmsoms.cern.ch/agg/api', 'v1', cert_verify=False)
    omsapi.auth_krb()
    return omsapi

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
  omsapi = get_omsapi()

  outDict = {}

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

    for run_i in runs:
      q_lumis = omsapi.query("lumisections")
      q_lumis.set_verbose(False)
      q_lumis.filter("run_number", run_i)
      q_lumis.paginate(page=1, per_page=1)
      data_lumis = q_lumis.data()
      data_lumis_dict = data_lumis.json()
      ntot_lumis_tmp = data_lumis_dict["meta"]["totalResourceCount"]
      npages_lumis = int(1+ntot_lumis_tmp/1e5)
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
            rate_Parking = 0
            rate_Scouting = 0
            break

        ntot_streams = data_streams_dict["meta"]["totalResourceCount"]

        if ntot_streams == 0:
            continue

        rate_Physics = 0.
        rate_Parking = 0.
        rate_Scouting = 0.
        rate_ALCA = 0.
        rate_DQM = 0.
        rate_Others = 0.

        npages_streams = int(1+ntot_streams/1e5)
        for page_idx in range(1, 1+npages_streams):
          q_streams.paginate(page=page_idx, per_page=int(1e5))
          data_streams = q_streams.data()
          data_streams_dict = data_streams.json()['data']
          for stream_i in data_streams_dict:
            streamName_i = stream_i['attributes']['stream_name']
            streamRate_i = stream_i['attributes']['rate']

            if streamName_i.startswith('Physics'):
              rate_Physics += streamRate_i

            elif streamName_i.startswith('Parking'):
              rate_Parking += streamRate_i

            elif streamName_i.startswith('Scouting'):
              rate_Scouting += streamRate_i

            elif streamName_i.startswith('ALCA'):
              rate_ALCA += streamRate_i

            elif streamName_i.startswith('DQM'):
              rate_DQM += streamRate_i

            else:
              rate_Others += streamRate_i

        fill_id = int(fill_i["id"])
        run_id = int(run_i)
        lumi_id = int(lumi_i)

        if fill_id not in outDict:
            outDict[fill_id] = {}
        if run_id not in outDict[fill_id]:
            outDict[fill_id][run_id] = {}
        if lumi_id not in outDict[fill_id][run_id]:
            outDict[fill_id][run_id][lumi_id] = {}

        outDict[fill_id][run_id][lumi_id]['Prompt'] = rate_Physics
        outDict[fill_id][run_id][lumi_id]['Parking'] = rate_Parking
        outDict[fill_id][run_id][lumi_id]['Scouting'] = rate_Scouting

# save final results
json.dump(outDict, open(args.output, 'w'), sort_keys=True, indent=2)
