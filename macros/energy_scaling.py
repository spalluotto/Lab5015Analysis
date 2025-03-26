from utils import *
import ROOT
import numpy as np
from scipy.optimize import fsolve

# simulation --  recHit for single muons
g_e_vs_eta_sim = ROOT.TFile.Open("energy_vs_eta_MinBias14TeV.root").Get("g_energy_vs_eta_MinBias14TeV")

fit_func_pol2 = 'pol2'
fit_func_true = '[0] * 0.86 / cos(pi/2 - 2 * atan(exp(-x)))'

k_posCor = 18


# ---- fit graph from simulation --------------
def fit_simulation(g, fit_f=fit_func_true, plot_name=None):
    fit_func = ROOT.TF1("fit_func", fit_f, 0, 1.65)
    g.Fit(fit_func, "R")
    fit_params = [fit_func.GetParameter(i) for i in range(fit_func.GetNpar())]
    print("fit pars ", fit_params)

    if plot_name:
        canvas = ROOT.TCanvas("", "", 600, 500)    
        g.GetXaxis().SetLimits(0,1.65)
        g.SetMinimum(1.8)
        g.SetMaximum(12)
        g.SetMarkerStyle(20)
        g.SetMarkerColor(4)
        g.SetTitle(";#eta;Energy [MeV]")
        g.Draw("AP")
        fit_func.SetLineColor(2)
        fit_func.Draw("SAME")
        canvas.SaveAs(plot_name)
    return fit_params


pars_fit_pol2 = fit_simulation(g_e_vs_eta_sim, fit_f=fit_func_pol2)
pars_func_true = fit_simulation(g_e_vs_eta_sim)

# draw sim and fit
#pltname=f"/eos/home-s/spalluot/www/MTD/MTDTB_CERN_Sep23/for_paper/energy_studies/c_energy_vs_eta_simulation"
#ROOT.gStyle.SetOptFit(0)
#fit_simulation(g_e_vs_eta_sim, plot_name=pltname+'_true.png')
#fit_simulation(g_e_vs_eta_sim, fit_f=fit_func_pol2, plot_name=pltname+'_pol2.png') 


# extract eta from the graph, given the energy deposited
def eq_energy_vs_eta(x, y):
    par0 = pars_func_true[0]
    return par0 * 0.86 / np.cos(np.pi / 2 - 2 * np.arctan(np.exp(-x))) - y

def eq_fit_sim_pol2(x,y):
    params = pars_fit_pol2
    return params[0] + params[1]*x + params[2]*x*x - y

def fit_sim_pol2(x):
    params = pars_fit_pol2
    return params[0] + params[1]*x + params[2]*x*x

def find_x(y,equat):
    initial_guess = 1.0
    x_solution = fsolve(equat, initial_guess, args=(y,))
    print(x_solution)
    return x_solution[0]
# usage :  find_x(edep, eq_energy_vs_eta)
#          find_x(edep, eq_fit_sim_pol2)


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
# --------------------------------------------------------------



# vere in cms, ma non con il TB per vari effetti di pt etc
def eta_func(alpha):
    ang = math.radians((90-alpha)/2)
    return -math.log(math.tan(ang))
def alpha_func(eta):
    theta = math.degrees(2*math.atan(math.exp(-eta)))
    return (90-theta)
def eta_from_alpha(a, t=3.75, eq=eq_fit_sim_pol2):
    E = energy_deposited(a, thickness=t)
    print("angle ", a , "  thickness ",t, "    energy : ", E)
    #e_vs_eta = energy_vs_eta()
    # given the energy deposited at alpha, find the corresponding eta given the simulation fit
    eta = find_x(E,eq)
    return float(eta)

def alpha_from_E(E, thickness=3.75, eMIP=0.86):
    alpha = math.acos(eMIP*thickness/E)
    return alpha

def alpha_from_eta(eta,t=3.75, eq=eq_fit_sim_pol2):
    E = fit_sim_pol2(eta)
    alpha = alpha_from_E(E,thickness=t)
    return alpha
# ---------------------




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



# position correction
def posCor(eta,slope=k_posCor):
    theta = alpha_from_eta(eta) # e gia in radianti
    space = 3.12/math.cos(theta)
    # sqrt(12) under the assumption beam was uniform
    # 2 because given the center of the bar you have half the spread
    t = slope*space / math.sqrt(12) / 2
    return t

def scale_tot_posCor(eta, E, E_ref, s_ref, n_ref, d_ref):
    stoch = scale_stoch(E, E_ref, s_ref)
    noise = scale_noise(E, E_ref, n_ref)
    dcr = scale_dcr(E, E_ref, d_ref)
    positCor = posCor(eta)
    print(" %%%%%%%%   ----   eta ", eta, "  position correction ", positCor)
    tot = math.sqrt(stoch**2 + noise**2 + dcr**2 + positCor**2)
    return tot

# ----------------------------------------------------
