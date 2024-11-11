import math
import ROOT
import numpy as np
from scipy.optimize import fsolve

# simulation --  recHit for single muons
g_e_vs_eta_sim = ROOT.TFile.Open("energy_vs_eta_MinBias14TeV.root").Get("g_energy_vs_eta_MinBias14TeV")


def fit_simulation(g, plot_name=None):
    fit_func = ROOT.TF1("fit_func", "[0] * 0.86 / cos(pi/2 - 2 * atan(exp(-x)))", 0, 1.65)
    g.Fit(fit_func, "R")
    print("fit par ", fit_func.GetParameter(0))
    if plot_name:
        canvas = ROOT.TCanvas("", "", 600, 500)    
        g.GetXaxis().SetLimits(0,1.65)
        g.SetMinimum(1.8)
        g.SetMaximum(12)
        g.SetMarkerStyle(20)
        g.SetMarkerColor(4)
        g.Draw("AP")
        fit_func.SetLineColor(2)
        fit_func.Draw("SAME")
        canvas.SaveAs(plot_name)
    return fit_func.GetParameter(0)

par0 = fit_simulation(g_e_vs_eta_sim)
def eq_energy_vs_eta(x, y):
    return par0 * 0.86 / np.cos(np.pi / 2 - 2 * np.arctan(np.exp(-x))) - y

def find_x(y):
    initial_guess = 1.0
    x_solution = fsolve(eq_energy_vs_eta, initial_guess, args=(y,))
    print(x_solution)
    return x_solution[0]



def find_x_given_y(graph, y_target):
    n_points = graph.GetN()
    for i in range(n_points - 1):
        x1, y1 = graph.GetX()[i], graph.GetY()[i]
        x2, y2 = graph.GetX()[i + 1], graph.GetY()[i + 1]
        if (y1 <= y_target <= y2) or (y2 <= y_target <= y1):
            x_target = x1 + (x2 - x1) * (y_target - y1) / (y2 - y1)
            return x_target
    if round(y2,5)==round(y_target,5):
        x_target = x1 + (x2 - x1) * (y_target - y1) / (y2 - y1)
        return x_target
    return None


def eta_func(alpha):
    ang = math.radians((90-alpha)/2)
    return -math.log(math.tan(ang))
def alpha_func(eta):
    theta = math.degrees(2*math.atan(math.exp(-eta)))
    return (90-theta)

# energy functions ----
def energy_deposited(alpha, thickness=3.75, eMIP=0.86):     # Edep = eMIP * thickness / cos(angle) --> angle = angle at TB
    edep = eMIP * thickness / math.cos(math.radians(alpha))
    return edep

def energy_vs_eta(beta_max=80, thickness=3.75, plot_name=None): # obtain a graph which is energy deposited vs eta given a TB angle (beta) for specific thickness
    graph = ROOT.TGraphErrors()    
    for beta in range(beta_max):
        eta = eta_func(beta)
        energy = energy_deposited(beta,thickness)
        graph.SetPoint(graph.GetN(), eta, energy)
        
    # If plot_name is specified, save the plot
    if plot_name:
        canvas = ROOT.TCanvas("", "", 600, 500)
        graph.SetTitle(";#eta;Energy [MeV]")
        graph.SetMarkerColor(2)
        graph.GetXaxis().SetLimits(0,1.65)
        graph.SetMinimum(1.8)
        graph.SetMaximum(12)
        graph.Draw("AP")
        g_e_vs_eta_sim.SetLineColor(4)
        g_e_vs_eta_sim.SetLineWidth(2)
        g_e_vs_eta_sim.Draw("LSAME")

        # Add a text label for thickness
        label = ROOT.TLatex()
        label.SetNDC()
        label.SetTextSize(0.05)
        label.DrawLatex(0.20, 0.85, f"Thickness = {round(thickness,2)} mm")

        # Add a legend
        legend = ROOT.TLegend(0.6, 0.7, 0.89, 0.89)  # Position (x1, y1, x2, y2)
        legend.SetTextSize(0.05)
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)
        legend.AddEntry(graph, "Expected", "p") 
        legend.AddEntry(g_e_vs_eta_sim, "Simulation", "l")
        legend.Draw()
    
        canvas.SaveAs(plot_name)
        print("saving ", plot_name)
    return graph

def energy_vs_alpha(beta_max=80, thickness=3.75, plot_name=None): # obtain a graph which is energy deposited vs eta given a TB angle (beta) for specific thickness
    graph = ROOT.TGraphErrors()
    graph_eta = ROOT.TGraphErrors()
    
    for beta in range(beta_max):
        energy = energy_deposited(beta,thickness)
        graph.SetPoint(graph.GetN(), beta, energy)
    if plot_name:
        canvas = ROOT.TCanvas("", "", 600, 500)
        graph.SetTitle(";#alpha_{TB};Energy [MeV]")
        graph.SetLineColor(2)
        graph.SetLineWidth(2)
        graph.GetXaxis().SetLimits(0,66)
        graph.SetMinimum(1.8)
        graph.SetMaximum(12)
        graph.Draw("AL")

        # Add a text label for thickness
        label = ROOT.TLatex()
        label.SetNDC()
        label.SetTextSize(0.05)
        label.DrawLatex(0.20, 0.85, f"Thickness = {round(thickness,2)} mm")
        
        canvas.SaveAs(plot_name)
        print("saving ", plot_name)
    return graph

    
def eta_from_alpha(a, t=3.75):
    E = energy_deposited(a, thickness=t)
    print("angle ", a , "  thickness ",t, "    energy : ", E)
    #e_vs_eta = energy_vs_eta()
    eta = find_x(E)
    return float(eta)
