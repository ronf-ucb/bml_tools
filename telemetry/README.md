BML Tools
===============

Telemetry
---------

Code for importing, plotting, and working with telemetry from the ImageProc control boards will be available here.

### telemetryImport.py  (Python)

This provides a simple python function to import telemetry data from a VelociRoACH. A TelemetryData object with named fields is returned.

Example usage:

	In [1]:		from telemetryImport import *
				S = telemetryImport('vr_telem_example.txt')
				S
	
				Importing  vr_telem_example.txt
				Got 100 samples
	Out[2]:
				<telemetryImport.TelemetryData instance at 0x075E6FA8>

### telemetry_plotter.ipynb  (iPython)
iPython notebook to read telemetry file from robot, and plot state data, as well as calculated torque/power. 

Usage
	1. In Windows or Linux command shell:
		c:bml_tools\ipython notebook
	2. In web browser, edit file name in cell. Example data is
	provided in example_imudata.txt/ 
	3. Cell -> Run All.
	4. Figures are in .png and can be saved from
	 the web browser. Example plots are sensor-info.png and 	power-info.png
Note that the .txt file can not have any characters after the last line.


This notebook can be used to import telemetry data into an iPython notebook. This will be obsoleted very shortly.
This will become an example of how to use the TelemetryData object after importing.

### importORTelem_ip25.m  (MATLAB)

This function will import telemetry data recorded & downloaded from an OctoRoach robot, running with an ImageProc v2.5 control board.

Telemetry formats change very often, largely because of adaptation for new research and engineering goals.
Users are encouraged to look at the code and verify that it matches that header included in the telemetry files they are working with.

The telemetry data will be returned in a data structure with named fields.

Example:

	>> S = importORTelem_ip25('sine1.txt')
	Got 112996 samples

	S = 
		times: [112996x1 double]
		inputL: [112996x1 double]
		inputR: [112996x1 double]
		DCA: [112996x1 double]
		DCB: [112996x1 double]
		DCC: [112996x1 double]
		DCD: [112996x1 double]
		wx: [112996x1 double]
		wy: [112996x1 double]
		wz: [112996x1 double]
		wzavg: [112996x1 double]
		xlx: [112996x1 double]
		xly: [112996x1 double]
		xlz: [112996x1 double]
		BEMFA: [112996x1 double]
		BEMFB: [112996x1 double]
		BEMFC: [112996x1 double]
		BEMFD: [112996x1 double]
		steeringIn: [112996x1 double]
		steeringOut: [112996x1 double]
		vbatt: [112996x1 double]
		yawAngle: [112996x1 double]
		stimes: [112996x1 double]


### importVRTelem.m  (MATLAB)

This function is similar to importORTelem_ip25() above, except the format for the VelociRoACH is expected.

*TODO: Sync this with current roach 'master' branch, add in all BMEF & DC channels, controller information.* (Andrew P)

*TODO: Add motor power as a named field, calculated as a post-processing step.* (Jessica)
