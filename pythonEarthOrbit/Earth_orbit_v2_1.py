import numpy as np
import matplotlib.pyplot as plt
import os
    
def Earth_orbit_v2_1(varargin = None): 
    # EARTH_ORBIT_V2_1 M-file for Earth_orbit_v2_1.fig
#   This is the function that raises the main model GUI and provides all model controls.
#   Normally, this is the only function that needs to be called on the command propmt in order
#   to run the model.  For details, see the model publication and the
#   ReadMe.txt file.  The code in the file below is a mix of MATLAB(r)
#   generated code and model author generated code.  Comments are provided
#   where needed. The external functions that are called are necessary for
#   the model to run and are also commented. T.K., Sept. 30, 2013.
    
    
    #      EARTH_ORBIT_V2_1, by itself, creates a new EARTH_ORBIT_V2_1 or raises the existing
#      singleton*.
    
    #      H = EARTH_ORBIT_V2_1 returns the handle to a new EARTH_ORBIT_V2_1 or the handle to
#      the existing singleton*.
    
    #      EARTH_ORBIT_V2_1('CALLBACK',hObject,eventData,handles,...) calls the
#      local
#      function named CALLBACK in EARTH_ORBIT_V2_1.M with the given input arguments.
    
    #      EARTH_ORBIT_V2_1('Property','Value',...) creates a new EARTH_ORBIT_V2_1 or raises
#      the existing singleton*.  Starting from the left, property value pairs are
#      applied to the GUI before orbit_gui_OpeningFunction gets called.  An
#      unrecognized property name or invalid value makes property application
#      stop.  All inputs are passed to Earth_orbit_v2_1_OpeningFcn via varargin.
    
    #      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
#      instance to run (singleton)".
    
    # See also: GUIDE, GUIDATA, GUIHANDLES
    
    # Edit the above text to modify the response to help Earth_orbit_v2_1
    
    # Last Modified by GUIDE v2.5 18-Mar-2014 20:47:15
    
    # Begin initialization code - DO NOT EDIT
    gui_Singleton = 1
    gui_State = struct('gui_Name',mfilename,'gui_Singleton',gui_Singleton,'gui_OpeningFcn',Earth_orbit_v2_1_OpeningFcn,'gui_OutputFcn',Earth_orbit_v2_1_OutputFcn,'gui_LayoutFcn',[],'gui_Callback',[])
    if len(varargin) and ischar(varargin[0]):
        gui_State.gui_Callback = str2func(varargin[0])
    
    if nargout:
        varargout[np.arange[1,nargout+1]] = gui_mainfcn(gui_State,varargin[:])
    else:
        gui_mainfcn(gui_State,varargin[:])
    
    # End initialization code - DO NOT EDIT
    
    # --- Executes just before Earth_orbit_v2_1 is made visible.
    
def Earth_orbit_v2_1_OpeningFcn(hObject = None,eventdata = None,handles = None,varargin = None): 
    # This function has no output args, see OutputFcn.
# hObject    handle to figure
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
# varargin   command line arguments to Earth_orbit_v2_1 (see VARARGIN)
    
    # Choose default command line output for Earth_orbit_v2_1
    handles.output = hObject
    # Update handles structure
    guidata(hObject,handles)
    initialize_gui(hObject,handles,False)
    # UIWAIT makes Earth_orbit_v2_1 wait for user response (see UIRESUME)
# uiwait(handles.main_panel);
    
    # --- Outputs from this function are returned to the command line.
    
def Earth_orbit_v2_1_OutputFcn(hObject = None,eventdata = None,handles = None): 
    # varargout  cell array for returning output args (see VARARGOUT);
# hObject    handle to figure
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Get default command line output from handles structure
    varargout[0] = handles.output
    # --- Executes during object creation, after setting all properties.
    
def e_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to e (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: edit controls usually have a white background, change
#       'usewhitebg' to 0 to use default.  See ISPC and COMPUTER.
    usewhitebg = 1
    if usewhitebg:
        set(hObject,'BackgroundColor','white')
    else:
        set(hObject,'BackgroundColor',get(0,'defaultUicontrolBackgroundColor'))
    
    
def e_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to e (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'String') returns contents of e as text
#        str2double(get(hObject,'String')) returns contents of e as a double
    e = str2double(get(hObject,'String'))
    if np.logical_or(np.isnan(e),not (e >= np.logical_and(get(handles.e_slider,'Min'),e) <= get(handles.e_slider,'Max')) ):
        e = handles.data.e
        set(hObject,'String',e)
        errordlg(np.array(['Input must be a number b/n ',num2str(get(handles.e_slider,'Min')),' and ',num2str(get(handles.e_slider,'Max'))]),'Error')
    
    # Save the new e value
    handles.data.e = e
    #update slider
    set(handles.e_slider,'Value',e)
    guidata(hObject,handles)
    # --- Executes on button press in calculate.
    
def calculate_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to calculate (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
#cla;
    try:
        clf(1)
    finally:
        pass
    
    ecc = handles.data.e
    obliq = handles.data.obliquity
    omega_bar = handles.data.precession
    prec_for_orbit = 180 - omega_bar
    
    if prec_for_orbit < 0:
        #messes up some things within orbit.m, particularly the season length calculations
        prec_for_orbit = 360 + prec_for_orbit
    
    omega = 180 + omega_bar
    
    if omega > 360:
        omega = omega - 360
    
    if handles.data.cal_mode == 2:
        perihelion_dayofyear = 2
        if 1 == handles.data.month:
            ndays = 0
        else:
            if 2 == handles.data.month:
                ndays = 31
            else:
                if 3 == handles.data.month:
                    ndays = 59
                else:
                    if 4 == handles.data.month:
                        ndays = 90
                    else:
                        if 5 == handles.data.month:
                            ndays = 120
                        else:
                            if 6 == handles.data.month:
                                ndays = 151
                            else:
                                if 7 == handles.data.month:
                                    ndays = 181
                                else:
                                    if 8 == handles.data.month:
                                        ndays = 212
                                    else:
                                        if 9 == handles.data.month:
                                            ndays = 243
                                        else:
                                            if 10 == handles.data.month:
                                                ndays = 273
                                            else:
                                                if 11 == handles.data.month:
                                                    ndays = 304
                                                else:
                                                    if 12 == handles.data.month:
                                                        ndays = 334
                                                    else:
                                                        raise Exception('')
        dayofyear = ndays + handles.data.day - 1
        #there have passed 31 das of teh year, on Dec. 1 - 334, and on Dec. 31 - 364!
#Setting perihelion on the date of Jan. 3, 00 Z, this means it occurs after
#two days have passed since Jan. 1, 00 Z.
        time_elapsed = dayofyear - perihelion_dayofyear
        if time_elapsed < 0:
            time_elapsed = handles.data.period + time_elapsed
        M = 360 * (time_elapsed / handles.data.period)
        mean_solar = - 999
    else:
        if handles.data.cal_mode == 1:
            #compute M for a calendar that is equinox-fixed on March 21 at 0 Z
            dayofequinox = 31 + 28 + 19
            if 1 == handles.data.month:
                ndays = 0
            else:
                if 2 == handles.data.month:
                    ndays = 31
                else:
                    if 3 == handles.data.month:
                        ndays = 59
                    else:
                        if 4 == handles.data.month:
                            ndays = 90
                        else:
                            if 5 == handles.data.month:
                                ndays = 120
                            else:
                                if 6 == handles.data.month:
                                    ndays = 151
                                else:
                                    if 7 == handles.data.month:
                                        ndays = 181
                                    else:
                                        if 8 == handles.data.month:
                                            ndays = 212
                                        else:
                                            if 9 == handles.data.month:
                                                ndays = 243
                                            else:
                                                if 10 == handles.data.month:
                                                    ndays = 273
                                                else:
                                                    if 11 == handles.data.month:
                                                        ndays = 304
                                                    else:
                                                        if 12 == handles.data.month:
                                                            ndays = 334
                                                        else:
                                                            raise Exception('')
            dayofyear = ndays + handles.data.day - 1
            days_since_spring = dayofyear - dayofequinox
            if days_since_spring < 0:
                days_since_spring = 365 + days_since_spring
            mean_solar = 360 * (days_since_spring / handles.data.period)
            #determine mean anomaly of spring equinox - this will be March 20 always and will depend on precession's value;
            time_since_perihelion,mean_anomaly_equinox = keplerian(handles.data.period,ecc,prec_for_orbit)
            time_elapsed = np.mod(days_since_spring + time_since_perihelion,handles.data.period)
            #starting the whole day count at the time of vernal equinox
            M = 360 * (time_elapsed / handles.data.period)
        else:
            raise Exception('Unknown calendar mode. Specify equinox-fixed or perihelion-fixed')
    
    #ready to call orbit function
    f1h = plt.figure(1)
    clf
    set(f1h,'Name','3D Orbital Configuration','NumberTitle','off','Units','normalized','OuterPosition',np.array([0.3,0.15,0.7,0.85]))
    r_vec_length,period,sun_dec,sol,season_length,daylength,true_anomaly = orbit(handles.data.sm_axis,handles.data.AU,handles.data.period,ecc,obliq,prec_for_orbit,M,handles.data.Fo,handles.data.latitude)
    plt.axis('off')
    ###########################
#### The following line was added May 20, 2015 to fix clipping issues that
#### occured with Matlab R2014 and later. This line is NOT in the GMD
#### publication!!!
    set(gca,'Clipping','off')
    ############################################################
############################################################
    
    #Calculate true solar longitude:
    true_solar = np.mod(true_anomaly + omega,360)
    
    #Write output to the GUI outputs box
    set(handles.sun_dec,'String',sprintf('%5.3f',sun_dec))
    set(handles.insolation,'String',sprintf('%8.4f',sol))
    set(handles.daylength,'String',sprintf('%5.2f',daylength))
    set(handles.rvec_length,'String',sprintf('%12.9f',r_vec_length))
    set(handles.distance_au,'String',sprintf('%12.9f',r_vec_length / handles.data.AU))
    set(handles.spring_len,'String',sprintf('%5.2f',season_length(1)))
    set(handles.summer_len,'String',sprintf('%5.2f',season_length(2)))
    set(handles.fall_len,'String',sprintf('%5.2f',season_length(3)))
    set(handles.winter_len,'String',sprintf('%5.2f',season_length(4)))
    #Solar Longitudes
    set(handles.mean_solar_text,'String',sprintf('%7.4f',mean_solar))
    set(handles.trueSolar_text,'String',sprintf('%7.4f',true_solar))
    set(handles.e,'String',sprintf('%8.7f',ecc))
    set(handles.obliquity,'String',sprintf('%6.4f',obliq))
    set(handles.precession,'String',sprintf('%6.4f',omega_bar))
    set(handles.lon_perihelion,'String',sprintf('%3.2f',omega))
    guidata(hObject,handles)
    # --------------------------------------------------------------------
    
def initialize_gui(fig_handle = None,handles = None,isreset = None): 
    #Default values
    handles.data.AU = 149.5978707
    
    handles.data.sm_axis = 1.00000261 * handles.data.AU
    #(Standish, E. Myles; Williams, James C.. "Orbital Ephemerides of the
#Sun, Moon, and Planets" (PDF). International Astronomical Union Commission 4: (Ephemerides). Retrieved 2010-04-03. See table 8.10.2.
    handles.data.e = 0.01670236225492288
    
    handles.data.obliquity = 0.4090928042223415 * (180 / np.pi)
    
    handles.data.precession = 1.796256991128036 * (180 / np.pi)
    
    handles.data.latitude = 43
    
    #set initial year values
    handles.data.myear = 0
    handles.data.laskar_year_text = 0
    handles.data.period = 365.256363
    
    handles.data.Fo = 1366
    
    #Initialize date of model to current date taken from computer clock
    handles.data.month = str2double(datestr(now,5))
    handles.data.day = str2double(datestr(now,7))
    handles.data.cal_mode = 1
    
    handles.data.solutions_mode = 0
    
    handles.data.start_year_text = - 200
    handles.data.end_year_text = 200
    handles.data.save_insol_data = 0
    
    #Set initial field values
    set(handles.sm_axis,'String',sprintf('%12.9f',handles.data.sm_axis))
    set(handles.myear,'String',handles.data.myear)
    set(handles.laskar_year_text,'String',handles.data.laskar_year_text)
    set(handles.e,'String',handles.data.e)
    set(handles.obliquity,'String',handles.data.obliquity)
    set(handles.precession,'String',handles.data.precession)
    set(handles.latitude,'String',handles.data.latitude)
    set(handles.period,'String',sprintf('%12.7f',handles.data.period))
    set(handles.Fo,'String',handles.data.Fo)
    set(handles.month,'Value',str2double(datestr(now,5)))
    set(handles.day,'Value',str2double(datestr(now,7)))
    set(handles.calendar_mode,'Value',1)
    set(handles.start_year_text,'String',handles.data.start_year_text)
    set(handles.end_year_text,'String',handles.data.end_year_text)
    set(handles.saving_data_checkbox,'Value',get(handles.saving_data_checkbox,'Min'))
    
    #Set sliders properties
    set(handles.e_slider,'Min',0.005)
    set(handles.e_slider,'Max',0.9)
    set(handles.e_slider,'Value',handles.data.e)
    set(handles.obliquity_slider,'Min',0)
    set(handles.obliquity_slider,'Max',60)
    set(handles.obliquity_slider,'Value',handles.data.obliquity)
    set(handles.precession_slider,'Min',0)
    set(handles.precession_slider,'Max',360)
    set(handles.precession_slider,'Value',handles.data.precession)
    #Set values for year slider
    set(handles.year_slider,'Min',- 1000)
    
    set(handles.year_slider,'Max',1000)
    
    set(handles.year_slider,'Value',handles.data.myear)
    set(handles.laskar_year_slider,'Min',- 101000)
    
    set(handles.laskar_year_slider,'Max',21000)
    
    set(handles.laskar_year_slider,'Value',handles.data.laskar_year_text)
    #Disable year text box and slider for Berger and Laskar- not part of the default demo
    set(handles.year_slider,'Enable','off')
    set(handles.myear,'Enable','off')
    #Disable laskar slider and text - demo mode is default
    set(handles.laskar_year_slider,'Enable','off')
    set(handles.laskar_year_text,'Enable','off')
    #Disable Time series options - only allowed with Berger or Laskar real astronomical solution
    set(handles.timeSeries_button,'Enable','off','Value',0)
    set(handles.start_year_text,'Enable','off')
    set(handles.end_year_text,'Enable','off')
    set(handles.paleo_data_plot_button,'Enable','off','Value',0)
    #Load Laskar's input files into the handles structure - will be used by getLaskar within the
#laskar_year_text and laskar_year_slider callbacks
    handles.data.laskar_pos = scipy.io.loadmat('INSOLP.LA2004.BTL.ASC')
    handles.data.laskar_neg = scipy.io.loadmat('INSOLN.LA2004.BTL.100.ASC')
    # Update handles structure
    guidata(handles.main_panel,handles)
    # --- Executes on key press over calculate with no controls selected.
    
# def calculate_KeyPressFcn(hObject = None,eventdata = None,handles = None): 
#     # hObject    handle to calculate (see GCBO)
# # eventdata  reserved - to be defined in a future version of MATLAB
# # handles    structure with handles and user data (see GUIDATA)
    
#     # --- Executes on slider movement.
    
def e_slider_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to e_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'Value') returns position of slider
#        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
    a = get(hObject,'Value')
    #update value of corresponding field
    set(handles.e,'String',a)
    #update value of e;
    handles.data.e = a
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def e_slider_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to e_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: slider controls usually have a light gray background.
    if get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor',np.array([0.9,0.9,0.9]))
    
    
def obliquity_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to obliquity (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'String') returns contents of obliquity as text
#        str2double(get(hObject,'String')) returns contents of obliquity as a double
    e = str2double(get(hObject,'String'))
    if np.logical_or(np.isnan(e),not (e >= np.logical_and(get(handles.obliquity_slider,'Min'),e) <= get(handles.obliquity_slider,'Max')) ):
        e = handles.data.obliquity
        set(hObject,'String',e)
        errordlg(np.array(['Input must be a number b/n',num2str(get(handles.obliquity_slider,'Min')),' and ',num2str(get(handles.obliquity_slider,'Max'))]),'Error')
    
    # Save the new e value
    handles.data.obliquity = e
    #update slider
    set(handles.obliquity_slider,'Value',e)
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def obliquity_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to obliquity (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: edit controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    
def precession_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to precession (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'String') returns contents of precession as text
#        str2double(get(hObject,'String')) returns contents of precession as a double
    e = str2double(get(hObject,'String'))
    if np.logical_or(np.isnan(e),not (e >= np.logical_and(get(handles.precession_slider,'Min'),e) <= get(handles.precession_slider,'Max')) ):
        e = handles.data.precession
        set(hObject,'String',e)
        errordlg(np.array(['Input must be a number b/n',num2str(get(handles.precession_slider,'Min')),' and ',num2str(get(handles.precession_slider,'Max'))]),'Error')
    
    # Save the new e value
    handles.data.precession = e
    #update slider
    set(handles.precession_slider,'Value',e)
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def precession_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to precession (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: edit controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    
def latitude_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to latitude (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'String') returns contents of latitude as text
#        str2double(get(hObject,'String')) returns contents of latitude as a double
    e = str2double(get(hObject,'String'))
    if np.logical_or(np.isnan(e),not (e >= np.logical_and(- 90,e) <= 90) ):
        e = handles.data.latitude
        set(hObject,'String',e)
        errordlg('Input must be a number b/n -90 and +90','Error')
    
    # Save the new e value
    handles.data.latitude = e
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def latitude_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to latitude (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: edit controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    # --- Executes on slider movement.
    
def obliquity_slider_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to obliquity_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'Value') returns position of slider
#        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
    a = get(hObject,'Value')
    #update value of corresponding field
    set(handles.obliquity,'String',a)
    #update value of e;
    handles.data.obliquity = a
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def obliquity_slider_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to obliquity_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: slider controls usually have a light gray background.
    if get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor',np.array([0.9,0.9,0.9]))
    
    # --- Executes on slider movement.
    
def precession_slider_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to precession_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'Value') returns position of slider
#        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
    a = get(hObject,'Value')
    #update value of corresponding field
    set(handles.precession,'String',a)
    #update value of e;
    handles.data.precession = a
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def precession_slider_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to precession_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: slider controls usually have a light gray background.
    if get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor',np.array([0.9,0.9,0.9]))
    
    
def Fo_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to Fo (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'String') returns contents of Fo as text
#        str2double(get(hObject,'String')) returns contents of Fo as a double
    e = str2double(get(hObject,'String'))
    if np.logical_or(np.isnan(e),not (e >= np.logical_and(500,e) <= 2500) ):
        e = handles.data.Fo
        set(hObject,'String',e)
        errordlg('Input must be a number b/n 500 and 2500','Error')
    
    # Save the new e value
    handles.data.Fo = e
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def Fo_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to Fo (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: edit controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    # --- Executes on selection change in month.
    
def month_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to month (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: contents = get(hObject,'String') returns month contents as cell array
#        contents{get(hObject,'Value')} returns selected item from month
    contents = get(hObject,'String')
    mo = contents[get(hObject,'Value')]
    if 'January' == mo:
        handles.data.month = 1
    else:
        if 'February' == mo:
            handles.data.month = 2
        else:
            if 'March' == mo:
                handles.data.month = 3
            else:
                if 'April' == mo:
                    handles.data.month = 4
                else:
                    if 'May' == mo:
                        handles.data.month = 5
                    else:
                        if 'June' == mo:
                            handles.data.month = 6
                        else:
                            if 'July' == mo:
                                handles.data.month = 7
                            else:
                                if 'August' == mo:
                                    handles.data.month = 8
                                else:
                                    if 'September' == mo:
                                        handles.data.month = 9
                                    else:
                                        if 'October' == mo:
                                            handles.data.month = 10
                                        else:
                                            if 'November' == mo:
                                                handles.data.month = 11
                                            else:
                                                if 'December' == mo:
                                                    handles.data.month = 12
                                                else:
                                                    raise Exception('')
    
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def month_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to month (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: popupmenu controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    # --- Executes on selection change in day.
    
def day_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to day (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: contents = get(hObject,'String') returns day contents as cell array
#        contents{get(hObject,'Value')} returns selected item from day
    contents = get(hObject,'String')
    day = str2num(contents[get(hObject,'Value')])
    if 1 == handles.data.month:
        handles.data.day = day
    else:
        if 2 == handles.data.month:
            if day == 29:
                set(hObject,'Value',1)
                errordlg('Invalid day selection. No leap years are allowed in this demo. Dec. 31 is assumed slightly longer instead.  Assuming day 1','Error')
                handles.data.day = 1
            else:
                if day > 29:
                    set(hObject,'Value',1)
                    errordlg('Invalid day selection. Assuming day 1','Error')
                    handles.data.day = 1
                else:
                    handles.data.day = day
        else:
            if 3 == handles.data.month:
                handles.data.day = day
            else:
                if 4 == handles.data.month:
                    if day > 30:
                        set(hObject,'Value',1)
                        errordlg('Invalid day selection. Assuming day 1','Error')
                        handles.data.day = 1
                    else:
                        handles.data.day = day
                else:
                    if 5 == handles.data.month:
                        handles.data.day = day
                    else:
                        if 6 == handles.data.month:
                            if day > 30:
                                set(hObject,'Value',1)
                                errordlg('Invalid day selection. Assuming day 1','Error')
                                handles.data.day = 1
                            else:
                                handles.data.day = day
                        else:
                            if 7 == handles.data.month:
                                handles.data.day = day
                            else:
                                if 8 == handles.data.month:
                                    handles.data.day = day
                                else:
                                    if 9 == handles.data.month:
                                        if day > 30:
                                            set(hObject,'Value',1)
                                            errordlg('Invalid day selection. Assuming day 1','Error')
                                            handles.data.day = 1
                                        else:
                                            handles.data.day = day
                                    else:
                                        if 10 == handles.data.month:
                                            handles.data.day = day
                                        else:
                                            if 11 == handles.data.month:
                                                if day > 30:
                                                    set(hObject,'Value',1)
                                                    errordlg('Invalid day selection. Assuming day 1','Error')
                                                    handles.data.day = 1
                                                else:
                                                    handles.data.day = day
                                            else:
                                                if 12 == handles.data.month:
                                                    handles.data.day = day
                                                else:
                                                    raise Exception('')
    
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def day_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to day (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: popupmenu controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    # --- Executes on selection change in calendar_mode.
    
def calendar_mode_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to calendar_mode (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: contents = get(hObject,'String') returns calendar_mode contents as cell array
#        contents{get(hObject,'Value')} returns selected item from calendar_mode
    contents = get(hObject,'String')
    selection = contents[get(hObject,'Value')]
    if 'Perihelion: Jan. 3' == selection:
        handles.data.cal_mode = 2
    else:
        if 'Vernal equinox: Mar. 20' == selection:
            handles.data.cal_mode = 1
        else:
            raise Exception('')
    
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def calendar_mode_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to calendar_mode (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: popupmenu controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    # --- Executes on button press in close_btn.
    
def close_btn_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to close_btn (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    user_response = questdlg('Really Exit Program?')
    if np.array(['No']) == user_response:
        pass
    else:
        if np.array(['Cancel']) == user_response:
            pass
        else:
            if np.array(['Yes']) == user_response:
                os.delete(handles.main_panel)
                close_('all')
    
    # --- Executes during object creation, after setting all properties.
    
# def main_panel_CreateFcn(hObject = None,eventdata = None,handles = None): 
#     # hObject    handle to main_panel (see GCBO)
# # eventdata  reserved - to be defined in a future version of MATLAB
# # handles    empty - handles not created until after all CreateFcns called
    
#     # --- Executes during object deletion, before destroying properties.
    
# def main_panel_DeleteFcn(hObject = None,eventdata = None,handles = None): 
#     # hObject    handle to main_panel (see GCBO)
# # eventdata  reserved - to be defined in a future version of MATLAB
# # handles    structure with handles and user data (see GUIDATA)
    
#     # --- Executes when main_panel is resized.
    
# def main_panel_ResizeFcn(hObject = None,eventdata = None,handles = None): 
#     # hObject    handle to main_panel (see GCBO)
# # eventdata  reserved - to be defined in a future version of MATLAB
# # handles    structure with handles and user data (see GUIDATA)
    
#     # --- Executes when user attempts to close main_panel.
    
def main_panel_CloseRequestFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to main_panel (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hint: delete(hObject) closes the figure
    os.delete(hObject)
    # --- Executes on slider movement.
    
def year_slider_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to year_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'Value') returns position of slider
#        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
    a = get(hObject,'Value')
    #update value of corresponding field
    set(handles.myear,'String',a)
    #update value of e;
    handles.data.myear = a
    #update Milankovitch parameters
#calculate
    
    if 0 == handles.data.solutions_mode:
        #msgbox('Demo method')
#No need to do anything here...
        raise Exception('Calling year slider when demo is chosen is incorrect...')
    else:
        if 1 == handles.data.solutions_mode:
            #msgbox('Berger method')
#Year between -999999 - +999999 as input by the user
            year_to_plot = handles.data.myear * 1000
            ecc = - 999
            obliq = ecc
            omega_bar = ecc
            #Call Berger's orbpar solution here
            ecc,obliq,omega = Berger_orbpar(year_to_plot + 2000)
            #Adjust the obliquity and omegar_bar values to the convention
            obliq = obliq * 180 / np.pi
            omega_bar = omega * (180 / np.pi) - 180
            if omega_bar < 0:
                omega_bar = 360 + omega_bar
            #prec_for_orbit = 360-omega_bar*180/pi;
            handles.data.e = ecc
            handles.data.precession = omega_bar
            handles.data.obliquity = obliq
        else:
            if 2 == handles.data.solutions_mode:
                raise Exception('Wrong solution slider chosen...')
            else:
                msgbox('Invalid solutions method')
    
    set(handles.e,'String',sprintf('%8.7f',handles.data.e))
    set(handles.obliquity,'String',sprintf('%6.4f',handles.data.obliquity))
    set(handles.precession,'String',sprintf('%6.4f',handles.data.precession))
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def year_slider_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to year_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: slider controls usually have a light gray background.
    if get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor',np.array([0.9,0.9,0.9]))
    
    #Callback for the Berger solution
    
def myear_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to myear (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'String') returns contents of myear as text
#        str2double(get(hObject,'String')) returns contents of myear as a double
    e = str2double(get(hObject,'String'))
    if np.isnan(e) or not (e >= get(handles.year_slider,'Min') and e <= get(handles.year_slider,'Max')) :
        e = handles.data.myear
        set(hObject,'String',e)
        errordlg(np.array(['Input must be a number b/n ',num2str(get(handles.year_slider,'Min')),' and ',num2str(get(handles.year_slider,'Max'))]),'Error')
    
    # Save the new e value
    handles.data.myear = e
    #update slider
    set(handles.year_slider,'Value',e)
    if 0 == handles.data.solutions_mode:
        #msgbox('Demo method')
#No need to do anything here...
        raise Exception('Calling year slider when demo is chosen is incorrect...')
    else:
        if 1 == handles.data.solutions_mode:
            #msgbox('Berger method')
#Year between -999999 - +999999 as input by the user
            year_to_plot = handles.data.myear * 1000
            ecc = - 999
            obliq = ecc
            omega_bar = ecc
            #Call Berger's orbpar solution here
            ecc,obliq,omega = Berger_orbpar(year_to_plot + 2000)
            #Adjust the obliquity and omegar_bar values to the convention
            obliq = obliq * 180 / np.pi
            omega_bar = omega * (180 / np.pi) - 180
            if omega_bar < 0:
                omega_bar = 360 + omega_bar
            #prec_for_orbit = 360-omega_bar*180/pi;
            handles.data.e = ecc
            handles.data.precession = omega_bar
            handles.data.obliquity = obliq
        else:
            if 2 == handles.data.solutions_mode:
                raise Exception('Incorrect solution called...')
            else:
                msgbox('Invalid solutions method')
    
    set(handles.e,'String',sprintf('%8.7f',handles.data.e))
    set(handles.obliquity,'String',sprintf('%6.4f',handles.data.obliquity))
    set(handles.precession,'String',sprintf('%6.4f',handles.data.precession))
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def myear_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to myear (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: edit controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    # --- Executes on selection change in solution_menu.
    
def solution_menu_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to solution_menu (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: contents = cellstr(get(hObject,'String')) returns solution_menu contents as cell array
#        contents{get(hObject,'Value')} returns selected item from solution_menu
    
    contents = get(hObject,'String')
    selection = contents[get(hObject,'Value')]
    if 'Orbital Parameters Demo' == selection:
        ###handles.data.cal_mode = 2;
        handles.data.solutions_mode = 0
        #set(handles.data.myear, 'String', 0);
#set(handles.data.year_slider,  0;
        set(handles.myear,'Enable','off')
        set(handles.year_slider,'Enable','off')
        set(handles.laskar_year_text,'Enable','off')
        set(handles.laskar_year_slider,'Enable','off')
        set(handles.e,'Enable','on')
        set(handles.obliquity,'Enable','on')
        set(handles.precession,'Enable','on')
        set(handles.obliquity_slider,'Enable','on')
        set(handles.precession_slider,'Enable','on')
        set(handles.e_slider,'Enable','on')
        #Disable Time series options - only allowed with real astro solutions
        set(handles.timeSeries_button,'Enable','off')
        set(handles.start_year_text,'Enable','off')
        set(handles.end_year_text,'Enable','off')
        set(handles.paleo_data_plot_button,'Enable','off')
        #Extract demo values for ecc, obliq, and omega_bar
#and set them to the corresponding text boxes/sliders
        handles.data.e = 0.6
        handles.data.obliquity = 45
        handles.data.precession = 225
        set(handles.e,'String',handles.data.e)
        set(handles.obliquity,'String',handles.data.obliquity)
        set(handles.precession,'String',handles.data.precession)
        #Update the sliders as well:
        set(handles.e_slider,'Value',handles.data.e)
        set(handles.obliquity_slider,'Value',handles.data.obliquity)
        set(handles.precession_slider,'Value',handles.data.precession)
    else:
        if 'Berger (1978)' == selection:
            handles.data.solutions_mode = 1
            set(handles.myear,'Enable','on')
            set(handles.year_slider,'Enable','on')
            set(handles.laskar_year_text,'Enable','off')
            set(handles.laskar_year_slider,'Enable','off')
            set(handles.e,'Enable','off')
            set(handles.obliquity,'Enable','off')
            set(handles.precession,'Enable','off')
            set(handles.obliquity_slider,'Enable','off')
            set(handles.precession_slider,'Enable','off')
            set(handles.e_slider,'Enable','off')
            #Set Berger year back to zero
            set(handles.myear,'String',0)
            set(handles.year_slider,'Value',0)
            #Set laskar year back to zero
            set(handles.laskar_year_text,'String',0)
            set(handles.laskar_year_slider,'Value',0)
            #Enable Time series options
            set(handles.timeSeries_button,'Enable','on')
            set(handles.start_year_text,'Enable','on')
            set(handles.end_year_text,'Enable','on')
            set(handles.paleo_data_plot_button,'Enable','on')
            #Extract contemporary (year 0) values for ecc, obliq, and omega_bar
#from Berger and set them to the corresponding text boxes - Adjust Milankovitch
#text box parameters to the contemporary values based on the Berger solution
#same algorithm as myear callback
            year_to_plot = 0
            #Call Berger_orbpar with contemporary year
            ecc,obliq,omega = Berger_orbpar(year_to_plot + 2000)
            #Adjust the obliquity and omegar_bar values to the convention
            obliq = obliq * 180 / np.pi
            omega_bar = omega * (180 / np.pi) - 180
            if omega_bar < 0:
                omega_bar = 360 + omega_bar
            #prec_for_orbit = 360-omega_bar*180/pi;
            set(handles.e,'String',sprintf('%8.7f',ecc))
            set(handles.obliquity,'String',sprintf('%6.4f',obliq))
            set(handles.precession,'String',sprintf('%6.4f',omega_bar))
            #Update ecc, obliq & precession values in data structure
            handles.data.e = ecc
            handles.data.precession = omega_bar
            handles.data.obliquity = obliq
        else:
            if 'Laskar et al. (2004)' == selection:
                handles.data.solutions_mode = 2
                set(handles.myear,'Enable','off')
                set(handles.year_slider,'Enable','off')
                set(handles.laskar_year_text,'Enable','on')
                set(handles.laskar_year_slider,'Enable','on')
                #Update text boxes and sliders
                set(handles.e,'Enable','off')
                set(handles.obliquity,'Enable','off')
                set(handles.precession,'Enable','off')
                set(handles.obliquity_slider,'Enable','off')
                set(handles.precession_slider,'Enable','off')
                set(handles.e_slider,'Enable','off')
                #Set Laskar year back to zero
                set(handles.laskar_year_text,'String',0)
                set(handles.laskar_year_slider,'Value',0)
                #Set Berger year back to zero
                set(handles.myear,'String',0)
                set(handles.year_slider,'Value',0)
                #Enable Time series options
                set(handles.timeSeries_button,'Enable','on')
                set(handles.start_year_text,'Enable','on')
                set(handles.end_year_text,'Enable','on')
                set(handles.paleo_data_plot_button,'Enable','on')
                #Adjust Milankovitch text box and slider parameters to the contemporary values
#base on the Laskar solution
                year_to_plot = 0
                #Call getLaskar with year 0
                ecc,obliq,omega_bar = getLaskar(year_to_plot,handles.data.laskar_neg,handles.data.laskar_pos)
                set(handles.e,'String',sprintf('%8.7f',ecc))
                set(handles.obliquity,'String',sprintf('%6.4f',obliq))
                set(handles.precession,'String',sprintf('%6.4f',omega_bar))
                #set(handles.start_year_text, 'String', handles.data.start_year_text);
#set(handles.end_year_text, 'String', handles.data.end_year_text);
                #Update ecc, oblilq & precession values in data structure
                handles.data.e = ecc
                handles.data.precession = omega_bar
                handles.data.obliquity = obliq
            else:
                raise Exception('')
    
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def solution_menu_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to solution_menu (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: popupmenu controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    # --- Executes on button press in help_button.
    
def help_button_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to help_button (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    wm = warndlg('The ReadMe.txt in the model root directory should open in ~6 s in your default editor. If not, open it manually to view the help.')
    pause(6)
    if ishandle(wm):
        close_(wm)
    
    edit('ReadMe.txt')
    # --- Executes on button press in timeSeries_button. - Plots LASKAR's
# solution only - need to make a note of this in the GUI or help
    
def timeSeries_button_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to timeSeries_button (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    #get the start and end years from the corresonding time series text boxes
    
    st_year = handles.data.start_year_text
    en_year = handles.data.end_year_text
    #figure out if Berger or Laskar solution should be used
    if 0 == handles.data.solutions_mode:
        msgbox('Error - this functionality cannot be used in demo mode')
    else:
        if 1 == handles.data.solutions_mode:
            #Berger_data.dat = output data from Tiho's Berger78_driver function
#output = year; ecc; obliq; omega
            Berger_solution = scipy.io.loadmat('Berger78_data.dat')
            #Year values
            table_year = Berger_solution[:,1] / 1000 - 2
            #IMPORTANT!!! NEED to offset Berger years by 2,000 years because he has calendar years,
#Laskar has years since J2000.0
            #eccentricity values
            ecc = Berger_solution[:,2]
            #obliquity values
            obliq = Berger_solution[:,3]
            #precession - need to adjust
            precess = Berger_solution[:,4] - 180
            pn = precess < 0
            precess[pn] = precess(pn) + 360
        else:
            if 2 == handles.data.solutions_mode:
                #THIS CODE TAKEN AND AMENDED FROM GETLASKAR
                laskar_neg = handles.data.laskar_neg
                laskar_pos = handles.data.laskar_pos
                #Remove 0 row from negative file
                laskar_neg[1,:] = []
                #Flip the negative file
                laskar_neg = flipud(laskar_neg)
                #Concatenate the files
                Laskar_solution = vertcat(laskar_neg,laskar_pos)
                #Extract each column and assign variables
#Year values
                table_year = Laskar_solution[:,1]
                #Eccentricity values - no adjustment needed
                ecc = Laskar_solution[:,2]
                #obliquity values - no asjustment needed
                obliq = (180 / np.pi) * Laskar_solution[:,3]
                #Need to adjust precession angle - find where it jumps from 360 to 0
                precess = (180 / np.pi) * Laskar_solution[:,4]
            else:
                msgbox('Invalid solutions method')
    
    #####PREPARE TO COMPUTE INSOLATION TIME SERIES ###########
    wm = warndlg('Please wait for the computation to complete.  This may take from a few moments to more than a minute, depending on the length of your time series and the speed of your computer...')
    q = find(table_year <= st_year,1,'last')
    q2 = find(table_year >= en_year,1,'first')
    #Truncate table years and Milankovitch vectors to only the requested time interval
    table_year = table_year(np.arange(q,q2+1))
    ecc = ecc(np.arange(q,q2+1))
    obliq = obliq(np.arange(q,q2+1))
    precess = precess(np.arange(q,q2+1))
    #Plot in steps of 1,000 years, otherwise it is too slow:
    
    #Alternatively, or in additon, INSIDE insol_TS, if time series is too long,
#we can down sample more to up to 5,000 years steps.
    if handles.data.solutions_mode == 1:
        #Years are in units of thousands of years, select whole thousands from the tables only, with the end and beginning always selected
#q3 = abs(rem(table_year,1)) < 1e-6; #Exact thousand years (integer)
        bind = np.arange(1,len(table_year)+10,10)
        table_year = np.array([[table_year(bind)],[table_year(end())]])
        ecc = np.array([[ecc(bind)],[ecc(end())]])
        obliq = np.array([[obliq(bind)],[obliq(end())]])
        precess = np.array([[precess(bind)],[precess(end())]])
    
    #The following snippet (4 code lines) is taken from the insolation snapshot button
#callback:
    prec_for_orbit = 180 - precess
    
    if prec_for_orbit < 0:
        #messes up some things within orbit.m, particularly the season length calculations
        prec_for_orbit = 360 + prec_for_orbit
    
    dayofyear = np.arange(1,365+1)
    sol,solstice_sol,annual_mean_sol = insol_TS(handles.data.sm_axis,handles.data.AU,handles.data.period,table_year,dayofyear,ecc,obliq,prec_for_orbit,handles.data.Fo,handles.data.latitude,handles.data.month,handles.data.day)
    if ishandle(wm):
        close_(wm)
    
    f3h = plt.figure(3)
    clf
    set(f3h,'Name','Milankovitch Parameters Time Series','NumberTitle','off','Units','normalized','OuterPosition',np.array([0.1,0.1,0.7,0.85]))
    subplot(3,1,1)
    plt.plot(table_year,ecc,'b-')
    plt.title('Eccentricity')
    plt.axis(np.array([st_year,en_year,0,0.06]))
    plt.ylabel('dimensionless')
    hold('on')
    plt.plot(np.array([0,0]),np.array([0,0.06]),'m-')
    #obliquity in green
    subplot(3,1,2)
    plt.plot(table_year,obliq,'g-')
    plt.title('Obliquity')
    plt.axis(np.array([st_year,en_year,21.5,25]))
    plt.ylabel('degrees')
    hold('on')
    plt.plot(np.array([0,0]),np.array([21.5,25]),'m-')
    #precession in red
    
    #Use precess (omega_bar, longitude of perihelion) to reconstruct omega,
#longitude of perigee, the quantity needed to reconstruct climatic precession:
    omega = np.mod(precess + 180,360)
    
    subplot(3,1,3)
    ax,h1,h2 = plotyy(table_year,precess,table_year,np.multiply(ecc,np.sin(omega * (np.pi / 180))))
    plt.title('Longitude of perihelion/Climatic Precession')
    set(get(ax(1),'Ylabel'),'String','Long. of perihelion, \omega_t_i_l_d_e, deg.')
    set(get(ax(2),'Ylabel'),'String','Climatic precession, e*sin(\omega)','Color','red')
    set(h1,'LineStyle','-','Color',np.array([0.6,0.6,0.6]))
    set(h2,'LineStyle','-','Color','r')
    plt.axis(ax(1),np.array([st_year,en_year,- 5,365]))
    plt.axis(ax(2),np.array([st_year,en_year,- 0.051,0.051]))
    set(ax(2),'YColor','red')
    set(ax(1),'YColor','k','YTick',np.array([0,90,180,270,360]))
    set(ax(2),'YColor','r','YTick',np.array([- 0.05,- 0.025,0,0.025,0.05]))
    #Plot some interesting paleoclimatological data here...
#Test for plotyy
    box('off')
    hold('on')
    plt.plot(ax(1),np.array([0,0]),np.array([- 5,365]),'m-')
    ############################
############  PLOT TIME SERIES OF INSOLATION #############
#######################################
    mo_string = ''
    if 1 == handles.data.month:
        mo_string = 'January'
    else:
        if 2 == handles.data.month:
            mo_string = 'February'
        else:
            if 3 == handles.data.month:
                mo_string = 'March'
            else:
                if 4 == handles.data.month:
                    mo_string = 'April'
                else:
                    if 5 == handles.data.month:
                        mo_string = 'May'
                    else:
                        if 6 == handles.data.month:
                            mo_string = 'June'
                        else:
                            if 7 == handles.data.month:
                                mo_string = 'July'
                            else:
                                if 8 == handles.data.month:
                                    mo_string = 'August'
                                else:
                                    if 9 == handles.data.month:
                                        mo_string = 'September'
                                    else:
                                        if 10 == handles.data.month:
                                            mo_string = 'October'
                                        else:
                                            if 11 == handles.data.month:
                                                mo_string = 'November'
                                            else:
                                                if 12 == handles.data.month:
                                                    mo_string = 'December'
                                                else:
                                                    raise Exception('')
    
    f4h = plt.figure(4)
    clf
    set(f4h,'Name','Insolation Time Series at Specified Date and Latitude','NumberTitle','off','Units','normalized','OuterPosition',np.array([0.15,0.3,0.7,0.6]))
    
    ax,h1,h2 = plotyy(table_year,solstice_sol,table_year,annual_mean_sol)
    set(get(ax(1),'Ylabel'),'String',np.array(['Insolation for ',mo_string,' ',num2str(handles.data.day),', W m^-^2']))
    set(get(ax(2),'Ylabel'),'String','Annual mean of daily insolation, W m^-^2')
    set(ax(2),'YColor','r')
    set(h2,'Color','r')
    plt.xlabel('Thousand of years since J2000')
    plt.title(np.array(['Insolation at ',num2str(handles.data.latitude),'^o latitude, W m^-^2']))
    rng = np.amax(solstice_sol) - np.amin(solstice_sol)
    if rng <= 0:
        rng = 10
    
    rng2 = np.amax(annual_mean_sol) - np.amin(annual_mean_sol)
    if rng2 <= 0:
        rng2 = 10
    
    y1lim = np.array([np.amin(solstice_sol) - 0.1 * rng,np.amax(solstice_sol) + 0.1 * rng])
    y2lim = np.array([np.amin(annual_mean_sol) - 0.1 * rng2,np.amax(annual_mean_sol) + 0.1 * rng2])
    plt.axis(ax(1),np.array([st_year,en_year,y1lim]))
    plt.axis(ax(2),np.array([st_year,en_year,y2lim]))
    s = axis
    hold('on')
    plt.plot(ax(1),np.array([0,0]),np.array([s(3),s(4)]),'m-')
    box('off')
    set(ax(1),'YTickMode','auto')
    set(ax(1),'YTickLabelMode','auto')
    set(ax(2),'YTickMode','auto')
    set(ax(2),'YTickLabelMode','auto')
    f5h = plt.figure(5)
    clf
    set(f5h,'Name','3D Insolation Time Series','NumberTitle','off','Units','normalized','OuterPosition',np.array([0.2,0.25,0.5,0.6]))
    surf(table_year,dayofyear,sol)
    view(2)
    plt.axis(np.array([- Inf,Inf,1,365]))
    plt.axis('ij')
    shading('interp')
    colorbar
    plt.xlabel('Thousands of years since J2000')
    plt.ylabel('Day of year')
    plt.title(np.array(['Daily insolation at ',num2str(handles.data.latitude),'^o latitude averaged over 24 hrs, W m^-^2']))
    if handles.data.save_insol_data:
        ofile,opath = uiputfile('orbit_output/*.dat','Save Insolation Time Series data as')
        if ofile:
            tmp = np.array([NaN,dayofyear])
            tmp = np.transpose(tmp)
            out = np.array([[np.transpose(table_year)],[sol]])
            out = np.array([tmp,out])
            save('-ascii',np.array([opath,ofile]),'out')
    
    guidata(hObject,handles)
    # --- Executes on button press in insolation_button.
    
def insolation_button_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to insolation_button (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    prec_for_orbit = 180 - handles.data.precession
    
    if prec_for_orbit < 0:
        #messes up some things within orbit.m, particularly the season length calculations
        prec_for_orbit = 360 + prec_for_orbit
    
    wm = warndlg('Please wait for the computation to complete. This can take a few moments...')
    dayofyear = np.array([np.arange(1,365+5,5),365])
    lats = np.arange(90,- 90+- 5,- 5)
    sol,__ = insol_3d(handles.data.sm_axis,handles.data.AU,handles.data.period,handles.data.e,handles.data.obliquity,prec_for_orbit,handles.data.Fo,dayofyear,lats)
    if ishandle(wm):
        close_(wm)
    
    f2h = plt.figure(2)
    clf
    set(f2h,'Name','3D Global Insolation in a Specified Year','NumberTitle','off','Units','normalized','OuterPosition',np.array([0.05,0.25,0.7,0.75]))
    subplot(2,1,1)
    surf(dayofyear,lats,sol)
    view(2)
    plt.axis(np.array([1,365,- 90,90]))
    shading('interp')
    colorbar
    plt.xlabel('Day of year')
    plt.ylabel('Latitude, degrees')
    plt.title('Daily insolation averaged over 24 hrs, W m^-^2')
    contemporary_sol = scipy.io.loadmat('contemp_insol.dat')
    
    sol_anomaly = sol - contemporary_sol
    subplot(2,1,2)
    surf(dayofyear,lats,sol_anomaly)
    view(2)
    plt.axis(np.array([1,365,- 90,90]))
    shading('interp')
    colorbar
    plt.xlabel('Day of year')
    plt.ylabel('Latitude, degrees')
    plt.title('Daily insolation anomaly, W m^-^2')
    if handles.data.save_insol_data:
        ofile,opath = uiputfile('orbit_output/*.dat','Save Insolation data as')
        if ofile:
            out = np.array([[dayofyear],[sol]])
            tmp = np.array([NaN,lats])
            tmp = np.transpose(tmp)
            out = np.array([tmp,out])
            save('-ascii',np.array([opath,ofile]),'out')
        ofile,opath = uiputfile('orbit_output/*.dat','Save Insolation Anomalies data as')
        if ofile:
            out = np.array([[dayofyear],[sol_anomaly]])
            tmp = np.array([NaN,lats])
            tmp = np.transpose(tmp)
            out = np.array([tmp,out])
            save('-ascii',np.array([opath,ofile]),'out')
    
    
def start_year_text_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to start_year_text (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'String') returns contents of start_year_text as text
#        str2double(get(hObject,'String')) returns contents of start_year_text as a double
    e = str2double(get(hObject,'String'))
    # if isnan(e) | ~(e>=get(handles.start_year_text,'Min') & e<= get(handles.obliquity_slider,'Max'))
#     e = handles.data.obliquity; #assume the old value
#     set(hObject, 'String', e);
#     errordlg(['Input must be a number b/n', num2str(get(handles.obliquity_slider,'Min')), ' and ' ,...
#         num2str(get(handles.obliquity_slider,'Max'))],'Error');
# end
# Save the new e value
    handles.data.start_year_text = e
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def start_year_text_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to start_year_text (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: edit controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    
def end_year_text_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to end_year_text (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'String') returns contents of end_year_text as text
#        str2double(get(hObject,'String')) returns contents of end_year_text as a double
    e = str2double(get(hObject,'String'))
    handles.data.end_year_text = e
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def end_year_text_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to end_year_text (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: edit controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    # --- Executes on slider movement.
    
def laskar_year_slider_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to laskar_year_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'Value') returns position of slider
#        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
    
    a = get(hObject,'Value')
    #update value of corresponding field
    set(handles.laskar_year_text,'String',a)
    #update value of e;
    handles.data.laskar_year_text = a
    #update Milankovitch parameters
#calculate
    
    if 0 == handles.data.solutions_mode:
        #msgbox('Demo method')
#No need to do anything here...
        raise Exception('Calling year slider when demo is chosen is incorrect...')
    else:
        if 1 == handles.data.solutions_mode:
            #msgbox('Berger method')
            raise Exception('Wrong solution slider chosen...')
        else:
            if 2 == handles.data.solutions_mode:
                #year_to_plot = handles.data.laskar_year_text;
#         #msgbox('Laskar method')
#         #Implement Laskar method
                ecc = - 999
                obliq = ecc
                omega_bar = ecc
                #Call getLaskar method to obtain Milank values for the input year
#Divide year by 1000 b/c Laskar gives his values every 1000 years
                ecc,obliq,omega_bar = getLaskar(handles.data.laskar_year_text,handles.data.laskar_neg,handles.data.laskar_pos)
                handles.data.e = ecc
                handles.data.precession = omega_bar
                handles.data.obliquity = obliq
            else:
                msgbox('Invalid solutions method')
    
    set(handles.e,'String',sprintf('%8.7f',handles.data.e))
    set(handles.obliquity,'String',sprintf('%6.4f',handles.data.obliquity))
    set(handles.precession,'String',sprintf('%6.4f',handles.data.precession))
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def laskar_year_slider_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to laskar_year_slider (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: slider controls usually have a light gray background.
    if get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor',np.array([0.9,0.9,0.9]))
    
    
def laskar_year_text_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to laskar_year_text (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hints: get(hObject,'String') returns contents of laskar_year_text as text
#        str2double(get(hObject,'String')) returns contents of laskar_year_text as a double
    
    e = str2double(get(hObject,'String'))
    if np.isnan(e) or not (e >= get(handles.laskar_year_slider,'Min') and e <= get(handles.laskar_year_slider,'Max')) :
        e = handles.data.laskar_year_text
        set(hObject,'String',e)
        errordlg(np.array(['Input must be a number b/n ',num2str(get(handles.laskar_year_slider,'Min')),' and ',num2str(get(handles.laskar_year_slider,'Max'))]),'Error')
    
    # Save the new e value
    handles.data.laskar_year_text = e
    #update slider
    set(handles.laskar_year_slider,'Value',e)
    if 0 == handles.data.solutions_mode:
        #msgbox('Demo method')
#No need to do anything here...
        raise Exception('Calling year slider when demo is chosen is incorrect...')
    else:
        if 1 == handles.data.solutions_mode:
            raise Exception('Wrong solution referenced...')
        else:
            if 2 == handles.data.solutions_mode:
                #year_to_plot = handles.data.laskar_year_text;
#         #msgbox('Laskar method')
#         #Implement Laskar method
                ecc = - 999
                obliq = ecc
                omega_bar = ecc
                #Call getLaskar method to obtain Milank values for the input year
#Divide year by 1000 b/c Laskar gives his values every 1000 years
                ecc,obliq,omega_bar = getLaskar(handles.data.laskar_year_text,handles.data.laskar_neg,handles.data.laskar_pos)
                handles.data.e = ecc
                handles.data.precession = omega_bar
                handles.data.obliquity = obliq
            else:
                msgbox('Invalid solutions method')
    
    set(handles.e,'String',sprintf('%8.7f',handles.data.e))
    set(handles.obliquity,'String',sprintf('%6.4f',handles.data.obliquity))
    set(handles.precession,'String',sprintf('%6.4f',handles.data.precession))
    guidata(hObject,handles)
    # --- Executes during object creation, after setting all properties.
    
def laskar_year_text_CreateFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to laskar_year_text (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    empty - handles not created until after all CreateFcns called
    
    # Hint: edit controls usually have a white background on Windows.
#       See ISPC and COMPUTER.
    if ispc and get(hObject,'BackgroundColor')==get(0,'defaultUicontrolBackgroundColor'):
        set(hObject,'BackgroundColor','white')
    
    # --- Executes on key press with focus on help_button and none of its controls.
    
# def help_button_KeyPressFcn(hObject = None,eventdata = None,handles = None): 
#     # hObject    handle to help_button (see GCBO)
# # eventdata  structure with the following fields (see UICONTROL)
# #	Key: name of the key that was pressed, in lower case
# #	Character: character interpretation of the key(s) that was pressed
# #	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
# # handles    structure with handles and user data (see GUIDATA)
    
#     # --- Executes on button press in saving_data_checkbox.
    
def saving_data_checkbox_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to saving_data_checkbox (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    if get(hObject,'Value') == get(hObject,'Max'):
        handles.data.save_insol_data = 1
    else:
        handles.data.save_insol_data = 0
    
    guidata(hObject,handles)
    # Hint: get(hObject,'Value') returns toggle state of saving_data_checkbox
    
    # --- Executes on button press in paleo_data_plot_button.
    
def paleo_data_plot_button_Callback(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to paleo_data_plot_button (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    
    # Hint: get(hObject,'Value') returns toggle state of paleo_data_plot_button
# if get(hObject,'Value')==get(hObject,'Max')
#     handles.data.plot_paleo_data = 1;
# else
#     handles.data.plot_paleo_data = 0;
# end
    st_year = handles.data.start_year_text
    en_year = handles.data.end_year_text
    #Load EPICA CO2 data
    co2 = scipy.io.loadmat('EPICA_CO2.dat')
    co2[:,1] = - co2[:,1]
    #Load EPICA deuterium/temperature data
    deut = scipy.io.loadmat('EPICA_deuterium.dat')
    deut[:,3] = - (deut[:,3] + 50)
    #Load the Lisiecki and Raymo 2005 benthic d-O-18 stack data:
    LR04 = scipy.io.loadmat('LR04_dO18_benthic_stack.dat')
    #Load the Zachos et al. (2001) benthic d-O-18 data set:
    Zachos = scipy.io.loadmat('Zachos01_d18O.dat')
    f6h = plt.figure(6)
    clf
    set(f6h,'Name','Paleoclimatological Data Time Series','NumberTitle','off','Units','normalized','OuterPosition',np.array([0.11,0.11,0.7,0.85]))
    subplot(2,1,1)
    ax,h1,h2 = plotyy(co2[:,1] / 1000,co2[:,2],deut[:,3] / 1000,deut[:,5])
    plt.axis(ax(1),np.array([st_year,en_year,180,295]))
    plt.axis(ax(2),np.array([st_year,en_year,- 11,5.5]))
    plt.title('EPICA CO_2 and temperature')
    set(get(ax(1),'Ylabel'),'String','[CO_2], ppmv')
    set(get(ax(2),'Ylabel'),'String','Temperature, \circC')
    set(ax(1),'YTick',np.array([np.arange(180,300+20,20)]))
    set(ax(2),'YTick',np.array([- 10,- 7.5,- 5,- 2.5,0,2.5,5]))
    plt.xlabel('Thousands of years since J2000')
    hold('on')
    plt.plot(ax(1),np.array([0,0]),np.array([180,295]),'m-')
    set(ax(1),'box','off')
    subplot(2,1,2)
    q = - LR04[:,1] >= np.logical_and(st_year,- LR04[:,1]) <= en_year
    q2 = - Zachos[:,1] >= np.logical_and(st_year / 1000,- Zachos[:,1]) <= en_year / 1000
    plt.plot(- LR04(q,1),LR04(q,2),'b-')
    hold('on')
    plt.plot(- Zachos(q2,1) * 1000,Zachos(q2,2),'r-')
    ymin = 0.95 * np.amin(np.array([[LR04(q,2)],[Zachos(q2,2)]]))
    ymax = 1.05 * np.amax(np.array([[LR04(q,2)],[Zachos(q2,2)]]))
    plt.axis(np.array([st_year,en_year,ymin,ymax]))
    set(gca,'YDir','reverse')
    plt.xlabel('Thousands of years since J2000')
    plt.ylabel(np.array(['Benthic Foraminiferal \delta^1^8O, ',char(8240)]))
    plt.legend(np.array(['Lisiecki and Raymo 2005 \delta^1^8O','Zachos et al. (2001) \delta^1^8O']),'Location','NorthOutside','Orientation','Horizontal')
    plt.plot(np.array([0,0]),np.array([ymin,ymax]),'m-')
    guidata(hObject,handles)
    # --- If Enable == 'on', executes on mouse press in 5 pixel border.
# --- Otherwise, executes on mouse press in 5 pixel border or over timeSeries_button.
    
# def timeSeries_button_ButtonDownFcn(hObject = None,eventdata = None,handles = None): 
#     # hObject    handle to timeSeries_button (see GCBO)
# # eventdata  reserved - to be defined in a future version of MATLAB
# # handles    structure with handles and user data (see GUIDATA)
    
#     # --- If Enable == 'on', executes on mouse press in 5 pixel border.
# # --- Otherwise, executes on mouse press in 5 pixel border or over paleo_data_plot_button.
    
def paleo_data_plot_button_ButtonDownFcn(hObject = None,eventdata = None,handles = None): 
    # hObject    handle to paleo_data_plot_button (see GCBO)
# eventdata  reserved - to be defined in a future version of MATLAB
# handles    structure with handles and user data (see GUIDATA)
    return varargout