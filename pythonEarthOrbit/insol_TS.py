import numpy as np
    
def insol_TS(a = None,AU = None,T = None,years = None,dayofyear = None,e = None,obliquity = None,precession = None,Fo = None,lat = None,month = None,day = None): 
    # [sol, chosen_day_sol, annual_mean_sol] = insol_TS(a,AU,T,years,dayofyear, e,obliquity,precession,Fo,lat,month,day)
    
    # Loops through days of year (counting starts Jan. 1, and vernal equinox is fixed to be March 20, at the
# beginning of the day) and latitudes and calculated daily insolation for
# each latitude band and each day, given solutions of the Milankovitch
# orbital parameters for a given year, or demo/arbitrary values.
    
    #See orbit.m for citations and more detailed explanation of input and output
    
    # Dr. Tihomir S. Kostadinov, Roy Gilb, November 2006 - September 2013
    
    if len(varargin) == 0:
        # !!! IMPORTANT!!! The constants and variables below are NOT normally used in the model,
#instead they are passed as arguments by the caller functions of this function.
#These are the default values provided here for testing of this
#function in stand-alone mode.
        AU = 149.5978707
        a = 1.00000261 * AU
        #Sun, Moon, and Planets" (PDF). International Astronomical Union Commission 4: (Ephemerides).
#e = 0.01670236225492288; #Laskar 2004 solution for J2000.0 (year 0  for him)
        obliquity = 0.4090928042223415
        precession = np.pi - 1.796256991128036
        mean_anomaly = 90
        Fo = 1366
        lat = 43
        T = 365.256363
        #T is prescribed a-priori, as Kepler's III Law is not in the model
        years = np.arange(- 500,500+20,20)
        e = np.arange(0.001,0.51+0.01,0.01)
        precession = precession * np.ones((e.shape,e.shape))
        obliquity = obliquity * np.ones((e.shape,e.shape))
        dayofyear = np.array([np.arange(1,365+5,5),365])
    else:
        obliquity = obliquity * (np.pi / 180)
        precession = precession * (np.pi / 180)
    
    years = years
    e = e
    precession = precession
    obliquity = obliquity
    if not (len(years) == len(e) and len(years) == len(precession) and len(years) == len(obliquity)) :
        raise Exception('Time series of years and Milankovitch parameters passed to insol_TS.m are invalid')
    
    dayofequinox = 31 + 28 + 19
    
    if 1 == month:
        ndays = 0
    else:
        if 2 == month:
            ndays = 31
        else:
            if 3 == month:
                ndays = 59
            else:
                if 4 == month:
                    ndays = 90
                else:
                    if 5 == month:
                        ndays = 120
                    else:
                        if 6 == month:
                            ndays = 151
                        else:
                            if 7 == month:
                                ndays = 181
                            else:
                                if 8 == month:
                                    ndays = 212
                                else:
                                    if 9 == month:
                                        ndays = 243
                                    else:
                                        if 10 == month:
                                            ndays = 273
                                        else:
                                            if 11 == month:
                                                ndays = 304
                                            else:
                                                if 12 == month:
                                                    ndays = 334
                                                else:
                                                    raise Exception('')
    
    chosen_day = ndays + day
    
    sol = np.full([len(dayofyear),len(years)],np.nan)
    for dd in np.arange(1,len(dayofyear)+1).reshape(-1):
        for yy in np.arange(1,len(years)+1).reshape(-1):
            time_since_perihelion,__ = keplerian(T,e(yy),precession(yy) * (180 / np.pi))
            days_since_spring = dayofyear(dd) - dayofequinox
            if days_since_spring < 0:
                days_since_spring = 365 + days_since_spring
            #determine mean anomaly of spring equinox - this wil be March 21 always and will depedn on precession's value;
            time_elapsed = np.mod(days_since_spring + time_since_perihelion - 1,T)
            #   starting the whole day count at the time of vernal equinox
            M = 360 * (time_elapsed) / T
            #begin snippet that is common to this script and insol_3d.m & orbit.m
            position_e = (np.pi / 180) * keplerian_inverse(T,e(yy),M)
            r = a * (1 - e(yy) ** 2) / (1 + e(yy) * np.cos(position_e))
            r_vector = np.array([r * np.cos(position_e),r * np.sin(position_e),0])
            tilt_m = generate_rot_m(obliquity(yy),precession(yy))
            k = np.transpose(np.array([0,0,1]))
            kk = tilt_m * k
            sun_declination = (180 / np.pi) * np.arccos(np.dot(r_vector,kk) / (norm(kk) * norm(r_vector))) - 90
            sol[dd,yy],__ = insolation(Fo,r,lat,sun_declination,AU)
    
    chosen_day_sol = sol[chosen_day,:]
    
    annual_mean_sol = mean(sol)
    
    return sol,chosen_day_sol,annual_mean_sol