from utils import *

parser = argparse.ArgumentParser()  
parser.add_argument("-n","--comparisonNumber", required = True, type=str, help="comparison number")    
args = parser.parse_args()   


#---- init ---
compareNum = int(args.comparisonNumber)
#-------------


plotsdir = '/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/'

# settings
marker_code = True
color_code = True
compareToModel = False
verbose = False
tofhirVersion = '2c'

fnal_dir = '/eos/home-s/spalluot/MTD/TB_FNAL_Mar23/Lab5015Analysis/plots'
may_dir = '/eos/home-s/spalluot/MTD/TB_CERN_May23/Lab5015Analysis/plots'

specific_position = False
add_string = False


# ------ different comparisons ------
# types
if compareNum == 1:
    sipmTypes = ['HPK_nonIrr_LYSO818','HPK_nonIrr_LYSO813','HPK_nonIrr_LYSO816']
    nameComparison = 'HPK_nonIrr_angle64_T5C_types'
    extraLabel = ['','','']
    extraName = ['_angle64_T5C', '_angle64_T5C', '_angle64_T5C']

# angles
elif compareNum == 2:
    sipmTypes = ['HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO818', 'HPK_nonIrr_LYSO818']
    nameComparison = 'HPK_nonIrr_LYSO818_T5C_angles'
    extraLabel = [' 32^{o}',' 52^{o}', ' 64^{o}']
    extraName = ['_angle32_T5C', '_angle52_T5C','_angle64_T5C',]

# sipm cell sizes
elif compareNum == 3:
    sipmTypes = ['HPK_nonIrr_LYSO820', 'HPK_nonIrr_LYSO813', 'HPK_nonIrr_LYSO814', 'HPK_nonIrr_LYSO528']
    nameComparison = 'HPK_nonIrr_angle52_cellSizes_withFNAL'
    extraLabel = ['', '', '  FNAL', '']
    specific_position = True
    plots_special = ['%s'%plotsdir, '%s'%plotsdir, '%s'%fnal_dir, '%s'%plotsdir]    
    extraName = ['_angle52_T5C', '_angle52_T5C',  '_angle52_T12C', '_angle52_T5C']
#--------------------------------------------------------------------------------------


# ---- color settings ----
if color_code:
    #color_map = [632, 600, 416]
    color_map = [806,896,613,886,597,866,429,846,816,413,629,397,590,611,795,1,2,3,4,5,6,7,8,9,10,11]
if marker_code:
    marker_map = [20,20,20,20,20,20,20,20]
# ------------------------



# --- summary plots names and pulse shape names ----
# - sipm_base is necessary for retrieving the pulse shape name which does contain also the Vov (loop basis)
sipm_base = {}
fnames   = {}
for it, sipm in enumerate(sipmTypes):
    sipmTypes[it] = sipm + extraName[it]
    sipm_base[it] = sipm
    if specific_position:
        if add_string and add_str[it] != '':
            sipmTypes[it] = sipm + extraName[it] + add_str[it]
        fnames[sipmTypes[it]] = '%s/summaryPlots_%s.root'%(plots_special[it], sipmTypes[it])
    else:
        fnames[sipmTypes[it]] = '%s/summaryPlots_%s.root'%(plotsdir, sipmTypes[it])

if verbose:
    print('sipmTypes: ', sipmTypes , '\t outfile: ', outFileName)
#---------






#--------------------------------------------------------------------------------------
# ----- output --------
# - root file
outFileName = plotsdir+'/plot_tRes_'+nameComparison+'.root'
outfile = ROOT.TFile(outFileName, 'RECREATE')

# - plots on web
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/plot_tRes/%s/'%nameComparison
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
# --------------------------------------------------------------------------------------






# -------- retrieve module infos --------
labels   = {}
cols     = {}
markers  = {}
LO       = {}
tau      = {}
tauRise  = {}
NpeFrac  = {}
thick    = {}

for it, sipm in enumerate(sipmTypes):
    labels[sipm]   = label_(sipm) + extraLabel[it]
    cols[sipm]     = color_map[it]
    markers[sipm]  = marker_map[it]
    LO[sipm]       = light_output(sipm)
    tau[sipm]      = tau_decay(sipm)
    tauRise[sipm]  = tau_rise(sipm)
    NpeFrac[sipm]  = Npe_frac(sipm)
    thick[sipm]    = thickness(sipm)



if compareToModel:
    g_SR_vs_Vov_model = {}
    for it,name in enumerate(SRmodelGraphs):
        SRmodelfile = ROOT.TFile.Open(SRmodelfileName)
        g_SR_vs_Vov_model[sipmTypes[it]] = SRmodelfile.Get(name)



if verbose:
    print('defining graphs')
np         = 3
errSRsyst  = 0.10 # error on the slew rate
errPDE     = 0.05 # assumed uncertainty on PDE (5-10%)


g_data = {}
g_data_average = {}


# ------ vs Vov -----
g_Noise_vs_Vov     = {}
g_Stoch_vs_Vov     = {}
g_StochExp_vs_Vov    = {}
g_TotExp_vs_Vov    = {}


g_bestTh_vs_Vov    = {}
g_SR_vs_Vov        = {}
g_Npe_vs_Vov       = {}


# ------ vs Npe / Gain -----
g_Stoch_vs_Npe     = {}
g_data_vs_Npe      = {}

g_SR_vs_GainNpe    = {}
g_data_vs_GainNpe  = {}

# ------ vs bar -----
g_bestTh_vs_bar    = {}
g_SR_vs_bar        = {}
g_Noise_vs_bar     = {}
g_Stoch_vs_bar     = {}
g_StochExp_vs_bar     = {}
g_TotExp_vs_bar       = {}

# --- vs SR
g_data_vs_SR        = {}
g_Stoch_vs_SR      = {}
g_Noise_vs_SR      = {}




if verbose:
    print('retrieving bars and ovs')

# --- retrieve bars and ovs from summary plots
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
print('\novs union: ', VovsUnion, '\t bars union: ', barsUnion)

# ------   




f      = {}
fPS    = {}
Npe    = {}
gain   = {}

##################
for it,sipm in enumerate(sipmTypes):
    f[sipm] = ROOT.TFile.Open(fnames[sipm])
    if not f[sipm]:
        print('summary plot file not found')
        sys.exit()

    g_data_average[sipm] = f[sipm].Get('g_deltaT_totRatioCorr_bestTh_vs_vov_enBin01_average')
    Npe[sipm]                = {}
    gain[sipm]               = {}

    g_data[sipm]             = {}

    g_Npe_vs_Vov[sipm]       = ROOT.TGraphErrors()
    g_Noise_vs_Vov[sipm]     = {}
    g_Stoch_vs_Vov[sipm]     = {}
    g_StochExp_vs_Vov[sipm]     = {}
    g_TotExp_vs_Vov[sipm]     = {}

    g_SR_vs_Vov[sipm]        = {}
    g_bestTh_vs_Vov[sipm]    = {}

    g_Stoch_vs_Npe[sipm]     = {}
    g_data_vs_Npe[sipm]      = ROOT.TGraphErrors()
    g_SR_vs_GainNpe[sipm]    = {}
    g_data_vs_GainNpe[sipm]  = ROOT.TGraphErrors()

    g_SR_vs_bar[sipm]        = {}
    g_bestTh_vs_bar[sipm]    = {}
    g_Noise_vs_bar[sipm]     = {}
    g_Stoch_vs_bar[sipm]     = {}
    g_StochExp_vs_bar[sipm]     = {}
    g_TotExp_vs_bar[sipm]       = {}

    g_Stoch_vs_SR[sipm] = {}
    g_Noise_vs_SR[sipm] = {}
    g_data_vs_SR[sipm] = {}

    g_data_vs_Npe[sipm] = ROOT.TGraphErrors()
    g_data_vs_GainNpe[sipm] = ROOT.TGraphErrors()


    if verbose:
        print('retrieving pulse shapes')

    fPS[sipm] = {}
    for ov in Vovs[sipm]:
        if specific_position:
            fPS[sipm][ov] = ROOT.TFile.Open('%s/pulseShape_%s_Vov%.2f%s.root'%(plots_special[it],sipm_base[it],ov,extraName[it]))
        else:
            fPS[sipm][ov] = ROOT.TFile.Open('%s/pulseShape_%s_Vov%.2f%s.root'%(plotsdir,sipm_base[it],ov,extraName[it]))
        if not fPS[sipm][ov]:
            print('pulse shape file not found')
            sys.exit()
            
        g_SR_vs_bar[sipm][ov]        = ROOT.TGraphErrors()
        g_bestTh_vs_bar[sipm][ov]    = ROOT.TGraphErrors()
        g_Noise_vs_bar[sipm][ov]     = ROOT.TGraphErrors()
        g_Stoch_vs_bar[sipm][ov]     = ROOT.TGraphErrors()
        g_StochExp_vs_bar[sipm][ov]  = ROOT.TGraphErrors()
        g_TotExp_vs_bar[sipm][ov]    = ROOT.TGraphErrors()
        g_Stoch_vs_SR[sipm][ov]      = ROOT.TGraphErrors()
        g_Noise_vs_SR[sipm][ov]      = ROOT.TGraphErrors()
        g_data_vs_SR[sipm][ov]       = ROOT.TGraphErrors()

    if verbose:
        print('retrieving summary plots')

    for bar in bars[sipm]:
        g_data[sipm][bar] = f[sipm].Get('g_deltaT_totRatioCorr_bestTh_vs_vov_bar%02d_enBin01'%bar)

        if verbose:
            print('\n check sipm ', sipm , '  bar ', bar)
            for ipoint in range(g_data[sipm][bar].GetN()):
                print('tres ', g_data[sipm][bar].GetPointY(ipoint), '  ov: ', g_data[sipm][bar].GetPointX(ipoint))
            if g_data[sipm][bar].GetN == 0:
                print('no point found in summary plot')

        g_Noise_vs_Vov[sipm][bar]     = ROOT.TGraphErrors()
        g_Stoch_vs_Vov[sipm][bar]     = ROOT.TGraphErrors()
        g_StochExp_vs_Vov[sipm][bar]  = ROOT.TGraphErrors()
        g_TotExp_vs_Vov[sipm][bar]    = ROOT.TGraphErrors()

        g_Stoch_vs_Npe[sipm][bar]     = ROOT.TGraphErrors()
        g_SR_vs_GainNpe[sipm][bar]    = ROOT.TGraphErrors()

        g_SR_vs_Vov[sipm][bar]        = ROOT.TGraphErrors()
        g_bestTh_vs_Vov[sipm][bar]    = ROOT.TGraphErrors()

        s_stoch_ref = 0
        err_s_stoch_ref = 0


        #ov_ref = ov_reference(sipm) # ----> could be hard-coded here --> for non irradiated is 3.5V
        ov_ref = 3.5
        if 'HPK_nonIrr_LYSO818_angle64' in sipm:
            ov_ref = 1.0        
        if ov_ref in Vovs[sipm]:
            if verbose:
                print("computing ref stoch ")

                
            #-------------
            # here I only want to consider the values for ov = 3.5  --> to extract the ref stochastic
            s_data = g_data[sipm][bar].Eval(ov_ref)
            indref = [i for i in range(0, g_data[sipm][bar].GetN()) if g_data[sipm][bar].GetPointX(i) == ov_ref]
            if ( len(indref)<1): 
                if verbose: print('no ov ref found')
                continue
            err_s_data = g_data[sipm][bar].GetErrorY(indref[0])
            g_psL = fPS[sipm][ov_ref].Get('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov_ref))
            g_psR = fPS[sipm][ov_ref].Get('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov_ref))
            if (g_psL==None): 
                if verbose: print("no ps left")
                continue
            if (g_psR==None): 
                if verbose:print("no ps right")
                continue
            g_psL.SetName('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov_ref))
            g_psR.SetName('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov_ref))
            timingThreshold = findTimingThreshold(f[sipm].Get('g_deltaT_totRatioCorr_vs_th_bar%02d_Vov%.2f_enBin01'%(bar,ov_ref)))
            gtempL = ROOT.TGraphErrors()
            gtempR = ROOT.TGraphErrors()
            srL,err_srL = getSlewRateFromPulseShape(g_psL, timingThreshold, np, gtempL, ov, sipm)
            srR,err_srR = getSlewRateFromPulseShape(g_psR, timingThreshold, np, gtempR, ov, sipm)
            
            if verbose:
                print("slew rate: \t left: ", srL, '\t right: ', srR)

            # check the extracted slew rates at left and right and combine them
            if (srL>0 and srR>0):
                # weighted average
                if (err_srL*err_srL)==0 or (err_srR*err_srR)==0 or (1./(err_srL*err_srL) + 1./(err_srR*err_srR) ) == 0: # ---> check denominator
                    continue
                sr =  ( (srL/(err_srL*err_srL) + srR/(err_srR*err_srR) ) / (1./(err_srL*err_srL) + 1./(err_srR*err_srR) ) )
                errSR = 1./math.sqrt( 1./(err_srL*err_srL)  +  1./(err_srR*err_srR) )
                errSR = errSR/sr
            elif (srL>0 and srR<0):
                sr = srL
                errSR = err_srL/sr
            elif (srL<0 and srR>0):
                sr = srR
                errSR = err_srR/sr
            else:
                print('negative SR : bar%02d:  time :%.1f'%(bar, s_data) )
                continue

            # adding a systematic 
            errSR = math.sqrt(errSR*errSR+errSRsyst*errSRsyst) 
            s_noise = sigma_noise(sr, tofhirVersion)
            # compute stoch ref
            if (s_data>=s_noise):
                s_stoch_ref = math.sqrt(s_data*s_data - s_noise*s_noise)
                err_s_noise = 0.5*(sigma_noise(sr*(1-errSR), tofhirVersion)-sigma_noise(sr*(1+errSR), tofhirVersion))
                err_s_stoch_ref = 1./s_stoch_ref*math.sqrt( pow(err_s_data*s_data,2)+pow( s_noise*err_s_noise ,2) )
            else:
                print('data < noise : skipping bar%02d:  %.1f <  %.1f'%(bar, s_data, s_noise) )
                continue
        else:
            print('!!!!!    -------  >  ov ref was not measured')
            s_stoch_ref = 0
            err_s_stoch_ref = 0

        # loop over ovs 
        for ov in Vovs[sipm]:
            if verbose:
                print("\nov: ", ov)
            s_meas = g_data[sipm][bar].Eval(ov)
            indref = [i for i in range(0, g_data[sipm][bar].GetN()) if g_data[sipm][bar].GetPointX(i) == ov]
            if ( len(indref)<1 ): continue
            err_s_meas = g_data[sipm][bar].GetErrorY(indref[0])
            Npe[sipm][ov]  = 4.2*LO[sipm]*NpeFrac[sipm]*PDE_(ov,sipm)/PDE_(3.5,sipm,'0')
            gain[sipm][ov] = Gain_(ov,sipm)
            g_psL = fPS[sipm][ov].Get('g_pulseShapeL_bar%02d_Vov%.2f'%(bar,ov))
            g_psR = fPS[sipm][ov].Get('g_pulseShapeR_bar%02d_Vov%.2f'%(bar,ov))
            if (g_psL==None): continue
            if (g_psR==None): continue
            g_psL.SetName('g_pulseShapeL_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            g_psR.SetName('g_pulseShapeR_bar%02d_Vov%.2f_%s'%(bar,ov,sipm))
            timingThreshold = findTimingThreshold(f[sipm].Get('g_deltaT_totRatioCorr_vs_th_bar%02d_Vov%.2f_enBin01'%(bar,ov)))
            srL = -1
            srR = -1
            sr = -1
            err_srL = -1
            err_srR = -1

            # draw pulse shape
            c = ROOT.TCanvas('c_%s_%s'%(g_psL.GetName().replace('g_pulseShapeL','pulseShape'),sipm),'',600,500)  
            hdummy = ROOT.TH2F('hdummy','', 100, min(g_psL.GetX())-1., 5., 100, 0., 15.)
            hdummy.GetXaxis().SetTitle('time [ns]')
            hdummy.GetYaxis().SetTitle('amplitude [#muA]')
            hdummy.Draw()
            gtempL = ROOT.TGraphErrors()
            gtempR = ROOT.TGraphErrors()
            srL,err_srL = getSlewRateFromPulseShape(g_psL, timingThreshold, np, gtempL, ov, sipm, c)
            srR,err_srR = getSlewRateFromPulseShape(g_psR, timingThreshold, np, gtempR, ov, sipm, c) 
            line = ROOT.TLine(min(g_psL.GetX())-1., timingThreshold*0.313, 30., timingThreshold*0.313)
            line.SetLineStyle(7)
            line.SetLineWidth(2)
            line.SetLineColor(ROOT.kOrange+1)        
            line.Draw('same')

            # labels
            lat_s = latex_sipm(sipm)
            lat_s.Draw()
            lat = latex_vov(ov)
            lat.Draw()
            lat_b = latex_bar(bar)
            lat_b.Draw()
            c.SaveAs(outdir+'/pulseShape/'+c.GetName()+'.png')   
            hdummy.Delete()


            # compute slew rate for each ov 
            if (srL>0 and srR>0):
                # weighted average
                if (err_srL*err_srL)==0 or (err_srR*err_srR)==0 or (1./(err_srL*err_srL) + 1./(err_srR*err_srR) ) == 0: # ---> check denominator
                    continue
                sr =  ( (srL/(err_srL*err_srL) + srR/(err_srR*err_srR) ) / (1./(err_srL*err_srL) + 1./(err_srR*err_srR) ) )
                errSR = 1./math.sqrt( 1./(err_srL*err_srL)  +  1./(err_srR*err_srR) )
            if (srL>0 and srR<0):
                sr = srL
                errSR = err_srL
            if (srL<0 and srR>0):
                sr = srR
                errSR = err_srR
            if (srL<0 and srR<0): continue

            errSR = math.sqrt(errSR*errSR+errSRsyst*errSRsyst*sr*sr) 

            s_noise = sigma_noise(sr, tofhirVersion)
            err_s_noise =  0.5*(sigma_noise(sr*(1-errSR/sr), tofhirVersion)-sigma_noise(sr*(1+errSR/sr), tofhirVersion))

            g_SR_vs_GainNpe[sipm][bar].SetPoint( g_SR_vs_GainNpe[sipm][bar].GetN(), gain[sipm][ov]*Npe[sipm][ov], sr )
            g_SR_vs_GainNpe[sipm][bar].SetPointError( g_SR_vs_GainNpe[sipm][bar].GetN()-1, 0, errSR )

            # fill graph vs vov
            g_Npe_vs_Vov[sipm].SetPoint(g_Npe_vs_Vov[sipm].GetN(), ov, Npe[sipm][ov])
            g_SR_vs_Vov[sipm][bar].SetPoint( g_SR_vs_Vov[sipm][bar].GetN(), ov, sr )
            g_SR_vs_Vov[sipm][bar].SetPointError( g_SR_vs_Vov[sipm][bar].GetN()-1, 0, errSR )
            g_bestTh_vs_Vov[sipm][bar].SetPoint( g_bestTh_vs_Vov[sipm][bar].GetN(), ov, timingThreshold )
            g_bestTh_vs_Vov[sipm][bar].SetPointError( g_bestTh_vs_Vov[sipm][bar].GetN()-1, 0, 0 )
            g_Noise_vs_Vov[sipm][bar].SetPoint(g_Noise_vs_Vov[sipm][bar].GetN(), ov, s_noise)
            g_Noise_vs_Vov[sipm][bar].SetPointError(g_Noise_vs_Vov[sipm][bar].GetN()-1, 0, err_s_noise)
            
            # vs bar
            if bar in goodbars[sipm][ov]:
                if ('818' in sipm) and (3.5==ov):
                    print("SLEW RATE ____  ov ", ov , " bar ", bar, "      sr   ", sr)
                    if sr < 40:
                        continue
                g_SR_vs_bar[sipm][ov].SetPoint( g_SR_vs_bar[sipm][ov].GetN(), bar, sr )
                g_SR_vs_bar[sipm][ov].SetPointError( g_SR_vs_bar[sipm][ov].GetN()-1, 0, errSR )
                g_bestTh_vs_bar[sipm][ov].SetPoint( g_bestTh_vs_bar[sipm][ov].GetN(), bar, timingThreshold )
                g_bestTh_vs_bar[sipm][ov].SetPointError( g_bestTh_vs_bar[sipm][ov].GetN()-1, 0, 0)
                g_Noise_vs_bar[sipm][ov].SetPoint( g_Noise_vs_bar[sipm][ov].GetN(), bar, s_noise )
                g_Noise_vs_bar[sipm][ov].SetPointError( g_Noise_vs_bar[sipm][ov].GetN()-1, 0,  err_s_noise)
            
            # vs SR
            g_data_vs_SR[sipm][ov].SetPoint(g_data_vs_SR[sipm][ov].GetN(), sr, s_data)
            g_data_vs_SR[sipm][ov].SetPointError(g_data_vs_SR[sipm][ov].GetN()-1, errSR, err_s_data)
            g_Noise_vs_SR[sipm][ov].SetPoint(g_Noise_vs_SR[sipm][ov].GetN(), sr, s_noise)
            g_Noise_vs_SR[sipm][ov].SetPointError(g_Noise_vs_SR[sipm][ov].GetN()-1, errSR, err_s_noise)


            # compute s_stoch as diff in quadrature between measured tRes and noise term
            if ( s_meas > s_noise):
                s_stoch = math.sqrt(s_meas*s_meas-s_noise*s_noise)     # -----> real stoch measured, not the ref one
                err_s_stoch = 1./s_stoch * math.sqrt( pow(s_meas*err_s_meas, 2) + pow(s_noise*err_s_noise ,2) )

                # fill all the stochastic vs stuff graphs
                g_Stoch_vs_Npe[sipm][bar].SetPoint(g_Stoch_vs_Npe[sipm][bar].GetN(), Npe[sipm][ov], s_stoch)
                g_Stoch_vs_Npe[sipm][bar].SetPointError(g_Stoch_vs_Npe[sipm][bar].GetN()-1, 0, err_s_stoch)
                g_Stoch_vs_Vov[sipm][bar].SetPoint(g_Stoch_vs_Vov[sipm][bar].GetN(), ov, s_stoch)
                g_Stoch_vs_Vov[sipm][bar].SetPointError(g_Stoch_vs_Vov[sipm][bar].GetN()-1, 0, err_s_stoch)

                if bar in goodbars[sipm][ov]:
                    g_Stoch_vs_bar[sipm][ov].SetPoint( g_Stoch_vs_bar[sipm][ov].GetN(), bar, s_stoch )
                    g_Stoch_vs_bar[sipm][ov].SetPointError( g_Stoch_vs_bar[sipm][ov].GetN()-1, 0,  err_s_stoch)

                g_Stoch_vs_SR[sipm][ov].SetPoint(g_Stoch_vs_SR[sipm][ov].GetN(), sr, s_stoch)
                g_Stoch_vs_SR[sipm][ov].SetPointError(g_Stoch_vs_SR[sipm][ov].GetN()-1, errSR, err_s_stoch)
            

            if verbose:
                print('\n\n   s_meas ', s_meas, '    s_noise: ', s_noise, '    s_stoch: ', s_stoch)


            # compute expected stochastic term  by scaling from 3.5 V OV    
            s_stoch_exp = s_stoch_ref / math.sqrt( PDE_(ov,sipm)/PDE_(ov_ref,sipm)  )
            err_s_stoch_exp = err_s_stoch_ref/math.sqrt( PDE_(ov, sipm)/PDE_(ov_ref, sipm) )

            g_StochExp_vs_Vov[sipm][bar].SetPoint(g_StochExp_vs_Vov[sipm][bar].GetN(), ov, s_stoch_exp)
            g_StochExp_vs_Vov[sipm][bar].SetPointError(g_StochExp_vs_Vov[sipm][bar].GetN()-1, 0, err_s_stoch_exp)

            if bar in goodbars[sipm][ov]:
                g_StochExp_vs_bar[sipm][ov].SetPoint(g_StochExp_vs_bar[sipm][ov].GetN(), bar, s_stoch_exp)
                g_StochExp_vs_bar[sipm][ov].SetPointError(g_StochExp_vs_bar[sipm][ov].GetN()-1, 0, err_s_stoch_exp)

            # tot resolution summing noise + stochastic (scaled) in quadrature -------> expected total resolution from pde scaling + noise
            s_tot_exp = math.sqrt( s_stoch_exp*s_stoch_exp + s_noise*s_noise )
            err_s_tot_exp = 1./s_tot_exp * math.sqrt( pow( err_s_stoch_exp*s_stoch_exp,2) + pow(s_noise*g_Noise_vs_Vov[sipm][bar].GetErrorY(g_Noise_vs_Vov[sipm][bar].GetN()-1),2))

            g_TotExp_vs_Vov[sipm][bar].SetPoint(g_TotExp_vs_Vov[sipm][bar].GetN(), ov, s_tot_exp)
            g_TotExp_vs_Vov[sipm][bar].SetPointError(g_TotExp_vs_Vov[sipm][bar].GetN()-1, 0, err_s_tot_exp)

            g_TotExp_vs_bar[sipm][ov].SetPoint(g_TotExp_vs_bar[sipm][ov].GetN(), bar, s_tot_exp)
            g_TotExp_vs_bar[sipm][ov].SetPointError(g_TotExp_vs_bar[sipm][ov].GetN()-1, 0, err_s_tot_exp)

            # -----------------------------------------------------------------------------




if verbose:
    print('computing average graphs')


#  ----------------------------------------
#  -------------- average -----------------

rms_thresh = 1

g_SR_vs_Vov_average = {}
g_Noise_vs_Vov_average = {}
g_Stoch_vs_Vov_average = {}
g_StochExp_vs_Vov_average = {}
g_TotExp_vs_Vov_average = {}


for sipm in sipmTypes:
    print("\n ", sipm)
    g_SR_vs_Vov_average[sipm]     = ROOT.TGraphErrors()
    g_Noise_vs_Vov_average[sipm]  = ROOT.TGraphErrors()
    g_Stoch_vs_Vov_average[sipm]  = ROOT.TGraphErrors()
    g_TotExp_vs_Vov_average[sipm] = ROOT.TGraphErrors()
    g_StochExp_vs_Vov_average[sipm] = ROOT.TGraphErrors()

    for ov in Vovs[sipm]:
        if (ov in  g_SR_vs_bar[sipm].keys()): 

            print("ov ", ov)
            # average SR
            fitpol0_sr = ROOT.TF1('fitpol0_sr','pol0',-100,100)
            if (g_SR_vs_bar[sipm][ov].GetN()==0): continue;            
            g_SR_vs_bar[sipm][ov].Fit(fitpol0_sr,'QNR')
            sr = fitpol0_sr.GetParameter(0)
            g_SR_vs_Vov_average[sipm].SetPoint(g_SR_vs_Vov_average[sipm].GetN(), ov, sr)
            g_SR_vs_Vov_average[sipm].SetPointError(g_SR_vs_Vov_average[sipm].GetN()-1, 0, fitpol0_sr.GetParError(0))

            # noise using average SR
            g_Noise_vs_Vov_average[sipm].SetPoint(g_Noise_vs_Vov_average[sipm].GetN(), ov, sigma_noise(sr, tofhirVersion))
            sr_err = max(fitpol0_sr.GetParError(0), errSRsyst*sr)
            sr_up   = sr + sr_err 
            sr_down = sr - sr_err 
            noise_err  = 0.5 * ( sigma_noise(sr_down, tofhirVersion) - sigma_noise(sr_up, tofhirVersion) ) 
            g_Noise_vs_Vov_average[sipm].SetPointError(g_Noise_vs_Vov_average[sipm].GetN()-1, 0, noise_err) 
    
            # average stochastic 
            fitpol0_stoch = ROOT.TF1('fitpol0_stoch','pol0',-100,100)  
            g_Stoch_vs_bar[sipm][ov].Fit(fitpol0_stoch,'QNR')
            s_stoch = fitpol0_stoch.GetParameter(0)
            err_s_stoch = g_Stoch_vs_bar[sipm][ov].GetRMS(2)/math.sqrt(16) # fixme!
            g_Stoch_vs_Vov_average[sipm].SetPoint(g_Stoch_vs_Vov_average[sipm].GetN(), ov, s_stoch)
            g_Stoch_vs_Vov_average[sipm].SetPointError(g_Stoch_vs_Vov_average[sipm].GetN()-1, 0, err_s_stoch)

            # average expected stochastic
            fitpol0_stoch_exp = ROOT.TF1('fitpol0_stoch_exp','pol0',-100,100)
            g_StochExp_vs_bar[sipm][ov].Fit(fitpol0_stoch_exp,'QNR')
            s_stoch_exp = fitpol0_stoch_exp.GetParameter(0)
            err_s_stoch_exp = g_StochExp_vs_bar[sipm][ov].GetRMS(2)/math.sqrt(16)
            g_StochExp_vs_Vov_average[sipm].SetPoint(g_StochExp_vs_Vov_average[sipm].GetN(), ov, s_stoch_exp)
            g_StochExp_vs_Vov_average[sipm].SetPointError(g_StochExp_vs_Vov_average[sipm].GetN()-1, 0, err_s_stoch_exp)


            # tot resolution summing noise + expected stochastic in quadrature        
            tot = math.sqrt( s_stoch_exp*s_stoch_exp + sigma_noise(sr, tofhirVersion)*sigma_noise(sr, tofhirVersion) )
            err_tot = 1./tot * math.sqrt( pow( err_s_stoch_exp*s_stoch_exp,2) + pow(noise_err*sigma_noise(sr, tofhirVersion),2) )
            g_TotExp_vs_Vov_average[sipm].SetPoint(g_TotExp_vs_Vov_average[sipm].GetN(), ov, tot)
            g_TotExp_vs_Vov_average[sipm].SetPointError(g_TotExp_vs_Vov_average[sipm].GetN()-1, 0, err_tot)

            


#----------------------------------------------------------------------------------
# ratio of stochatic terms at 3.5 OV
g_ratio_stoch1 = ROOT.TGraphErrors()
g_ratio_stoch2 = ROOT.TGraphErrors()
g_ratio_stoch3 = ROOT.TGraphErrors()
for bar in range(0,16):
    if (bar not in bars[sipmTypes[1]]): continue
    if (bar not in bars[sipmTypes[0]]): continue
    if (g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5)<=0): continue
    ratio_stoch =  g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5)/g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5)
    err1 = [  g_Stoch_vs_Vov[sipmTypes[1]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[1]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[1]][bar].GetX()[i] == 3.50]
    err0 = [  g_Stoch_vs_Vov[sipmTypes[0]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[0]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[0]][bar].GetX()[i] == 3.50]
    if (err1 == [] or err0 == []): continue
    err_ratio_stoch = ratio_stoch * math.sqrt( pow(err1[0]/g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5),2) + pow(err0[0]/g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5),2) ) 
    if verbose:
        print(sipmTypes[1], sipmTypes[0], ' ratio stochastic term at 3.5 V OV = ', ratio_stoch)
    g_ratio_stoch1.SetPoint(g_ratio_stoch1.GetN(), bar, ratio_stoch)
    g_ratio_stoch1.SetPointError(g_ratio_stoch1.GetN()-1, 0, err_ratio_stoch)

for bar in range(0,16):
    if (bar not in bars[sipmTypes[1]]): continue
    if (bar not in bars[sipmTypes[2]]): continue
    if (g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5)<=0): continue
    if (g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5)<=0): continue
    ratio_stoch =  g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5)/g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5)
    err1 = [  g_Stoch_vs_Vov[sipmTypes[1]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[1]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[1]][bar].GetX()[i] == 3.50]
    err0 = [  g_Stoch_vs_Vov[sipmTypes[2]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[2]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[2]][bar].GetX()[i] == 3.50]
    if (err1 == [] or err0 == []): continue
    err_ratio_stoch = ratio_stoch * math.sqrt( pow(err1[0]/g_Stoch_vs_Vov[sipmTypes[1]][bar].Eval(3.5),2) + pow(err0[0]/g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5),2) ) 
    if verbose:
        print(sipmTypes[1], sipmTypes[2],' ratio stochastic term at 3.5 V OV = ', ratio_stoch)
    g_ratio_stoch2.SetPoint(g_ratio_stoch2.GetN(), bar, ratio_stoch)
    g_ratio_stoch2.SetPointError(g_ratio_stoch2.GetN()-1, 0, err_ratio_stoch)



for bar in range(0,16):
    if (bar not in bars[sipmTypes[0]]): continue
    if (bar not in bars[sipmTypes[2]]): continue
    if (g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5)<=0): continue
    if (g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5)<=0): continue
    ratio_stoch =  g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5)/g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5)
    err1 = [  g_Stoch_vs_Vov[sipmTypes[0]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[0]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[0]][bar].GetX()[i] == 3.50]
    err0 = [  g_Stoch_vs_Vov[sipmTypes[2]][bar].GetErrorY(i) for i in range(0, g_Stoch_vs_Vov[sipmTypes[2]][bar].GetN()) if g_Stoch_vs_Vov[sipmTypes[2]][bar].GetX()[i] == 3.50]
    if (err1 == [] or err0 == []): continue
    err_ratio_stoch = ratio_stoch * math.sqrt( pow(err1[0]/g_Stoch_vs_Vov[sipmTypes[0]][bar].Eval(3.5),2) + pow(err0[0]/g_Stoch_vs_Vov[sipmTypes[2]][bar].Eval(3.5),2) ) 
    if verbose:
        print(sipmTypes[0], sipmTypes[2],' ratio stochastic term at 3.5 V OV = ', ratio_stoch)
    g_ratio_stoch3.SetPoint(g_ratio_stoch3.GetN(), bar, ratio_stoch)
    g_ratio_stoch3.SetPointError(g_ratio_stoch3.GetN()-1, 0, err_ratio_stoch)
        









if verbose:
    print('\n\nstart drawing')


#------------------
#------ draw ------
#------------------


leg = {}

# Tres vs OV
print('Plotting time resolution vs OV...')
for sipm in sipmTypes:
    leg[sipm] = ROOT.TLegend(0.65,0.60,0.89,0.79)
    leg[sipm].SetBorderSize(0)
    leg[sipm].SetFillStyle(0)
    for i,bar in enumerate(bars[sipm]):
        if (bar not in g_data[sipm].keys()): continue
        if (g_data[sipm][bar].GetN()==0): continue
        c =  ROOT.TCanvas('c_timeResolution_vs_Vov_%s_bar%02d'%(sipm,bar),'c_timeResolution_vs_Vov_%s_bar%02d'%(sipm,bar),650,500)
        c.SetGridy()
        c.cd()
        xmin = 0.0
        xmax = 4.0
        hdummy = ROOT.TH2F('hdummy_%s_%d'%(sipm,bar),'',100,xmin,xmax,140,0,140)
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

        g_StochExp_vs_Vov[sipm][bar].SetLineWidth(2)
        g_StochExp_vs_Vov[sipm][bar].SetLineColor(ROOT.kGreen+2)
        g_StochExp_vs_Vov[sipm][bar].SetFillColor(ROOT.kGreen+2)
        g_StochExp_vs_Vov[sipm][bar].SetFillStyle(3001)
        g_StochExp_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kGreen+2,0.5)
        g_StochExp_vs_Vov[sipm][bar].Draw('E3lsame')

        g_TotExp_vs_Vov[sipm][bar].SetLineWidth(2)
        g_TotExp_vs_Vov[sipm][bar].SetLineColor(ROOT.kRed+1)
        g_TotExp_vs_Vov[sipm][bar].SetFillColor(ROOT.kRed+1)
        g_TotExp_vs_Vov[sipm][bar].SetFillColorAlpha(ROOT.kRed+1,0.5)
        g_TotExp_vs_Vov[sipm][bar].SetFillStyle(3001)
        g_TotExp_vs_Vov[sipm][bar].Draw('E3lsame')

        #save on file
        outfile.cd()
        g_data[sipm][bar].Write('g_Data_vs_Vov_%s_bar%02d'%(sipm,  bar))
        g_Noise_vs_Vov[sipm][bar].Write('g_Noise_vs_Vov_%s_bar%02d'%(sipm, bar))
        g_StochExp_vs_Vov[sipm][bar].Write('g_Stoch_vs_Vov_%s_bar%02d'%(sipm, bar))
        g_Stoch_vs_Vov[sipm][bar].Write('g_StochMeas_vs_Vov_%s_bar%02d'%(sipm, bar))

        if (i==0):
            leg[sipm].AddEntry(g_data[sipm][bar], 'data', 'PL')
            leg[sipm].AddEntry(g_Noise_vs_Vov[sipm][bar], 'noise', 'L')
            leg[sipm].AddEntry(g_StochExp_vs_Vov[sipm][bar], 'stoch', 'L')

        leg[sipm].Draw('same')

        lat_s = latex_sipm(sipm)
        lat_s.Draw()
        lat_b = latex_bar(bar)
        lat_b.Draw()
        cms_logo = draw_logo()
        cms_logo.Draw()

        c.SaveAs(outdir+'/tRes_vs_Vov_perBar/'+c.GetName()+'.png')
        c.SaveAs(outdir+'/tRes_vs_Vov_perBar/'+c.GetName()+'.pdf')
        hdummy.Delete()


# -----------   vs npe  ----------------


# SR and best threshold vs Vov
leg2 = ROOT.TLegend(0.20,0.70,0.45,0.89)
leg2.SetBorderSize(0)
leg2.SetFillStyle(0)

    
bar = barsIntersection[0]
for sipm in sipmTypes:
    g_SR_vs_Vov[sipm][bar].SetMarkerColor(cols[sipm])
    g_SR_vs_Vov[sipm][bar].SetLineColor(cols[sipm])
    leg2.AddEntry(g_SR_vs_Vov[sipm][bar], '%s'%labels[sipm], 'PL')

#i = 0
for bar in range(0,16):
    if (bar not in g_data[sipm].keys()): continue
    if (g_data[sipm][bar].GetN()==0): continue     
    c = ROOT.TCanvas('c_slewRate_vs_Vov_bar%02d'%(bar),'c_slewRate_vs_Vov_bar%02d'%(bar),650,500)
    c.SetGridy()
    c.cd()
    xmin = 0.0
    xmax = 4.0
    ymax = 45
    hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,xmin,xmax,100,0,ymax)
    hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
    hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
    hdummy.Draw()
    for sipm in sipmTypes:
        #if (i==0):
          #  leg2.AddEntry(g_SR_vs_Vov[sipm][bar], '%s'%labels[sipm], 'PL')
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


    c = ROOT.TCanvas('c_slewRate_vs_GainNpe_bar%02d'%(bar),'c_slewRate_vs_GainNpe_bar%02d'%(bar),650,500)
    c.SetGridy()
    c.cd()
    hdummy = ROOT.TH2F('hdummy_%d'%(bar),'',100,0,6E09,100,0,80)
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

    c = ROOT.TCanvas('c_bestTh_vs_Vov_bar%02d'%(bar),'c_bestTh_vs_Vov_bar%02d'%(bar),650,500)
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






# average slew rate vs OV
c =  ROOT.TCanvas('c_slewRate_vs_Vov_average','c_slewRate_vs_Vov_average',650,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',16, 0.0, 4.0 ,100, 0,80)
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







# average time resolution vs Npe
c =  ROOT.TCanvas('c_timeResolution_vs_Npe_average','c_timeResolution_vs_Npe_average',650,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',1000, 1000, 6000, 100, 20, 140)
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






# average time resolution vs GainxNpe
c =  ROOT.TCanvas('c_timeResolution_vs_GainNpe_average','c_timeResolution_vs_GainNpe_average',650,500)
c.SetGridx()
c.SetGridy()
c.cd()    
hdummy = ROOT.TH2F('hdummy','',1000, 0, 6E09, 100, 20, 140)
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
                                       

# average tRes
for sipm in sipmTypes:
    lat_s = latex_sipm(sipm)

    c =  ROOT.TCanvas('c_timeResolution_vs_Vov_average_%s'%(sipm),'c_timeResolution_vs_Vov_average_%s'%(sipm),650,500)
    c.cd()
    hdummy = ROOT.TH2F('hdummy','',100, 0., 4.,100,0,120)
    hdummy.GetXaxis().SetTitle('V_{OV}^{eff} [V]')
    hdummy.GetYaxis().SetTitle('time resolution [ps]')
    hdummy.Draw()
    g_data_average[sipm].SetMarkerStyle(20)
    g_data_average[sipm].SetMarkerSize(1)
    g_data_average[sipm].SetMarkerColor(1)
    g_data_average[sipm].SetLineColor(1)
    g_data_average[sipm].SetLineWidth(2)
    g_data_average[sipm].Draw('plsame')

    g_Noise_vs_Vov_average[sipm].SetLineWidth(2)
    g_Noise_vs_Vov_average[sipm].SetLineColor(ROOT.kBlue)
    g_Noise_vs_Vov_average[sipm].SetFillColor(ROOT.kBlue)
    g_Noise_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kBlue,0.5)
    g_Noise_vs_Vov_average[sipm].SetFillStyle(3004)
    g_Noise_vs_Vov_average[sipm].Draw('E3lsame')
    g_StochExp_vs_Vov_average[sipm].SetLineWidth(2)
    g_StochExp_vs_Vov_average[sipm].SetLineColor(ROOT.kGreen+2)
    g_StochExp_vs_Vov_average[sipm].SetFillColor(ROOT.kGreen+2)
    g_StochExp_vs_Vov_average[sipm].SetFillStyle(3001)
    g_StochExp_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kGreen+2,0.5)
    g_StochExp_vs_Vov_average[sipm].Draw('E3lsame')
    g_TotExp_vs_Vov_average[sipm].SetLineWidth(2)
    g_TotExp_vs_Vov_average[sipm].SetLineColor(ROOT.kRed+1)
    g_TotExp_vs_Vov_average[sipm].SetFillColor(ROOT.kRed+1)
    g_TotExp_vs_Vov_average[sipm].SetFillColorAlpha(ROOT.kRed+1,0.5)
    g_TotExp_vs_Vov_average[sipm].SetFillStyle(3001)
    g_TotExp_vs_Vov_average[sipm].Draw('E3lsame')
    leg[sipm].Draw()

    lat_s.Draw()
    outfile.cd()
    g_data_average[sipm].Write('g_data_vs_Vov_average_%s'%sipm)
    g_Noise_vs_Vov_average[sipm].Write('g_Noise_vs_Vov_average_%s'%sipm)
    g_Stoch_vs_Vov_average[sipm].Write('g_StochMeas_vs_Vov_average_%s'%sipm)
    g_StochExp_vs_Vov_average[sipm].Write('g_Stoch_vs_Vov_average_%s'%sipm)
    g_TotExp_vs_Vov_average[sipm].Write('g_TotExp_vs_Vov_average_%s'%sipm)

    cms_logo = draw_logo()
    cms_logo.Draw()
    c.SaveAs(outdir+'/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/'+c.GetName()+'.pdf')
    hdummy.Delete()


# SR and best threshold vs bar
for sipm in sipmTypes:
    for ov in Vovs[sipm]:
        if (ov not in g_SR_vs_bar[sipm].keys()): continue
        ov = Vovs_eff(sipm, ov)        
        c = ROOT.TCanvas('c_slewRate_vs_bar_%s_Vov%.2f'%(sipm,ov),'c_slewRate_vs_bar_%s_Vov%.2f'%(sipm,ov),650,500)
        c.SetGridy()
        c.cd()
        #hdummy = ROOT.TH2F('hdummy5_%d'%(ov),'',100,-0.5,15.5,100,0,15)
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,80)
        hdummy.GetXaxis().SetTitle('bar')
        hdummy.GetYaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy.Draw()
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

        c = ROOT.TCanvas('c_bestTh_vs_bar_%s_Vov%.2f'%(sipm,ov),'c_bestTh_vs_bar_%s_Vov%.2f'%(sipm,ov),650,500)
        c.SetGridy()
        c.cd()
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,20)
        hdummy.GetXaxis().SetTitle('bar')
        hdummy.GetYaxis().SetTitle('timing threshold [DAC]')
        hdummy.Draw()
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





#------- vs SR -------
for sipm in sipmTypes:
    for ov in Vovs[sipm]:
        if (ov not in g_Stoch_vs_SR[sipm].keys()): continue
        ov = Vovs_eff(sipm, ov)        
        c = ROOT.TCanvas('c_stoch_vs_SR_%s_Vov%.2f'%(sipm,ov),'c_stoch_vs_SR_%s_Vov%.2f'%(sipm,ov),650,500)
        c.SetGridy()
        c.cd()
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,0,80,100,0,60)
        hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy.GetYaxis().SetTitle('#sigma_{stoch} [ps]')
        hdummy.Draw()

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


        c = ROOT.TCanvas('c_noise_vs_SR_%s_Vov%.2f'%(sipm,ov),'c_noise_vs_SR_%s_Vov%.2f'%(sipm,ov),650,500)
        c.SetGridy()
        c.cd()
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,0,80,100,0,60)
        hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy.GetYaxis().SetTitle('#sigma_{noise} [ps]')
        hdummy.Draw()

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

        c = ROOT.TCanvas('c_data_vs_SR_%s_Vov%.2f'%(sipm,ov),'c_data_vs_SR_%s_Vov%.2f'%(sipm,ov),650,500)
        c.SetGridy()
        c.cd()
        hdummy = ROOT.TH2F('hdummy_%s_%.2f'%(sipm,ov),'',100,-0.5,15.5,100,0,140)
        hdummy.GetXaxis().SetTitle('slew rate at the timing thr. [#muA/ns]')
        hdummy.GetYaxis().SetTitle('#sigma_{t} [ps]')
        hdummy.Draw()

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







# --- stoch and noise term vs bar - all sipms on same canvas
for ov in VovsUnion:
    c = ROOT.TCanvas('c_noise_vs_bar_Vov%.2f'%(ov),'c_noise_vs_bar_Vov%.2f'%(ov),650,500)
    c.cd()
    hdummy = ROOT.TH2F('hdummy_Vov%.2f'%(ov),'',100,-0.5,15.5,100,0,100)
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

    c = ROOT.TCanvas('c_stoch_vs_bar_Vov%.2f'%(ov),'c_stoch_vs_bar_Vov%.2f'%(ov),650,500)
    c.cd()
    hdummy = ROOT.TH2F('hdummy_Vov%.2f'%(ov),'',100,-0.5,15.5,100,0,100)
    hdummy.GetXaxis().SetTitle('bar')
    hdummy.GetYaxis().SetTitle('#sigma_{t, stoch} [ps]')
    hdummy.Draw()
    for j, sipm in enumerate(sipmTypes):
        if ov not in g_StochExp_vs_bar[sipm].keys():
            continue
        g_StochExp_vs_bar[sipm][ov].SetMarkerStyle( markers[sipm] )
        g_StochExp_vs_bar[sipm][ov].SetMarkerColor(cols[sipm])
        g_StochExp_vs_bar[sipm][ov].SetLineColor(cols[sipm])
        g_StochExp_vs_bar[sipm][ov].Draw('psame')
    leg2.Draw()
    lat = latex_vov(ov)
    lat.Draw()
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.png')
    c.SaveAs(outdir+'/tRes_vs_bar_perVov/'+c.GetName()+'.pdf')
    hdummy.Delete()



outfile.Close()
