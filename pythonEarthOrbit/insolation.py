import numpy as np
    
def insolation(Fo = None,r = None,phi = None,delta = None,AU = None): 
    # [F_bar,daylength ] = insolation(Fo,r,phi,delta,AU)
# Calculates insolation averaged over 24 hrs centered on local solar noon, given the inputs as decsribed below
    
    ########## INPUT ###################
#Fo - solar "constant" (the total solar irradiance at 1 AU at the TOA), in W/m^2  (but can be any unit)
#r - length of radius vector of Earth in the same units af those of AU, e.g. millions of km
#phi - geographic latitude on Earth, in degrees
#delta - solar declination in degrees
#AU - the length of 1 AU (e.g. in millions of km), needs to be in the same units as r
####################################
    
    ######### OUTPUT ##############
#F_bar - insolation at the top of the atmosphere (TOA), averaged over 24 hrs centered on local solar noon;
#   It will be given in the units of Fo, usually W/m^2
#daylength - length of day (meaning the duartion of daylight hours) in hours
###############################
    
    ## Dr. T. S. Kostadinov, May 2007 - January 2013
    
    ############ References/Works consulted ########################
################################################################
    
    delta = delta * (np.pi / 180)
    phi = phi * (np.pi / 180)
    #Check if we are in the special regions where the Sun never rises
#or sets and deal with these special cases in a different way.
#Compute daylength
    
    flag = 0
    
    if delta >= 0:
        if phi <= delta - np.pi / 2:
            daylength = 0
            F_bar = 0
            flag = 0
        else:
            if phi >= np.pi / 2 - delta:
                daylength = 24
                t = np.arange(0,2 * np.pi+0.001,0.001)
                flag = 1
            else:
                flag = 1
                daylength = (24 / np.pi) * np.arccos(- np.tan(phi) * np.tan(delta))
                t_sunset = np.arccos(- np.tan(delta) * np.tan(phi))
                t = np.array([np.arange(0,t_sunset+0.001,0.001)])
    else:
        if delta < 0:
            if phi >= delta + np.pi / 2:
                daylength = 0
                F_bar = 0
                flag = 0
            else:
                if phi <= - np.pi / 2 - delta:
                    daylength = 24
                    t = np.arange(0,2 * np.pi+0.001,0.001)
                    flag = 1
                else:
                    flag = 1
                    daylength = (24 / np.pi) * np.arccos(- np.tan(phi) * np.tan(delta))
                    #in radians, hour angle of sunset (measurement starts from solar noon- i.e. south)!
                    t_sunset = np.arccos(- np.tan(delta) * np.tan(phi))
                    t = np.array([np.arange(0,t_sunset+0.001,0.001)])
    
    if flag == 1:
        #correction for Sun-Earth distance:
        For = Fo * ((AU / r) ** 2)
        #Compute the average value of the sin(h) function
#Because of the symmetry b/n sunrise and sunset, this is the average value
#from sunrise to sunset as well, although the computed value is from solar noon to sunset only
        sinh_ave = (1 / t(end())) * trapz(t,np.sin(delta) * np.sin(phi) + np.cos(delta) * np.cos(phi) * np.cos(t))
        F_bar = For * sinh_ave
        F_bar = F_bar * (daylength / 24)
    
    return F_bar,daylength