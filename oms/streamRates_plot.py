#!/usr/bin/env python3
import fnmatch
import json
import ROOT

import sys

def fill_tgraph(name, data):
    ret = ROOT.TGraph()
    ret.SetName(name)
    for idx,(x,y) in enumerate(data):
        ret.SetPoint(idx,x,y)
    return ret

if __name__ == '__main__':
    ROOT.gROOT.SetBatch()

    data = json.load(open(sys.argv[1]))
    outputFileName = sys.argv[2]

    ymax = 40

    fill_id = '9877'
    run_id = '382913'

    v_prompt = []
    v_parking = []
    v_scouting = []
    for ls_str in data[fill_id][run_id]:
        ls_id = int(ls_str)

#        if ls_id % 10 > 0: continue

        rates = data['9877']['382913'][ls_str]
        prompt_rate_kHz = rates['Prompt'] / 1e3
        parking_rate_kHz = rates['Parking'] / 1e3
        scouting_rate_kHz = rates['Scouting'] / 1e3

        v_prompt += [[ls_id, prompt_rate_kHz]]
        v_parking += [[ls_id, parking_rate_kHz + prompt_rate_kHz]]
        v_scouting += [[ls_id, scouting_rate_kHz]]

    g_prompt = fill_tgraph('prompt', v_prompt)
    g_prompt.SetMarkerSize(1.2)
    g_prompt.SetMarkerStyle(24)
    g_prompt.SetMarkerColor(1)
    g_prompt.SetLineColor(1)
    g_prompt.SetLineStyle(1)
    g_prompt.SetLineWidth(2)

    g_parking = fill_tgraph('parking', v_parking)
    g_parking.SetMarkerSize(1.2)
    g_parking.SetMarkerStyle(20)
    g_parking.SetMarkerColor(2)
    g_parking.SetLineColor(2)
    g_parking.SetLineStyle(1)
    g_parking.SetLineWidth(2)

    g_scouting = fill_tgraph('scouting', v_scouting)
    g_scouting.SetMarkerSize(1.2)
    g_scouting.SetMarkerStyle(21)
    g_scouting.SetMarkerColor(4)
    g_scouting.SetLineColor(4)
    g_scouting.SetLineStyle(1)
    g_scouting.SetLineWidth(2)

    canvas_name = 'rate_plot'
    canvas = ROOT.TCanvas(canvas_name, canvas_name, 1400, 800)
    canvas.cd()
    canvas.SetGrid(0,0)

    TOP = 0.08
    BOT = 0.12
    LEF = 0.11
    RIG = 0.11

    canvas.SetTopMargin(TOP)
    canvas.SetBottomMargin(BOT)
    canvas.SetLeftMargin(LEF)
    canvas.SetRightMargin(RIG)

    h0 = ROOT.TH1D('h_tmp', '', v_prompt[-1][0]-v_prompt[0][0], v_prompt[0][0], v_prompt[-1][0])
    h0.SetStats(0)
    h0.Draw()

    nDivs = 506

    h0.GetXaxis().SetTitle('Lumisection')
    h0.GetXaxis().SetTitleSize(0.05 * 1.0)
    h0.GetXaxis().SetTitleOffset(1.0)
    h0.GetXaxis().SetLabelSize( h0.GetXaxis().GetLabelSize() * 1.2 * 1.0 )

    h0.GetYaxis().SetTitle('HLT Rate [kHz]')
    h0.GetYaxis().SetTitleSize(0.05 * 1.0)
    h0.GetYaxis().SetTitleOffset(1.0)
    h0.GetYaxis().SetRangeUser(0, ymax)
    h0.GetYaxis().SetNdivisions(nDivs)
    h0.GetYaxis().SetLabelSize( h0.GetYaxis().GetLabelSize() * 1.2 * 1.0 )

    txt0 = ROOT.TPaveText(LEF * 0.95, 0.94, LEF * 0.95 + 0.10, 0.98, 'NDC')
    txt0.SetBorderSize(0)
    txt0.SetFillColor(0)
    txt0.SetFillStyle(1001)
    txt0.SetTextAlign(12)
    txt0.SetTextFont(62)
    txt0.SetTextSize(0.05)
    txt0.SetTextColor(1)
    txt0.AddText('CMS')
    txt0.Draw('same')

    txt1 = ROOT.TPaveText(0.65, 0.94, 0.95, 0.98, 'NDC')
    txt1.SetBorderSize(0)
    txt1.SetFillColor(0)
    txt1.SetFillStyle(1001)
    txt1.SetTextAlign(12)
    txt1.SetTextFont(42)
    txt1.SetTextSize(0.030)
    txt1.SetTextColor(1)
    txt1.AddText(f'Fill {fill_id}, 2024 (13.6 TeV)')
    txt1.Draw('same')

    g_prompt.Draw('lp')
    g_parking.Draw('lp')
    g_scouting.Draw('lp')

    leg = ROOT.TLegend(0.17, 0.71, 0.35, 0.91)
    leg.SetBorderSize(2)
    leg.SetTextFont(42)
    leg.SetTextSize(0.03)
    leg.SetFillColor(0)
    leg.AddEntry(g_prompt, 'Standard', 'lp')
    leg.AddEntry(g_parking, 'Standard + Parking', 'lp')
    leg.AddEntry(g_scouting, 'Scouting', 'lp')
    leg.Draw('same')

    canvas.SaveAs(f'{outputFileName}.png')
    canvas.SaveAs(f'{outputFileName}.pdf')
