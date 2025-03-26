#! /usr/bin/env python
from energy_scaling import *



# --- EDIT ---
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
power = 30 # mW
verbose = True

low_eta = '32'
med_eta = '52'
high_eta = '64'

ang_offset = 3

suffix = ''

# plot settings
ymin = 0 
ymax = 120
xmax = 1.65
label_on_top = ''


if verbose:
    print("Variation ", suffix)



# --------------------------------------------------------------------------  
#      c e un hard code malvagio nella sezione dopo il print speziali
# --------------------------------------------------------------------------


# angle variation for eta unc evaluation
if 'up' in suffix:
    low_eta = float(low_eta)+1
    med_eta = float(med_eta)+1
    high_eta = float(high_eta)+1    
elif 'down' in suffix:
    low_eta = float(low_eta)-1
    med_eta = float(med_eta)-1
    high_eta = float(high_eta)-1

    
low_ang_true = float(low_eta)-3
med_ang_true = float(med_eta)-3
high_ang_true = float(high_eta)-3


pivot = {"irr" : low_eta, "irr_1e14" : low_eta, "nonIrr": low_eta}


etaMap = {low_eta : 0, med_eta: 0, high_eta: 0}
energyMap = {low_eta : 0, med_eta: 0, high_eta: 0}

# computed as variation of one degree 
etaUncMap = {low_eta: 0.0630431, med_eta: 0.0369712, high_eta: 0.0429036}


# -------- retrieve energy and eta maps ---------
for angle in energyMap:
    edep_tb = energy_deposited(float(angle))   # eMIP * thick/cos(angle)
    print("Energy deposited at TB ", edep_tb, " at an angle of ", angle)
    # # fitto la simulazione con una pol2 ed estrapolo cosi i valori di eta
    # etaMap[angle] = find_x(edep_tb, eq_fit_sim_pol2)
    # energyMap[angle] = fit_sim_pol2(etaMap[angle])
    
    # questo nell'approccio in cui prendo i punti e interpolo dalla simulazione
    etaMap[angle] = find_x_given_y(g_e_vs_eta_sim, edep_tb) # taking eta as the x point in simulation to which correspond edep_tb

    # se proprio non trova il punto nel grafico faccio una estrapolazione dall equazione
    if etaMap[angle] == None:
        etaMap[angle] = float(find_x(edep_tb,eq_energy_vs_eta))
    energyMap[angle] = g_e_vs_eta_sim.Eval(etaMap[angle]) # se dio vuole dovrebbe essere edep_tb 

print("\n ===== ")
print("eta map ", etaMap)
print("energy map in CMS ", energyMap)
# -------------------------------------------------



# --- settings ---
data_config = {
    'irr': {
        'fnames': {
            low_eta: '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_T-35C_angles.root',
            med_eta: '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_T-35C_angles.root',
            high_eta: '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_2E14_LYSO100056_T-35C_angles.root'
        },
        'labels': {
            low_eta: 'HPK_2E14_LYSO100056_angle32_T-35C',
            med_eta: 'HPK_2E14_LYSO100056_angle52_T-35C',
            high_eta: 'HPK_2E14_LYSO100056_angle64_T-35C'
        },
        'scale' : True
    },

    'irr_1e14': {
        'fnames': {
            low_eta: '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_T-32C_angles.root',
            med_eta: '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_T-32C_angles.root',
            high_eta: '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/plot_tRes_HPK_1E14_LYSO819_T-32C_angles.root'
        },
        'labels': {
            low_eta: 'HPK_1E14_LYSO819_angle32_T-32C',
            med_eta: 'HPK_1E14_LYSO819_angle52_T-32C',
            high_eta: 'HPK_1E14_LYSO819_angle64_T-32C'
        },
        'scale'	: False
    },



    'nonIrr': {
        'fnames': {
            low_eta: '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root',
            med_eta: '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root',
            #high_eta: '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/plot_tRes_HPK_nonIrr_LYSO818_T5C_angles.root'
        },
        'labels': {
            low_eta: 'HPK_nonIrr_LYSO818_angle32_T5C',
            med_eta: 'HPK_nonIrr_LYSO818_angle52_T5C',
            #high_eta: 'HPK_nonIrr_LYSO818_angle64_T5C'
        },
        'scale' : True
    }
}


# ------- angle correction ------
angle_true = {
    low_eta : low_ang_true,
    med_eta : med_ang_true,
    high_eta : high_ang_true
}

if verbose:
    print("\n ===== computing angle scaling")
enScale = {}

for irrad in data_config:
    enScale[irrad] = {}
    for it,angle in enumerate(angle_true):
        # se non serve lo scaling uso questa cosa, poi mi rendo conto che e un overkill ma mi veniva facile cosi
        if data_config[irrad]['scale']:
            ang = angle_true[angle]
        else:
            ang = float(angle)
        enScale[irrad][angle] = math.cos(math.radians(ang)) / math.cos(math.radians(float(angle)))
# -----------------------------

# objects definition
plotAttrs_ang = {     low_eta : [20, ROOT.kGreen+2,  '32^{o}'],    med_eta : [21, ROOT.kBlue,     '52^{o}'],    high_eta : [22, ROOT.kRed,      '64^{o}']}
plotAttrs = { 'irr' : [20, ROOT.kBlue, '2 #times 10^{14} n_{eq}/cm^{2}'], 'irr_1e14' : [21, ROOT.kGreen+1, '1 #times 10^{14} n_{eq}/cm^{2}'], 'nonIrr' : [22, ROOT.kRed, 'non-irradiated']}


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
    print("\n ===== retrieving files")
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
            
            if 'irr' in irrad:
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
    print("\n ===== files and graphs retrieved. Taking contributions")
for irrad in data_config:
    if verbose:
        print("\n", irrad)
    fnames = data_config[irrad]['fnames']
    labels = data_config[irrad]['labels']    
    for par in fnames:
        if verbose:
            print("\n ", par)
        # retrieving single contribution - for energy scaling
        g_Noise_not_scaled = f[irrad][par].Get('g_Noise_vs_Vov_average_%s'%labels[par])
        g_Stoch_not_scaled = f[irrad][par].Get('g_Stoch_vs_Vov_average_%s'%labels[par])
        g_SR_not_scaled   = f[irrad][par].Get('g_SR_vs_Vov_average_%s'%labels[par])

        g_Noise[irrad][par] = ROOT.TGraphErrors()
        g_Stoch[irrad][par] = ROOT.TGraphErrors()
        g_SR[irrad][par] = ROOT.TGraphErrors()
        
        if 'irr' in irrad:
            g_DCR_not_scaled   = f[irrad][par].Get('g_DCR_vs_Vov_average_%s'%labels[par])
            g_DCR[irrad][par] = ROOT.TGraphErrors()
            
        for i in range(0, g[irrad][par].GetN()):
            vov = g[irrad][par].GetX()[i]
            
            # scaling slew rate
            if round(vov,2) != round(g_SR_not_scaled.GetX()[i],2):
                print("Vov from SR vs Vov is different in index wrt data vs Vov")
                sys.exit()
            sr = g_SR_not_scaled.GetY()[i]
            err_sr = g_SR_not_scaled.GetEY()[i]
            s_noise,err_s_noise =  sigma_noise(sr*enScale[irrad][par], '2c', err_sr*enScale[irrad][par])
            g_Noise[irrad][par].SetPoint(g_Noise[irrad][par].GetN(), vov, s_noise)
            g_Noise[irrad][par].SetPointError(g_Noise[irrad][par].GetN()-1, 0, err_s_noise)
            
            # scaling stoch
            if round(vov,2) != round(g_Stoch_not_scaled.GetX()[i],2):
                print("Vov from Stoch vs Vov is different in index wrt data vs Vov")
                sys.exit()
            s_stoch = g_Stoch_not_scaled.Eval(vov)/math.pow(enScale[irrad][par], stochPow)
            err_s_stoch = g_Stoch_not_scaled.GetEY()[i]/math.pow(enScale[irrad][par],stochPow)
            g_Stoch[irrad][par].SetPoint(g_Stoch[irrad][par].GetN(), vov, s_stoch)
            g_Stoch[irrad][par].SetPointError(g_Stoch[irrad][par].GetN()-1, 0, err_s_stoch)

            
            # scaling dcr
            s_dcr = 0
            err_s_dcr = 0            
            if 'irr' in irrad:
                s_dcr = g_DCR_not_scaled.Eval(vov)/enScale[irrad][par]
                err_s_dcr = g_DCR_not_scaled.GetEY()[i]/enScale[irrad][par]
                g_DCR[irrad][par].SetPoint(g_DCR[irrad][par].GetN(), vov, s_dcr)
                g_DCR[irrad][par].SetPointError(g_DCR[irrad][par].GetN()-1, 0, err_s_dcr)
            else:
                s_dcr = 0
                err_s_dcr = 0

            s_tot = math.sqrt(s_noise*s_noise + s_stoch*s_stoch + s_dcr*s_dcr)
            err_s_tot = g[irrad][par].GetEY()[i]
                    
            if verbose:
                print("\n-------------ov : ", vov, "\t data scaled : ", round(s_tot,2), "   (not scaled ", g[irrad][par].GetY()[i],")")
                print(" ---- noise true : ", round(sigma_noise(sr,"2c",err_sr)[0],2), "  noise scaled: ", round(s_noise,2), "  stoch true ", round(g_Stoch_not_scaled.Eval(vov),2), "  stoch scaled ", round(s_stoch,2))
                if irrad=='irr':
                    print(' dcr true : ', round(g_DCR_not_scaled.Eval(vov),2), ' dcr scaled : ', round(s_dcr,2))

            # saving pivot point for scaling
            if par == pivot[irrad]:
                if ("irr" not in irrad and vov==3.5) or ("irr" in irrad and abs(g_vs_power[irrad][par].GetX()[i] - power) <= 7):
                    s_stoch_ref[irrad] = s_stoch
                    s_noise_ref[irrad] = s_noise
                    s_dcr_ref[irrad] = s_dcr
                    if 'irr' in irrad:
                        power_approx = g_vs_power[irrad][par].GetX()[i]
                    if verbose:
                        print("reference --> eta: ", etaMap[pivot[irrad]], '  ov ', vov)
                    
            g_scaled[irrad][par].SetPoint(g_scaled[irrad][par].GetN(), vov, s_tot)
            g_scaled[irrad][par].SetPointError(g_scaled[irrad][par].GetN()-1, 0, err_s_tot)

            g_vs_eta[irrad][par] = ROOT.TGraphErrors()
            
            if 'irr' in irrad:
                try:
                    g_scaled_vs_power[irrad][par].SetPoint(i, g_vs_power[irrad][par].GetX()[i], s_tot)
                    g_scaled_vs_power[irrad][par].SetPointError(i, 0 , err_s_tot)
                except IndexError:
                    index_out_of_bounds = True
                    print("Index out of bounds")



if verbose:
    print("\n ===== check pivot: stoch_ref ", s_stoch_ref, "\tnoise ref ", s_noise_ref,"\t dcr ref",s_dcr_ref, "\teta: ",etaMap[pivot[irrad]])

# evaluating tres at maximum static power for irr and 3.5 OV for non irr
if verbose:
    print("\n ===== filling graph vs eta")
for irrad in data_config:
    fnames = data_config[irrad]['fnames']
    for par in fnames:
        if 'irr' in irrad:
            tres = g_scaled_vs_power[irrad][par].Eval(power_approx)
            err_tres = interpolate_error(g_scaled_vs_power[irrad][par], power_approx)
        else:
            tres = g_scaled[irrad][par].Eval(3.5)
            err_tres = interpolate_error(g_scaled[irrad][par], 3.5)
            
        g_vs_eta[irrad][par].SetPoint(g_vs_eta[irrad][par].GetN(), etaMap[par], tres)
        g_vs_eta[irrad][par].SetPointError(g_vs_eta[irrad][par].GetN()-1, etaUncMap[par], 2)
            
        #if verbose:
        print("eta ", etaMap[par], "t res : ", tres, " errore ", err_tres)
            


            
print("\n ===== ")
print("\n\n EXPECTED \n\n")
g
g_vs_eta_expected_posCor = {}

# expected time resolution vs eta - 
for irrad in data_config:
    print("\n irradiation : ", irrad)
    fnames = data_config[irrad]['fnames']
    g_vs_eta_expected[irrad] = ROOT.TGraphErrors()
    g_vs_eta_expected_posCor[irrad] = ROOT.TGraphErrors()
    for eta in np.arange(0, 1.5 + 0.01, 0.01):
        et = eta
        en = fit_sim_pol2(et)   # if we extract eta through the simulation fit
        # en = g_e_vs_eta_sim.Eval(et)    # if we extract eta directly from simulation points

        s_tot = scale_tot(en, energyMap[pivot[irrad]], s_stoch_ref[irrad], s_noise_ref[irrad], s_dcr_ref[irrad])
        g_vs_eta_expected[irrad].SetPoint(g_vs_eta_expected[irrad].GetN(), et, s_tot)

        if verbose:
            print("\neta : ", round(et,3), "  tres ", round(s_tot,1))
            print("energy : ", round(en,2))
        
        s_tot_posCor = scale_tot_posCor(et, en, energyMap[pivot[irrad]], s_stoch_ref[irrad], s_noise_ref[irrad], s_dcr_ref[irrad])
        g_vs_eta_expected_posCor[irrad].SetPoint(g_vs_eta_expected_posCor[irrad].GetN(), et, s_tot_posCor)
        

        
    print("\n SPEZIALI----")
    for par in etaMap:
        et = etaMap[par]
        #en = g_e_vs_eta_sim.Eval(et)
        en = fit_sim_pol2(et)
        s_tot = scale_tot(en, energyMap[pivot[irrad]], s_stoch_ref[irrad], s_noise_ref[irrad], s_dcr_ref[irrad])
        g_vs_eta_expected[irrad].SetPoint(g_vs_eta_expected[irrad].GetN(), et, s_tot)
    
        if verbose:
            print("eta : ", round(et,3), "  tres ", round(s_tot,1))

        s_tot_posCor = scale_tot_posCor(et, en, energyMap[pivot[irrad]], s_stoch_ref[irrad], s_noise_ref[irrad], s_dcr_ref[irrad])
        g_vs_eta_expected_posCor[irrad].SetPoint(g_vs_eta_expected_posCor[irrad].GetN(), et, s_tot_posCor)
        
    g_vs_eta_expected[irrad].Sort()
    g_vs_eta_expected_posCor[irrad].Sort()




    
if verbose:
    print("\n ===== drawing")

# plot    
leg = ROOT.TLegend(0.55, 0.67, 0.89, 0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045) 

leg2 = ROOT.TLegend(0.20, 0.67, 0.40, 0.89)
leg2.SetBorderSize(0)
leg2.SetFillStyle(0)
leg2.SetTextFont(42)
leg2.SetTextSize(0.045) 

irrad = 'nonIrr'
leg2.AddEntry(g_vs_eta[irrad]['32'], "Data", "P")
leg2.AddEntry(g_vs_eta_expected[irrad], "BTL expectation", "L")
leg2.AddEntry(g_vs_eta_expected_posCor[irrad], "TB expectation", "L")


# ------- time resolution vs eta ----------
c = ROOT.TCanvas("c_timeResolution_vs_eta{}".format(suffix), "c_timeResolution_vs_eta{}".format(suffix), 600, 500)
hPad = ROOT.gPad.DrawFrame(0.,ymin,xmax,ymax)
hPad.SetTitle(";#left|#eta#right|;time resolution [ps]")
hPad.Draw()
ROOT.gPad.SetTicks(1)
for irrad in data_config:
    fnames = data_config[irrad]['fnames']
    for par in fnames:
        print(irrad, par)
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

    g_vs_eta_expected_posCor[irrad].SetLineColor(plotAttrs[irrad][1])
    g_vs_eta_expected_posCor[irrad].SetLineStyle(3)
    g_vs_eta_expected_posCor[irrad].Draw('csame')


    leg.AddEntry(g_vs_eta[irrad][par], plotAttrs[irrad][2], 'L')
leg.Draw()
leg2.Draw()
tl2 = ROOT.TLatex()
tl2.SetNDC()
tl2.SetTextFont(42)
tl2.SetTextSize(0.045)
#tl2.DrawLatex(0.20,0.80,label_on_top)
c.SaveAs(outdir+'%s.png'%c.GetName())
c.SaveAs(outdir+'%s.pdf'%c.GetName())

print("\n\nsaved in ", outdir,c.GetName())
