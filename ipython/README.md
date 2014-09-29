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
