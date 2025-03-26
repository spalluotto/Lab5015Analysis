from utils import*

ymax = 2000

ROOT.gStyle.SetTitleOffset(1.28,'Y')
# Nomi dei file e dell'istogramma
file1_name = "/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/moduleCharacterization_step1_HPK_nonIrr_LYSO818_Vov1.00_angle52_checkGoodBeam_T5C.root"
file2_name = "/afs/cern.ch/user/s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/moduleCharacterization_step1_HPK_nonIrr_LYSO818_Vov1.00_angle52_checkGoodBeam_T5C_veto200.root"
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'
plotname = 'c_compareEnergySpectra_vetoingXT_minEn200'
hist_name = "h1_energy_bar07L-R_Vov1.00_th11"

# Caricamento dei file ROOT
file1 = ROOT.TFile.Open(file1_name)
file2 = ROOT.TFile.Open(file2_name)

# Estrazione degli istogrammi dai file
hist1 = file1.Get(hist_name)
hist2 = file2.Get(hist_name)

# Verifica che gli istogrammi siano stati caricati correttamente
if not hist1 or not hist2:
    print("Errore: impossibile trovare l'istogramma in uno dei file.")
    exit()

# Stile degli istogrammi per differenziarli
hist1.SetLineColor(ROOT.kBlue)
hist1.SetLineWidth(2)
hist2.SetLineColor(ROOT.kRed)
hist2.SetLineWidth(2)
hist2.SetFillColorAlpha(2, 0.2)
# Creazione della canvas
canvas = ROOT.TCanvas("", "", 600, 500)

hPad = ROOT.gPad.DrawFrame(0.,0.1,1000.0,ymax)
hPad.SetTitle(';energy [ADC]; entries')
ROOT.gPad.SetTicks(1)
hPad.Draw()
hPad.GetXaxis().SetNdivisions(205)
hist1.GetXaxis().SetNdivisions(205)
hist2.GetXaxis().SetNdivisions(205)
hist1.Draw("same")
hist2.Draw("same")

# fit landau
fun = ROOT.TF1("landau_fit", "landau", 280,450)
hist1.Fit(fun, "R")
fun.SetLineColor(1)
fun.SetLineWidth(1)
fun.Draw('same')
l1 = ROOT.TLine(fun.GetParameter(1)*0.80,0,fun.GetParameter(1)*0.80, ymax)
l2 = ROOT.TLine(950,0,950,ymax)
l1.SetLineStyle(2)
l2.SetLineStyle(2)
l1.Draw()
l2.Draw()
tl = ROOT.TLatex()
tl.SetNDC()
tl.SetTextFont(42)
tl.SetTextSize(0.045)
tl.SetTextColor(1)
tl.DrawLatex(0.65,0.82,'#splitline{V_{OV} = 1.00 V}{HPK, 25 #mum}')


# Aggiungi una legenda per distinguere gli istogrammi
legend = ROOT.TLegend(0.65, 0.2, 0.89, 0.4)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextFont(42)
legend.SetTextSize(0.045)
legend.AddEntry(hist1, "No veto", "l")
legend.AddEntry(hist2, "Veto", "l")
legend.Draw()

# Mostra la canvas
canvas.Draw()
canvas.SaveAs(f"{outdir}{plotname}.png")
