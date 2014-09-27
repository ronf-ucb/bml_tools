BML Code Tools
===============

iPython
---------

iPython notebooks go here. This does not include pure python code (.py files) .

Uncertain how usage examples will work for iPython notebooks!

### telemetryImport.py

This provides a simple python function to import telemetry data from a VelociRoACH. A TelemetryData object with named fields is returned.

Example usage:

	In [1]:		from telemetryImport import *
				S = telemetryImport('vr_telem_example.txt')
				S
	
				Importing  vr_telem_example.txt
				Got 100 samples
	Out[2]:
				<telemetryImport.TelemetryData instance at 0x075E6FA8>

### telemetry_plotter.ipynb

This notebook can be used to import telemetry data into an iPython notebook. This will be obsoleted very shortly.
This will become an example of how to use the TelemetryData object after importing.