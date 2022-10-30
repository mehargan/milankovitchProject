import numpy as np
    
def insol_3d(a = None,AU = None,T = None,e = None,obliquity = None,precession = None,Fo = None,dayofyear = None,lats = None): 
    # [sol,daylength] = insol_3d(a,AU,T,e,obliquity,precession,Fo,dayofyear,lats)
    
    #Built June 19-26, 2012, HJA, Blue river, Oregon, using code snippets from orbit.m
# Minor revisions February 2013, moved plotting to main GUI function
# Loops through days of year (counting starts Jan. 1, and vernal equinox is fixed to be March 20, at the
# beginning of the day) and latitudes and calculated daily insolation for
# each latitude band and each day, given solutions of the Milankovitch
# orbital parameters for a given year, or demo/arbitrary values.
    
    #See orbit.m for citations and more detailed explanation of input and output
    
    # Dr. Tihomir S. Kostadinov, Roy Gilb, November 2006 - January 2013
    
    if len(varargin) == 0:
        # !!! IMPORTANT!!! The constants and variables below are NOT normally used in the model,
#instead they are passed as arguments by the caller functions of this function.
#These are the default values provided here for easy use of this
#function in stand-alone mode.
        AU = 149.5978707
        a = 1.00000261 * AU
        #Sun, Moon, and Planets" (PDF). International Astronomical Union Commission 4: (Ephemerides).
        e = 0.01670236225492288
        obliquity = 0.4090928042223415
        precession = np.pi - 1.796256991128036
        mean_anomaly = 90
        Fo = 1366
        dayofyear = np.array([np.arange(1,365+5,5),365])
        lats = np.arange(90,- 90+- 5,- 5)
        T = 365.256363
        #T is prescribed a-priori, as Kepler's III Law is not in the model
    else:
        obliquity = obliquity * (np.pi / 180)
        precession = precession * (np.pi / 180)
    
    dayofequinox = 31 + 28 + 19
    
    time_since_perihelion,mean_anomaly_equinox = keplerian(T,e,precession * (180 / np.pi))
    M = NaN * np.ones((dayofyear.shape,dayofyear.shape))
    for i in np.arange(1,len(dayofyear)+1).reshape(-1):
        days_since_spring = dayofyear(i) - dayofequinox
        if days_since_spring < 0:
            days_since_spring = 365 + days_since_spring
        #determine mean anomaly of spring equinox - this wil be March 21 always and will depedn on precession's value;
        time_elapsed = np.mod(days_since_spring + time_since_perihelion - 1,T)
        #   starting the whole day count at the time of vernal equinox
        M[i] = 360 * (time_elapsed) / T
    
    #Preallocate arrays for speed
    sol = np.full([len(lats),len(M)],np.nan)
    daylength = sol
    for dd in np.arange(1,len(M)+1).reshape(-1):
        for ss in np.arange(1,len(lats)+1).reshape(-1):
            position_e = (np.pi / 180) * keplerian_inverse(T,e,M(dd))
            r = a * (1 - e ** 2) / (1 + e * np.cos(position_e))
            r_vector = np.array([r * np.cos(position_e),r * np.sin(position_e),0])
            tilt_m = generate_rot_m(obliquity,precession)
            k = np.transpose(np.array([0,0,1]))
            kk = tilt_m * k
            sun_declination = (180 / np.pi) * np.arccos(np.dot(r_vector,kk) / (norm(kk) * norm(r_vector))) - 90
            sol[ss,dd],daylength[ss,dd] = insolation(Fo,r,lats(ss),sun_declination,AU)
    
    return sol,daylength