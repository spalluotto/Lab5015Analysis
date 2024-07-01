import os, ROOT
import CMS_lumi, tdrstyle
from utils import *
from SiPM import *
from moduleDict import * 
ROOT.gStyle.SetOptFit(1)

plotdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
indir = '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/'

files = {
    'LYSO829'    : ['12', '0', '-19', '-32'],
    'LYSO819'    : ['-22', '-27', '-32', '-37'],
    'LYSO100056' : ['-30', '-35', '-40'],    
}

angle_true = 49
angle_offset = 3

# --- angle offset scaling ---
enScale = {}
if not isinstance(angle_true, list):
    ang_true = angle_true
    angle_target = angle_true + angle_offset
else:
    ang_true = angle_true[it]
    angle_target = angle_true[it] + angle_offset
enScale = math.cos(math.radians(ang_true)) / math.cos(math.radians(angle_target))
    

# graphs definition ----- 
g_cur   = {}
g_data  = {}
g_noise = {}
g_stoch = {}
g_sdcr  = {}

g_scaled = {}


# retrieve files and graph
for module in files:
    g_cur[module] = {}
    g_data[module] = {}

    g_noise[module] = {}
    g_stoch[module] = {}
    g_sdcr[module] = {}

    sipm = sipm_(module)
    infile = f'{indir}/plot_tRes_{sipm}_{module}_temperatures.root'
    temperatures = files[module]
    file = ROOT.TFile(infile)
    if not file:
        print("FILE NOT FOUND")
    print(temperatures)
    for t in temperatures:
        conf_label = f'{sipm}_{module}_angle52_T{t}C'
        #g_dcr[module][t] = file.Get(f'g_DCR_vs_DCRNpe_average_{conf_label}')
        g_cur[module][t] = file.Get(f'g_current_vs_Vov_{conf_label}')        
        g_data[module][t] = file.Get(f'g_data_vs_Vov_average_{conf_label}')

        g_noise[module][t] = file.Get(f'g_Noise_vs_Vov_average_{conf_label}')
        g_stoch[module][t] = file.Get(f'g_Stoch_vs_Vov_average_{conf_label}')
        g_sdcr[module][t] = file.Get(f'g_DCR_vs_Vov_average_{conf_label}')
        
        if not g_cur[module][t]:
            print(g_cur[module][t], ' not found in ',infile)

ov_ref = 0.7
it = 0

# ovs = {}
# ovs_set = {}
# index = {}
# for module in files:
#     ovs[module] = {}
#     ovs_set[module] = {}
#     index[module] = {}
#     temperatures = files[module]
#     for t in temperatures:
#         ovs[module][t] = []
#         ovs_set[module][t] = []
#         for i in range(g_cur[module][t].GetN()):
#             ovSet = g_cur[module][t].GetX()[i]
#             I = g_cur[module][t].GetX()[i]
#             ovEff_at_ovSet = ovSet-25*I*16/1000
#             ovs[module][t].append(ovEff_at_ovSet)
#             ovs_set[module][t].append(ovSet)
# for module in files:
#     print(module)
#     temperatures = files[module]
#     for t in temperatures:
#         print(t)
#         ovs_n = numpy.array(ovs[module][t])
#         ovs_diff = ovs_n - ov_ref
#         abs_diff = numpy.abs(ovs_diff)
#         min_abs_index = numpy.argmin(abs_diff)
#         min_abs_value = numpy.min(abs_diff)
#         #print("array : ", ovs_n, "    valore minimo : ", min_abs_value, "   indice ", min_abs_index, "    che corrisponde a ov set: ", ovs_set[module][t][min_abs_index])
#         index[module][t] = min_abs_index.item()

#print(index)
        
for module in files:
    print("\n\n")
    print(module)
    g_scaled[module] = {}
    temperatures = files[module]
    col = it+1
            
    for t in temperatures:
        print(t)
        g_scaled[module][t] = ROOT.TGraphErrors()
        g_scaled[module][t].SetMarkerColor(col)
        
        #cur = g_cur[module][t].Eval(ovs_set[module][t][index[module][t]])
        cur = g_cur[module][t].Eval(ov_ref)
        data = g_data[module][t].Eval(ov_ref)
        y = data
        y_err = 0 # to be fixed
        x = cur

        print("x ",x, "y ", y)
        y_scaled = y # to be fixed
        if "100056" in module:
            y_scaled = y/1.065
        g_scaled[module][t].SetPoint(g_scaled[module][t].GetN(),x,y_scaled)
    it+=1  
            
# --- draw 
c = ROOT.TCanvas("c_timeResolution_vs_current", "c_timeResolution_vs_current", 600, 500)
c.cd()
hPad = ROOT.gPad.DrawFrame(0,0,1.4,150)
hPad.SetTitle(";I;#sigma_{t} [ps]")
hPad.Draw()

leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.SetTextFont(42)
leg.SetTextSize(0.050)
it=0
for module in files:
    temperatures = files[module]
    j = 0
    for t in temperatures:
        if j==0:
            leg.AddEntry(g_scaled[module][t], f"{sipm_(module).split('HPK_')[1]}", "p")
        g_scaled[module][t].SetMarkerStyle(20+it*2)
        g_scaled[module][t].Draw("PSAME")
        #    leg.AddEntry(g_scaled[module][t], f"{sipm_(module).split('HPK_')[1]} T {t}C", "p")
        j+=1
    it+=1

    
leg.Draw("same")    
c.SaveAs(f'{plotdir}/{c.GetName()}.png')

        
