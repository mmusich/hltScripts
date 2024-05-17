#!/usr/bin/env python3
import fnmatch
import json
import ROOT

ROOT.gROOT.SetBatch()

testOneOnly = False

def fill_tgraph(name, data):
    ret = ROOT.TGraph()
    ret.SetName(name)
    for idx,(x,y) in enumerate(data):
        ret.SetPoint(idx,x,y)
    return ret

def draw_fit(name):
    return (not name.startswith('ParkingDoubleElectronLowMass') and name != 'NanoDST' and name != 'Parking*')

extraStreamNames = [
  'Physics*',
  'PhysicsMuon*',
  'PhysicsEGamma*',
  'PhysicsJetMET*',
  'Parking*',
  'ParkingDoubleMuonLowMass*',
  'ParkingDoubleElectronLowMass*',
  'ParkingSingleMuon*',
  'ParkingVBF*',
]

runDict = {
  361303: (2, f'2022 (run 361303)'),
  361971: (2, f'2022 (run 361971)'),
  370332: (4, f'2023 (run 370332)'),
}

data = {}
streamNames = extraStreamNames[:]
for runNumber in runDict:
 data[runNumber] = json.load(open(f'{runNumber}.json'))
 streamNames += list(data[runNumber].keys())
streamNames = sorted(list(set(streamNames)))

streamRateVsPU = {}
for runNumber in runDict:
 streamRateVsPU_tmp = {}
 for streamName in streamNames:
    streamRateVsPU_tmp[streamName] = {}
    for stream in data[runNumber]:
        if not fnmatch.fnmatch(stream, streamName):
            continue
        for entry in data[runNumber][stream]:
            if entry['LS'] in streamRateVsPU_tmp[streamName]:
                if streamRateVsPU_tmp[streamName][entry['LS']][0] != entry['pileup']:
                    raise RuntimeError(f'ERROR - inconsistent pileup values (stream = {streamName}): {streamRateVsPU_tmp[entry["LS"]][0]} != {entry["pileup"]}')
                streamRateVsPU_tmp[streamName][entry['LS']][1] += entry['rate']
            else:
                streamRateVsPU_tmp[streamName][entry['LS']] = [entry['pileup'], entry['rate']]

 streamRateVsPU[runNumber] = {}
 for streamName in streamRateVsPU_tmp:
     streamRateVsPU[runNumber][streamName] = [streamRateVsPU_tmp[streamName][LS] for LS in streamRateVsPU_tmp[streamName]]

streamMinMaxDict = {}
for runNumber in streamRateVsPU:
    for streamName in streamRateVsPU[runNumber]:
        if not bool(streamRateVsPU[runNumber][streamName]):
            print(f'WARNING - empty {runNumber} {streamName}')
            continue
        x_min = min(streamRateVsPU[runNumber][streamName], key=lambda x: x[0])[0]
        y_min = min(streamRateVsPU[runNumber][streamName], key=lambda x: x[1])[1]
        x_max = max(streamRateVsPU[runNumber][streamName], key=lambda x: x[0])[0]
        y_max = max(streamRateVsPU[runNumber][streamName], key=lambda x: x[1])[1]
        if streamName not in streamMinMaxDict:
            streamMinMaxDict[streamName] = [x_min, y_min, x_max, y_max]
        else:
            streamMinMaxDict[streamName][0] = min(x_min, streamMinMaxDict[streamName][0])
            streamMinMaxDict[streamName][1] = min(y_min, streamMinMaxDict[streamName][1])
            streamMinMaxDict[streamName][2] = max(x_max, streamMinMaxDict[streamName][2])
            streamMinMaxDict[streamName][3] = max(y_max, streamMinMaxDict[streamName][3])

for runNumber in runDict:
 runColor = runDict[runNumber][0]
 runLabel = runDict[runNumber][1]

 for stream in streamRateVsPU[runNumber]:
#    if bool(streamRateVsPU[runNumber][stream]):
#        print(f'WARNING: {stream} has no data')
#        continue

    tg = fill_tgraph(stream, streamRateVsPU[runNumber][stream])
    tg.SetName(stream)
    tg.SetTitle(stream)
    tg.SetMarkerSize(0.6)
    tg.SetMarkerStyle(20)
    tg.SetMarkerColor(runColor)

    min_x = 0.8 * streamMinMaxDict[stream][0]
    min_y = 0.8 * streamMinMaxDict[stream][1]
    max_x = 1.2 * streamMinMaxDict[stream][2]
    max_y = 1.2 * streamMinMaxDict[stream][3]

    tf_name = f'tf_{stream}'
    tf = ROOT.TF1(tf_name, 'pol1', min_x, max_x)
    tf.SetLineColor(runColor)
    tf.SetLineWidth(2)
    tf.SetLineStyle(1)

#    tf.SetParLimits(0, 0, 1e6)
#    tf.SetParLimits(1, 0, 1e6)
#    tf.SetParLimits(2, 0, 1e6)

    if tg.GetN():
        tg.Fit(tf, 'B0')

    drawFit = tg.GetN() and draw_fit(stream)

    par0 = tf.GetParameter(0)
    par1 = tf.GetParameter(1)
#    par2 = tf.GetParameter(2)

    canvas_name = f'{stream}'
    canvas = ROOT.TCanvas(canvas_name, canvas_name, 1000, 800)
    canvas.cd()
    canvas.SetGrid(1,1)
    h0 = canvas.DrawFrame(0, min_y, 70, max_y)
    h0.GetXaxis().SetTitle('Pileup')
    h0.GetYaxis().SetTitle('Rate [Hz]')
    h0.GetXaxis().SetTitleSize(0.05)
    h0.GetYaxis().SetTitleSize(0.05)
    h0.GetXaxis().SetTitleOffset(1.0)
    h0.GetYaxis().SetTitleOffset(1.0)

    tg.Draw('p,same')
    if drawFit:
        tf.Draw('l,same')

    txt1 = ROOT.TPaveText(0.15, 0.82, 0.45, 0.88, 'NDC')
    txt1.SetBorderSize(0)
    txt1.SetFillColor(0)
    txt1.SetFillStyle(1001)
    txt1.SetTextAlign(12)
    txt1.SetTextFont(42)
    txt1.SetTextSize(0.035)
    txt1.SetTextColor(ROOT.kBlack)
    txt1.AddText(f'Stream: {stream}')
    txt1.Draw('same')

    txt2 = ROOT.TPaveText(0.15, 0.76, 0.45, 0.82, 'NDC')
    txt2.SetFillColor(0)
    txt2.SetFillStyle(1001)
    txt2.SetTextAlign(12)
    txt2.SetTextFont(42)
    txt2.SetTextSize(0.035)
    txt2.SetBorderSize(0)
    txt2.SetTextColor(runColor)
    txt2.AddText(runLabel)
    txt2.Draw('same')

    if drawFit:
        txt3 = ROOT.TPaveText(0.15, 0.70, 0.45, 0.76, 'NDC')
        txt3.SetFillColor(0)
        txt3.SetFillStyle(1001)
        txt3.SetTextColor(runColor)
        txt3.SetTextAlign(12)
        txt3.SetTextFont(42)
        txt3.SetTextSize(0.035)
        txt3.SetBorderSize(0)
        txt3.AddText(f'Fit: {par0:.3f} + x * {par1:.3f}')
#        txt3.AddText(f'Fit: {par0:.3f} + x * {par1:.3f} + x^{2} * {par2:.3f}')
        txt3.Draw('same')

    outputFileName = f'streamRateVsPU_231111/streamRateVsPU_'+stream.replace('*','Star')+f'_run{runNumber}'
    canvas.SaveAs(f'{outputFileName}.png')
    canvas.SaveAs(f'{outputFileName}.pdf')

    if testOneOnly:
        break

### 2022 vs 2023
for stream in streamNames:

    min_x = 0.8 * streamMinMaxDict[stream][0]
    min_y = 0.8 * streamMinMaxDict[stream][1]
    max_x = 1.2 * streamMinMaxDict[stream][2]
    max_y = 1.2 * streamMinMaxDict[stream][3]

    ### 2022
    runNumber2022 = 361303
    runColor2022 = runDict[runNumber2022][0]
    runLabel2022 = runDict[runNumber2022][1]

    tg2022 = fill_tgraph(stream, streamRateVsPU[runNumber2022][stream])
    tg2022.SetName(stream)
    tg2022.SetTitle(stream)
    tg2022.SetMarkerSize(0.6)
    tg2022.SetMarkerStyle(20)
    tg2022.SetMarkerColor(runColor2022)

    tf2022_name = f'tf2022_{stream}'
    tf2022 = ROOT.TF1(tf_name, 'pol1', min_x, max_x)
    tf2022.SetLineColor(runColor2022)
    tf2022.SetLineWidth(2)
    tf2022.SetLineStyle(1)

    drawGraph2022 = tg2022.GetN() > 0
    drawFit2022 = drawGraph2022 and draw_fit(stream)

    if drawGraph2022:
        tg2022.Fit(tf2022, 'B0')

    par0_2022 = tf2022.GetParameter(0)
    par1_2022 = tf2022.GetParameter(1)

    ### 2023
    runNumber2023 = 370332
    runColor2023 = runDict[runNumber2023][0]
    runLabel2023 = runDict[runNumber2023][1]

    tg2023 = fill_tgraph(stream, streamRateVsPU[runNumber2023][stream])
    tg2023.SetName(stream)
    tg2023.SetTitle(stream)
    tg2023.SetMarkerSize(0.6)
    tg2023.SetMarkerStyle(20)
    tg2023.SetMarkerColor(runColor2023)

    tf2023_name = f'tf_{stream}'
    tf2023 = ROOT.TF1(tf2023_name, 'pol1', min_x, max_x)
    tf2023.SetLineColor(runColor2023)
    tf2023.SetLineWidth(2)
    tf2023.SetLineStyle(1)

    drawGraph2023 = tg2023.GetN() > 0
    drawFit2023 = drawGraph2023 and draw_fit(stream)

    if drawGraph2023:
        tg2023.Fit(tf2023, 'B0')

    par0_2023 = tf2023.GetParameter(0)
    par1_2023 = tf2023.GetParameter(1)

    canvas_name = f'{stream}'
    canvas = ROOT.TCanvas(canvas_name, canvas_name, 1000, 800)
    canvas.cd()
    canvas.SetGrid(1,1)
    h0 = canvas.DrawFrame(0, min_y, 70, max_y)
    h0.GetXaxis().SetTitle('Pileup')
    h0.GetYaxis().SetTitle('Rate [Hz]')
    h0.GetXaxis().SetTitleSize(0.05)
    h0.GetYaxis().SetTitleSize(0.05)
    h0.GetXaxis().SetTitleOffset(1.0)
    h0.GetYaxis().SetTitleOffset(1.0)

    tg2022.Draw('p,same')
    if drawFit2022:
        tf2022.Draw('l,same')

    tg2023.Draw('p,same')
    if drawFit2023:
        tf2023.Draw('l,same')

    txt1 = ROOT.TPaveText(0.15, 0.82, 0.45, 0.88, 'NDC')
    txt1.SetBorderSize(0)
    txt1.SetFillColor(0)
    txt1.SetFillStyle(1001)
    txt1.SetTextAlign(12)
    txt1.SetTextFont(42)
    txt1.SetTextSize(0.035)
    txt1.SetTextColor(ROOT.kBlack)
    txt1.AddText(f'Stream: {stream}')
    txt1.Draw('same')

    if drawGraph2022:
        txt2 = ROOT.TPaveText(0.15, 0.76, 0.45, 0.82, 'NDC')
        txt2.SetFillColor(0)
        txt2.SetFillStyle(1001)
        txt2.SetTextAlign(12)
        txt2.SetTextFont(42)
        txt2.SetTextSize(0.035)
        txt2.SetBorderSize(0)
        txt2.SetTextColor(runColor2022)
        txt2.AddText(runLabel2022)
        txt2.Draw('same')

    if drawFit2022:
        txt3 = ROOT.TPaveText(0.15, 0.70, 0.45, 0.76, 'NDC')
        txt3.SetFillColor(0)
        txt3.SetFillStyle(1001)
        txt3.SetTextColor(runColor2022)
        txt3.SetTextAlign(12)
        txt3.SetTextFont(42)
        txt3.SetTextSize(0.035)
        txt3.SetBorderSize(0)
        txt3.AddText(f'Fit: {par0_2022:.3f} + x * {par1_2022:.3f}')
        txt3.Draw('same')

    if drawGraph2023:
        txt4 = ROOT.TPaveText(0.15, 0.64, 0.45, 0.70, 'NDC')
        txt4.SetFillColor(0)
        txt4.SetFillStyle(1001)
        txt4.SetTextAlign(12)
        txt4.SetTextFont(42)
        txt4.SetTextSize(0.035)
        txt4.SetBorderSize(0)
        txt4.SetTextColor(runColor2023)
        txt4.AddText(runLabel2023)
        txt4.Draw('same')

    if drawFit2023:
        txt5 = ROOT.TPaveText(0.15, 0.58, 0.45, 0.64, 'NDC')
        txt5.SetFillColor(0)
        txt5.SetFillStyle(1001)
        txt5.SetTextColor(runColor2023)
        txt5.SetTextAlign(12)
        txt5.SetTextFont(42)
        txt5.SetTextSize(0.035)
        txt5.SetBorderSize(0)
        txt5.AddText(f'Fit: {par0_2023:.3f} + x * {par1_2023:.3f}')
        txt5.Draw('same')

    outputFileName = f'streamRateVsPU_231111/streamRateVsPU_'+stream.replace('*','Star')+f'_run{runNumber2022}vs{runNumber2023}'
    canvas.SaveAs(f'{outputFileName}.png')
    canvas.SaveAs(f'{outputFileName}.pdf')

    if testOneOnly:
        break
