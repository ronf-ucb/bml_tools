BML Code Tools
===============

Python
---------

Python code will be located here. This does not include iPython notebooks. This is for pure python code.

### importOTtelem.py

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
	