from utils import *

parser = argparse.ArgumentParser()  
parser.add_argument("-n","--comparisonNumber", required = True, type=str, help="comparison number")    
parser.add_argument('--refTh', action='store_true', help="use a fixed threshold instead of the best threshold")
args = parser.parse_args()   


#---- init ---
comparisonNum = int(args.comparisonNumber)

#-------------
plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/'
color_code = True
marker_code = True
tofhirVersion = '2c'

verbose = True
refTh = args.refTh
# ------------------ 



#  ---------- temperatures ------------
if comparisonNum == 1:
    modules =       ['LYSO815', 'LYSO815']  #,       'LYSO815']
    temperatures =  ['-40',     '-35' ]     # ,           '-30']
    extraName =     ['_angle52','_angle52'] #,      '_angle52']
    extraLabel =    ['',        ''         ]#,     '']
    outSuffix =     'HPK_2E14_LYSO815_temperatures'
    color_code = False
    color_map = [860,800,2]


elif comparisonNum == 2:
    modules =       ['LYSO825', 'LYSO825',       'LYSO825']
    temperatures =  ['-40',     '-35',           '-30']
    extraName =     ['_angle52','_angle52',      '_angle52']
    extraLabel =    ['',        '',              '']
    outSuffix =     'HPK_2E14_LYSO825_temperatures'
    color_code = False
    color_map = [860,800,2]

elif comparisonNum == 3:
    modules =       ['LYSO200104', 'LYSO200104'] #,       'LYSO200104']
    temperatures =  ['-40',     '-35'] #,           '-30']
    extraName =     ['_angle52','_angle52'] #,      '_angle52']
    extraLabel =    ['',        '' ] #,              '']
    outSuffix =     'HPK_2E14_LYSO200104_temperatures'
    color_code = False
    color_map = [860,800,2]

elif comparisonNum == 4:
    modules =       ['LYSO100056', 'LYSO100056',       'LYSO100056']
    temperatures =  ['-40',     '-35',           '-30']
    extraName =     ['_angle52','_angle52',      '_angle52']
    extraLabel =    ['',        '',              '']
    outSuffix =     'HPK_2E14_LYSO100056_temperatures'
    color_code = False
    color_map = [860,800,2]

    
elif comparisonNum == 5:
    print("!! -- WARNING -- !!\nHARD-CODED : 819 and 829 currents and data taken from may TB") # moduleDict includes a "if statement" to take may current 
    tofhirVersion = '2x'
    plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/'
    modules =       ['LYSO819', 'LYSO819',       'LYSO819', 'LYSO819']
    temperatures =  ['-37',     '-32',           '-27', '-22']
    extraName =     ['_angle52','_angle52',      '_angle52', '_angle52']
    extraLabel =    ['',        '',              '', '']
    outSuffix =     'HPK_1E14_LYSO819_temperatures'
    color_code = False
    color_map = [860,870,800,2]
    # modules =       ['LYSO819', 'LYSO819',       'LYSO819']
    # temperatures =  ['-37',     '-32',           '-27']
    # extraName =     ['_angle52','_angle52',      '_angle52']
    # extraLabel =    ['',        '',              '']

    

# ---- MAY TB DATA ------
elif comparisonNum == 6:
    print("!! -- WARNING -- !!\nHARD-CODED : 819 and 829 currents taken from may TB")
    tofhirVersion = '2x'
    plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots/'
    modules =       ['LYSO829', 'LYSO829',       'LYSO829',    'LYSO829']
    temperatures =  ['12',      '0',             '-19',        '-32']
    extraName =     ['_angle52','_angle52',      '_angle52',   '_angle52']
    extraLabel =    ['',        '',              '',           '']
    outSuffix =     'HPK_1E13_LYSO829_temperatures'
    color_code = False
    color_map = [2,800,870,860]

    


# ----------- angles ------------
elif comparisonNum == 10:
    modules =       ['LYSO100056', 'LYSO100056',       'LYSO100056']
    temperatures =  ['-35',     '-35',           '-35']
    extraName =     ['_angle32','_angle52',      '_angle64']
    extraLabel =    [' 32^{o}',        ' 52^{o}',              ' 64^{o}']
    outSuffix =     'HPK_2E14_LYSO100056_T-35C_angles'

elif comparisonNum == 11:
             #   --- angle 32 missing run ---
    # modules =       ['LYSO819', 'LYSO819',       'LYSO819']
    # temperatures =  ['-32',     '-32',           '-32']
    # extraName =     ['_angle32','_angle52',      '_angle64']
    # extraLabel =    [' 32^{o}',        ' 52^{o}',              ' 64^{o}']
    # outSuffix =     'HPK_1E14_LYSO819_T-32C_angles'
    modules =       ['LYSO819',    'LYSO819']
    temperatures =  ['-32',           '-32']
    extraName =     ['_angle52',      '_angle64']
    extraLabel =    [' 52^{o}',       ' 64^{o}']
    outSuffix =     'HPK_1E14_LYSO819_T-32C_angles'




# ----------- types ------------   
elif comparisonNum == 20:
    modules =       ['LYSO100056', 'LYSO815',       'LYSO300032']
    temperatures =  ['-35',     '-35',           '-35']
    extraName =     ['_angle64','_angle64',      '_angle64']
    extraLabel =    ['',        '',              '']
    outSuffix =     'HPK_2E14_T-35C_angle64_types'
    color_code = False
    color_map = [417,2,1]

elif comparisonNum == 21:
    modules =       ['LYSO100056', 'LYSO815']
    temperatures =  ['-35',     '-35']
    extraName =     ['_angle52','_angle52']
    extraLabel =    ['',        '',              '']
    outSuffix =     'HPK_2E14_T-35C_angle52_types'
    color_code = False
    color_map = [417,2]


    

# ----------- cell sizes ------------  
elif comparisonNum == 30:
    modules =       ['LYSO200104', 'LYSO815',       'LYSO825']
    temperatures =  ['-35',     '-35',           '-35']
    extraName =     ['_angle52', '_angle52',      '_angle52']
    extraLabel =    ['',        '',              '']
    outSuffix =     'HPK_2E14_T-35C_angle52_cellSize'


    
#--------------------------------------------------------------------------------------


if refTh:
    outSuffix += "_refTh"


    
if len(modules) != len(temperatures):
    print('ERROR: either one LYSO or temperature is missing')
    sys.exit()

sipmTypes = []
sipmBase = []

outFileName = plotsdir+'/plot_tRes_'+outSuffix+'.root'
outfile = ROOT.TFile(outFileName, 'RECREATE')

for it,module in enumerate(modules):
    sipmTypes.append(sipm_(module)+'_'+lyso_(module)+extraName[it]+'_T'+temperatures[it]+'C')
    print('test: ', sipmTypes[it], '   temp : ', temperatures[it])
    sipmBase.append(sipm_(module)+'_'+lyso_(module))


if verbose:
    print('---- module: ', sipmTypes , '\t outfile: ', outfile," --------")


if color_code:
    color_map = [2,210,4,6,7,8,94]

if marker_code:
    marker_map = [20,20,20,20,20,20,20,20]


# ----- output --------
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/plot_tRes/%s/'%outSuffix

if (os.path.exists(outdir)==False):
    os.mkdir(outdir)
if (os.path.exists(outdir+'/pulseShape')==False):
    os.mkdir(outdir+'/pulseShape/')
if (os.path.exists(outdir+'/bestTh')==False):
    os.mkdir(outdir+'/bestTh/')

if (os.path.exists(outdir+'/slewRate_vs_Vov_perBar')==False):
    os.mkdir(outdir+'/slewRate_vs_Vov_perBar/')

if (os.path.exists(outdir+'/slewRate_vs_bar_perVov')==False):
    os.mkdir(outdir+'/slewRate_vs_bar_perVov/')

if (os.path.exists(outdir+'/slewRate_vs_GainNpe_perBar')==False):
    os.mkdir(outdir+'/slewRate_vs_GainNpe_perBar/')


if (os.path.exists(outdir+'/tRes_vs_bar_perVov')==False):
    os.mkdir(outdir+'/tRes_vs_bar_perVov/')

if (os.path.exists(outdir+'/tRes_vs_Vov_perBar')==False):
    os.mkdir(outdir+'/tRes_vs_Vov_perBar/')

if (os.path.exists(outdir+'/tRes_vs_slewRate')==False):
    os.mkdir(outdir+'/tRes_vs_slewRate/')

if (os.path.exists(outdir+'/tRes_vs_DCRNpe_perBar')==False):
    os.mkdir(outdir+'/tRes_vs_DCRNpe_perBar/')





# -------- retrieve module infos --------
fnames   = {}
labels   = {}
cols     = {}
markers  = {}
LO       = {}
tau      = {}
tauRise  = {}
NpeFrac  = {}
thick    = {}

for it, sipm in enumerate(sipmTypes):
    fnames[sipm]   = '%s/summaryPlots_%s.root'%(plotsdir,sipm)
    labels[sipm]   = label_(sipm) + extraLabel[it]
    cols[sipm]     = color_map[it]
    markers[sipm]  = marker_map[it]
    LO[sipm]       = light_output(sipm)
    tau[sipm]      = tau_decay(sipm)
    tauRise[sipm]  = tau_rise(sipm)
    NpeFrac[sipm]  = Npe_frac(sipm)
    thick[sipm]    = thickness(sipm)






if verbose:
    print(fnames)
    print('defining graphs')
np         = 3
errSRsyst  = 0.10 # error on the slew rate
errPDE     = 0.05 # assumed uncertainty on PDE (5-10%)
errGain    = 0.05

g_data = {}

g_data_vs_Vov_average = {}


# ------ vs Vov -----
g_Noise_vs_Vov     = {}
g_Stoch_vs_Vov     = {}
g_TotExp_vs_Vov    = {}

g_current_vs_Vov   = {}
g_sDCR_vs_Vov      = {}
g_bestTh_vs_Vov    = {}
g_SR_vs_Vov        = {}
g_Npe_vs_Vov       = {}



# ------ vs Npe / Gain -----
g_Stoch_vs_Npe     = {}
g_sDCR_vs_Npe       = {}
g_data_vs_Npe      = {}

g_SR_vs_GainNpe    = {}
g_data_vs_GainNpe  = {}

# ------ vs bar -----
g_bestTh_vs_bar    = {}
g_SR_vs_bar        = {}
g_Noise_vs_bar     = {}
g_Stoch_vs_bar     = {}
g_TotExp_vs_bar       = {}

g_sDCR_vs_bar       = {}

# --- vs SR
g_sDCR_vs_SR       = {}

g_data_vs_SR        = {}
g_Stoch_vs_SR      = {}
g_Noise_vs_SR      = {}

# --- vs DCR 
g_data_vs_DCR      = {}

g_data_vs_staticPower = {}



if verbose:
    print('retrieving bars and ovs')

# --- retrieve bars and ovs from moduleChar plots
bars = {}
goodbars = {}
Vovs = {}
for sipm in sipmTypes:
    f = ROOT.TFile.Open(fnames[sipm])
    print(sipm, fnames[sipm])
    listOfKeys = [key.GetName().replace('g_deltaT_totRatioCorr_bestTh_vs_vov_','') for key in ROOT.gDirectory.GetListOfKeys() if ( 'g_deltaT_totRatioCorr_bestTh_vs_vov_bar' in key.GetName())]
    bars[sipm] = []
    for k in listOfKeys:
        bars[sipm].append( int(k[3:5]) )
    listOfKeys2 = [key.GetName().replace('g_deltaT_totRatioCorr_bestTh_vs_bar_','') for key in ROOT.gDirectory.GetListOfKeys() if key.GetName().startswith('g_deltaT_totRatioCorr_bestTh_vs_bar_')]
    Vovs[sipm] = []
    for k in listOfKeys2:
        Vovs[sipm].append( float(k[3:7]) )

    print(bars[sipm])
    print(Vovs[sipm])
    goodbars[sipm] = good_bars(sipm,Vovs[sipm],bars[sipm])
    

VovsUnion = []
barsUnion = []
barsIntersection = []
for it, sipm in enumerate(sipmTypes):
    if it == 0:
        VovsUnion = Vovs[sipm]
        barsUnion = bars[sipm]
        barsIntersection = bars[sipm]
    else:
        VovsUnion = union(VovsUnion, Vovs[sipm]) 
        barsUnion = union(barsUnion, bars[sipm])
        barsIntersection = intersection(barsIntersection, bars[sipm])
print('ovs union: ', VovsUnion, '\t bars union: ', barsUnion)

# ------   






f      = {}
fPS    = {}
Npe    = {}
gain   = {}

##################
for it,sipm in enumerate(sipmTypes):
    if verbose:
        print("\n  --->  ", fnames[sipm])
        print("\n  --->  ", sipm)
    f[sipm] = ROOT.TFile.Open(fnames[sipm])
    if not f[sipm]:
        print('summary plot file not found')
        sys.exit()

    if refTh:
            g_data_vs_Vov_average[sipm] = f[sipm].Get('g_deltaT_totRatioCorr_refTh_vs_vov_enBin01_average')
    else:
            g_data_vs_Vov_average[sipm] = f[sipm].Get('g_deltaT_totRatioCorr_bestTh_vs_vov_enBin01_average')

    if not isinstance(g_data_vs_Vov_average[sipm], ROOT.TGraphErrors):
        print("AVERAGE GRAPH NOT FOUND IN SUMMARY PLOTS")
        sys.exit()
        
    Npe[sipm]                 = {}
    gain[sipm]                = {}

    g_data[sipm]              = {}

    g_Npe_vs_Vov[sipm]        = ROOT.TGraphErrors()
    g_Noise_vs_Vov[sipm]      = {}
    g_Stoch_vs_Vov[sipm]      = {}
    g_TotExp_vs_Vov[sipm]     = {}

    g_sDCR_vs_Vov[sipm]       = {}
    g_current_vs_Vov[sipm]    = ROOT.TGraphErrors()
    g_SR_vs_Vov[sipm]         = {}
    g_bestTh_vs_Vov[sipm]     = {}
    g_sDCR_vs_Npe[sipm]       = {}


    g_Stoch_vs_Npe[sipm]      = {}
    g_data_vs_Npe[sipm]       = ROOT.TGraphErrors()
    g_SR_vs_GainNpe[sipm]     = {}
    g_data_vs_GainNpe[sipm]   = ROOT.TGraphErrors()


    g_SR_vs_bar[sipm]         = {}
    g_bestTh_vs_bar[sipm]     = {}
    g_Noise_vs_bar[sipm]      = {}
    g_Stoch_vs_bar[sipm]      = {}
    g_TotExp_vs_bar[sipm]     = {}

    g_sDCR_vs_bar[sipm]       = {} # sigma DCR
    
    g_sDCR_vs_SR[sipm]        = {}

    g_Stoch_vs_SR[sipm] = {}
    g_Noise_vs_SR[sipm] = {}
    g_data_vs_SR[sipm] = {}

    g_data_vs_Npe[sipm] = ROOT.TGraphErrors()
    g_data_vs_DCR[sipm] = ROOT.TGraphErrors()
    g_data_vs_staticPower[sipm] = ROOT.TGraphErrors()
    g_data_vs_GainNpe[sipm] = ROOT.TGraphErrors()


    if verbose:
        print('       retrieving pulse shapes')

    fPS[sipm] = {}
    for ov in Vovs[sipm]:
        fPS[sipm][ov] = ROOT.TFile.Open('%s/pulseShape_%s_Vov%.2f%s_T%sC.root'%(plotsdir,sipmBase[it],ov,extraName[it],temperatures[it]))
        if not fPS[sipm][ov]:
            print('pulse shape file not found')

        g_SR_vs_bar[sipm][ov]        = ROOT.TGraphErrors()
        g_bestTh_vs_bar[sipm][ov]    = ROOT.TGraphErrors()
        g_Noise_vs_bar[sipm][ov]     = ROOT.TGraphErrors()
        g_Stoch_vs_bar[sipm][ov]     = ROOT.TGraphErrors()
        g_TotExp_vs_bar[sipm][ov]       = ROOT.TGraphErrors()
        g_sDCR_vs_bar[sipm][ov]       = ROOT.TGraphErrors()

        g_sDCR_vs_SR[sipm][ov]       = ROOT.TGraphErrors()

        g_Stoch_vs_SR[sipm][ov]      = ROOT.TGraphErrors()
        g_Noise_vs_SR[sipm][ov]      = ROOT.TGraphErrors()
        g_data_vs_SR[sipm][ov]        = ROOT.TGraphErrors()



    if verbose:
        print('           retrieving summary plots, loop on bars')


    for bar in bars[sipm]:
        if refTh:
            g_data[sipm][bar] = f[sipm].Get('g_deltaT_totRatioCorr_refTh_vs_vov_bar%02d_enBin01'%bar)
        else:
            g_data[sipm][bar] = f[sipm].Get('g_deltaT_totRatioCorr_bestTh_vs_vov_bar%02d_enBin01'%bar)

        if not isinstance(g_data[sipm][bar], ROOT.TGraphErrors):
            print("GRAPH NOT FOUND IN SUMMARY PLOTS")
            sys.exit()

        if verbose:
            print('\n            bar ', bar)
            for ipoint in range(g_data[sipm][bar].GetN()):
                print('              tres from g_data ', g_data[sipm][bar].GetPointY(ipoint), '  ov: ', g_data[sipm][bar].GetPointX(ipoint))

        g_Noise_vs_Vov[sipm][bar]     = ROOT.TGraphErrors()
        g_Stoch_vs_Vov[sipm][bar]     = ROOT.TGraphErrors()

        g_TotExp_vs_Vov[sipm][bar]    = ROOT.TGraphErrors()
        g_sDCR_vs_Vov[sipm][bar]       = ROOT.TGraphErrors()
        
        g_Stoch_vs_Npe[sipm][bar]     = ROOT.TGraphErrors()
        g_sDCR_vs_Npe[sipm][bar]       = ROOT.TGraphErrors()

        g_SR_vs_Vov[sipm][bar]        = ROOT.TGraphErrors()
        g_SR_vs_GainNpe[sipm][bar]    = ROOT.TGraphErrors()
        g_bestTh_vs_Vov[sipm][bar]    = ROOT.TGraphErrors()
        
    



        if verbose:
            print('           starting loop on ov')

    # --- loop on ov ----        g_data = tRes vs vov
        for ov in Vovs[sipm]:

            ovEff = Vovs_eff(sipm, ov)

            # -- current vs ov eff
            current = getVovEffDCR(sipm, ov)[2]
            g_current_vs_Vov[sipm].SetPoint(g_current_vs_Vov[sipm].GetN(), ovEff, current)

            dcr = DCR(sipm,ovEff)
            
            # --- get measured t_res
            s_data = g_data[sipm][bar].Eval(ovEff)
            indref = [i for i in range(0, g_data[sipm][bar].GetN()) if g_data[sipm][bar].GetPointX(i) == ovEff]
            if ( len(indref)<1 ): continue
            if verbose:
                print("\n              ov: ", ov)
                print("\n              computing slew rates")

            err_s_data = g_data[sipm][bar].GetErrorY(indref[0])            
            
            # Npe and Gain at this OVeff
            Npe[sipm][ov]  = 4.2*LO[sipm]*NpeFrac[sipm]*PDE_(ovEff,sipm)/PDE_(3.5,sipm,'0') 
            gain[sipm][ov] = Gain_(ovEff,sipm)

            # get pulse shapes
            g_psL = fPS[sipm][ov].Get('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov))
            g_psR = fPS[sipm][ov].Get('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov))
            if (g_psL==None and g_psR==None): continue
            if (g_psL!=None): g_psL.SetName('g_pulseShapeL_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            if (g_psR!=None): g_psR.SetName('g_pulseShapeR_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            timingThreshold = findTimingThreshold(f[sipm].Get('g_deltaT_energyRatioCorr_vs_th_bar%02d_Vov%.2f_enBin01'%(bar,ov)))
            srL     = -1
            srR     = -1
            sr      = -1
            err_srL = -1
            err_srR = -1
            c = ROOT.TCanvas('c_%s'%(g_psL.GetName().replace('g_pulseShapeL','pulseShape').replace('Vov%.2f'%ov,'VovEff%.2f'%ovEff)),'',600,500)  
            hdummy = ROOT.TH2F('hdummy','', 100, min(g_psL.GetX())-1., 5, 100, 0., 15.)
            hdummy.GetXaxis().SetTitle('time [ns]')
            hdummy.GetYaxis().SetTitle('amplitude [#muA]')
            hdummy.Draw()
            gtempL = ROOT.TGraphErrors()
            gtempR = ROOT.TGraphErrors()
            
            np = 3
 
            if (g_psL!=None): 
                srL,err_srL = getSlewRateFromPulseShape(g_psL, timingThreshold, np, gtempL, ov, sipm, c)
            if (g_psR!=None): 
                srR,err_srR = getSlewRateFromPulseShape(g_psR, timingThreshold, np, gtempR, ov, sipm, c) 
            line = ROOT.TLine(min(g_psL.GetX())-1., timingThreshold*0.313, 30., timingThreshold*0.313)
            line.SetLineStyle(7)
            line.SetLineWidth(2)
            line.SetLineColor(ROOT.kOrange+1)        
            line.Draw('same')

            # ---- some labels ----
            lat_s = latex_sipm(sipm)
            lat_s.Draw()
            lat = latex_vov(ov)
            lat.Draw()
            lat_b = latex_bar(bar)
            lat_b.Draw()
            c.SaveAs(outdir+'/pulseShape/'+c.GetName()+'.png')   
            hdummy.Delete()


            if (srL>0 and srR>0):
                # weighted average
                # print('srL ', srL, '  srR ', srR, '   err_srR ', err_srR, '  err_srL ', err_srL)
                sr =  ( (srL/(err_srL*err_srL) + srR/(err_srR*err_srR) ) / (1./(err_srL*err_srL) + 1./(err_srR*err_srR) ) )
                errSR = 1./math.sqrt( 1./(err_srL*err_srL)  +  1./(err_srR*err_srR) )
                errSR = errSR
            if (srL>0 and srR<0):
                sr = srL
                errSR = err_srL
            if (srL<0 and srR>0):
                sr = srR
                errSR = err_srR
            if (srL<0 and srR<0): continue
            errSR = math.sqrt(errSR*errSR+errSRsyst*errSRsyst*sr*sr) 

            if errSR>5:
                continue

            if verbose:
                print("            slew rate computed : ", sr)
            s_noise,err_s_noise = sigma_noise(sr, tofhirVersion, errSR)
            #err_s_noise =  0.5*(sigma_noise(sr*(1-errSR/sr), tofhirVersion )-sigma_noise(sr*(1+errSR/sr), tofhirVersion) )

            # compute s_stoch by scaling the stochastic term measured for non-irradiated SiPMs for sqrt(PDE) 
            alpha = 0.73
            PDE = PDE_(ovEff,sipm)
            PDE_nonIrr = PDE_(1.0,sipm,'0') 
            PDE_ratio = PDE / PDE_nonIrr
            #            PDE_nonIrr = PDE_(ov_reference(module),sipm,'0')

            stoch_ref,err_stoch_ref = stoch_ref_fromFit(sipm)
            s_stoch = stoch_ref/pow( PDE_ratio, alpha ) 
            err_s_stoch = math.sqrt( math.pow(math.pow(1/PDE_ratio,alpha)*err_stoch_ref ,2) + math.pow(stoch_ref/math.pow(PDE,alpha)*alpha*math.pow(PDE_nonIrr,(alpha-1))*PDE_nonIrr*errPDE ,2)+ math.pow(stoch_ref *math.pow(PDE_nonIrr, alpha)*(-alpha) * math.pow(PDE,-alpha-1)*PDE*errPDE,2) )
            
            # old method ----
            #stoch_ref = 15/math.pow(PDE_nonIrr, alpha)
            # stoch_ref = stoch_reference(sipm)

            # assume 5% uncertainty on PDE...
            # s_stoch_up = stoch_ref/pow( PDE*(1-errPDE)/PDE_nonIrr, alpha  )
            # s_stoch_down = stoch_ref/pow( PDE*(1+errPDE)/PDE_nonIrr, alpha  )
            # err_s_stoch = 0.5*(s_stoch_up-s_stoch_down)

            
            g_SR_vs_GainNpe[sipm][bar].SetPoint( g_SR_vs_GainNpe[sipm][bar].GetN(), gain[sipm][ov]*Npe[sipm][ov], sr )
            g_SR_vs_GainNpe[sipm][bar].SetPointError( g_SR_vs_GainNpe[sipm][bar].GetN()-1, 0, errSR )
            
            # fill graph vs vov 
            g_Npe_vs_Vov[sipm].SetPoint(g_Npe_vs_Vov[sipm].GetN(), ovEff, Npe[sipm][ov])
            g_SR_vs_Vov[sipm][bar].SetPoint( g_SR_vs_Vov[sipm][bar].GetN(), ovEff, sr )
            g_SR_vs_Vov[sipm][bar].SetPointError( g_SR_vs_Vov[sipm][bar].GetN()-1, 0, errSR )
            g_bestTh_vs_Vov[sipm][bar].SetPoint( g_bestTh_vs_Vov[sipm][bar].GetN(), ovEff, timingThreshold )
            g_bestTh_vs_Vov[sipm][bar].SetPointError( g_bestTh_vs_Vov[sipm][bar].GetN()-1, 0, 0 )
            g_Noise_vs_Vov[sipm][bar].SetPoint(g_Noise_vs_Vov[sipm][bar].GetN(), ovEff, s_noise)
            g_Noise_vs_Vov[sipm][bar].SetPointError(g_Noise_vs_Vov[sipm][bar].GetN()-1, 0, err_s_noise)
            
            # vs bar
            if bar in goodbars[sipm][ov]:
                print("           this bar is ok")
                g_SR_vs_bar[sipm][ov].SetPoint( g_SR_vs_bar[sipm][ov].GetN(), bar, sr )
                g_SR_vs_bar[sipm][ov].SetPointError( g_SR_vs_bar[sipm][ov].GetN()-1, 0, errSR )
                g_bestTh_vs_bar[sipm][ov].SetPoint( g_bestTh_vs_bar[sipm][ov].GetN(), bar, timingThreshold )
                g_bestTh_vs_bar[sipm][ov].SetPointError( g_bestTh_vs_bar[sipm][ov].GetN()-1, 0, 0)
                g_Noise_vs_bar[sipm][ov].SetPoint( g_Noise_vs_bar[sipm][ov].GetN(), bar, s_noise )
                g_Noise_vs_bar[sipm][ov].SetPointError( g_Noise_vs_bar[sipm][ov].GetN()-1, 0,  err_s_noise)
                g_Stoch_vs_bar[sipm][ov].SetPoint( g_Stoch_vs_bar[sipm][ov].GetN(), bar, s_stoch )
                g_Stoch_vs_bar[sipm][ov].SetPointError( g_Stoch_vs_bar[sipm][ov].GetN()-1, 0,  err_s_stoch)
                
            g_Stoch_vs_Vov[sipm][bar].SetPoint(g_Stoch_vs_Vov[sipm][bar].GetN(), ovEff, s_stoch)
            g_Stoch_vs_Vov[sipm][bar].SetPointError(g_Stoch_vs_Vov[sipm][bar].GetN()-1, 0, err_s_stoch)

            if verbose:
                print('          s_data ', s_data, '  s_stoch  ', s_stoch, '   s_noise  ',s_noise)

            # compute sigma_DCR as difference in quadrature between measured tRes and noise, stoch
            if ( s_data*s_data - s_stoch*s_stoch - s_noise*s_noise > 0):
                s_dcr = math.sqrt( s_data*s_data - s_stoch*s_stoch - s_noise*s_noise )
                err_s_dcr = 1./s_dcr * math.sqrt( pow( err_s_data*s_data,2) + pow( err_s_stoch*s_stoch,2) + pow(err_s_noise*s_noise,2))
                if verbose:
                    print("\n          check : ", s_dcr)

                
                g_sDCR_vs_Vov[sipm][bar].SetPoint(g_sDCR_vs_Vov[sipm][bar].GetN(), ovEff, s_dcr)
                g_sDCR_vs_Vov[sipm][bar].SetPointError(g_sDCR_vs_Vov[sipm][bar].GetN()-1, 0, err_s_dcr)

                if bar in goodbars[sipm][ov]:
                    g_sDCR_vs_bar[sipm][ov].SetPoint( g_sDCR_vs_bar[sipm][ov].GetN(), bar, s_dcr )
                    g_sDCR_vs_bar[sipm][ov].SetPointError( g_sDCR_vs_bar[sipm][ov].GetN()-1, 0,  err_s_dcr)
                
                g_sDCR_vs_Npe[sipm][bar].SetPoint( g_sDCR_vs_Npe[sipm][bar].GetN(), math.sqrt(dcr)/Npe[sipm][ov]/(math.sqrt(30.)/3000.), s_dcr )
                g_sDCR_vs_Npe[sipm][bar].SetPointError( g_sDCR_vs_Npe[sipm][bar].GetN()-1, 0,  err_s_dcr)

                # total time resolution   EXPECTED 
                s_tot = math.sqrt( s_stoch*s_stoch + s_noise*s_noise + s_dcr*s_dcr )
                err_s_tot = 1./s_tot * math.sqrt( pow( err_s_stoch*s_stoch,2) + pow(s_noise*err_s_noise,2) + pow(s_dcr*err_s_dcr,2))

                g_TotExp_vs_Vov[sipm][bar].SetPoint(g_TotExp_vs_Vov[sipm][bar].GetN(), ovEff, s_tot)
                g_TotExp_vs_Vov[sipm][bar].SetPointError(g_TotExp_vs_Vov[sipm][bar].GetN()-1, 0, err_s_tot)

                if bar in goodbars[sipm][ov]:
                    g_TotExp_vs_bar[sipm][ov].SetPoint(g_TotExp_vs_bar[sipm][ov].GetN(), bar, s_tot)
                    g_TotExp_vs_bar[sipm][ov].SetPointError(g_TotExp_vs_bar[sipm][ov].GetN()-1, 0, err_s_tot)

                g_sDCR_vs_SR[sipm][ov].SetPoint(g_sDCR_vs_SR[sipm][ov].GetN(), sr, s_dcr)  #  questo non e normalizzato a sqrt(dcr) !! diverso da quello medio che faccio sotto
                g_sDCR_vs_SR[sipm][ov].SetPointError(g_sDCR_vs_SR[sipm][ov].GetN()-1, errSR, err_s_dcr)

                    
            # tRes contributions vs SR
            g_Stoch_vs_SR[sipm][ov].SetPoint(g_Stoch_vs_SR[sipm][ov].GetN(), sr, s_stoch)
            g_Stoch_vs_SR[sipm][ov].SetPointError(g_Stoch_vs_SR[sipm][ov].GetN()-1, errSR, err_s_stoch)

            g_data_vs_SR[sipm][ov].SetPoint(g_data_vs_SR[sipm][ov].GetN(), sr, s_data)
            g_data_vs_SR[sipm][ov].SetPointError(g_data_vs_SR[sipm][ov].GetN()-1, errSR, err_s_data)

            g_Noise_vs_SR[sipm][ov].SetPoint(g_Noise_vs_SR[sipm][ov].GetN(), sr, s_noise)
            g_Noise_vs_SR[sipm][ov].SetPointError(g_Noise_vs_SR[sipm][ov].GetN()-1, errSR, err_s_noise)


            if verbose:
                print("           end loop")


if verbose:
    print('computing average graphs')


#  ----------------------------------------
#  -------------- average -----------------

g_SR_vs_Vov_average = {}
g_Noise_vs_Vov_average = {}
g_Stoch_vs_Vov_average = {}

g_sDCR_vs_Vov_average = {}
g_TotExp_vs_Vov_average = {}

g_DCR_vs_Vov_average = {}

g_sDCR_vs_DCRNpe_average = {}
g_sDCR_vs_DCRNpe_average_all = ROOT.TGraphErrors()

g_sDCRNpe_vs_DCR_average = {}
g_sDCRNpe_vs_DCR_average_all = ROOT.TGraphErrors()

g_sDCR_vs_SR_average = {}
g_sDCR_pdeScaled_vs_DCR_average = {}

g_Noise_vs_Gain_average = {}

# ---

g_Stoch_vs_Npe_average = {}
g_SR_vs_GainPDE_average = {}


for sipm in sipmTypes:
    g_SR_vs_Vov_average[sipm]      = ROOT.TGraphErrors()
    g_sDCR_vs_DCRNpe_average[sipm] = ROOT.TGraphErrors()
    g_sDCRNpe_vs_DCR_average[sipm] = ROOT.TGraphErrors()
    
    g_Noise_vs_Vov_average[sipm]   = ROOT.TGraphErrors()
    g_Stoch_vs_Vov_average[sipm]   = ROOT.TGraphErrors()
    g_sDCR_vs_Vov_average[sipm]    = ROOT.TGraphErrors()
    g_TotExp_vs_Vov_average[sipm]  = ROOT.TGraphErrors()
    g_DCR_vs_Vov_average[sipm]     = ROOT.TGraphErrors()
    
    g_sDCR_vs_SR_average[sipm]            = ROOT.TGraphErrors()
    g_sDCR_pdeScaled_vs_DCR_average[sipm] = ROOT.TGraphErrors()

    g_Noise_vs_Gain_average[sipm] = ROOT.TGraphErrors()
    
    g_Stoch_vs_Npe_average[sipm]  = ROOT.TGraphErrors()
    g_SR_vs_GainPDE_average[sipm] = ROOT.TGraphErrors()

    if verbose:
        print("\n\n ---------------    sipm ", sipm)
    for ov in Vovs[sipm]:
        print(ov)
        ovEff = Vovs_eff(sipm, ov) 
        dcr   = DCR(sipm, ov)
        staticCurrent = float(current_(sipm,ov)) * 1E-03
        #staticCurrent = dcr*1E09 * Gain_(ovEff,sipm) * 1.602E-19
        staticPower = staticCurrent * (37. + ovEff) * 1000.    # in mW
        if verbose:
            print('    ov   : ',ov ,'static power: ', staticPower)

        if (ov in  g_SR_vs_bar[sipm].keys()): 

            # data
            s_meas = g_data_vs_Vov_average[sipm].Eval(ovEff)
            err_s_meas = interp1d(g_data_vs_Vov_average[sipm].GetX(), g_data_vs_Vov_average[sipm].GetEY(), kind='linear')(ovEff)   # interpolating error associated to evaluated point  
            print("s_meas  ", round(s_meas,2), ' err_s_meas ', err_s_meas)
            
            
            # average SR
            fitpol0_sr = ROOT.TF1('fitpol0_sr','pol0',-100,100)
            if (g_SR_vs_bar[sipm][ov].GetN()==0): continue;
            g_SR_vs_bar[sipm][ov].Fit(fitpol0_sr,'QNR')
            sr = fitpol0_sr.GetParameter(0)
            g_SR_vs_Vov_average[sipm].SetPoint(g_SR_vs_Vov_average[sipm].GetN(), ovEff, sr)
            g_SR_vs_Vov_average[sipm].SetPointError(g_SR_vs_Vov_average[sipm].GetN()-1, 0, fitpol0_sr.GetParError(0))

            # noise using average SR
            sr_err = max(fitpol0_sr.GetParError(0), errSRsyst*sr)
            s_noise,err_s_noise = sigma_noise(sr, tofhirVersion,sr_err)
            g_Noise_vs_Vov_average[sipm].SetPoint(g_Noise_vs_Vov_average[sipm].GetN(), ovEff, s_noise)
            #sr_up   = sr + sr_err 
            #sr_down = sr - sr_err 
            #err_s_noise  = 0.5 * ( sigma_noise(sr_down, tofhirVersion) - sigma_noise(sr_up, tofhirVersion) ) 
            g_Noise_vs_Vov_average[sipm].SetPointError(g_Noise_vs_Vov_average[sipm].GetN()-1, 0, err_s_noise) 
            print("s_noise  ", round(s_noise,2), ' err_s_noise ', round(err_s_noise,2))

            
            # average stochastic 
            fitpol0_stoch = ROOT.TF1('fitpol0_stoch','pol0',-100,100)  
            g_Stoch_vs_bar[sipm][ov].Fit(fitpol0_stoch,'QNR')
            s_stoch = fitpol0_stoch.GetParameter(0)
            err_s_stoch = fitpol0_stoch.GetParError(0)
            g_Stoch_vs_Vov_average[sipm].SetPoint(g_Stoch_vs_Vov_average[sipm].GetN(), ovEff, s_stoch)
            g_Stoch_vs_Vov_average[sipm].SetPointError(g_Stoch_vs_Vov_average[sipm].GetN()-1, 0, err_s_stoch)
            print("s_stoch  ", round(s_stoch,2), ' err_s_stoch ', round(err_s_stoch,2))
            
            # average dcr
            fitpol0_sdcr = ROOT.TF1('fitpol0_sdcr','pol0',-100,100)  
            g_sDCR_vs_bar[sipm][ov].Fit(fitpol0_sdcr,'QNR')
            #s_dcr =  fitpol0_sdcr.GetParameter(0)
            #err_s_dcr = fitpol0_sdcr.GetParError(0)
            if (s_meas*s_meas - s_noise*s_noise - s_stoch*s_stoch > 0):
                s_dcr = math.sqrt(s_meas*s_meas - s_noise*s_noise - s_stoch*s_stoch)
                err_s_dcr = 1./s_dcr * math.sqrt( pow(s_meas*err_s_meas,2) + pow( err_s_stoch*s_stoch,2) + pow(err_s_noise*s_noise,2))
            else:
                s_dcr =  fitpol0_sdcr.GetParameter(0)
                err_s_dcr = fitpol0_sdcr.GetParError(0)

            print("s_dcr  ", round(s_dcr,2), ' err_s_dcr ', round(err_s_dcr,2))
            g_sDCR_vs_Vov_average[sipm].SetPoint(g_sDCR_vs_Vov_average[sipm].GetN(), ovEff, s_dcr)
            g_sDCR_vs_Vov_average[sipm].SetPointError(g_sDCR_vs_Vov_average[sipm].GetN()-1, 0, err_s_dcr)

            # tot resolution summing noise + stochastic + dcr in quadrature
            tot = math.sqrt( s_stoch*s_stoch + s_noise*s_noise + s_dcr*s_dcr )
            err_tot = 1./tot * math.sqrt( pow( err_s_stoch*s_stoch,2) + pow(err_s_noise*s_noise,2) + pow(s_dcr*err_s_dcr, 2) )
            g_TotExp_vs_Vov_average[sipm].SetPoint(g_TotExp_vs_Vov_average[sipm].GetN(), ovEff, tot)
            g_TotExp_vs_Vov_average[sipm].SetPointError(g_TotExp_vs_Vov_average[sipm].GetN()-1, 0, err_tot)


            print("      CHECKONE ::: ", round(s_meas,1), " noise : ", round(s_noise,1)," stoch : ",round(s_stoch,1), " dcr : ", round(s_dcr,1))
            
            # DCR, non sigma DCR
            dcr = getVovEffDCR(sipm, ov)[1]
            err_dcr = 0
            g_DCR_vs_Vov_average[sipm].SetPoint(g_sDCR_vs_Vov_average[sipm].GetN(), ovEff, dcr)
            g_DCR_vs_Vov_average[sipm].SetPointError(g_DCR_vs_Vov_average[sipm].GetN()-1, 0, err_dcr)

            
            # sigma dcr ave vs SR average
            g_sDCR_vs_SR_average[sipm].SetPoint(g_sDCR_vs_SR_average[sipm].GetN(), sr, s_dcr/math.sqrt(dcr))
            err = math.sqrt(err_s_dcr*err_s_dcr/dcr + s_dcr*s_dcr*err_dcr*err_dcr/(4*dcr*dcr*dcr))
            g_sDCR_vs_SR_average[sipm].SetPointError(g_sDCR_vs_SR_average[sipm].GetN()-1, fitpol0_sr.GetParError(0), err)

            
            # average tRes vs Npe, DCR, static power, GainNpe            
            g_data_vs_Npe[sipm].SetPoint(g_data_vs_Npe[sipm].GetN(), Npe[sipm][ov], s_meas)
            g_data_vs_Npe[sipm].SetPointError(g_data_vs_Npe[sipm].GetN()-1, 0, err_s_meas)

            g_data_vs_DCR[sipm].SetPoint(g_data_vs_DCR[sipm].GetN(), dcr, s_meas)
            g_data_vs_DCR[sipm].SetPointError(g_data_vs_DCR[sipm].GetN()-1, 0,  err_s_meas)

            g_data_vs_staticPower[sipm].SetPoint(g_data_vs_staticPower[sipm].GetN(), staticPower, s_meas)
            g_data_vs_staticPower[sipm].SetPointError(g_data_vs_staticPower[sipm].GetN()-1, 0,  err_s_meas)

            g_data_vs_GainNpe[sipm].SetPoint(g_data_vs_GainNpe[sipm].GetN(), gain[sipm][ov]*Npe[sipm][ov],s_meas)
            g_data_vs_GainNpe[sipm].SetPointError(g_data_vs_GainNpe[sipm].GetN()-1, 0, err_s_meas)

            
            # errors missing  -------
            x = math.sqrt(dcr)/Npe[sipm][ov]/ (math.sqrt(30.)/3000)
            x_down = math.sqrt(dcr)/(Npe[sipm][ov]*(1+errPDE) )/ (math.sqrt(30.)/3000)
            x_up   = math.sqrt(dcr)/(Npe[sipm][ov]*(1-errPDE))/ (math.sqrt(30.)/3000)
            if (g_sDCR_vs_bar[sipm][ov].GetN()==0):continue
            g_sDCR_vs_DCRNpe_average[sipm].SetPoint( g_sDCR_vs_DCRNpe_average[sipm].GetN(), x,  s_dcr)
            g_sDCR_vs_DCRNpe_average_all.SetPoint( g_sDCR_vs_DCRNpe_average_all.GetN(), x,  s_dcr)
            y = s_dcr * Npe[sipm][ov]/6000 
            g_sDCRNpe_vs_DCR_average[sipm].SetPoint( g_sDCRNpe_vs_DCR_average[sipm].GetN(), dcr, y )
            g_sDCRNpe_vs_DCR_average_all.SetPoint( g_sDCRNpe_vs_DCR_average_all.GetN(), dcr, y)
            gainPDE = gain[sipm][ov]*PDE_(ovEff,sipm)
            g_SR_vs_GainPDE_average[sipm].SetPoint(g_SR_vs_GainPDE_average[sipm].GetN(), gainPDE, sr)
            # ----------------

            # ------ sigma dcr scaled per pde ratio vs dcr ------
            pderef = PDE_(1.0,'LYSO818','0')
            pde = PDE_(ovEff,sipm)
            err_pderef = pderef*errPDE
            err_pde = pde*errPDE
            err_s_dcr_pdeScaled = 1/pderef * math.sqrt(math.pow(pde*err_s_dcr,2) + math.pow(s_dcr*err_pde,2) + math.pow(s_dcr*pde/pderef*err_pderef,2) )
            g_sDCR_pdeScaled_vs_DCR_average[sipm].SetPoint(g_sDCR_pdeScaled_vs_DCR_average[sipm].GetN(), dcr, s_dcr*pde/pderef)
            g_sDCR_pdeScaled_vs_DCR_average[sipm].SetPointError(g_sDCR_pdeScaled_vs_DCR_average[sipm].GetN()-1, err_dcr,err_s_dcr_pdeScaled) 


            # ---- noise vs gain ----
            g_Noise_vs_Gain_average[sipm].SetPoint(g_Noise_vs_Gain_average[sipm].GetN(),Gain_(ovEff,sipm), s_noise)
            g_Noise_vs_Gain_average[sipm].SetPointError(g_Noise_vs_Gain_average[sipm].GetN()-1, Gain_(ovEff,sipm)*errGain, err_s_noise)
            

            
# Andrea's model
fitFun_tRes_dcr_model = ROOT.TF1('fitFun_tRes_dcr_model','[1] * pow(x,[0])', 0,10)
fitFun_tRes_dcr_model.SetParameter(0,0.4)
fitFun_tRes_dcr_model.SetParameter(1,40)
fitFun_tRes_dcr_model.SetLineColor(1)
g_sDCR_vs_DCRNpe_average_all.Fit(fitFun_tRes_dcr_model)



if verbose:
    print('\n\nstart drawing')



#################### #################### #################### #################### #################### #################### 
###### DRAW  #################### #################### #################### #################### #################### ####################
################### #################### #################### #################### #################### ####################


leg = {}

# --------------------------------------------------------------------------------------------------------------
# ----- things vs things per bar
# Tres vs OV -- per bar
print('Plotting time resolution vs OV...')
for sipm in sipmTypes:
    leg[sipm] = ROOT.TLegend(0.65,0.60,0.89,0.79)
    leg[sipm].SetBorderSize(0)
    leg[sipm].SetFillStyle(0)
    for i,bar in enumerate(bars[sipm]):
        if (bar not in g_data[sipm].keys()): continue
        if (g_data[sipm][bar].GetN()==0): continue
        c =  ROOT.TCanvas('c_timeResolution_vs_Vov_%s_bar%02d'%(sipm,bar),'c_timeResolution_vs_Vov_%s_bar%02d'%(sipm,bar),600,500)
        c.SetGridy()
        c.cd()
        xmin = 0.0
        xmax = 2.0
        hdummy = ROOT.TH2F('hdummy_%s_%d'%(sipm,bar),'',100,xmin,xmax,140,0,120)
        hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
        hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
        hdummy.Draw()

        g_data[sipm][bar].SetMarkerStyle(20)
        g_data[sipm][bar].SetMarkerSize(1)
        g_data[sipm][bar].SetMarkerColor(1)
        g_data[sipm][bar].SetLineColor(1)
        g_data[sipm][bar].SetLineWidth(2)
        g_data[sipm][bar].Draw('plsame')
        if (bar not in g_Noise_vs_Vov[sipm].keys()): continue

        g_Noise_vs_Vov[sipm][bar].SetLineWidth(2)
        g_Noise_vs_Vov[sipm][bar].SetLineColor(ROOT.kBlue)
        g_Noise_vs_Vov[sipm][bar].SetFillColor(ROOT.kBlue)
        g_Noise_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kBlue,0.5)
        g_Noise_vs_Vov[sipm][bar].SetFillStyle(3004)
        g_Noise_vs_Vov[sipm][bar].Draw('E3lsame')

        g_Stoch_vs_Vov[sipm][bar].SetLineWidth(2)
        g_Stoch_vs_Vov[sipm][bar].SetLineColor(ROOT.kGreen+2)
        g_Stoch_vs_Vov[sipm][bar].SetFillColor(ROOT.kGreen+2)
        g_Stoch_vs_Vov[sipm][bar].SetFillStyle(3001)
        g_Stoch_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kGreen+2,0.5)
        g_Stoch_vs_Vov[sipm][bar].Draw('E3lsame')

        g_sDCR_vs_Vov[sipm][bar].SetLineWidth(2)
        g_sDCR_vs_Vov[sipm][bar].SetLineColor(ROOT.kOrange+2)
        g_sDCR_vs_Vov[sipm][bar].SetFillColor(ROOT.kOrange+2)
        g_sDCR_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kOrange+2,0.5)
        g_sDCR_vs_Vov[sipm][bar].SetFillStyle(3001)
        g_sDCR_vs_Vov[sipm][bar].Draw('E3lsame')

        g_TotExp_vs_Vov[sipm][bar].SetLineWidth(2)
        g_TotExp_vs_Vov[sipm][bar].SetLineColor(ROOT.kRed+1)
        g_TotExp_vs_Vov[sipm][bar].SetFillColor(ROOT.kRed+1)
        g_TotExp_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kRed+1,0.5)
        g_TotExp_vs_Vov[sipm][bar].SetFillStyle(3001)

        #save on file
        outfile.cd()
        g_data[sipm][bar].Write('g_Data_vs_Vov_%s_bar%02d'%(sipm,  bar))
        g_Noise_vs_Vov[sipm][bar].Write('g_Noise_vs_Vov_%s_bar%02d'%(sipm, bar))
        g_Stoch_vs_Vov[sipm][bar].Write('g_Stoch_vs_Vov_%s_bar%02d'%(sipm, bar))
        g_sDCR_vs_Vov[sipm][bar].Write('g_DCR_vs_Vov_%s_bar%02d'%(sipm, bar))

        if (i==0):
            leg[sipm].AddEntry(g_data[sipm][bar], 'data', 'PL')
            leg[sipm].AddEntry(g_Noise_vs_Vov[sipm][bar], 'noise', 'L')
            leg[sipm].AddEntry(g_Stoch_vs_Vov[sipm][bar], 'stoch', 'L')
            leg[sipm].AddEntry(g_sDCR_vs_Vov[sipm][bar], 'DCR', 'L')

        leg[sipm].Draw('same')

        latex = ROOT.TLatex(0.20,0.85,'%s'%(sipm.replace('_',' ').replace('T','T=')))
        latex.SetNDC()
        latex.SetTextSize(0.045)
        latex.SetTextFont(42)
        latex.Draw('same')

        cms_logo = draw_logo()
        cms_logo.Draw()

        c.SaveAs(outdir+'/tRes_vs_Vov_perBar/'+c.GetName()+'.png')
        c.SaveAs(outdir+'/tRes_vs_Vov_perBar/'+c.GetName()+'.pdf')
        hdummy.Delete()
        

# -----------   vs npe per bar ----------------
print('Plotting tRes_DCR vs Npe...')

for bar in range(0,16):      
    c =  ROOT.TCanvas('c_timeResolutionDCR_vs_DCRNpe_bar%02d'%(bar),'c_timeResolutionDCR_vs_DCRNpe_bar%02d'%(bar),600,500)
    c.SetGridx()
    c.SetGridy()
    c.cd()
    xmax = 2
    ymax = 100
    hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,0,xmax,100,0,ymax)
    hdummy.GetXaxis().SetTitle('#sqrt{DCR/30GHz}/(Npe/3000)')
    hdummy.GetYaxis().SetTitle('#sigma_{t}^{DCR} [ps]')
    hdummy.Draw()
    for sipm in sipmTypes:
        if (bar not in g_sDCR_vs_Npe[sipm].keys()): continue
        g_sDCR_vs_Npe[sipm][bar].SetMarkerStyle(markers[sipm])
        g_sDCR_vs_Npe[sipm][bar].SetMarkerColor(cols[sipm])
        g_sDCR_vs_Npe[sipm][bar].SetLineWidth(1)
        g_sDCR_vs_Npe[sipm][bar].SetLineColor(cols[sipm])
        g_sDCR_vs_Npe[sipm][bar].Draw('psame')

    cms_logo = draw_logo()
    cms_logo.Draw()

    c.SaveAs(outdir+'/tRes_vs_DCRNpe_perBar/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_DCRNpe_perBar/'+c.GetName()+'.pdf')
    hdummy.Delete()

# SR and best threshold vs Vov
leg2 = ROOT.TLegend(0.40,0.65,0.85,0.9)
leg2.SetBorderSize(0)
leg2.SetFillStyle(0)

bar = barsIntersection[0]
for sipm in sipmTypes:
    g_SR_vs_Vov[sipm][bar].SetMarkerStyle(markers[sipm])
    g_SR_vs_Vov[sipm][bar].SetMarkerColor(cols[sipm])
    g_SR_vs_Vov[sipm][bar].SetLineColor(cols[sipm])
    leg2.AddEntry(g_SR_vs_Vov[sipm][bar], '%s'%labels[sipm], 'PL')

for bar in range(0,16):
    if (bar not in g_data[sipm].keys()): continue
    if (g_data[sipm][bar].GetN()==0): continue     
    c = ROOT.TCanvas('c_slewRate_vs_Vov_bar%02d'%(bar),'c_slewRate_vs_Vov_bar%02d'%(bar),600,500)
    c.SetGridy()
    c.cd()
    xmin = 0.0
    xmax = 2.0
    ymax = 35
    hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,xmin,xmax,100,0,ymax)
    hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
    hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.Draw()
    for sipm in sipmTypes:
        if (bar not in g_SR_vs_Vov[sipm].keys()): continue
        g_SR_vs_Vov[sipm][bar].SetMarkerStyle(markers[sipm])
        g_SR_vs_Vov[sipm][bar].SetMarkerColor(cols[sipm])
        g_SR_vs_Vov[sipm][bar].SetLineColor(cols[sipm])
        g_SR_vs_Vov[sipm][bar].Draw('plsame')
    leg2.Draw()
    outfile.cd()
    g_SR_vs_Vov[sipm][bar].Write('g_SR_vs_Vov_%s_bar%02d'%(sipm,bar))
    c.SaveAs(outdir+'/slewRate_vs_Vov_perBar/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/slewRate_vs_Vov_perBar/'+c.GetName()+'.pdf')
    hdummy.Delete()
    i=i+1


    c = ROOT.TCanvas('c_slewRate_vs_GainNpe_bar%02d'%(bar),'c_slewRate_vs_GainNpe_bar%02d'%(bar),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,0,3E09,100,0,35)
    hdummy.GetXaxis().SetTitle('gain x Npe')
    hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.Draw()
    for sipm in sipmTypes:
        if (bar not in g_SR_vs_GainNpe[sipm].keys()): continue
        g_SR_vs_GainNpe[sipm][bar].SetMarkerStyle( markers[sipm] )
        g_SR_vs_GainNpe[sipm][bar].SetMarkerColor(cols[sipm])
        g_SR_vs_GainNpe[sipm][bar].SetLineColor(cols[sipm])
        g_SR_vs_GainNpe[sipm][bar].Draw('psame')
    leg2.Draw()


    cms_logo = draw_logo()
    cms_logo.Draw()

    c.SaveAs(outdir+'/slewRate_vs_GainNpe_perBar/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/slewRate_vs_GainNpe_perBar/'+c.GetName()+'.pdf')
    hdummy.Delete()

    c = ROOT.TCanvas('c_bestTh_vs_Vov_bar%02d'%(bar),'c_bestTh_vs_Vov_bar%02d'%(bar),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,xmin,xmax,100,0,20)
    hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
    hdummy.GetYaxis().SetTitle('best threshold [DAC]')
    hdummy.Draw()
    

    for sipm in sipmTypes:
        if (bar not in g_bestTh_vs_Vov[sipm].keys()): continue
        g_bestTh_vs_Vov[sipm][bar].SetMarkerStyle(markers[sipm])
        g_bestTh_vs_Vov[sipm][bar].SetMarkerColor(cols[sipm])
        g_bestTh_vs_Vov[sipm][bar].SetLineColor(cols[sipm])
        g_bestTh_vs_Vov[sipm][bar].Draw('plsame')


    cms_logo = draw_logo()
    cms_logo.Draw()

    c.SaveAs(outdir+'/bestTh/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/bestTh/'+c.GetName()+'.pdf')
    hdummy.Delete()
# --------------------------------------------------------------------------------------------------------------






# --------------------------------------------------------------------------------------------------------------
# --- sigma DCR vs things
# --- DCRNpe vs DCR
c =  ROOT.TCanvas('c_timeResolutionDCRNpe_vs_DCR_average','c_timeResolutionDCRNpe_vs_DCR_average',600,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,0,50,100,0,100)
hdummy.GetXaxis().SetTitle('DCR[GHz]')
hdummy.GetYaxis().SetTitle('(Npe/6000) #times #sigma_{t}^{DCR} [ps]')
hdummy.Draw()
fitFun_tRes_dcr = ROOT.TF1('fitFun_tRes_dcr','[1] * pow(x/30.,[0])', 0,10)  
fitFun_tRes_dcr.SetParameter(0,0.5)
fitFun_tRes_dcr.SetParameter(1,40)
fitFun_tRes_dcr.SetLineColor(1)

g_sDCRNpe_vs_DCR_average_all.Fit(fitFun_tRes_dcr)
g_sDCRNpe_vs_DCR_average_all.SetMarkerSize(0.1)
g_sDCRNpe_vs_DCR_average_all.Draw('p*same')
fitFun_tRes_dcr.Draw('same')
outfile.cd() 
g_sDCRNpe_vs_DCR_average_all.Write('g_DCRNpe_vs_DCR_average_all')

for sipm in sipmTypes:
    g_sDCRNpe_vs_DCR_average[sipm].SetMarkerStyle(markers[sipm])
    g_sDCRNpe_vs_DCR_average[sipm].SetMarkerColor(cols[sipm])
    g_sDCRNpe_vs_DCR_average[sipm].SetLineWidth(1)
    g_sDCRNpe_vs_DCR_average[sipm].SetLineColor(cols[sipm])
    g_sDCRNpe_vs_DCR_average[sipm].Draw('psame')
    outfile.cd() 
    g_sDCRNpe_vs_DCR_average[sipm].Write('g_DCRNpe_vs_DCR_average_%s'%sipm)

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()


# ---- average sigma DCR vs average slew rate --------
c =  ROOT.TCanvas('c_DCR_vs_SR_average','c_DCR_vs_SR_average',600,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',20, 0, 35,100, 0, 30)
hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
hdummy.GetYaxis().SetTitle('#sigma_{t, DCR}/#sqrt{DCR} [ps]')
hdummy.Draw()
for sipm in sipmTypes:
    g_sDCR_vs_SR_average[sipm].SetMarkerStyle(markers[sipm])
    g_sDCR_vs_SR_average[sipm].SetMarkerColor(cols[sipm])
    g_sDCR_vs_SR_average[sipm].SetLineWidth(1)
    g_sDCR_vs_SR_average[sipm].SetLineColor(cols[sipm])
    g_sDCR_vs_SR_average[sipm].Draw('plsame')
    outfile.cd()
    g_sDCR_vs_SR_average[sipm].Write('g_DCR_vs_SR_average_%s'%(sipm))
leg2.Draw()


cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()



# -- average DCR vs DCRNpe
c =  ROOT.TCanvas('c_timeResolutionDCR_vs_DCRNpe_average','c_timeResolutionDCR_vs_DCRNpe_average',600,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,0,2.0,100,0,100)
hdummy.GetXaxis().SetTitle('#sqrt{DCR/30GHz}/(Npe/3000)')
hdummy.GetYaxis().SetTitle('#sigma_{t}^{DCR} [ps]')
hdummy.Draw()
g_sDCR_vs_DCRNpe_average_all.SetMarkerSize(0.1)
g_sDCR_vs_DCRNpe_average_all.Draw('p*same')
fitFun_tRes_dcr_model.Draw('same')
outfile.cd() 
g_sDCR_vs_DCRNpe_average_all.Write('g_DCR_vs_DCRNpe_average_all')
for sipm in sipmTypes:
    g_sDCR_vs_DCRNpe_average[sipm].SetMarkerStyle(markers[sipm])
    g_sDCR_vs_DCRNpe_average[sipm].SetMarkerColor(cols[sipm])
    g_sDCR_vs_DCRNpe_average[sipm].SetLineWidth(1)
    g_sDCR_vs_DCRNpe_average[sipm].SetLineColor(cols[sipm])
    g_sDCR_vs_DCRNpe_average[sipm].Draw('psame')
    outfile.cd() 
    g_sDCR_vs_DCRNpe_average[sipm].Write('g_DCR_vs_DCRNpe_average_%s'%sipm)

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()


# ---- average sigma DCR vs average slew rate --------
c =  ROOT.TCanvas('c_DCR_pdescaled_vs_DCR_average','c_DCR_pdescaled_vs_DCR_average',600,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',20, 0, 70,100, 0, 100)
hdummy.GetXaxis().SetTitle('DCR [Ghz]')
hdummy.GetYaxis().SetTitle('#sigma_{t, DCR} pdescaled [ps]')
hdummy.Draw()
for sipm in sipmTypes:
    g_sDCR_pdeScaled_vs_DCR_average[sipm].SetMarkerStyle(markers[sipm])
    g_sDCR_pdeScaled_vs_DCR_average[sipm].SetMarkerColor(cols[sipm])
    g_sDCR_pdeScaled_vs_DCR_average[sipm].SetLineWidth(1)
    g_sDCR_pdeScaled_vs_DCR_average[sipm].SetLineColor(cols[sipm])
    g_sDCR_pdeScaled_vs_DCR_average[sipm].Draw('plsame')
    outfile.cd()
    g_sDCR_pdeScaled_vs_DCR_average[sipm].Write('g_DCR_pdescaled_vs_DCR_average_%s'%(sipm))
leg2.Draw()


cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()



# --------------------------------------------------------------------------------------------------------------







# -------- average things vs Vov
# --- data average vs Vov Eff
c =  ROOT.TCanvas('c_data_average_vs_Vov', 'c_data_average_vs_Vov',600,500)
c.SetGridx()
c.SetGridy()
c.cd()
hdummy = ROOT.TH2F('hdummy','',16, 0.0, 2.0 ,100, 0,120)
hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.Draw()
for sipm in sipmTypes:
    g_data_vs_Vov_average[sipm].SetMarkerStyle(markers[sipm])
    g_data_vs_Vov_average[sipm].SetMarkerColor(cols[sipm])
    g_data_vs_Vov_average[sipm].SetLineWidth(1)
    g_data_vs_Vov_average[sipm].SetLineColor(cols[sipm])
    g_data_vs_Vov_average[sipm].Draw('plsame')
    outfile.cd()
leg2.Draw()

cms_logo = draw_logo()
cms_logo.Draw()
c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()
del hdummy
del c



# --- current vs Vov Eff
c =  ROOT.TCanvas('c_current_vs_Vov', 'c_current_vs_Vov',600,500)
c.SetGridx()
c.SetGridy()
c.cd()
hdummy = ROOT.TH2F('hdummy','',16, 0.0, 2.0 ,100, 0, 2.5)
hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
hdummy.GetYaxis().SetTitle('I')
hdummy.Draw()
for sipm in sipmTypes:
    g_current_vs_Vov[sipm].Sort()
    g_current_vs_Vov[sipm].SetMarkerStyle(markers[sipm])
    g_current_vs_Vov[sipm].SetMarkerColor(cols[sipm])
    g_current_vs_Vov[sipm].SetLineWidth(1)
    g_current_vs_Vov[sipm].SetLineColor(cols[sipm])
    g_current_vs_Vov[sipm].Draw('plsame')
    outfile.cd()
    g_current_vs_Vov[sipm].Write('g_current_vs_Vov_%s'%(sipm))
leg2.Draw()

cms_logo = draw_logo()
cms_logo.Draw()
c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()
del hdummy
del c


# average slew rate vs OV
c =  ROOT.TCanvas('c_slewRate_vs_Vov_average','c_slewRate_vs_Vov_average',600,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',16, 0.0, 2.0 ,100, 0,35)
hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
hdummy.Draw()
for sipm in sipmTypes:
    g_SR_vs_Vov_average[sipm].SetMarkerStyle(markers[sipm])
    g_SR_vs_Vov_average[sipm].SetMarkerColor(cols[sipm])
    g_SR_vs_Vov_average[sipm].SetLineWidth(1)
    g_SR_vs_Vov_average[sipm].SetLineColor(cols[sipm])
    g_SR_vs_Vov_average[sipm].Draw('plsame')
    outfile.cd()
    g_SR_vs_Vov_average[sipm].Write('g_SR_vs_Vov_average_%s'%(sipm))
leg2.Draw()

cms_logo = draw_logo()
cms_logo.Draw()
c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()
# --------------------------------------------------------------------------------------------------------------













# ----------- average time resolution vs things -----------

# average time resolution vs Npe
c =  ROOT.TCanvas('c_timeResolution_vs_Npe_average','c_timeResolution_vs_Npe_average',600,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',1000, 1000, 10000, 100, 20, 120)
hdummy.GetXaxis().SetTitle('Npe')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.GetXaxis().SetNdivisions(505)
hdummy.Draw()
for sipm in sipmTypes:
    g_data_vs_Npe[sipm].SetMarkerStyle(markers[sipm])
    g_data_vs_Npe[sipm].SetMarkerColor(cols[sipm])
    g_data_vs_Npe[sipm].SetLineWidth(1)
    g_data_vs_Npe[sipm].SetLineColor(cols[sipm])
    g_data_vs_Npe[sipm].Draw('plsame')
    outfile.cd()
    g_data_vs_Npe[sipm].Write('g_data_vs_Npe_average_%s'%(sipm))
leg2.Draw()  

cms_logo = draw_logo()
cms_logo.Draw()


c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()

c =  ROOT.TCanvas('c_timeResolution_vs_DCR_average','c_timeResolution_vs_DCR_average',600,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',1000, 0, 100, 20, 0, 120)
hdummy.GetXaxis().SetTitle('DCR [GHz]')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.Draw()
for sipm in sipmTypes:
    g_data_vs_DCR[sipm].SetMarkerStyle(markers[sipm])
    g_data_vs_DCR[sipm].SetMarkerColor(cols[sipm])
    g_data_vs_DCR[sipm].SetLineWidth(1)
    g_data_vs_DCR[sipm].SetLineColor(cols[sipm])
    g_data_vs_DCR[sipm].Draw('plsame')
    outfile.cd()
    g_data_vs_DCR[sipm].Write('g_data_vs_DCR_average_%s'%(sipm))
leg2.Draw()  

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()


# average time resolution vs static power
c =  ROOT.TCanvas('c_timeResolution_vs_staticPower_average','c_timeResolution_vs_staticPower_average',600,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',1000, 0, 120, 100, 0, 120)
hdummy.GetXaxis().SetTitle('static power [mW]')


hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.Draw()
for sipm in sipmTypes:
    g_data_vs_staticPower[sipm].SetMarkerStyle(markers[sipm])
    g_data_vs_staticPower[sipm].SetMarkerColor(cols[sipm])
    g_data_vs_staticPower[sipm].SetLineWidth(1)
    g_data_vs_staticPower[sipm].SetLineColor(cols[sipm])
    g_data_vs_staticPower[sipm].Draw('plsame')
    outfile.cd()
    g_data_vs_staticPower[sipm].Write('g_data_vs_staticPower_average_%s'%(sipm))
leg2.Draw()  

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()

# average time resolution vs GainxNpe
c =  ROOT.TCanvas('c_timeResolution_vs_GainNpe_average','c_timeResolution_vs_GainNpe_average',600,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',1000, 0, 3E09, 100, 20, 120)
hdummy.GetXaxis().SetTitle('Gain x Npe')
hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
hdummy.GetXaxis().SetNdivisions(505)
hdummy.Draw()
for sipm in sipmTypes:
    g_data_vs_GainNpe[sipm].SetMarkerStyle(markers[sipm])
    g_data_vs_GainNpe[sipm].SetMarkerColor(cols[sipm])
    g_data_vs_GainNpe[sipm].SetLineWidth(1)
    g_data_vs_GainNpe[sipm].SetLineColor(cols[sipm])
    g_data_vs_GainNpe[sipm].Draw('plsame')
leg2.Draw()  

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()
# --------------------------------------------------------------------------------------------------------------












# --------------------------------------------------------------------------------------------------------------
#  ---  average time resolution with contributions ----------------
for sipm in sipmTypes:
    latex = ROOT.TLatex(0.18,0.84,'%s'%(labels[sipm]))
    latex.SetNDC()
    latex.SetTextSize(0.05)
    latex.SetTextFont(42)
    c =  ROOT.TCanvas('c_timeResolution_vs_Vov_average_%s'%(sipm),'c_timeResolution_vs_Vov_average_%s'%(sipm),600,500)
    c.cd()
    hdummy = ROOT.TH2F('hdummy','',100, 0., 2.,100,0,120)
    hdummy.GetXaxis().SetTitle('V_{OV} [V]')
    hdummy.GetYaxis().SetTitle('time resolution [ps]')
    hdummy.Draw()
    
    ROOT.gPad.SetTicks(1)
    g_data_vs_Vov_average[sipm].SetMarkerStyle(20)
    g_data_vs_Vov_average[sipm].SetMarkerSize(1)
    g_data_vs_Vov_average[sipm].SetMarkerColor(1)
    g_data_vs_Vov_average[sipm].SetLineColor(1)
    g_data_vs_Vov_average[sipm].SetLineWidth(2)
    g_data_vs_Vov_average[sipm].Draw('plsame')

    g_Noise_vs_Vov_average[sipm].SetLineWidth(2)
    g_Noise_vs_Vov_average[sipm].SetLineColor(ROOT.kBlue)
    g_Noise_vs_Vov_average[sipm].SetFillColor(ROOT.kBlue)
    g_Noise_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kBlue,0.5)
    g_Noise_vs_Vov_average[sipm].SetFillStyle(3004)
    g_Noise_vs_Vov_average[sipm].Draw('E3lsame')
    g_Stoch_vs_Vov_average[sipm].SetLineWidth(2)
    g_Stoch_vs_Vov_average[sipm].SetLineColor(ROOT.kGreen+2)
    g_Stoch_vs_Vov_average[sipm].SetFillColor(ROOT.kGreen+2)
    g_Stoch_vs_Vov_average[sipm].SetFillStyle(3001)
    g_Stoch_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kGreen+2,0.5)
    g_Stoch_vs_Vov_average[sipm].Draw('E3lsame')
    g_sDCR_vs_Vov_average[sipm].SetLineWidth(2)
    g_sDCR_vs_Vov_average[sipm].SetLineColor(ROOT.kOrange+2)
    g_sDCR_vs_Vov_average[sipm].SetFillColor(ROOT.kOrange+2)
    g_sDCR_vs_Vov_average[sipm].SetFillStyle(3001)
    g_sDCR_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kOrange+2,0.5)
    g_sDCR_vs_Vov_average[sipm].Draw('E3lsame')
    g_TotExp_vs_Vov_average[sipm].SetLineWidth(2)
    g_TotExp_vs_Vov_average[sipm].SetLineColor(ROOT.kRed+1)
    g_TotExp_vs_Vov_average[sipm].SetFillColor(ROOT.kRed+1)
    g_TotExp_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kRed+1,0.5)
    g_TotExp_vs_Vov_average[sipm].SetFillStyle(3001)
    # g_TotExp_vs_Vov_average[sipm].Draw('E3lsame')
    leg[sipm].Draw()

    latex.Draw()
    outfile.cd()
    g_data_vs_Vov_average[sipm].Write('g_data_vs_Vov_average_%s'%sipm)
    g_Noise_vs_Vov_average[sipm].Write('g_Noise_vs_Vov_average_%s'%sipm)
    g_Stoch_vs_Vov_average[sipm].Write('g_Stoch_vs_Vov_average_%s'%sipm)
    g_sDCR_vs_Vov_average[sipm].Write('g_DCR_vs_Vov_average_%s'%sipm)
    g_TotExp_vs_Vov_average[sipm].Write('g_Tot_vs_Vov_average_%s'%sipm)
    g_DCR_vs_Vov_average[sipm].Write('g_DCRate_vs_Vov_average_%s'%sipm)
    

    cms_logo = draw_logo()
    cms_logo.Draw()
    c.SaveAs(outdir+'/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
    hdummy.Delete()
# --------------------------------------------------------------------------------------------------------------







# ----------- things vs things per ov --------------------------------------------------------
# -----  SR and best threshold vs bar per ov
for ov in VovsUnion:
    c = ROOT.TCanvas('c_slewRate_vs_bar_%s_Vov%.2f'%(sipm,ov),'c_slewRate_vs_bar_%s_Vov%.2f'%(sipm,ov),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,35)
    hdummy.GetXaxis().SetTitle('bar')
    hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_SR_vs_bar[sipm].keys():
            continue
        g_SR_vs_bar[sipm][ov].SetMarkerStyle(markers[sipm])
        g_SR_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])

        g_SR_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_SR_vs_bar[sipm][ov].Draw('psame')
    leg2.Draw()
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/slewRate_vs_bar_perVov/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/slewRate_vs_bar_perVov/'+c.GetName()+'.pdf')
    hdummy.Delete()


    c = ROOT.TCanvas('c_bestTh_vs_bar_%s_Vov%.2f'%(sipm,ov),'c_bestTh_vs_bar_%s_Vov%.2f'%(sipm,ov),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,20)
    hdummy.GetXaxis().SetTitle('bar')
    hdummy.GetYaxis().SetTitle('timing threshold [DAC]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_bestTh_vs_bar[sipm].keys():
            continue
        g_bestTh_vs_bar[sipm][ov].SetMarkerStyle(markers[sipm])
        g_bestTh_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
        g_bestTh_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_bestTh_vs_bar[sipm][ov].Draw('plsame')
    leg2.Draw()        
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/bestTh/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/bestTh/'+c.GetName()+'.pdf')
    hdummy.Delete()

    c = ROOT.TCanvas('c_noise_vs_bar_%s_Vov%.2f'%(sipm,ov),'c_noise_vs_bar_%s_Vov%.2f'%(sipm,ov),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,80)
    hdummy.GetXaxis().SetTitle('bar')
    hdummy.GetYaxis().SetTitle('#sigma_{t, noise} [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_Noise_vs_bar[sipm].keys():
            continue
        g_Noise_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
        g_Noise_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
        g_Noise_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_Noise_vs_bar[sipm][ov].Draw('psame')
    leg2.Draw()
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.pdf')
    hdummy.Delete()

    c = ROOT.TCanvas('c_stoch_vs_bar_%s_Vov%.2f'%(sipm,ov),'c_stoch_vs_bar_%s_Vov%.2f'%(sipm,ov),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,80)
    hdummy.GetXaxis().SetTitle('bar')
    hdummy.GetYaxis().SetTitle('#sigma_{t, stoch} [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_Stoch_vs_bar[sipm].keys():
            continue
        g_Stoch_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
        g_Stoch_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
        g_Stoch_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_Stoch_vs_bar[sipm][ov].Draw('psame')
    leg2.Draw()
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.pdf')
    hdummy.Delete()

    c = ROOT.TCanvas('c_DCR_vs_bar_%s_Vov%.2f'%(sipm,ov),'c_DCR_vs_bar_%s_Vov%.2f'%(sipm,ov),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,120)
    hdummy.GetXaxis().SetTitle('bar')
    hdummy.GetYaxis().SetTitle('#sigma_{t, DCR} [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_sDCR_vs_bar[sipm].keys():
            continue
        g_sDCR_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
        g_sDCR_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
        g_sDCR_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_sDCR_vs_bar[sipm][ov].Draw('psame')
    leg2.Draw()
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.pdf')
    hdummy.Delete()

#------- vs SR per ov -------
for ov in VovsUnion:
    c = ROOT.TCanvas('c_stoch_vs_SR_%s_Vov%.2f'%(sipm,ov),'c_stoch_vs_SR_%s_Vov%.2f'%(sipm,ov),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,0,35.5,100,0,60)
    hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.GetYaxis().SetTitle('#sigma_{stoch} [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_Stoch_vs_SR[sipm].keys():
            continue
        g_Stoch_vs_SR[sipm][ov].SetMarkerStyle(markers[sipm])
        g_Stoch_vs_SR[sipm][ov].SetMarkerColor(cols[sipm])
        g_Stoch_vs_SR[sipm][ov].SetLineColor(cols[sipm])
        g_Stoch_vs_SR[sipm][ov].Draw('psame')
    leg2.Draw()
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.pdf')
    hdummy.Delete()


    c = ROOT.TCanvas('c_noise_vs_SR_%s_Vov%.2f'%(sipm,ov),'c_noise_vs_SR_%s_Vov%.2f'%(sipm,ov),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,0,35,100,0,60)
    hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.GetYaxis().SetTitle('#sigma_{noise} [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_Noise_vs_SR[sipm].keys():
            continue
        g_Noise_vs_SR[sipm][ov].SetMarkerStyle(markers[sipm])
        g_Noise_vs_SR[sipm][ov].SetMarkerColor(cols[sipm])
        g_Noise_vs_SR[sipm][ov].SetLineColor(cols[sipm])
        g_Noise_vs_SR[sipm][ov].Draw('plsame')
    leg2.Draw()        
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.pdf')
    hdummy.Delete()


    c = ROOT.TCanvas('c_DCR_vs_SR_%s_Vov%.2f'%(sipm,ov),'c_DCR_vs_SR_%s_Vov%.2f'%(sipm,ov),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,0,35,100,0,60)
    hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.GetYaxis().SetTitle('#sigma_{DCR}  [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_sDCR_vs_SR[sipm].keys():
            continue
        g_sDCR_vs_SR[sipm][ov].SetMarkerStyle( markers[sipm] )
        g_sDCR_vs_SR[sipm][ov].SetMarkerColor(cols[sipm])
        g_sDCR_vs_SR[sipm][ov].SetLineColor(cols[sipm])
        g_sDCR_vs_SR[sipm][ov].Draw('psame')
    leg2.Draw()
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.pdf')
    hdummy.Delete()


    c = ROOT.TCanvas('c_data_vs_SR_%s_Vov%.2f'%(sipm,ov),'c_data_vs_SR_%s_Vov%.2f'%(sipm,ov),600,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,120)
    hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_data_vs_SR[sipm].keys():
            continue
        g_data_vs_SR[sipm][ov].SetMarkerStyle( markers[sipm] )
        g_data_vs_SR[sipm][ov].SetMarkerColor(cols[sipm])
        g_data_vs_SR[sipm][ov].SetLineColor(cols[sipm])
        g_data_vs_SR[sipm][ov].Draw('psame')
    leg2.Draw()
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_slewRate/'+c.GetName()+'.pdf')
    hdummy.Delete()
# --------------------------------------------------------------------------------------------------------------











# ---------------------------
# ------ check model --------
# ---------------------------

# -- average slew rate vs Gain x PDE 
c =  ROOT.TCanvas('c_SR_vs_GainPDE_average_%s'%sipm, 'c_SR_vs_GainPDE_average_%s'%sipm, 600, 500)
c.SetGridx()
c.SetGridy()
c.cd()
hdummy = ROOT.TH2F('hdummy','',2, 10000, 200000, 2, 0., 35.)
hdummy.GetXaxis().SetTitle('Gain x PDE')
hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
hdummy.GetXaxis().SetNdivisions(505)
hdummy.Draw()
for sipm in sipmTypes:
    g_SR_vs_GainPDE_average[sipm].SetMarkerStyle(markers[sipm])
    g_SR_vs_GainPDE_average[sipm].SetMarkerColor(cols[sipm])
    g_SR_vs_GainPDE_average[sipm].SetLineWidth(1)
    g_SR_vs_GainPDE_average[sipm].SetLineColor(cols[sipm])
    g_SR_vs_GainPDE_average[sipm].Draw('plsame')
leg2.Draw()

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()


# -- average expected stochasti vs Npe
c =  ROOT.TCanvas('c_stoch_vs_Npe_average_%s'%sipm, 'c_stoch_vs_Npe_average_%s'%sipm, 600, 500)
c.SetGridx()
c.SetGridy()
c.cd()
hdummy = ROOT.TH2F('hdummy','',2, 2e3, 8e3,2, 20, 80)
hdummy.GetXaxis().SetTitle('Npe')
hdummy.GetYaxis().SetTitle('#sigma_{t, stoch} [ps]')
hdummy.GetXaxis().SetNdivisions(505)
hdummy.Draw()
for sipm in sipmTypes:
    g_Stoch_vs_Npe_average[sipm].SetMarkerStyle(markers[sipm])
    g_Stoch_vs_Npe_average[sipm].SetMarkerColor(cols[sipm])
    g_Stoch_vs_Npe_average[sipm].SetLineWidth(1)
    g_Stoch_vs_Npe_average[sipm].SetLineColor(cols[sipm])
    g_Stoch_vs_Npe_average[sipm].Draw('plsame')
leg2.Draw()

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()



# -- average DCR vs Vov
c =  ROOT.TCanvas('c_DCR_vs_Vov_average_%s'%sipm, 'c_DCR_vs_Vov_average_%s'%sipm, 600, 500)
c.SetGridx()
c.SetGridy()
c.cd()
hdummy = ROOT.TH2F('hdummy','',2, 0, 2,2, 0, 50)
hdummy.GetXaxis().SetTitle('V_{ov} [V]')
hdummy.GetYaxis().SetTitle('DCR [GHz]')
hdummy.GetXaxis().SetNdivisions(505)
hdummy.Draw()
for sipm in sipmTypes:
    g_DCR_vs_Vov_average[sipm].SetMarkerStyle(markers[sipm])
    g_DCR_vs_Vov_average[sipm].SetMarkerColor(cols[sipm])
    g_DCR_vs_Vov_average[sipm].SetLineWidth(1)
    g_DCR_vs_Vov_average[sipm].SetLineColor(cols[sipm])
    g_DCR_vs_Vov_average[sipm].Draw('plsame')
leg2.Draw()

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()



# -- average noise vs gain
c =  ROOT.TCanvas('c_Noise_vs_Gain_average_%s'%sipm, 'c_Noise_vs_Gain_average_%s'%sipm, 600, 500)
c.SetGridx()
c.SetGridy()
c.cd()
hdummy = ROOT.TH2F('hdummy','',2, 0, 2,2, 0, 50)
hdummy.GetXaxis().SetTitle('V_{ov} [V]')
hdummy.GetYaxis().SetTitle('DCR [GHz]')
hdummy.GetXaxis().SetNdivisions(505)
hdummy.Draw()
for sipm in sipmTypes:
    g_Noise_vs_Gain_average[sipm].SetMarkerStyle(markers[sipm])
    g_Noise_vs_Gain_average[sipm].SetMarkerColor(cols[sipm])
    g_Noise_vs_Gain_average[sipm].SetLineWidth(1)
    g_Noise_vs_Gain_average[sipm].SetLineColor(cols[sipm])
    g_Noise_vs_Gain_average[sipm].Draw('plsame')
    g_Noise_vs_Gain_average[sipm].Write('g_Noise_vs_Gain_average_%s'%sipm)
leg2.Draw()

cms_logo = draw_logo()
cms_logo.Draw()

c.SaveAs(outdir+'/'+c.GetName()+'.png')
c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
hdummy.Delete()




# --------------------------------------------------------------------------------------------------------------


    
outfile.Close()
