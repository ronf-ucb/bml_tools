import os
import csv


class OTData:
    def __init__(self):
        self.handedness = 'RIGHT'
        self.framecount = 0
        self.TrackableCount = 0
        self.RigidBodies = []
        self.Trackables = []
        self.Frames = []
    
class RigidBody:
    def __init__(self):
        self.Name = None
        self.ID = None
        self.MarkerCount = 0
        self.MarkerPositions = []
    
class Frame:
    def __init__(self):
        self.FrameIndex = None
        self.Timestamp = None
        self.TrackableCount = 0
        self.Trackables = []
        self.MarkerCount = 0
        self.MarkerData = []
        self.MarkerIDs = []

class Trackable:
    def __init__(self):
        self.FramesPresent = []
        self.TrackedTimestamps = []
        self.Name = None
        self.ID = None
        self.FramesSinceLastTracked = None
        self.MarkerCount = 0
        self.MarkerData = []
        self.PointCloud = []
        self.MarkerTracked = 0
        self.MarkerQuality = 0
        self.MeanError = 0
        self.Position = []
        self.Quaternion = []
        self.Euler = []

class TrackableEntry:
    def __init__(self):
        FrameIndex = None
        Timestamp = None
        Name = None
        ID = None
        FramesSinceLastTracked = 0
        MarkerCount = 0
        MarkerData = []
        PointCloud = []
        MarkerTracked = []
        MarkerQuality = None
        MeanError = None
        
class FrameTrackable:
    def __init__(self):
        self.ID = None
        self.Position = []
        self.Quaternion = []
        self.Euler = []


def importOTdata(filename):
    file = open(filename)
    rawfile = file.readlines()
    reader = csv.reader(file)

    trackdataraw = []
    framedataraw = []
    
    file.seek(0)
    S = OTData()

    for row in reader:
        if row[0] == 'trackable':
            trackdataraw.append(row)
        if row[0] == 'frame':
            framedataraw.append(row)
        if row[0] == 'info':
            if row[1] == 'trackablecount':
                S.TrackableCount = int(row[2])
            if row[1] == 'framecount':
                S.framecount = int(row[2])
        if row[0] == 'righthanded':
            S.handedness = 'RIGHT'
            



    fixed = []
    for item in framedataraw:
        fixed.append( map(lambda x: 'NAN' if x == '-1.#IND0000' else x,item) )
    framedataraw = fixed;



    # The first trackablecount entries in trackdataraw will all be trackable definitions
    # This will populate all rigid bodies and the associated marker data
    S.RigidBodies = [];
    for i in range(0,S.TrackableCount):
        thisrow = trackdataraw[i] #for clarity
        newRB = RigidBody()
        newRB.Name = thisrow[1]
        newRB.ID = int(thisrow[2])
        markerdata = map(float, thisrow[3:])
        newRB.MarkerCount = int( markerdata[0] )
        coords = markerdata[2:];
        newRB.MarkerPositions = [coords[(3*j):(3*j)+3] for j in range(0,len(coords)/3)];
        S.RigidBodies.append( newRB )



    # Parse all the 'frame' lines
    for thisframe in framedataraw:
        newFrame = Frame()
        fdata = map(float, thisframe[1:])
        newFrame.FrameIndex = int(fdata[0])
        newFrame.Timestamp = fdata[1]
        newFrame.TrackableCount = int( fdata[2] )
        trackdata = fdata[3:(3+11*newFrame.TrackableCount)]
        rest = fdata[(3+11*newFrame.TrackableCount):]  # rest of the data
        trackdata = [trackdata[j:j+11] for j in range(0,11*newFrame.TrackableCount,11)];
        for item in trackdata:    #for each trackable reported in this frame ...
            newFrameTrackable = FrameTrackable()
            newFrameTrackable.ID = int(item[0])
            newFrameTrackable.Position = item[1:4]
            newFrameTrackable.Quaternion = item[4:8]
            newFrameTrackable.Euler = item[8:11]
            newFrame.Trackables.append(newFrameTrackable)
        
        newFrame.MarkerCount = int(rest[0])
        markerdata = rest[1:]
        newFrame.MarkerIDs = map( int, [markerdata[4*k+3] for k in range(newFrame.MarkerCount)])
        newFrame.MarkerData = [markerdata[4*k:4*k+3] for k in range(newFrame.MarkerCount)]
        
        S.Frames.append(newFrame)



    temptrackables = []

    for thistrack in trackdataraw[len(S.RigidBodies):]:
        tdata = thistrack[1:]
        newtrack = TrackableEntry()
        newtrack.FrameIndex = int(tdata[0])
        newtrack.Timestamp = float(tdata[1])
        newtrack.Name = tdata[2]
        newtrack.ID = int(tdata[3])
        newtrack.FramesSinceLastTracked = int(tdata[4])
        newtrack.MarkerCount = int(tdata[5])
        rest = map(float,tdata[6:])
        idx = 0
        newtrack.MarkerData = [rest[idx+3*k:3*(k+1)] for k in range(newtrack.MarkerCount)]
        idx = idx + 3*newtrack.MarkerCount
        newtrack.PointCloud = [rest[idx+3*k:idx+3*(k+1)] for k in range(newtrack.MarkerCount)]
        idx = idx + 3*newtrack.MarkerCount
        newtrack.MarkerTracked = map(int, rest[idx:idx+newtrack.MarkerCount])
        idx = idx + newtrack.MarkerCount
        newtrack.MarkerQuality = rest[idx:idx+newtrack.MarkerCount]
        idx = idx + newtrack.MarkerCount
        newtrack.MeanError = rest[idx]
        
        temptrackables.append(newtrack)



    uniqueIDs = set([item.ID for item in S.RigidBodies])
    for rb in S.RigidBodies:
        newtrack = Trackable()
        newtrack.ID = rb.ID
        newtrack.name = rb.Name
        newtrack.FramesSinceLastTracked = [tt.FramesSinceLastTracked for tt in temptrackables]
        fp = []
        trackedtimestamps = []
        for frame in S.Frames:
            ids = [trackable.ID for trackable in frame.Trackables]
            if rb.ID in ids:
                fp.append(frame.FrameIndex)
                trackedtimestamps.append(frame.Timestamp)
        newtrack.FramesPresent = fp
        newtrack.TrackedTimestamps = trackedtimestamps

        #Just congregating info from here down
        newtrack.MarkerCount =   [tt.MarkerCount for tt in temptrackables]
        newtrack.MarkerData =    [tt.MarkerData for tt in temptrackables]
        newtrack.PointCloud =    [tt.PointCloud for tt in temptrackables]
        newtrack.MarkerTracked = [tt.MarkerTracked for tt in temptrackables]
        newtrack.MarkerQuality = [tt.MarkerQuality for tt in temptrackables]    
        newtrack.MeanError =     [tt.MeanError for tt in temptrackables]      
        
        #Extract all position data into a series PER TRACKABLE
        pos = []
        quat = []
        eul = []
        for frame in S.Frames:
           for trackable in frame.Trackables:
                if trackable.ID == rb.ID:
                    pos.append(trackable.Position)
                    quat.append(trackable.Quaternion)
                    eul.append(trackable.Euler)
        newtrack.Position = pos
        newtrack.Quaternion = quat
        newtrack.Euler = eul
        
        # Finished building trackable structure, add to top level object
        S.Trackables.append(newtrack)

    file.close()
    
    return S


