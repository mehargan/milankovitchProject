import numpy as np
import matplotlib.pyplot as plt
import numpy.matlib
import generate_rot_m
import Berger_orbpar
import Earth_orbit_v2_1
import getLasker
import insol_3d
import insol_TS
import insolation
import keplerian
from keplerian_inverse import keplerian_inverse
# from symbol import arglist
    
def orbit(a = None,AU = None,T = None,e = None,obliquity = None,precession = None,mean_anomaly = None,Fo = None,latitude = None): 
    #[r_vec_length, period,sun_dec, sol,season_length, daylength, true_anomaly] = orbit(a,AU,T,e,obliquity,precession,mean_anomaly, Fo, latitude)
# Plots the orbit in 3D, given the orbital parameters. Also returns useful derived variables (see below)
    
    ########## INPUT ###################
#a - semi-major axis of Earth's orbit in millions of km
#AU - the length of the astronomical unit for distance in millions of km
#T - true anomaly in degrees - measured CCW from periapsis
#e - eccentricity of Earth's orbit (dimensionless)
#obliquity - obliquity of Earth's axis in degrees
#precession - Precession angle, in degrees, expressed here internally in degrees as
#     "precession = 180 - (longitude of perihelion)", where longitude of perihelion is defined
#     as in Berger et al. (2010) and represents the angle from the direction of fall equinox to the direction of perihelion,
#     measured CCW in the plane of the ecliptic. Users of the model enter the longitude of perihelion and the
#     angle called precession here is used only internally for this function.
#     The longitude of perihelion is denoted omega_tilde in Berger et al. (2010), Figure 1;
#     The direction of fall equinox means the direction of the radius-vector of Earth when it is in fall equinox, i.e. around Sept. 22 in the contemporary Gregorian calendar.
#     Also note that the strict definition of longitude of perihelion for a generic orbit is more involved, as it is the sum of two angles in different planes.
#     For the purposes of this model, the defintion in Berger et al. (2010) is relevant.
#mean_anomaly - mean anomaly of the Earth for a given date/time, in degrees. Measured CCW from perihelion.
#Fo - solar "constant" in W/m^2, i.e. total (full spectrum-integrated) solar irradiance (TSI),
#    received at exactly 1 AU distance from the Sun ata surface of 1 m^2 perpendicular to the rays
#latitude - Latitude on Earth in degrees. By default we mean geographic
#   latitude here.
####################################
    
    ######### OUTPUT ##############
#r_vec_length - length of the radius-vector of Earth, in the units of a
#period - oribal period in days (just returns the input T without manipulation)
#sun_dec - geocentric declination of the Sun in degrees
#sol - insolation at the TOA averaged over 24 hrs, in the units of Fo
#season_length - length/duration of seasons in days
#daylength - duration of daylight in hours
#true_anomaly - true anolamy of Earth in degrees
###############################
    
    ## Dr. T. S. Kostadinov, November 2006 - November 2013
    
    ############ References/Works consulted ########################
# Meeus, J. (1998), Astronomical Algorithms, Willmann-Bell, Richmond, VA. (2009 ed.)
# http://scienceworld.wolfram.com/physics/EccentricAnomaly.html
# http://en.wikipedia.org/wiki/Kepler#27s_laws_of_planetary_motion
# http://en.wikipedia.org/wiki/Mean_anomaly
# http://en.wikipedia.org/wiki/Eccentric_anomaly
# http://en.wikipedia.org/wiki/Ellipse
# MATLAB(r) Documentation
# Other references cited in the model accompaying paper and the rest of the
#   mode m-files.
################################################################
    if (True):
        # #Define constants:
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
        latitude = 43
        T = 365.256363
        #T is prescribed a-priori, as Kepler's III Law is not in the model
    else:
        obliquity = obliquity * (np.pi / 180)
        precession = precession * (np.pi / 180)
    
    true_anomaly = keplerian_inverse(T,e,mean_anomaly)
    position_e = true_anomaly * np.pi / 180
    
    b = np.sqrt(a ** 2 * (1 - e ** 2))
    c = e * a
    
    sun_shift = np.array([- c,0,0])
    
    R = 0.15 * a
    
    R_sun = 1 / 3 * R
    
    #radius-vectors for the directions of the start of the four seasons:
    position = precession
    r = a * (1 - e ** 2) / (1 + e * np.cos(position))
    r_spring = np.array([r * np.cos(position),r * np.sin(position),0])
    position = precession + np.pi / 2
    r = a * (1 - e ** 2) / (1 + e * np.cos(position))
    r_summer = np.array([r * np.cos(position),r * np.sin(position),0])
    position = precession + np.pi
    r = a * (1 - e ** 2) / (1 + e * np.cos(position))
    r_fall = np.array([r * np.cos(position),r * np.sin(position),0])
    position = precession + 3 * np.pi / 2
    r = a * (1 - e ** 2) / (1 + e * np.cos(position))
    r_winter = np.array([r * np.cos(position),r * np.sin(position),0])
    #Radius vector of the Earth
    r = a * (1 - e ** 2) / (1 + e * np.cos(position_e))
    
    r_vector = np.array([r * np.cos(position_e),r * np.sin(position_e),0])
    #Parameterize and plot orbital ellipse
    t = np.arange(0,2 * np.pi+0.01,0.01)
    t[-1] = 2 * np.pi
    
    plt.plot(a * np.cos(t) + sun_shift(1),b * np.sin(t) + sun_shift(2),np.zeros((t.shape,t.shape)) + sun_shift(3),'b','LineWidth',1)
    
    #Plot orbital axes:
    major = np.array([1,0,0])
    s = np.arange(- a,a+0.01,0.01)
    plt.plot(s * major(1) + sun_shift(1),s * major(2) + sun_shift(2),s * major(3) + sun_shift(3),'r-','LineWidth',1)
    minor = np.array([0,1,0])
    s = np.arange(- b,b+0.01,0.01)
    plt.plot(s * minor(1) + sun_shift(1),s * minor(2) + sun_shift(2),s * minor(3) + sun_shift(3),'r-','LineWidth',1)
    plt.grid(color='r', linestyle='-', linewidth=2)
    plt.axis('square')
    s = np.amax(np.array([a,b])) + c
    plt.axis(np.array([- s,s,- s,s,- s,s]))
    #Parameterize Earth's sphere for 3D plotting:
    theta,phi = np.meshgrid(np.array([np.arange(0,2 * np.pi+0.1,0.1),2 * np.pi]),np.array([np.arange(0,np.pi+0.1,0.1),np.pi]))
    x = np.multiply(R * np.sin(phi),np.cos(theta))
    y = np.multiply(R * np.sin(phi),np.sin(theta))
    z = R * np.cos(phi)
    #Compute a rotation matrix about a vector in the xy plane (plane of the ecplitic),
#whose orinettaion is determined by the precession angle; angle of rotation around that vector's
#direction will be equal to the obliquity. That way the Earth's equatorial plane ends up at an
#angle equal to the obliquity with respect to the ecliptic plane.
    tilt_m = generate_rot_m(obliquity,precession)
    #Rotate Earth AND translate it
    xx = np.zeros((x.shape,x.shape))
    yy = np.zeros((y.shape,y.shape))
    zz = np.zeros((z.shape,z.shape))
    for i in np.arange(1,x.shape[1-1]+1).reshape(-1):
        for j in np.arange(1,x.shape[2-1]+1).reshape(-1):
            new_vec = tilt_m * np.array([[x(i,j)],[y(i,j)],[z(i,j)]])
            xx[i,j] = new_vec(1) + r_vector(1)
            yy[i,j] = new_vec(2) + r_vector(2)
            zz[i,j] = new_vec(3) + r_vector(3)
    
    #Actually plot sphere of Earth (!!!NOT to scale!!!)
    plt.colormap('jet')
    h = np.meshgrid(xx,yy,zz,np.matlib.repmat((180 / np.pi) * (np.pi / 2 - phi[:,1]),1,theta.shape[2-1]))
    
    set(h,'EdgeColor','interp')
    set(h,'FaceAlpha',0.3)
    #Rotate i,j,k reference frame for Earth AND translate it to is proper spot on ORBIT
    i = np.transpose(np.array([R,0,0]))
    j = np.transpose(np.array([0,R,0]))
    k = np.transpose(np.array([0,0,R * 1.5]))
    ii = tilt_m * i
    jj = tilt_m * j
    kk = tilt_m * k
    s = np.arange(- 1,1+0.01,0.01)
    #Plot Earth's reference frame
    plt.plot(s * ii(1) + r_vector(1),s * ii(2) + r_vector(2),s * ii(3) + r_vector(3),'k.-')
    plt.plot(s * jj(1) + r_vector(1),s * jj(2) + r_vector(2),s * jj(3) + r_vector(3),'k.-')
    plt.plot(s * kk(1) + r_vector(1),s * kk(2) + r_vector(2),s * kk(3) + r_vector(3),'k.-')
    #plot Equator of Earth as a parameterized circle:
    thetaEq = np.array([np.arange(0,2 * np.pi+0.1,0.1),2 * np.pi])
    xeq = R * np.cos(thetaEq)
    yeq = R * np.sin(thetaEq)
    zeq = np.zeros((thetaEq.shape,thetaEq.shape))
    #tilt the same way we tilted Earth's surface and coordiante system:
    xxeq = np.zeros((xeq.shape,xeq.shape))
    yyeq = xxeq
    zzeq = xxeq
    for eqc in np.arange(1,xeq.shape[2-1]+1).reshape(-1):
        eqvec = tilt_m * np.array([[xeq(eqc)],[yeq(eqc)],[zeq(eqc)]])
        xxeq[eqc] = eqvec(1) + r_vector(1)
        yyeq[eqc] = eqvec(2) + r_vector(2)
        zzeq[eqc] = eqvec(3) + r_vector(3)
    
    plt.plot(xxeq,yyeq,zzeq,'k','LineWidth',1.5)
    plt.axis('square')
    #Plot Earth's radius-vector
    h = plt.plot(np.array([0,r_vector(1)]),np.array([0,r_vector(2)]),np.array([0,r_vector(3)]))
    set(h,'LineStyle','-','Color','g','LineWidth',2)
    #Plot radius-vectors corresponding to the seasons (directions of solstices & equinoxes)
    h = plt.plot(np.array([0,r_spring(1)]),np.array([0,r_spring(2)]),np.array([0,r_spring(3)]))
    set(h,'LineStyle','-','Color','k')
    h = plt.plot(np.array([0,r_summer(1)]),np.array([0,r_summer(2)]),np.array([0,r_summer(3)]))
    set(h,'LineStyle','-','Color','k')
    h = plt.plot(np.array([0,r_fall(1)]),np.array([0,r_fall(2)]),np.array([0,r_fall(3)]))
    set(h,'LineStyle','-','Color','k')
    h = plt.plot(np.array([0,r_winter(1)]),np.array([0,r_winter(2)]),np.array([0,r_winter(3)]))
    set(h,'LineStyle','-','Color','k')
    #Plot axes of fixed heliocentric coordinate system:
    h = plt.plot(np.array([0,R_sun]),np.array([0,0]),np.array([0,0]))
    h2 = plt.plot(np.array([0,0]),np.array([0,R_sun]),np.array([0,0]))
    h3 = plt.plot(np.array([0,0]),np.array([0,0]),np.array([0,R_sun]))
    set(np.array([h,h2,h3]),'LineStyle','-','Color','k')
    #Parameterize and plot sphere of Sun (NOT to scale!!!)
    theta_sun,phi_sun = np.meshgrid(np.array([np.arange(0,2 * np.pi+0.1,0.1),2 * np.pi]),np.array([np.arange(0,np.pi+0.1,0.1),np.pi]))
    x_sun = np.multiply(R_sun * np.sin(phi_sun),np.cos(theta_sun))
    y_sun = np.multiply(R_sun * np.sin(phi_sun),np.sin(theta_sun))
    z_sun = R_sun * np.cos(phi_sun)
    plt.colormap('jet')
    hsun = surf(x_sun,y_sun,z_sun,35 * np.ones((z_sun.shape,z_sun.shape)))
    set(hsun,'FaceColor','interp','EdgeColor','none')
    set(hsun,'FaceAlpha',0.4)
    #Label location of the other focus of the orbital ellipse
    text(- 2 * c,0,0,'x')
    
    #Label seasons and perihelion and aphelion:
    text(1.1 * r_spring(1),1.1 * r_spring(2),1.1 * r_spring(3),'NH spring','FontSize',9,'FontWeight','bold')
    text(1.1 * r_summer(1),1.1 * r_summer(2),1.1 * r_summer(3),'NH summer','FontSize',9,'FontWeight','bold')
    text(1.1 * r_fall(1),1.1 * r_fall(2),1.1 * r_fall(3),'NH fall','FontSize',9,'FontWeight','bold')
    text(1.1 * r_winter(1),1.1 * r_winter(2),1.1 * r_winter(3),'NH winter','FontSize',9,'FontWeight','bold')
    text(1.1 * (a - c),0,0,'perihelion','FontSize',10,'FontWeight','bold','FontAngle','italic','Color','red')
    #North Pole of Earth labeled for orientation
    text(1.2 * kk(1) + r_vector(1),1.2 * kk(2) + r_vector(2),1.2 * kk(3) + r_vector(3),'N','FontSize',10,'FontWeight','bold')
    # # For testing purposes, calculation of angle between the plane of the ecliptic and the plane formed by the Earth's axis of rotation and its radius-vector:
# # (calculated using the angle between the normals to these planes)
# # This is the absolute value of the declination of the Sun:
# # Tolerance levels for these angles will need to be considered, for example abs(diff))<=1e-12;
# # Commented out as it is not used in the operational version of the model
# ang = (180/pi)*acos(dot(cross(kk,r_vector), k)/(norm(k)*norm(cross(kk,r_vector))));
# issolstice = (abs(90-ang)==0);
# isequinox = (abs(90-ang)==obliquity*(180/pi));
    
    #Geocentric solar declination is the angle formed between the radius-vector of Earth and the northward/positive direction of Earth's axis of rotation
    sun_declination = (180 / np.pi) * np.arccos(np.dot(r_vector,kk) / (norm(kk) * norm(r_vector))) - 90
    #Lightly and transparently color (fill in) the part of the orbit Earth has swept since perihelion:
    sweep = np.arange(0,position_e+0.01,0.01)
    for i in np.arange(2,len(sweep)+1).reshape(-1):
        r = a * (1 - e ** 2) / (1 + e * np.cos(sweep(i - 1)))
        r2 = a * (1 - e ** 2) / (1 + e * np.cos(sweep(i)))
        #Radius-vectors
        rvec1 = np.array([r * np.cos(sweep(i - 1)),r * np.sin(sweep(i - 1)),0])
        rvec2 = np.array([r2 * np.cos(sweep(i)),r2 * np.sin(sweep(i)),0])
        h = fill(np.array([0,rvec1(1),rvec2(1)]),np.array([0,rvec1(2),rvec2(2)]),'g')
        set(h,'EdgeAlpha',0)
        set(h,'FaceAlpha',0.2)
    
    #fill in last patch - between last polygon and Earth' readius-vector itself
    r = a * (1 - e ** 2) / (1 + e * np.cos(sweep(end())))
    rvec1 = np.array([r * np.cos(sweep(end())),r * np.sin(sweep(end())),0])
    rvec2 = r_vector
    h = fill(np.array([0,rvec1(1),rvec2(1)]),np.array([0,rvec1(2),rvec2(2)]),'g')
    set(h,'EdgeAlpha',0)
    set(h,'FaceAlpha',0.2)
    ###################################################
# Computation of the length of the seasons ########
###################################################
#Strict & non-strict inequalities work below b/c keplerian.m returns T when
#true anonmlay is 360 degrees (as opposed to returning 0 for time of flight)
#Logic here will break down if this functionality of keplerian is not such.
    precession = precession * 180 / np.pi
    if precession <= 90:
        t1,ma = keplerian(T,e,precession)
        t2,ma = keplerian(T,e,270 + precession)
        t2 = T - t2
        winter_len = t1 + t2
        spring_len = keplerian(T,e,precession + 90) - t1
        summer_len = keplerian(T,e,precession + 180) - spring_len - t1
        fall_len = keplerian(T,e,precession + 270) - summer_len - spring_len - t1
        #check for consistency
#err_len = spring_len + summer_len + fall_len + winter_len - T;
    else:
        if precession > 90 and precession <= 180:
            t1,ma = keplerian(T,e,precession - 90)
            t2,ma = keplerian(T,e,180 + precession)
            t2 = T - t2
            fall_len = t1 + t2
            winter_len = keplerian(T,e,precession) - t1
            spring_len = keplerian(T,e,precession + 90) - winter_len - t1
            summer_len = keplerian(T,e,precession + 180) - spring_len - winter_len - t1
        else:
            if precession > 180 and precession <= 270:
                t1,ma = keplerian(T,e,precession - 180)
                t2,ma = keplerian(T,e,90 + precession)
                t2 = T - t2
                summer_len = t1 + t2
                fall_len = keplerian(T,e,precession - 90) - t1
                winter_len = keplerian(T,e,precession) - fall_len - t1
                spring_len = keplerian(T,e,precession + 90) - winter_len - fall_len - t1
            else:
                t1,ma = keplerian(T,e,precession - 270)
                t2,ma = keplerian(T,e,precession)
                t2 = T - t2
                spring_len = t1 + t2
                summer_len = keplerian(T,e,precession - 180) - t1
                fall_len = keplerian(T,e,precession - 90) - summer_len - t1
                winter_len = keplerian(T,e,precession) - fall_len - summer_len - t1
    
#########################################
#Outputs:
#########################################
    plt.show()
    sun_dec = sun_declination
    period = T
    
    r_vec_length = r
    sol,daylength = insolation(Fo,r_vec_length,latitude,sun_dec,AU)
    season_length = np.array([spring_len,summer_len,fall_len,winter_len])
    return r_vec_length,period,sun_dec,sol,season_length,daylength,true_anomaly

orbit(a = None,AU = None,T = None,e = None,obliquity = None,precession = None,mean_anomaly = None,Fo = None,latitude = None)