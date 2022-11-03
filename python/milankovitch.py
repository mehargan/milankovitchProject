import numpy as np
import matplotlib.pyplot as plt
import sys
import datetime as date
import scipy as scipy

    
def mag_func(s):
    tok = []
    for t in s.strip('[]').split(';'):
        tok.append('[' + ','.join(t.strip().split(' ')) + ']')
    b = eval('[' + ','.join(tok) + ']')
    return np.array(b)
    
def daily_insolation(kyear = None,lat = None,day = None,day_type = None): 
    # Usage:
#   Fsw = daily_insolation(kyear,lat,day)
    
    # Optional inputs/outputs:
#   [Fsw, ecc, obliquity, long_perh] = daily_insolation(kyear,lat,day,day_type)
    
    # Description:
#   Computes daily average insolation as a function of day and latitude at
#   any point during the past 5 million years.
    
    # Inputs:
#   kyear:    Thousands of years before 1950 AD (0 to 5000).
#   lat:      Latitude in degrees (-90 to 90).
#   day:      Indicator of time of year; calendar day by default.
#   day_type: Convention for specifying time of year (+/- 1,2) [optional].
#     day_type=1 (default): day input is calendar day (1-365.24), where day 1
#       is January first.  The calendar is referenced to the vernal equinox
#       which always occurs at day 80.
#     day_type=2: day input is solar longitude (0-360 degrees). Solar
#       longitude is the angle of the Earth's orbit measured from spring
#       equinox (21 March). Note that calendar days and solar longitude are
#       not linearly related because, by Kepler's Second Law, Earth's
#       angular velocity varies according to its distance from the sun.
#     If day_type is negative, kyear is taken to be a 3 element array
#       containing [eccentricity, obliquity, and longitude of perihelion].
    
    # Output:
#   Fsw = Daily average solar radiation in W/m^2.
#   Can also output orbital parameters.

    # === Get orbital parameters ===
    if day_type >= 0:
        ecc,epsilon,omega = orbital_parameters(kyear)
    else:
        if len(kyear) != 3:
            print('Error: expect 3-element kyear argument for day_type<0')
            Fsw = nan
            daily_insolation
            return Fsw,ecc,obliquity,long_perh
        ecc = kyear(1)
        epsilon = kyear(2) * np.pi / 180
        omega = kyear(3) * np.pi / 180
    
    # For output of orbital parameters
    obliquity = epsilon * 180 / np.pi
    long_perh = omega * 180 / np.pi
    # === Calculate insolation ===
    lat = lat * np.pi / 180
    
    # lambda (or solar longitude) is the angular distance along Earth's orbit measured from spring equinox (21 March)
    if np.abs(day_type) == 1:
        # estimate lambda from calendar day using an approximation from Berger 1978 section 3
        delta_lambda_m = (day - 80) * 2 * np.pi / 365.2422
        beta = (1 - ecc ** 2) ** (1 / 2)
        lambda_m0 = - 2 * (np.multiply(np.multiply((1 / 2 * ecc + 1 / 8 * ecc ** 3),(1 + beta)),np.sin(- omega)) - np.multiply(1 / 4 * ecc ** 2.0 * (1 / 2 + beta),np.sin(- 2 * omega)) + np.multiply(1 / 8 * ecc ** 3.0 * (1 / 3 + beta),(np.sin(- 3 * omega))))
        lambda_m = lambda_m0 + delta_lambda_m
        lambda_ = lambda_m + np.multiply((2 * ecc - 1 / 4 * ecc ** 3),np.sin(lambda_m - omega)) + (5 / 4) * ecc ** 2.0 * np.sin(2 * (lambda_m - omega)) + (13 / 12) * ecc ** 3.0 * np.sin(3 * (lambda_m - omega))
    else:
        if np.abs(day_type) == 2:
            lambda_ = day * 2 * np.pi / 360
        else:
            print('Error: invalid day_type')
            Fsw = nan
            daily_insolation
            return Fsw,ecc,obliquity,long_perh
    
    So = 1365
    
    delta = np.arcsin(np.multiply(np.sin(epsilon),np.sin(lambda_)))
    
    Ho = np.arccos(np.multiply(- np.tan(lat),np.tan(delta)))
    
    # no sunrise or no sunset: Berger 1978 eqn (8),(9)
    Ho[np.logical_and(np.abs(lat) >= np.pi / 2 - np.abs(delta), np.multiply(lat,delta) > 0)] = np.pi
    Ho[np.logical_and(np.abs(lat) >= np.pi / 2 - np.abs(delta),np.multiply(lat,delta) <= 0)] = 0
    # Insolation: Berger 1978 eq (10)
    Fsw = np.multiply(So / np.pi * (1 + np.multiply(ecc,np.cos(lambda_ - omega))) ** 2 / (1 - ecc ** 2) ** 2,(np.multiply(np.multiply(Ho,np.sin(lat)),np.sin(delta)) + np.multiply(np.multiply(np.cos(lat),np.cos(delta)),np.sin(Ho))))
    # === Calculate orbital parameters ===
    return Fsw
    
    
def orbital_parameters(kyear = None): 
    # === Load orbital parameters (given each kyr for 0-5Mya) ===
    with open('matrix.txt') as f:
        contents = f.read()
    m = mag_func(contents)
    kyear0 = -m[:,0]
    ecc0 =m[:,1]
    # add 180 degrees to omega (see lambda definition, Berger 1978 Appendix)
    omega0 = m[:,2] + 180
    
    omega0 = np.unwrap(omega0 * np.pi / 180) * 180 / np.pi
    
    epsilon0 = m[:,3]
    
    # Interpolate to requested dates
    eccTemp = scipy.interpolate.splrep(kyear0, ecc0, s=0)
    ecc = scipy.interpolate.splev(kyear, eccTemp, der=0)
    # ecc = scipy.interpolate.CubicSpline(kyear0,ecc0,kyear)
    
    omegaTemp = scipy.interpolate.splrep(kyear0,omega0,s=0) 
    omega = scipy.interpolate.splev(kyear, omegaTemp, der=0 ) * np.pi / 180
    epsilonTemp = scipy.interpolate.splrep(kyear0, epsilon0, s=0)
    epsilon = scipy.interpolate.splev(kyear,epsilonTemp,der=0) * np.pi / 180
    return ecc, epsilon, omega

plt.close('all')
# path(path,'/Users/damaya/Desktop/matlab_scripts/')
sys.path.append('/Users/damaya/Desktop/matlab_scripts/')
# path(path,'/Users/damaya/Desktop/matlab_scripts/snctools')
sys.path.append('/Users/damaya/Desktop/matlab_scripts/snctools')

##
# set(0,'DefaultTextFontname','CMU Sans Serif')
# set(0,'DefaultAxesFontName','CMU Sans Serif')
intv = np.arange(1,5000+2,1)
# clear fsw
# c=1;
# for k=intv
#     fsw(c)=daily_insolation(k,65,90,2);
#     c=c+1;
# end
# Fsw = daily_insolation(np.arange(1,5000+2,1),65,90,2)
# plt.plot(intv,Fsw)
# plt.ylabel('Insolation @ 65˚N on the Summer Solstice')
# plt.xlabel('Thousands of years before present', fontweight='bold')
# plt.rc('font', size=8)
# plt.show()
##
#Example 1: Summer solstice insolation at 65 N')
Fsw = daily_insolation(np.arange(0,1000+2),65,90,2)
plt.plot(np.arange(0,1000+2,1),Fsw)
plt.ylabel('Insolation @ 65˚N on the Summer Solstice', fontweight='bold')
plt.xlabel('Thousands of years before present', fontweight='bold')
plt.show()
##
#Example 2: Difference between June 20 (calendar day) and summer solstice insolation at 65 N
Fsw = daily_insolation(np.arange(0,100+2), 65, 90, 2)
plt.ylabel('Insolation @ 65˚N on the Summer Solstice', fontweight='bold')
plt.xlabel('Thousands of years before present', fontweight='bold')
plt.plot(np.arange(0,100+2,1), Fsw)
plt.show()
# june20 = date.toordinal(date(0,6,20) - 1)

# Fsw1 = daily_insolation(np.arange(0,1000+2),65,june20)

# Fsw2 = daily_insolation(np.arange(0,1000+2),65,90,2)

# plt.plot(np.arange(0,1000+1),Fsw2)

#DataIn = np.loadtxt('input.dat')