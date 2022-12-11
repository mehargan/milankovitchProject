# Ice Age Arcade
## ATLS 5519 Designing a Science Exhibit Fall 2022
The Ice Age Arcade is an exhibit designed to represent the relationship between Milankovitch cycles and ice ages in an inclusive, all-ages format, with a familiar design of an arcade game. The visitors to the exhibit would be presented with a 3D orbital model of the Earth around the Sun, which they can manipulate with a goal of obtaining the Milankovitch cycle conditions appropriate for the start of a Glacial Maximum (ice age). Once achieved, they will witness the climatic conditions during the last ice age through snowfall visualization and the formation of the Laurentide Ice Sheet over present-day Manhattan, NY. 
This exhibit has been designed for the National Center for Atmospheric Research (NCAR), Boulder, Colorado.


Supporting documents in [Google Drive](https://drive.google.com/drive/u/4/folders/142EvQBHvb3Fekmemog-yAIT2G5QtMwB0).

### Directory Setup
```
|- src      --> Python source directory 
|   |- inputDetection.py
|   |- main.py
|   |- milankovitch.py
|   |- test.py
|- data     --> Research data used to derive paleoclimate information about insolation and temperature
|   |- mtable.txt
|   |- vostok.txt
|- unity    --> Unity project for on-screen visualization
|   |- Assets
|   |- Build    --> Prebuilt windows .exe
|   |- Library
|   |- Logs
|   |- Packages
|   |- ProjectSettings
|   |- UserSettings
```

### Description
The software developed for the exhibit can be divided into three broad modules – input detection using computer vision (CV) (`src/inputDetection.py`), solar insolation calculation from the Milankovitch parameters (`src/milankovitch.py`), and the on-screen visualization (`unity`). The detection of user input, or the sensing of orbital information from the 3D model is done using computer vision in a Python script. The under-side of orbital model consists of multiple ArUco CV markers and a webcam, which detects the position and rotation of each marker to estimate the eccentricity and the longitude of Perihelion, as chosen by the visitor. These parameters are then used to look up the year in the past those parameters existed in and calculate the solar insolation on Earth during that time, using the table and formulae presented by Berger and Loutre. Once the information has been prepared, it is sent over User Datagram Protocol (UDP) to the on-screen visualization, which has been developed in the Unity Game Engine. The visualization updates the ongoing orbit animation with the user-chosen eccentricity and precession, as well as displays the year, Milankovitch cycle values, and the calculated solar insolation as feedback to the viewer. Once the viewer presses the GO button, the software checks the input configuration against the known orbital configuration required for an ice age, and outputs to the them on the screen whether they succeeded or not. If the chosen Milankovitch cycles are optimum to cause an ice age, a `START` message is sent over the Serial protocol to trigger the snowfall in the snowglobe component of the exhibit. 

### Instructions
There are 2 setups to run this code:
1. External camera with orbital marker detection + Unity visualization
2. User input + Unity visualization (when no camera or markers are available)

**Step 1**
Open the Unity project and run OR run the prebuilt Windows `ATLS5519-EarthOrbit.exe` inside `unity/build` to run the Unity visualization. The second option requires temporarily disabling system firewalls for the two programs to communicate with each other over UDP. 

**Step 2**
Run the Python script in `src`. If running with setup (1):
```
> python src/main.py
```
Else with setup (2): 
```
> python src/test.py
```
This would ask for user input for precession and eccentricity with the following requirements: Precession between (0.0, 360.0), Eccentricity as 0.014 OR 0.04. User input would send a command to update the Unity visualization. 
