import ROOT

def getSlewRateFromPulseShape(g1, timingThreshold, gtemp, canvas=None):
    if (g1.GetN() < 2):
        return (-1, -1)

    # Find the index at the timing threshold
    itiming = 0
    for i in range(0, g1.GetN()):
        if (round(g1.GetY()[i] / 0.313) == timingThreshold):
            itiming = i
            break

    # Initialize the indices for the starting and ending points of the fit
    start_index = itiming
    end_index = itiming

    # Find the first point with positive slope before the timing threshold
    for i in range(itiming, -1, -1):
        if (g1.GetX()[i] > g1.GetX()[i - 1]) and (g1.GetY()[i] > g1.GetY()[i - 1]):
            start_index = i
        else:
            break

    # Find the first point with positive slope after the timing threshold
    for i in range(itiming, g1.GetN() - 1):
        if (g1.GetX()[i] < g1.GetX()[i + 1]) and (g1.GetY()[i] < g1.GetY()[i + 1]:
            end_index = i
            break

    # Create a list to store the points for fitting
    fit_points_x = []
    fit_points_y = []

    # Add points to the fitting list while the slope is positive
    for i in range(start_index, end_index + 1):
        fit_points_x.append(g1.GetX()[i])
        fit_points_y.append(g1.GetY()[i])
        if i < g1.GetN() - 1 and g1.GetY()[i] > g1.GetY()[i + 1]:
            break

    if len(fit_points_x) < 2:
        return (-1, -1)  # Not enough points for fitting

    # Convert the fitting points to a TGraph
    gtemp = ROOT.TGraph(len(fit_points_x), fit_points_x, fit_points_y)

    fitSR = ROOT.TF1('fitSR', 'pol1', gtemp.GetX()[0], gtemp.GetX()[-1])
    fitSR.SetLineColor(g1.GetMarkerColor() + 1)
    fitSR.SetRange(gtemp.GetX()[0], gtemp.GetX()[-1])
    fitSR.SetParameters(0, 10)
    
    fitStatus = int(gtemp.Fit(fitSR, 'QRS+'))
    sr = fitSR.Derivative(gtemp.GetX()[itiming])
    err_sr = fitSR.GetParError(1)
    
    if (canvas != None):
        canvas.cd()
        gtemp.SetMarkerStyle(g1.GetMarkerStyle())
        gtemp.SetMarkerColor(g1.GetMarkerColor())
        gtemp.Draw('ap')
        g1.Draw('psames')
        fitSR.Draw('same')
        canvas.Update()
        ps = gtemp.FindObject("stats")
        ps.SetTextColor(g1.GetMarkerColor())
        if ('L' in g1.GetName()):
            ps.SetY1NDC(0.85)  # new y start position
            ps.SetY2NDC(0.95)  # new y end position
        if ('R' in g1.GetName()):
            ps.SetY1NDC(0.73)  # new y start position
            ps.SetY2NDC(0.83)  # new y end position

    return (sr, err_sr)
