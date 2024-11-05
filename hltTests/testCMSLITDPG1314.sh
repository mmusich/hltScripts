#!/bin/bash

foo(){
  [ -f "${1}".py ] || hltConfigFromDB --configName ${@:3} > "${1}".py
  ../storm/hltCheckCompatibilityWithL1TMenu.py "${1}".py -r 1 -t "${2}"
}

#foo cmshlt3325 L1Menu_CollisionsPPRef2024_v0_0_2_xml /users/xueli/HLT_PRef_2024UPC/V6
#foo cmshlt3340 L1Menu_CollisionsPPRef2024_v0_0_2_xml /users/cbennett/140X/HLT_ppRef_140X/V13
#foo cmshlt3343 L1Menu_CollisionsPPRef2024_v0_0_2_xml /users/pchou/HLT_140X/HLT_PRef1400v172/V1
#foo cmshlt3338 L1Menu_CollisionsHeavyIons2024_v1_0_0_xml /users/bputra/2024/CMSSW_14_0_11/HIDilepton24/V2

#foo tmp1 L1Menu_CollisionsHeavyIons2024_v1_0_4_xml --adg /cdaq/circulating/2024/v1.6.0/HLT
#foo tmp2 L1Menu_CollisionsPPRef2024_v1_0_0_xml     --adg /cdaq/circulating/2024/v1.6.0/HLT

#foo tmp3 L1Menu_CollisionsHeavyIons2024_v1_0_4_xml --adg /cdaq/cosmic/commissioning2024/v1.6.0/HLT
#foo tmp4 L1Menu_CollisionsPPRef2024_v1_0_0_xml     --adg /cdaq/cosmic/commissioning2024/v1.6.0/HLT

#foo tmp5 L1Menu_CollisionsHeavyIons2024_v1_0_2_xml --adg /cdaq/special/2024/LumiScan/v1.6.0/HLT
#foo tmp6 L1Menu_CollisionsPPRef2024_v1_0_0_xml     --adg /cdaq/special/2024/LumiScan/v1.6.0/HLT

#foo tmp7 L1Menu_CollisionsHeavyIons2024_v1_0_4_xml /dev/CMSSW_14_1_0/HIon

foo tmp08 L1Menu_CollisionsHeavyIons2024_v1_0_6_xml --adg /cdaq/cosmic/commissioning2024/v1.6.1/HLT
foo tmp09 L1Menu_CollisionsHeavyIons2024_v1_0_6_xml --adg /cdaq/circulating/2024/v1.6.0/HLT
foo tmp10 L1Menu_CollisionsHeavyIons2024_v1_0_6_xml --adg /cdaq/physics/Run2024HI/v1.0.1/HLT
