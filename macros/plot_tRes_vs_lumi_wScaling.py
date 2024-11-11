#! /usr/bin/env python
from utils import *

# --- EDIT ---
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
power = 30 # mW
stochPow = 0.73
verbose = True

variations = {"nominal" : 1, "up" : 1.05, "down" : 0.95}


# ----- dict definition ---
fnames = { 
    '0'    : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root',
    '1E13' : '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E13_LYSO829_temperatures.root',
    '1E14' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_temperatures.root',
    '2E14' : '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_temperatures.root'
}
labels = {
    '0'    : 'HPK_nonIrr_LYSO818_angle52_T5C',
    '1E13' : 'HPK_1E13_LYSO829_angle52_T-19C',
    '1E14' : 'HPK_1E14_LYSO819_angle52_T-32C',
    '2E14' : 'HPK_2E14_LYSO100056_angle52_T-35C'
}
lumiMap = { 
    '0'    : 0,
    '1E13' : 134,
    '1E14' : 1340,
    '2E14' : 2680,
}
alphaMap = {
    '0'    : 0,
    '1E13' : 0.0345,
    '1E14' : 0.345,
    '2E14' : 0.69
}

# ------- energy scaling ------
angle_true = {
    '0' : 49,
    '1E13' : 52,
    '1E14' : 49,
    '2E14' : 49
}
angle_target = 52
enScale = {}
for it,irr in enumerate(angle_true):
    ang = angle_true[irr]
    enScale[irr] = math.cos(math.radians(ang)) / math.cos(math.radians(angle_target))
# -----------------------------

# objects definition
plotAttrs = [20, ROOT.kGreen+2, 'T1 + 25 #mum']

g_Noise = {}
g_Stoch = {}
g_SR    = {}
g_DCR   = {}

g_vs_lumi    = ROOT.TGraphErrors()
g_vs_fluence = ROOT.TGraphErrors()
g_vs_alpha   = ROOT.TGraphErrors()

f = {}

g = {}
g_vs_power = {}

g_scaled = {}
g_scaled_vs_power = {}


# energy scaling
# retrieve files ----
for par in fnames:
    try:
        f[par] = ROOT.TFile.Open(fnames[par])
        if not f[par]:
            print(fnames[par])
            raise FileNotFoundError("File not found")
        g[par] = f[par].Get('g_data_vs_Vov_average_%s'%labels[par])
        if not g[par]:
            print('g_data_vs_Vov_average_',labels[par],'  not found in  ', fnames[par])
            raise AttributeError("Graph not found in file")

        if par != '0':
            g_vs_power[par] = f[par].Get('g_data_vs_staticPower_average_%s'%labels[par])
            if not g_vs_power[par]:
                print('g_data_vs_staticPower_average_',labels[par],'  not found in  ', fnames[par])
                raise AttributeError("Graph not found in file")

    except (FileNotFoundError, AttributeError) as e:
        print(f"Error: {e}")

    g_scaled[par] = {}
    g_scaled_vs_power[par] = {}

    for var in variations:
        g_scaled[par][var] = ROOT.TGraphErrors()
        g_scaled_vs_power[par][var] = ROOT.TGraphErrors()

    
if verbose:
    print("files and graphs retrieved. Taking contributions")

for par in fnames:
    if verbose:
        print("\n ", par)
    #f = ROOT.TFile.Open(fnames[par])
    # retrieving single contribution - for energy scaling
    g_Noise[par] = f[par].Get('g_Noise_vs_Vov_average_%s'%labels[par])
    g_Stoch[par] = f[par].Get('g_Stoch_vs_Vov_average_%s'%labels[par])
    g_SR[par]   = f[par].Get('g_SR_vs_Vov_average_%s'%labels[par])

    if par != '0':
        g_DCR[par]   = f[par].Get('g_DCR_vs_Vov_average_%s'%labels[par])

        
    for i in range(0, g[par].GetN()):
        vov = g[par].GetX()[i]

        # scaling slew rate
        if round(vov,2) != round(g_SR[par].GetX()[i],2):
            print("Vov from SR vs Vov is different in index wrt data vs Vov")
            sys.exit()
        sr = g_SR[par].GetY()[i]
        err_sr = g_SR[par].GetEY()[i]

        if round(vov,2) != round(g_Stoch[par].GetX()[i],2):
            print("Vov from Stoch vs Vov is different in index wrt data vs Vov")
            sys.exit()
            
        s_dcr = 0
        err_s_dcr = 0

        for var in variations:
            scale = enScale[par]*variations[var]
            s_noise,err_s_noise =  sigma_noise(sr*scale, '2c', err_sr*scale)
            s_stoch = g_Stoch[par].Eval(vov)/math.pow(scale, stochPow)
            err_s_stoch = g_Stoch[par].GetEY()[i]/math.pow(scale,stochPow)
            if par != '0':
                s_dcr = g_DCR[par].Eval(vov)/scale
                err_s_dcr = g_DCR[par].GetEY()[i]/scale

            s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)
            err_s_tot = g[par].GetEY()[i]

        
            if verbose and var=='nominal':
                print("ov : ", vov, "\t data scaled : ", round(s_tot,2))
                if par!='0':
                    print("tot : ", s_tot, " ---- noise true : ", sigma_noise(sr,"2c",err_sr), "  noise scaled: ", s_noise, "  stoch true ", g_Stoch[par].Eval(vov), "  stoch scaled ", s_stoch, ' dcr true : ', g_DCR[par].Eval(vov), ' dcr scaled : ', s_dcr)

            g_scaled[par][var].SetPoint(g_scaled[par][var].GetN(), vov, s_tot)
            g_scaled[par][var].SetPointError(g_scaled[par][var].GetN()-1, 0, err_s_tot)

            if par != '0':
                try:
                    g_scaled_vs_power[par][var].SetPoint(g_scaled_vs_power[par][var].GetN(), g_vs_power[par].GetX()[i], s_tot)
                    g_scaled_vs_power[par][var].SetPointError( g_scaled_vs_power[par][var].GetN()-1, 0 , err_s_tot)
                except IndexError:
                    index_out_of_bounds = True
                    print("Index out of bounds")
        

                    
# evaluate 5 perc variation as additional uncertainty
n = 'final'
var = 'nominal'
for par in fnames:
    g_scaled[par][n] = ROOT.TGraphErrors()
    if par != '0':
        g_scaled_vs_power[par][n] = ROOT.TGraphErrors()
    for i in range(0, g_scaled[par][var].GetN()):
        nom = g_scaled[par]['nominal'].GetY()[i]
        up = g_scaled[par]['up'].GetY()[i]
        down = g_scaled[par]['down'].GetY()[i]
        diff_up = abs(nom-up)
        diff_down = abs(nom-down)
        delta = (diff_up + diff_down) /2
        unc = math.sqrt(g_scaled[par][var].GetEY()[i]**2 + delta**2)
        g_scaled[par][n].SetPoint(g_scaled[par][n].GetN(), g_scaled[par][var].GetX()[i], g_scaled[par][var].GetY()[i])
        g_scaled[par][n].SetPointError(g_scaled[par][n].GetN()-1, g_scaled[par][var].GetEX()[i], unc)

        if par!='0':
            g_scaled_vs_power[par][n].SetPoint(g_scaled_vs_power[par][n].GetN(), g_scaled_vs_power[par][var].GetX()[i], g_scaled_vs_power[par][var].GetY()[i])
            g_scaled_vs_power[par][n].SetPointError(g_scaled_vs_power[par][n].GetN()-1, g_scaled_vs_power[par][var].GetEX()[i], unc)
            
            
        
# evaluating tres at maximum static power for irr and 3.5 OV for non irr
for par in fnames:
    if par != '0':
        tres = g_scaled_vs_power[par][n].Eval(power)
        err_tres = interpolate_error(g_scaled_vs_power[par][n], power)
    else:
        tres = g_scaled[par][n].Eval(3.5)
        err_tres = interpolate_error(g_scaled[par][n], 3.5)
    g_vs_lumi.SetPoint(g_vs_lumi.GetN(), lumiMap[par] , tres)
    g_vs_lumi.SetPointError(g_vs_lumi.GetN()-1, 0.1*lumiMap[par], err_tres)

    if verbose:
        print("t res : ", tres, " errore ", err_tres)


if verbose:
    print("drawing")
# Drawing 
tdrLine = ROOT.TLine(0, 30, 3100, 65)
tdrLine.SetLineStyle(2)
tdrLine.SetLineColor(ROOT.kGray+2)

leg = ROOT.TLegend(0.20, 0.65, 0.60, 0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045) 

# vs lumi
cname = 'c_timeResolution_vs_lumi'
c = ROOT.TCanvas(cname, cname, 600, 500)
hPad = ROOT.gPad.DrawFrame(0.,0.,3100.0,120.)
hPad.SetTitle(";Integrated luminosity [fb^{-1}]; time resolution [ps]")
hPad.Draw()
ROOT.gPad.SetTicks(1)
g_vs_lumi.SetMarkerSize(1)
g_vs_lumi.SetMarkerStyle(plotAttrs[0])
g_vs_lumi.SetMarkerColor(plotAttrs[1])
g_vs_lumi.SetLineColor(plotAttrs[1])
g_vs_lumi.SetFillColorAlpha(plotAttrs[1], 0.4)
g_vs_lumi.SetFillStyle(3001)
g_vs_lumi.Draw('E3 same')  # "E3" per la banda d'errore continua
g_vs_lumi.Draw('PL same')  # "PL" per disegnare i punti e la linea
leg.AddEntry( g_vs_lumi, '%s'%plotAttrs[2], 'PL')
leg.AddEntry( tdrLine, 'TDR', 'L')
tdrLine.Draw()
leg.Draw()
c.SaveAs(outdir+'%s.png'%c.GetName())
c.SaveAs(outdir+'%s.pdf'%c.GetName())
