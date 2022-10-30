import numpy as np
    
def keplerian_inverse(__ = None,e = None,M = None): 
    # nu = keplerian_inverse(~,e,M)
# From Meeus Ch. 30, page 206 - Third method.
# Due to Roger Sinnott, Sky & Telescope, 1985
# Solves the inverse Kepler problem, i.e. given time of flight since last periapsis,
#     returns true anomaly
    
    ###### INPUT #######
#T - orbital period in arbitrary time units (unused in this version,
#       replaced in argument list by ~)
#e - orbital eccentricity
#M - mean anomaly in degrees
####################
    
    ######  OUTPUT #####
# nu - true anomaly in degrees
####################
    
    # Dr. T. S. Kostadinov, Nov. 7 , 2006 - January 2013
    
    M = M * (np.pi / 180)
    N = 55
    
    #(Meeus recommends 53 for 16-digit precision machine)
    
    ######## SINNOTT code(as published by MEEUS), translated from BASIC by T.S. Kostadinov:
    F = np.sign(M)
    M = np.abs(M) / (2 * np.pi)
    M = (M - int(np.floor(M))) * 2 * np.pi * F
    if M < 0:
        M = M + 2 * np.pi
    
    F = 1
    if M > np.pi:
        F = - 1
        M = 2 * np.pi - M
    
    Eo = np.pi / 2
    D = np.pi / 4
    for j in np.arange(1,N+1).reshape(-1):
        M1 = Eo - e * np.sin(Eo)
        Eo = Eo + D * np.sign(M - M1)
        D = D / 2
    
    Eo = Eo * F
    #############END OF SINNOTT CODE ####################
    
    nu = 2 * np.arctan(np.tan(Eo / 2) * np.sqrt((1 + e) / (1 - e)))
    
    if nu < 0:
        nu = nu + 360
    
    return nu