from utils import * 

canvas_name = "c_graphs_types"
outdir = '/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/'

# File loading
file_irr = ROOT.TFile("../plots/graphs_irr_HPK_2E14_types.root")
file_nonIrr = ROOT.TFile("../plots/graphs_nonIrr_HPK_types.root")

# Graph retrieval
graph_names_irr = [
    "g_data_scaled_vs_Vov_average_HPK_2E14_LYSO100056_angle64_T-35C",
    "g_data_scaled_vs_Vov_average_HPK_2E14_LYSO815_angle64_T-35C",
    "g_data_scaled_vs_Vov_average_HPK_2E14_LYSO300032_angle64_T-35C"
]
graph_names_nonIrr = [
    "g_dataMeas_scaled_vs_Vov_average_HPK_nonIrr_LYSO818_angle64_T5C",
    "g_dataMeas_scaled_vs_Vov_average_HPK_nonIrr_LYSO813_angle64_T5C",
    "g_dataMeas_scaled_vs_Vov_average_HPK_nonIrr_LYSO816_angle64_T5C"
]

# Create the canvas
c = ROOT.TCanvas(canvas_name, f"{canvas_name}", 600, 500)

# Set up the frame and axis titles
xmin, xmax = 0, 4.
ymin, ymax = 20, 80
hPad = ROOT.gPad.DrawFrame(xmin, ymin, xmax, ymax)
hPad.SetTitle(";V_{OV} [V];time resolution [ps]")
hPad.Draw()
ROOT.gPad.SetTicks(1)

# Draw dashed lines at y=30 and y=60
line1 = ROOT.TLine(xmin, 30, xmax, 30) 
line1.SetLineStyle(2)              
line1.SetLineColor(ROOT.kGray + 1) 
line1.Draw("same")

line2 = ROOT.TLine(xmin, 60, xmax, 60)
line2.SetLineStyle(2)              
line2.SetLineColor(ROOT.kGray + 1) 
line2.Draw("same")

# Create the legend
leg = ROOT.TLegend(0.5, 0.6, 0.89, 0.89)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextFont(42)
leg.SetTextSize(0.045)

# Style attributes for graphs (can be customized)
plotAttrs = {
    0: [20, ROOT.kGreen+2, "type 1 irradiated"], 
    1: [21, ROOT.kBlue, "type 2 irradiated"],
    2: [22, ROOT.kRed, "type 3 irradiated"],
    3: [24, ROOT.kGreen+2, "type 1 non-irradiated"],
    4: [25, ROOT.kBlue, "type 2 non-irradiated"],
    5: [26, ROOT.kRed, "type 3 non-irradiated"]
}

# Draw the irradiated graphs
for i, name in enumerate(graph_names_irr):
    graph = file_irr.Get(name)
    graph.SetMarkerStyle(plotAttrs[i][0])
    graph.SetMarkerColor(plotAttrs[i][1])
    graph.SetLineColor(plotAttrs[i][1])
    graph.SetMarkerSize(1.15)
    leg.AddEntry(graph, plotAttrs[i][2], "PL")
    graph.Draw("P SAME")

# Draw the non-irradiated graphs
for i, name in enumerate(graph_names_nonIrr, start=len(graph_names_irr)):
    graph = file_nonIrr.Get(name)
    graph.SetMarkerStyle(plotAttrs[i][0])
    graph.SetMarkerColor(plotAttrs[i][1])
    graph.SetLineColor(plotAttrs[i][1])
    graph.SetMarkerSize(1.15)
    leg.AddEntry(graph, plotAttrs[i][2], "PL")
    graph.Draw("P SAME")

# Draw the legend
leg.Draw()

# Save the canvas to file
c.SaveAs(f"{outdir}{canvas_name}.png")
c.SaveAs(f"{outdir}{canvas_name}.pdf")
