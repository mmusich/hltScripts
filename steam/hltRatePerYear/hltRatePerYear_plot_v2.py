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

if __name__ == '__main__':

    outputFileName = f'ratePlot_230109'

    data = {
      2012: {'Prompt':  420.0, 'Parking':  400.0, 'Scouting':   996.0, 'Fill': 2998, 'Lumi': 0.50},
      2015: {'Prompt':  992.5, 'Parking':   98.8, 'Scouting':  1057.1, 'Fill': 4452, 'Lumi': 0.25},
      2016: {'Prompt': 1005.8, 'Parking':  514.5, 'Scouting':  4467.8, 'Fill': 5418, 'Lumi': 0.91},
      2017: {'Prompt':  976.0, 'Parking':  409.7, 'Scouting':  4635.0, 'Fill': 6324, 'Lumi': 1.01},
      2018: {'Prompt': 1046.4, 'Parking': 2918.7, 'Scouting':  4855.6, 'Fill': 7124, 'Lumi': 1.18},
      2022: {'Prompt': 1776.7, 'Parking': 2438.3, 'Scouting': 22296.7, 'Fill': 8489, 'Lumi': 1.45},
      2023: {'Prompt': 1683.8, 'Parking': 2660.2, 'Scouting': 17114.2, 'Fill': 9044, 'Lumi': 1.66},
    }

    years = sorted(data.keys())

    prompt_factor = 1000.
    parking_factor = 1000.
    scouting_factor = prompt_factor * 5.

    prompt_ymax = 6
    scouting_ymax = prompt_ymax * scouting_factor / prompt_factor

    v_prompt = []
    v_parking = []
    v_promptPlusParking = []
    v_scouting = []
    for idx,year in enumerate(years):
        v_prompt += [[idx+0.5, data[year]['Prompt'] / prompt_factor]]
        v_parking += [[idx+0.5, data[year]['Parking'] / parking_factor]]
        v_scouting += [[idx+0.5, data[year]['Scouting'] / scouting_factor]]
        v_promptPlusParking += [[idx+0.5, v_prompt[-1][1] + v_parking[-1][1]]]

    g_prompt = fill_tgraph('prompt', v_prompt)
    g_prompt.SetMarkerSize(1.2)
    g_prompt.SetMarkerStyle(24)
    g_prompt.SetMarkerColor(4)
    g_prompt.SetLineColor(4)
    g_prompt.SetLineStyle(2)
    g_prompt.SetLineWidth(2)

    g_parking = fill_tgraph('parking', v_parking)
    g_parking.SetMarkerSize(1.2)
    g_parking.SetMarkerStyle(20)
    g_parking.SetMarkerColor(ROOT.kViolet)
    g_parking.SetLineColor(ROOT.kViolet)
    g_parking.SetLineStyle(2)
    g_parking.SetLineWidth(2)

    g_scouting = fill_tgraph('scouting', v_scouting)
    g_scouting.SetMarkerSize(1.2)
    g_scouting.SetMarkerStyle(21)
    g_scouting.SetMarkerColor(2)
    g_scouting.SetLineColor(2)
    g_scouting.SetLineStyle(1)
    g_scouting.SetLineWidth(2)

    g_promptPlusParking = fill_tgraph('promptPlusParking', v_promptPlusParking)
    g_promptPlusParking.SetMarkerSize(1.2)
    g_promptPlusParking.SetMarkerStyle(20)
    g_promptPlusParking.SetMarkerColor(4)
    g_promptPlusParking.SetLineColor(4)
    g_promptPlusParking.SetLineStyle(1)
    g_promptPlusParking.SetLineWidth(2)

    canvas_name = 'rate_plot'
    canvas = ROOT.TCanvas(canvas_name, canvas_name, 1400, 800)
    canvas.cd()
    canvas.SetGrid(1,0)

    TOP = 0.08
    BOT = 0.12
    LEF = 0.11
    RIG = 0.11

    canvas.SetTopMargin(TOP)
    canvas.SetBottomMargin(BOT)
    canvas.SetLeftMargin(LEF)
    canvas.SetRightMargin(RIG)

    h0 = ROOT.TH1D('h_tmp', '', 7, 0, 7)
    h0.SetStats(0)
    h0.Draw()

    nDivs = 506

    ax1 = ROOT.TGaxis(0,0,0,prompt_ymax,0,prompt_ymax,nDivs,'')
    ax1.SetLineColor(4)
    ax1.SetLabelColor(4)
    ax1.SetTitleColor(4)
    ax1.SetTitle('HLT Rate (Standard, Parking) [kHz]')
    ax1.SetTitleSize( ax1.GetTitleSize() * 1.0)
    ax1.SetTitleOffset( ax1.GetTitleOffset() * 1.0)
    ax1.Draw()

    ax2 = ROOT.TGaxis(7,0,7,prompt_ymax,0,scouting_ymax,nDivs,'+L')
    ax2.SetLineColor(2)
    ax2.SetLabelColor(2)
    ax2.SetTitleColor(2)
    ax2.SetTitle('HLT Rate (Scouting) [kHz]')
    ax2.SetTitleSize( ax2.GetTitleSize() * 1.0)
    ax2.SetTitleOffset( ax2.GetTitleOffset() * 1.0)
    ax2.Draw()

    for idx,year in enumerate(years):
        h0.GetXaxis().SetBinLabel(idx+1, str(year))

    h0.GetXaxis().SetTitleSize(0.05)
    h0.GetXaxis().SetTitleOffset(1.0)
    h0.GetXaxis().SetLabelSize(0.05 * 1.2)
    h0.GetXaxis().SetLabelFont(62)

    h0.GetYaxis().SetTitle('HLT Rate (Standard, Parking) [kHz]')
    h0.GetYaxis().SetTitleSize(0.05 * 0)
    h0.GetYaxis().SetTitleOffset(1.0)
    h0.GetYaxis().SetRangeUser(0, prompt_ymax)
    h0.GetYaxis().SetNdivisions(nDivs)
    h0.GetYaxis().SetLabelSize( h0.GetYaxis().GetLabelSize() * 1.2 * 0 )

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

    tmp = []
    for idx,year in enumerate(years):
        fill_label = f'Fill {data[year]["Fill"]}'
        fill_label_xmin = LEF + (1-LEF-RIG)/7. * (idx + 0.125)
        txt1 = ROOT.TPaveText(fill_label_xmin, 0.87, fill_label_xmin+0.08, 0.91, 'NDC')
        txt1.SetBorderSize(0)
        txt1.SetFillColor(0)
        txt1.SetFillStyle(1001)
        txt1.SetTextAlign(22)
        txt1.SetTextFont(62)
        txt1.SetTextSize(0.0275)
        txt1.SetTextColor(ROOT.kGray+2)
        txt1.AddText(fill_label)
        txt1.Draw('same')
        tmp += [txt1]

        lumi_label = 'L_{inst} = ' + f'{data[year]["Lumi"]:3.2f}' + ' cm^{-2} s^{-1}'
        lumi_label_xmin = LEF + (1-LEF-RIG)/7. * (idx + 0.14)
        txt2 = ROOT.TPaveText(lumi_label_xmin, 0.83, lumi_label_xmin+0.08, 0.87, 'NDC')
        txt2.SetBorderSize(0)
        txt2.SetFillColor(0)
        txt2.SetFillStyle(1001)
        txt2.SetTextAlign(22)
        txt2.SetTextFont(62)
        txt2.SetTextSize(0.0175)
        txt2.SetTextColor(ROOT.kGray+2)
        txt2.AddText(lumi_label)
        txt2.Draw('same')
        tmp += [txt2]

    txt3 = ROOT.TPaveText(0.16, 0.66, 0.47, 0.78, 'NDC')
    txt3.SetBorderSize(0)
    txt3.SetFillColor(0)
    txt3.SetFillStyle(1001)
    txt3.SetTextAlign(12)
    txt3.SetTextFont(42)
    txt3.SetTextSize(0.030)
    txt3.SetTextColor(1)
    txt3.AddText('HLT rates and instantaneous luminosity averaged')
    txt3.AddText('over one typical Fill of a given data-taking year')
    txt3.Draw('same')

    g_prompt.Draw('lp')
#    g_parking.Draw('lp')
    g_promptPlusParking.Draw('lp')
    g_scouting.Draw('lp')

    leg = ROOT.TLegend(0.17, 0.43, 0.35, 0.63)
    leg.SetBorderSize(2)
    leg.SetTextFont(42)
    leg.SetTextSize(0.03)
    leg.SetFillColor(0)
    leg.AddEntry(g_prompt, 'Standard', 'lp')
#    leg.AddEntry(g_parking, 'Parking', 'lp')
    leg.AddEntry(g_promptPlusParking, 'Standard + Parking', 'lp')
    leg.AddEntry(g_scouting, 'Scouting', 'lp')
    leg.Draw('same')

    canvas.SaveAs(f'{outputFileName}.png')
    canvas.SaveAs(f'{outputFileName}.pdf')
