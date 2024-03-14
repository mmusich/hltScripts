import ROOT

redirector = 'root://cms-xrd-global.cern.ch/'

f0 = ROOT.TFile.Open(f"{redirector}/store/mc/Run3Winter24Digi/GluGluHToBB_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/133X_mcRun3_2024_realistic_v8-v2/2550000/30299a97-5be2-4550-9fcb-e7930560af15.root")
e0 = f0.Get("Events")

f1 = ROOT.TFile.Open(f"{redirector}/store/mc/Run3Winter24Digi/GluGluHToTauTau_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/133X_mcRun3_2024_realistic_v8-v2/50002/f6b37bad-7cbb-4f7b-b140-5b9aeb8f7a10.root")
e1 = f1.Get("Events")

h0 = ROOT.TH1F('h0', 'h0', 100, 0, 500)
h1 = ROOT.TH1F('h1', 'h1', 100, 0, 500)

var = 'recoGenParticles_genParticles__HLT.recoGenParticles_genParticles__HLT.obj.pt()'
sel = 'recoGenParticles_genParticles__HLT.recoGenParticles_genParticles__HLT.obj.isHardProcess() && recoGenParticles_genParticles__HLT.recoGenParticles_genParticles__HLT.obj.pdgId()==25'

e0.Draw(f"{var}>>h0", f"{sel}", 'goff')
e1.Draw(f"{var}>>h1", f"{sel}", 'goff')

h0.SetLineColor(1)
h0.SetLineWidth(2)
h1.SetLineColor(2)
h1.SetLineWidth(2)

h0.Scale(1. / h0.Integral())
h1.Scale(1. / h1.Integral())

h0.SetTitle(';GEN Higgs p_{T} [GeV];a.u.')
h1.SetTitle(';GEN Higgs p_{T} [GeV];a.u.')

h0.SetStats(0)
h1.SetStats(0)

h1.Draw('hist,e0')
h0.Draw('hist,e0,same')

leg = ROOT.TLegend(0.60, 0.80, 0.90, 0.90)
leg.AddEntry(h0, 'GluGluHToBB', 'le')
leg.AddEntry(h1, 'GluGluHToTauTau', 'le')
leg.Draw('same')
