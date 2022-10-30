import numpy as np
    
def keplerian(T = None,e = None,nu = None): 
    # [t, M] = keplerian(T,e,nu)
# Solves the forward Kepler problem, i.e. given true anomaly, returns time of flight
    
    ########## INPUT ###################
#T - orbital period in arbitrary time units
#e - orbtal eccentricity
#nu - true anomaly in degrees - measured CCW from periapsis
####################################
    
    ######### OUTPUT ##############
#t - period of time elapsed since last periapsis passage (perihelion for Earth)
#    Returned in the units of T. Also called time of flight.
#M - mean anomaly (in radians)
###############################
    
    # Dr. T. S. Kostadinov, Nov. 7 , 2006 - January 2013
    
    ############ References/Works consulted ########################
# Meeus, J. (1998), Astronomical Algorithms, Willmann-Bell, Richmond, VA. (2009 ed.)
# http://scienceworld.wolfram.com/physics/EccentricAnomaly.html
# http://en.wikipedia.org/wiki/Kepler#27s_laws_of_planetary_motion
# http://en.wikipedia.org/wiki/Mean_anomaly
# http://en.wikipedia.org/wiki/Eccentric_anomaly
################################################################
    
    #Treat special cases first, insure that T (instead of 0) is returned if nu==360
#This ensures that orbit.m code that calculates season lengths treats the
#cases when the longitude of perihelion is an integer multiple of pi/2
#radians correctly.
    
    #For nu>360 and negative nu's, return nu to remainder angle only, measured CCW from perihelion.
    if nu > np.logical_or(360,nu) < 0:
        nu = np.mod(nu,360)
    
    if nu == 0:
        t = 0
        M = 0
    else:
        if nu == 180:
            t = T / 2
            M = np.pi
        else:
            if nu == 360:
                t = T
                M = 2 * np.pi
            else:
                E = 2 * np.arctan(tand(nu / 2) * np.sqrt((1 - e) / (1 + e)))
                M = E - e * np.sin(E)
                t = (M * T) / (2 * np.pi)
                if M < 0:
                    M = M + 2 * np.pi
                    t = T + t
    
    return t,M