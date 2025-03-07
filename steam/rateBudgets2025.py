#!/usr/bin/env python3
from scipy.integrate import quad

# slope of luminosity decay [E34 Hz/cm2 / hours]
lumi_slope = (1.82 - 2.02) / (200 * 23.31 / 3600 )

# number of lumi-levelling hours
lumilevel_hours = 6

# peak instantaneous luminosity [E34 Hz/cm2]
peak_lumi = 2.1

# peak L1T rate pre-deadtime [kHz]
peak_l1tr = 110.

# deadtime [%]
deadtime = 0.04

# bare rate of L1_SingleMu5_BMTF at 2.1E34 Hz/cm2 [kHz]
l1t_mu5_peak_rate = 137

# max L1T rate available during luminosity decay [kHz]
#  - Depends on the number of prescale columns in the menu.
#  - For now, choosing 50 kHz, corresponding roughly to having the last prescale change at 1.2E34.
l1t_max_spare_rate = 50

# single-muon parking: relative increase wrt 2024 (35% for looser IP cut)
park_m1sfac = 1.35

# conversion factor from rate of L1_SingleMu5_BMTF to rate of HLT_Mu4_Barrel_IP4_v
# (for HLT-Scouting, no estimate available, assuming 92% based on 2024 data)
hltfrac_m1_parkin = 0.25
hltfrac_m1_hltsco = 0.92

# Reduction of RAW event size post-repacking at PU ~64
evtsize_repacking_factor = 0.85

# HLT rate of sum(prompt) at peak lumi [kHz]
peak_hlt_prompt = 3.0

# HLT rate of single-muon parking at peak lumi [kHz]
peak_hlt_parkin_SingleMu = 1.4 * park_m1sfac

# HLT rate of sum(parking), except SingleMu, at peak lumi [kHz]
#  3.00 kHz corresponds to the 2024 parking rate without single-muon triggers
#  0.25 kHz accounts for extra rate expected from the ParkingLLP PD(s)
#  0.10 kHz accounts for extra rate expected from the L1T-ML-Anomaly-Detection triggers
#  0.10 kHz accounts for contingency
peak_hlt_parkin_Others = 3.0 + 0.25 + 0.10 + 0.10

# HLT rate of HLT-Scouting at peak lumi [kHz]
peak_hlt_hltsco = 28.0

# HLT rate of AlCa+DQM+Express streams at peak lumi [kHz]
# - Estimated as 1 GB/s in bandwidth (1.16 = event size)
peak_hlt_others = 1.00 / 1.16

# instantaneous luminosity as function of time [Hz/cm2]
def lumi(time_hours):
    return min(peak_lumi, peak_lumi + lumi_slope * (time_hours - lumilevel_hours))

# ratio of instantaneous luminosity to peak instantaneous luminosity
def lumi_factor(time_hours):
    return lumi(time_hours) / peak_lumi

# L1T rate of the "2p0E34" PS column as function of time [kHz]
def l1t_rate(time_hours):
    return peak_l1tr * lumi_factor(time_hours)

# Extra rate from L1_SingleMu5_SQ14_BMTF [kHz].
# Corresponds to the lowest of two values.
#   1. The spare L1T rate available during luminosity decay.
#   2. The unprescaled rate of L1_SingleMu5_SQ14_BMTF (ignoring overlaps).
def l1t_mu5_extra_rate(time_hours):
    return max(0, min(l1t_mu5_peak_rate * lumi(time_hours) / peak_lumi, min(peak_l1tr - l1t_rate(time_hours), l1t_max_spare_rate)))

# HLT prompt rate as function of time [kHz]
def hlt_rate_prompt(time_hours):
    return peak_hlt_prompt * lumi_factor(time_hours)

# HLT parking rate as function of time [kHz]
# Assumptions.
#  - All the "spare" L1T rate comes from L1_SingleMu5_BMTF,
#    and translates to "times hltfrac_m1" extra HLT rate.
#  - The rate of all Parking streams goes down with luminosity
#    (not true for ParkingDoubleMuonLowMass, but the effect is not large).
#  - The L1T rate is maximised at all times as if there were infinite prescale (PS) columns;
#    this is conservative, given the limited number of PS columns used in reality.
def hlt_rate_parkin_SingleMu(time_hours):
    lumi_fac = lumi_factor(time_hours)
    return peak_hlt_parkin_SingleMu * lumi_fac + hltfrac_m1_parkin * (1 - deadtime) * l1t_mu5_extra_rate(time_hours)

def hlt_rate_parkin_Others(time_hours):
    lumi_fac = lumi_factor(time_hours)
    return peak_hlt_parkin_Others * lumi_fac

def hlt_rate_parkin(time_hours):
    return hlt_rate_parkin_SingleMu(time_hours) + hlt_rate_parkin_Others(time_hours)

# HLT scouting rate as function of time [kHz]
def hlt_rate_hltsco(time_hours):
    lumi_fac = lumi_factor(time_hours)
    return peak_hlt_hltsco * lumi_fac + hltfrac_m1_hltsco * (1 - deadtime) * l1t_mu5_extra_rate(time_hours)

# RAW event size post-repacking as function of time [MB/event]
def event_size(time_hours):
    return evtsize_repacking_factor * event_size_streamer_RAW(time_hours)

# RAW event size pre-repacking (streamer files) as function of time [MB/event]
def event_size_streamer_RAW(time_hours):
    return 0.23 + 0.44 * lumi(time_hours)

# HLTSCOUT event size pre-repacking (streamer files) as function of time [MB/event]
def event_size_streamer_HLTSCOUT(time_hours):
    return 0.008 + 0.006 * lumi(time_hours)

# HLT prompt bandwidth as function of time [GB/s]
def hlt_band_prompt(time_hours):
    return hlt_rate_prompt(time_hours) * event_size(time_hours)

# HLT parking bandwidth as function of time [GB/s]
def hlt_band_parkin_SingleMu(time_hours):
    return hlt_rate_parkin_SingleMu(time_hours) * event_size(time_hours)

def hlt_band_parkin_Others(time_hours):
    return hlt_rate_parkin_Others(time_hours) * event_size(time_hours)

def hlt_band_parkin(time_hours):
    return hlt_band_parkin_SingleMu(time_hours) + hlt_band_parkin_Others(time_hours)

# HLT prompt bandwidth (streamer files) as function of time [GB/s]
def hlt_band_prompt_streamer(time_hours):
    return hlt_rate_prompt(time_hours) * event_size_streamer_RAW(time_hours)

# HLT parkin bandwidth (streamer files) as function of time [GB/s]
def hlt_band_parkin_SingleMu_streamer(time_hours):
    return hlt_rate_parkin_SingleMu(time_hours) * event_size_streamer_RAW(time_hours)

def hlt_band_parkin_Others_streamer(time_hours):
    return hlt_rate_parkin_Others(time_hours) * event_size_streamer_RAW(time_hours)

def hlt_band_parkin_streamer(time_hours):
    return hlt_band_parkin_SingleMu_streamer(time_hours) + hlt_band_parkin_Others_streamer(time_hours)

# HLT-Scouting bandwidth (streamer files) as function of time [GB/s]
def hlt_band_hltsco_streamer(time_hours):
    return hlt_rate_hltsco(time_hours) * event_size_streamer_HLTSCOUT(time_hours)

# HLT bandwidth of auxiliary streams like AlCa, DQM, Express, etc (streamer files) as function of time [GB/s]
def hlt_band_others_streamer(time_hours):
    return peak_hlt_others * event_size_streamer_RAW(time_hours)

# HLT total output bandwidth (DAQ) [GB/s]
def hlt_band_total_streamer(time_hours):
    hlt_band_tot = 0
    hlt_band_tot += hlt_band_prompt_streamer(time_hours)
    hlt_band_tot += hlt_band_parkin_streamer(time_hours)
    hlt_band_tot += hlt_band_hltsco_streamer(time_hours)
    hlt_band_tot += hlt_band_others_streamer(time_hours)
    return hlt_band_tot

# Per-fill average of a certain quantity (e.g. hlt_band_parkin) as function of the fill duration in hours
def perfill_avg(func, time_hours):
    return quad(func, 0, time_hours)[0] / time_hours

# Per-fill maximum of a certain quantity (e.g. hlt_band_parkin) as function of the fill duration in hours
def perfill_max(func, time_hours):
    return max([func(time_hours * idx / 100) for idx in range(101)])

if __name__ == '__main__':
    print('-'*100)

    # Scenario #1
    #  - Luminosity levelling + 6h of luminosity decay
    lumidecay_hours_scenario1 = 6
    fill_total_hours_scenario1 = lumilevel_hours + lumidecay_hours_scenario1
    hlt_band_prompt_avg_scenario1 = perfill_avg(hlt_band_prompt, fill_total_hours_scenario1)
    hlt_band_parkin_avg_scenario1 = perfill_avg(hlt_band_parkin, fill_total_hours_scenario1)
    hlt_band_total_streamer_max_scenario1 = perfill_max(hlt_band_total_streamer, fill_total_hours_scenario1)
    print(f'Scenario #1: {lumilevel_hours}h leveling, {lumidecay_hours_scenario1}h decay')
    print(f' - Per-fill average bandwidth [GB/s]')
    print(f'   - Prompt  {hlt_band_prompt_avg_scenario1:>4.2f}')
    print(f'   - Parking {hlt_band_parkin_avg_scenario1:>4.2f}')
    print(f' - Max bandwidth (streamer files) [GB/s]')
    print(f'   - Total {hlt_band_total_streamer_max_scenario1:> .2f}')
    print('-'*100)

    # Scenario #2
    #  - Only luminosity levelling.
    #  - Number of hours does not matter here (peak == average)
    lumidecay_hours_scenario2 = 0
    fill_total_hours_scenario2 = lumilevel_hours + lumidecay_hours_scenario2
    hlt_band_prompt_avg_scenario2 = perfill_avg(hlt_band_prompt, fill_total_hours_scenario2)
    hlt_band_parkin_avg_scenario2 = perfill_avg(hlt_band_parkin, fill_total_hours_scenario2)
    hlt_band_total_streamer_max_scenario2 = perfill_max(hlt_band_total_streamer, fill_total_hours_scenario2)
    print(f'Scenario #2: {lumilevel_hours}h leveling, {lumidecay_hours_scenario2}h decay')
    print(f' - Per-fill average bandwidth [GB/s]')
    print(f'   - Prompt  {hlt_band_prompt_avg_scenario2:>4.2f}')
    print(f'   - Parking {hlt_band_parkin_avg_scenario2:>4.2f}')
    print(f' - Max bandwidth (streamer files) [GB/s]')
    print(f'   - Total {hlt_band_total_streamer_max_scenario2:> .2f}')
    print('-'*100)
