import math
stochPow = 0.73
# ------------- scaling contributions --------------
def scale_stoch(alpha, alpha_ref, stoch_ref):
    stoch_scaled = stoch_ref* math.pow(math.cos(math.radians(alpha)) / math.cos(math.radians(alpha_ref)), stochPow) 
    return stoch_scaled

def scale_noise(alpha, alpha_ref, noise_ref):
    _,_,tdc,_ = get_noise_pars('2c')
    tdc = tdc / math.sqrt(2)
    noise_ref_notdc = math.sqrt(noise_ref**2 - tdc**2)
    noise_scaled_notdc = noise_ref_notdc * math.cos(math.radians(alpha)) / math.cos(math.radians(alpha_ref))
    noise_scaled = math.sqrt(noise_scaled_notdc**2 + tdc**2)
    return noise_scaled

# assuming dcr does not scale with npe
def scale_dcr(alpha, alpha_ref, dcr_ref):
    dcr_scaled = dcr_ref * math.cos(math.radians(alpha)) / math.cos(math.radians(alpha_ref))
    return dcr_scaled

def scale_tot(a, a_ref, s_ref, n_ref, d_ref):
    stoch = scale_stoch(a, a_ref, s_ref)
    noise = scale_noise(a, a_ref, n_ref)
    dcr = scale_dcr(a, a_ref, d_ref)
    tot = math.sqrt(stoch**2 + noise**2 + dcr**2)
    return tot
