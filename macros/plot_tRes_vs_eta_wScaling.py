#! /usr/bin/env python
from utils import *

# --- EDIT ---
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
power = 30 # mW
verbose = True
stochPow = 0.73

ang_pivot = '32'
pivot = float(ang_pivot)

etaMap = {'32' : 0, '52': 0, '64': 0}
energyMap = {'32' : 0, '52': 0, '64': 0}

# plot settings
ymin = 0 
ymax = 120
xmax = 1.65
label_on_top = 'T1 + 25 #mum'
T1 = 3.75
thick = par0

# ------------- scaling contributions --------------
def scale_stoch(E, E_ref, stoch_ref):
    stoch_scaled = stoch_ref* math.pow( E_ref/E, stochPow) 
    return stoch_scaled

def scale_noise(E, E_ref, noise_ref):
    _,_,tdc,_ = get_noise_pars('2c')
    tdc = tdc / math.sqrt(2)
    noise_ref_notdc = math.sqrt(noise_ref**2 - tdc**2)
    noise_scaled_notdc = noise_ref_notdc *  E_ref/E
    noise_scaled = math.sqrt(noise_scaled_notdc**2 + tdc**2)
    return noise_scaled

# assuming dcr does not scale with npe
def scale_dcr(E, E_ref, dcr_ref):
    dcr_scaled = dcr_ref *  E_ref/E
    return dcr_scaled

def scale_tot(E, E_ref, s_ref, n_ref, d_ref):
    stoch = scale_stoch(E, E_ref, s_ref)
    noise = scale_noise(E, E_ref, n_ref)
    dcr = scale_dcr(E, E_ref, d_ref)
    tot = math.sqrt(stoch**2 + noise**2 + dcr**2)
    return tot
# ----------------------------------------------------

"""
for angle in etaMap:
    print(angle)
    etaMap[angle] = eta_from_alpha(float(angle), t=thick) # with effective thickness to compensate for bending effects
    energyMap[angle] = energy_deposited(float(angle), thickness=thick)
"""


etaMap = {'32' : 0.235144, '52' : 0.883181, '64' : 1.31032}
energyMap = {'32' : 3.80218, '52' : 5.23519, '64' : 7.34825}

print("eta map ", etaMap)
print("energy map ", energyMap)


# --- settings ---
data_config = {
    'irr': {
        'fnames': {
            '32': '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_T-35C_angles.root',
            '52': '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_T-35C_angles.root',
            '64': '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_T-35C_angles.root'
        },
        'labels': {
            '32': 'HPK_2E14_LYSO100056_angle32_T-35C',
            '52': 'HPK_2E14_LYSO100056_angle52_T-35C',
            '64': 'HPK_2E14_LYSO100056_angle64_T-35C'
        },
    },
    'nonIrr': {
        'fnames': {
            '32': '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root',
            '52': '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root',
            '64': '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root'
        },
        'labels': {
            '32': 'HPK_nonIrr_LYSO818_angle32_T5C',
            '52': 'HPK_nonIrr_LYSO818_angle52_T5C',
            '64': 'HPK_nonIrr_LYSO818_angle64_T5C'
        },    } }


# ------- angle correction ------
angle_true = {
    '32' : 29,
    '52' : 49,
    '64' : 61
}
if verbose:
    print("computing angle scaling")
enScale = {}
for it,angle in enumerate(angle_true):
    ang = angle_true[angle]
    enScale[angle] = math.cos(math.radians(ang)) / math.cos(math.radians(float(angle)))
# -----------------------------

# objects definition
plotAttrs_ang = {     '32' : [20, ROOT.kGreen+2,  '32^{o}'],    '52' : [21, ROOT.kBlue,     '52^{o}'],    '64' : [22, ROOT.kRed,      '64^{o}']}
plotAttrs = { 'irr' : [20, ROOT.kBlue, '2 #times 10^{14} 1 MeV n_{eq}/cm^{2}'], 'nonIrr' : [21, ROOT.kRed, 'non-irradiated']}

g_Noise = {}
g_Stoch = {}
g_SR    = {}
g_DCR   = {}

g_vs_eta = {}
g_vs_eta_expected = {}
f = {}
g = {}

g_vs_power = {}
g_scaled = {}
g_scaled_vs_power = {}

s_stoch_ref = {}
s_noise_ref = {}
s_dcr_ref = {}

for irrad in data_config:
    f[irrad] = {}
    g[irrad] = {}
    g_vs_power[irrad] = {}
    g_scaled[irrad] = {}
    g_scaled_vs_power[irrad] = {}
    g_Noise[irrad] = {}
    g_Stoch[irrad] = {}
    g_SR[irrad] = {}
    g_DCR[irrad] = {}
    g_vs_eta[irrad] = {}
    g_vs_eta_expected[irrad] = {}

# energy scaling
# retrieve files ----
if verbose:
    print("retrieving files")
for irrad in data_config:
    fnames = data_config[irrad]['fnames']
    labels = data_config[irrad]['labels']
    for par in fnames:
        try:
            f[irrad][par] = ROOT.TFile.Open(fnames[par])
            if not f[irrad][par]:
                print(fnames[par])
                raise FileNotFoundError("File not found")
            gname = f"g_data_vs_Vov_average_{labels[par]}"
            g[irrad][par] = f[irrad][par].Get(gname)
            if not g[irrad][par]:
                raise AttributeError(f"Graph {gname} not found in {fnames[par]}")
            
            if irrad=='irr':
                print("irradiated : ", irrad)
                gname = f"g_data_vs_staticPower_average_{labels[par]}"
                g_vs_power[irrad][par] = f[irrad][par].Get(gname)
                if not g_vs_power[irrad][par]:
                    raise AttributeError(f"Graph {gname} not found in {fnames[par]}")
        except (FileNotFoundError, AttributeError) as e:
            print(f"Error: {e}")
        g_scaled[irrad][par] = ROOT.TGraphErrors()
        g_scaled[irrad][par].SetName('g_data_scaled_vs_Vov_average_%s'%labels[par]) 
        
        g_scaled_vs_power[irrad][par] = ROOT.TGraphErrors()
        g_scaled_vs_power[irrad][par].SetName('g_data_scaled_vs_staticPower_average_%s'%labels[par])

    
if verbose:
    print("files and graphs retrieved. Taking contributions")
for irrad in data_config:
    if verbose:
        print("\n", irrad)
    fnames = data_config[irrad]['fnames']
    labels = data_config[irrad]['labels']    
    for par in fnames:
        if verbose:
            print("\n ", par)
        # retrieving single contribution - for energy scaling
        g_Noise[irrad][par] = f[irrad][par].Get('g_Noise_vs_Vov_average_%s'%labels[par])
        g_Stoch[irrad][par] = f[irrad][par].Get('g_Stoch_vs_Vov_average_%s'%labels[par])
        g_SR[irrad][par]   = f[irrad][par].Get('g_SR_vs_Vov_average_%s'%labels[par])

        if irrad=='irr':
            g_DCR[irrad][par]   = f[irrad][par].Get('g_DCR_vs_Vov_average_%s'%labels[par])
            
        for i in range(0, g[irrad][par].GetN()):
            vov = g[irrad][par].GetX()[i]
            
            # scaling slew rate
            if round(vov,2) != round(g_SR[irrad][par].GetX()[i],2):
                print("Vov from SR vs Vov is different in index wrt data vs Vov")
                sys.exit()
            sr = g_SR[irrad][par].GetY()[i]
            err_sr = g_SR[irrad][par].GetEY()[i]
            s_noise,err_s_noise =  sigma_noise(sr*enScale[par], '2c', err_sr*enScale[par])
            
            # scaling stoch
            if round(vov,2) != round(g_Stoch[irrad][par].GetX()[i],2):
                print("Vov from Stoch vs Vov is different in index wrt data vs Vov")
                sys.exit()
            s_stoch = g_Stoch[irrad][par].Eval(vov)/math.pow(enScale[par], stochPow)
            err_s_stoch = g_Stoch[irrad][par].GetEY()[i]/math.pow(enScale[par],stochPow)
            
            # scaling dcr
            s_dcr = 0
            err_s_dcr = 0            
            if irrad=='irr':
                s_dcr = g_DCR[irrad][par].Eval(vov)/enScale[par]
                err_s_dcr = g_DCR[irrad][par].GetEY()[i]/enScale[par]
            else:
                s_dcr = 0
                err_s_dcr = 0

            s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)
            err_s_tot = g[irrad][par].GetEY()[i]
                    
            if verbose:
                print("\n-------------ov : ", vov, "\t data scaled : ", round(s_tot,2), "   (not scaled ", g[irrad][par].GetY()[i],")")
                print(" ---- noise true : ", round(sigma_noise(sr,"2c",err_sr)[0],2), "  noise scaled: ", round(s_noise,2), "  stoch true ", round(g_Stoch[irrad][par].Eval(vov),2), "  stoch scaled ", round(s_stoch,2))
                if irrad=='irr':
                    print(' dcr true : ', round(g_DCR[irrad][par].Eval(vov),2), ' dcr scaled : ', round(s_dcr,2))

            # saving pivot point for scaling
            if par == ang_pivot:
                if (irrad!="irr" and vov==3.5) or (irrad =="irr" and abs(g_vs_power[irrad][par].GetX()[i] - power) <= 7):
                    s_stoch_ref[irrad] = s_stoch
                    s_noise_ref[irrad] = s_noise
                    s_dcr_ref[irrad] = s_dcr
                    if irrad=='irr':
                        power_approx = g_vs_power[irrad][par].GetX()[i]
                    if verbose:
                        print("reference")
                    
            g_scaled[irrad][par].SetPoint(g_scaled[irrad][par].GetN(), vov, s_tot)
            g_scaled[irrad][par].SetPointError(g_scaled[irrad][par].GetN()-1, 0, err_s_tot)

            g_vs_eta[irrad][par] = ROOT.TGraphErrors()
            
            if irrad=='irr':
                try:
                    g_scaled_vs_power[irrad][par].SetPoint(i, g_vs_power[irrad][par].GetX()[i], s_tot)
                    g_scaled_vs_power[irrad][par].SetPointError(i, 0 , err_s_tot)
                except IndexError:
                    index_out_of_bounds = True
                    print("Index out of bounds")
                    


if verbose:
    print("\ncheck pivot: stoch_ref ", s_stoch_ref, "\tnoise ref ", s_noise_ref,"\t dcr ref",s_dcr_ref)

# evaluating tres at maximum static power for irr and 3.5 OV for non irr
if verbose:
    print("\nfilling graph vs eta")
for irrad in data_config:
    fnames = data_config[irrad]['fnames']
    for par in fnames:
        if irrad=='irr':
            tres = g_scaled_vs_power[irrad][par].Eval(power_approx)
            err_tres = interpolate_error(g_scaled_vs_power[irrad][par], power_approx)
        else:
            tres = g_scaled[irrad][par].Eval(3.5)
            err_tres = interpolate_error(g_scaled[irrad][par], 3.5)
            
        g_vs_eta[irrad][par].SetPoint(g_vs_eta[irrad][par].GetN(), etaMap[par], tres)
        g_vs_eta[irrad][par].SetPointError(g_vs_eta[irrad][par].GetN()-1, etaMap[par]*0.1, 2)
            
        if verbose:
            print("eta ", etaMap[par], "t res : ", tres, " errore ", err_tres)
            


print("\n\n EXPECTED \n\n")
# expected time resolution vs eta - taking 52 as pivot
for irrad in data_config:
    fnames = data_config[irrad]['fnames']
    g_vs_eta_expected[irrad] = ROOT.TGraphErrors()
    for i in range(g_e_vs_eta_sim.GetN()):
        et = g_e_vs_eta_sim.GetX()[i]
        en = g_e_vs_eta_sim.GetY()[i]
        err_et = g_e_vs_eta_sim.GetEX()[i]
        err_en = g_e_vs_eta_sim.GetEY()[i]

        s_tot = scale_tot(en, energyMap[ang_pivot], s_stoch_ref[irrad], s_noise_ref[irrad], s_dcr_ref[irrad])
        
        g_vs_eta_expected[irrad].SetPoint(g_vs_eta_expected[irrad].GetN(), et, s_tot)
        g_vs_eta_expected[irrad].SetPointError(g_vs_eta_expected[irrad].GetN()-1, err_et, 2)
        print("eta : ", et, "  tres ", s_tot)
        
        
if verbose:
    print("drawing")

# plot    
leg = ROOT.TLegend(0.40, 0.65, 0.89, 0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045) 

# ------- time resolution vs eta ----------
c = ROOT.TCanvas("c_timeResolution_vs_eta", "c_timeResolution_vs_eta", 600, 500)
hPad = ROOT.gPad.DrawFrame(0.,ymin,xmax,ymax)
hPad.SetTitle(";#eta;time resolution [ps]")
hPad.Draw()
ROOT.gPad.SetTicks(1)
for irrad in data_config:
    for par in fnames:
        g_vs_eta[irrad][par].Sort()
        g_vs_eta[irrad][par].SetMarkerSize(1)
        g_vs_eta[irrad][par].SetMarkerStyle(plotAttrs[irrad][0])
        g_vs_eta[irrad][par].SetMarkerColor(plotAttrs[irrad][1])
        g_vs_eta[irrad][par].SetLineColor(plotAttrs[irrad][1])
        g_vs_eta[irrad][par].Draw('plsame')
    g_vs_eta_expected[irrad].SetLineColor(plotAttrs[irrad][1])
    g_vs_eta_expected[irrad].SetFillColorAlpha(plotAttrs[irrad][1], 0.4)
    g_vs_eta_expected[irrad].SetFillStyle(3001)
    g_vs_eta_expected[irrad].Draw('E3 l same')
    leg.AddEntry(g_vs_eta[irrad][par], plotAttrs[irrad][2], 'P')
leg.Draw()
tl2 = ROOT.TLatex()
tl2.SetNDC()
tl2.SetTextFont(42)
tl2.SetTextSize(0.045)
tl2.DrawLatex(0.20,0.80,label_on_top)
c.SaveAs(outdir+'%s.png'%c.GetName())
c.SaveAs(outdir+'%s.pdf'%c.GetName())
del(leg)

