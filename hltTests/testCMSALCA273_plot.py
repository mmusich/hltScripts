#!/usr/bin/env python3
import ROOT

if __name__ == '__main__':

 ROOT.gROOT.SetBatch()

 f0 = ROOT.TFile.Open('hlt0.root')
 f1 = ROOT.TFile.Open('hlt1.root')

 e0 = f0.Get('Events')
 e1 = f1.Get('Events')

 rhoLabels = [
   ['double', 'hltFixedGridRhoFastjetAllCalo', 30, 0, 60],
   ['double', 'hltFixedGridRhoFastjetAll', 30, 0, 60],
   ['double', 'hltFixedGridRhoFastjetAllCaloSerialSync', 30, 0, 60],
   ['double', 'hltFixedGridRhoFastjetAllSerialSync', 30, 0, 60],
   ['double', 'hltFixedGridRhoFastjetECALMFForMuons', 30, 0, 60],
   ['double', 'hltFixedGridRhoFastjetHCAL', 30, 0, 60],
   ['double', 'hltFixedGridRhoFastjetAllCaloForMuons', 30, 0, 60],
   ['double', 'hltFixedGridRhoFastjetAllCaloForMuonsWithCaloTowers', 30, 0, 60],
   ['double', 'hltFixedGridRhoProducerFastjetAllTau', 30, 0, 60],
 ]

 jetLabels = [
   ['recoCaloJets', 'hltAK4CaloJets'],
   ['recoCaloJets', 'hltAK4CaloJetsCorrected'],
   ['recoCaloJets', 'hltAK8CaloJets'],
   ['recoCaloJets', 'hltAK8CaloJetsCorrected'],
   ['recoPFJets', 'hltAK4PFJets'],
   ['recoPFJets', 'hltAK4PFJetsCorrected'],
   ['recoPFJets', 'hltAK8PFJets'],
   ['recoPFJets', 'hltAK8PFJetsCorrected'],
 ]

 jetRegions = [
    ['All', ''],
    ['HB', '0.0 <= abs(eta) && abs(eta) < 1.5'],
    ['HE', '1.5 <= abs(eta) && abs(eta) < 3.0'],
    ['HF', '3.0 <= abs(eta)'],
 ]

 jetVars = [
    ['pt', 200, 0, 200],
    ['eta', 50, -5, 5],
    ['phi', 60, -3.1416, 3.1416],
 ]

 hdict = {}

 outf = ROOT.TFile('testCMSALCA273_plots.root', 'recreate')

 for rhoVar in rhoLabels:
    rhoLabel = f'{rhoVar[0]}_{rhoVar[1]}__HLTX.{rhoVar[0]}_{rhoVar[1]}__HLTX.obj'

    hname = f'{rhoVar[1]}'
    print(hname)
    hname_ref = f'{hname}_ref'
    hname_tar = f'{hname}_tar'

    hdict[hname_ref] = ROOT.TH1F(hname_ref, hname_ref, rhoVar[2], rhoVar[3], rhoVar[4])
    hdict[hname_ref].Sumw2()
    hdict[hname_ref].SetLineColor(1)
    hdict[hname_ref].SetLineWidth(2)

    hdict[hname_tar] = ROOT.TH1F(hname_tar, hname_tar, rhoVar[2], rhoVar[3], rhoVar[4])
    hdict[hname_tar].Sumw2()
    hdict[hname_tar].SetLineColor(2)
    hdict[hname_tar].SetLineWidth(2)

    e0.Draw(f'{rhoLabel}>>{hname_ref}', '', '')
    e1.Draw(f'{rhoLabel}>>{hname_tar}', '', '')

    outf.cd()
    hdict[hname_ref].Write()
    hdict[hname_tar].Write()
    outc = ROOT.TCanvas(hname, hname, 800, 600)
    hdict[hname_ref].Draw('hist,e0')
    hdict[hname_tar].Draw('hist,e0,same')
    outc.Write()
    outc.Close()

 for jetLabel in jetLabels:
    jetP4 = f'{jetLabel[0]}_{jetLabel[1]}__HLTX.{jetLabel[0]}_{jetLabel[1]}__HLTX.obj.m_state.p4Polar_.fCoordinates'

    e0.SetAlias('pt', f'{jetP4}.fPt')
    e1.SetAlias('pt', f'{jetP4}.fPt')

    e0.SetAlias('eta', f'{jetP4}.fEta')
    e1.SetAlias('eta', f'{jetP4}.fEta')

    e0.SetAlias('phi', f'{jetP4}.fPhi')
    e1.SetAlias('phi', f'{jetP4}.fPhi')

    for jetReg in jetRegions:
        for jetVar in jetVars:
            hname = f'{jetLabel[1]}_{jetReg[0]}_{jetVar[0]}'
            print(hname)
            hname_ref = f'{hname}_ref'
            hname_tar = f'{hname}_tar'

            hdict[hname_ref] = ROOT.TH1F(hname_ref, hname_ref, jetVar[1], jetVar[2], jetVar[3])
            hdict[hname_ref].Sumw2()
            hdict[hname_ref].SetLineColor(1)
            hdict[hname_ref].SetLineWidth(2)

            hdict[hname_tar] = ROOT.TH1F(hname_tar, hname_tar, jetVar[1], jetVar[2], jetVar[3])
            hdict[hname_tar].Sumw2()
            hdict[hname_tar].SetLineColor(2)
            hdict[hname_tar].SetLineWidth(2)

            e0.Draw(f'{jetVar[0]}>>{hname_ref}', jetReg[1], '')
            e1.Draw(f'{jetVar[0]}>>{hname_tar}', jetReg[1], '')

            outf.cd()
            hdict[hname_ref].Write()
            hdict[hname_tar].Write()
            outc = ROOT.TCanvas(hname, hname, 800, 600)
            hdict[hname_ref].Draw('hist,e0')
            hdict[hname_tar].Draw('hist,e0,same')
            outc.Write()
            outc.Close()

 outf.Close()
