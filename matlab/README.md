BML Code Tools
===============

Matlab
---------

Matlab code will be located here.

It is recommended that users add the path of this directory to their MATLAB path.

Note that MATLAB requires separate files for each function. Documentation will be divided by sections: standalone functions and scripts

Functions
-----------

### importORTelem_ip25.m

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

### importORTelem.m

This function is similar to importORTelem_ip25() above, except the format from legacy IPv2.4 boards on Motile OctoRoACH's is expected.
Usage is the same as importORTelem_ip25(), with different output fields.

### importVRTelem.m

This function is similar to importORTelem_ip25() above, except the format for the VelociRoACH is expected.

*TODO: Sync this with current roach 'master' branch, add in all BMEF & DC channels, controller information.* (Andrew P)

*TODO: Add motor power as a named field, calculated as a post-processing step.* (Jessica)

	
### importOTdata.m

This function will import a CSV file from the OptiTrack system, and return a data structure with all of the tracking information extracted from the file,
and avaialble by trackable, or by frame.

Example:
	>> S = importOTdata('run001.csv')

	S = 

		Comments: {40x1 cell}
		Handedness: 'right'
		FrameCount: 1888
		EnumTrackableCount: 1
		NumRigidBody: 1
		RigidBody: [1x1 struct]
		Frame: [1888x1 struct]
		Trackables: [1x1 struct]

	>> S.Trackables(1).Position

	ans =

	   -0.0184    0.5049    0.6657
	   -0.0184    0.5050    0.6657
	   ...
	   
				
Scripts
-----------

### parseAllCSV.m

This is a simple script that will find all *.csv files in the current working directory, run importOTdata on all of them, and return a struct array of the results.
The struct array will be named DATA.

	>> parseAllCSV
	Importing run001.csv
	Importing run002.csv
	...
	Importing run030.csv
	>> DATA

	DATA = 

	1x30 struct array with fields:
		Comments
		Handedness
		FrameCount
		EnumTrackableCount
		NumRigidBody
		RigidBody
		Frame
		Trackables


