import ROOT

def make_canvas(name, x_title, y_title, x_range, y_range, gridy=True):
    c = ROOT.TCanvas(name)
    h = ROOT.TH2F(f"h_{name}", "", 100, *x_range, 100, *y_range)
    h.SetTitle(f";{x_title};{y_title}")
    h.Draw()
    if gridy:
        c.SetGridy()
    return c, h

def draw_graphs(graphs, colors, markers, legend, label_fmt):
    for i, (key, g) in enumerate(graphs.items()):
        g.Sort()
        g.SetMarkerStyle(markers[i])
        g.SetMarkerColor(colors[i])
        g.SetLineColor(colors[i])
        g.Draw("plsame")
        legend.AddEntry(g, label_fmt(key), "PL")

def save_canvas(canvas, outdir, subdir):
    path = f"{outdir}/summaryPlots/{subdir}/{canvas.GetName()}"
    canvas.SaveAs(path + ".png")
    canvas.SaveAs(path + ".pdf")
