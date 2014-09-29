BML Tools
===============

OptiTrack
---------

Tools and code for use with the OptiTrack system will be here.

For MATLAB functions, it is recommended that users add the path of this directory to their MATLAB path.
	
### importOTdata.m  (MATLAB)

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
	   
				

### parseAllCSV.m  (MATLAB)

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



### importOTdata.py  (Python)

This will import OptiTrack CSV files and provide objects with named fields for data. Usage is similar to the MATLAB implementation of importOTdata.
Usage case is largely intended to be inside an iPython environment, as a replacement to MATLAB.

	# This is an example usage in iPython
	from importOTdata import importOTdata
	import numpy as np
	import matplotlib.pyplot as plt
	%matplotlib
	
	S = importOTdata('run001.csv')
	S
	*Out[1]:* <importOTdata.OTData instance at 0x0795D8A0>
	
	# Produce a plot from imported data
	temp = np.array(S.Trackables[1].Position);
	fh1 = plt.figure()
	ph1 = plt.plot(S.Trackables[1].TrackedTimestamps,temp[:,2])
	ax1 = fh1.gca()
	ax1.set_xlabel("Position [m]",fontsize = 15);
	ax1.set_ylabel("Position [m]",fontsize = 15);
	plt.setp(ax1.get_xticklabels(), fontsize=15);
	plt.setp(ax1.get_yticklabels(), fontsize=15);
	
