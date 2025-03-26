from utils import *

canvas_name = "c_pulseShape"
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'

xmin = 10
xmax = 60
ymin = -10
ymax = 25

th1 = 2
th2 = 10


# File loading
f = ROOT.TFile("/eos/home-s/spalluot/MTD/TB_CERN_Sep23/Lab5015Analysis/plots/TOFHIR_pulseShape.root")

# Retrieve the histogram
hist_name = "hOuTot_0"
hOutot = f.Get(hist_name)

# Check if the histogram was loaded successfully
if not hOutot:
    print(f"Error: Histogram '{hist_name}' not found in file.")
    exit()

# Create the canvas
c = ROOT.TCanvas(canvas_name, f"{canvas_name}", 600, 500)

hPad = ROOT.gPad.DrawFrame(xmin, ymin, xmax, ymax)
hPad.SetTitle(";time [ns];Current")
hPad.Draw()
ROOT.gPad.SetTicks(1)

hOutot.Draw("same")

# thresholds
line1 = ROOT.TLine(xmin, th1, xmax, th1)
line1.SetLineStyle(2)
line1.SetLineColor(ROOT.kGray + 1)
line1.Draw("same")

line2 = ROOT.TLine(xmin, th2,xmax, th2)
line2.SetLineStyle(2)
line2.SetLineColor(ROOT.kGray + 1)
line2.Draw("same")


# Add labels for the thresholds
label1 = ROOT.TLatex(42, th1+1, "Threshold 1")
label1.SetTextColor(ROOT.kGray + 1)
label1.Draw("same")

label2 = ROOT.TLatex(42, th2+1, "Threshold 2")
label2.SetTextColor(ROOT.kGray + 1)
label2.Draw("same")


# Save the canvas to file
c.SaveAs(f"{outdir}{canvas_name}.png")
c.SaveAs(f"{outdir}{canvas_name}.pdf")
