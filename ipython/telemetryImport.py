import numpy as np

def telemetryImport(filename):
    file = open(filename)
    print "Importing ",filename

    S = TelemetryData()
    S.filename = file; #save filename with structure
    
    lines = file.readlines()
    file.close()
    
    # Time and Date stamps of trial
    S.dateStamp = lines[0].split()[3]
    S.timeStamp = lines[0].split()[4][:-1]

    # Stride Frequency R,L
    S.rightStrideFreq = float(lines[1].split()[5][:-1])
    S.leftStrideFreq = float(lines[2].split()[5][:-1])

    # Phase (fractional)
    S.phaseFractional = float(lines[3].split()[4][:-1])

    # Script that generated data
    S.script = lines[4].split()[1]

    # Motor Gains
    S.motorGains = map(float, lines[5][lines[5].find('[')+1:lines[5].find(']')].replace(',','').split())

    # test data read
    #print 'lines[8:15]', lines[8:15]

    # Data splitting
    columnHeaders = lines[7].replace("\"% ","").replace(" \"\r\n","").split(' | ')
    columns = len(columnHeaders)
    rows = len(lines)-8
    # unix: data = np.reshape(map(float,"".join(lines[8:]).replace('\r\n',',')[:-1].split(',')),(rows,columns))
    # windows
    data = np.reshape(map(float,"".join(lines[8:]).replace('\n',',')[:-1].split(',')),(rows,columns))

    # Timestamps
    S.time = data[:,0]/1000.0

    # Leg Position R,L
    S.rightLegPos = data[:,1]*S.legScale
    S.leftLegPos = data[:,2]*S.legScale

    # Commanded Leg Position R,L
    S.commandedRightLegPos = data[:,3]*S.legScale
    S.commandedLeftLegPos = data[:,4]*S.legScale

    # Duty Cycle R,L
    #DCR = -data[:,5]/4000.0
    #DCL = -data[:,6]/4000.0
    #DCR[DCR < -4000.0] = -4000.0
    #DCL[DCL < -4000.0] = -4000.0
    # raw 12 bit PWM value. Max = 3900.
    # convert to per cent
    S.DCR = 100.0 * data[:,5]/4096.0  # This is incorrect. PWM is not a 12 bit value. PWM is a 16 bit register. Maximum PWM is set by PTPER. AP 9/26/2014, TODO: make correct
    S.DCL = 100.0 * data[:,6]/4096.0  # This is incorrect. PWM is not a 12 bit value. PWM is a 16 bit register. Maximum PWM is set by PTPER. AP 9/26/2014, TODO: make correct

    # Gyro X,Y,Z
    S.GyroX = data[:,7]*S.gyroScale
    S.GyroY = data[:,8]*S.gyroScale
    S.GyroZ = data[:,9]*S.gyroScale

    # Accelerometer X,Y,Z
    S.AX = data[:,10]*S.xlScale
    S.AY = data[:,11]*S.xlScale
    S.AZ = data[:,12]*S.xlScale

    # BackEMF R,L
    # A/D data is 10 bits, Vref+ = AVdd = 3.3V, VRef- = AVss = 0.0V
    # BEMF volts = (15K)/(47K) * Vm + vref/2 - pidObjs[i].inputOffset
    #RBEMF = -data[:,13]*vdivide*vref/1023.0
    #LBEMF = -data[:,14]*vdivide*vref/1023.0
    S.RBEMF = data[:,13]*S.vref/1024.0/S.vgain  # scale A/D to 0 to 3.3 V range and undo diff amp gain
    S.LBEMF = data[:,14]*S.vref/1024/S.vgain

    # Battery Voltage in volts
    S.VBatt = data[:,15]*S.vdivide*S.vref/1023.0

    #Power calculation
    # i_m = (VBatt - BEMF)/R
    # V_m is just VBatt
    #PowerR = np.abs((DCR/4096.0)*VBatt*(VBatt - RBEMF)/RMotor) # P = V_m i_m x duty cycle
    #PowerL = np.abs((DCL/4096.0)*VBatt*(VBatt - LBEMF)/RMotor) # P = V_m i_m x duty cycle
    # using motor duty cycle as 0-100%
    S.PowerR = np.abs((S.DCR/100.0)*S.VBatt*(S.VBatt - S.RBEMF)/S.RMotor) # P = V_m i_m x duty cycle
    S.PowerL = np.abs((S.DCL/100.0)*S.VBatt*(S.VBatt - S.LBEMF)/S.RMotor) # P = V_m i_m x duty cycle

    S.Energy = np.zeros(len(S.VBatt))
    S.EnergyL = np.zeros(len(S.VBatt))
    S.EnergyR = np.zeros(len(S.VBatt))
    # This is a terrible way to report the delta t for the file. This is why timestamps are recorded in microseconds.
    # The average and standard deviation of all time differences should be stored. AP 9/26/2014
    S.dt = (S.time[1] - S.time[0]) / 1000.0 # time in seconds
    
    #print 'dt=', dt
    #energy calculation
    # This is an unnecessarily complicated way of integrating an array. Change to use trapz below. AP 9/26/2014
    #for i in range(1,len(VBatt)):
    #    S.Energy[i] = Energy[i-1] + (S.PowerR[i] + S.PowerL[i]) * dt
        
    S.EnergyL = np.trapz(S.PowerL, dx = S.dt)
    S.EnergyR = np.trapz(S.PowerR, dx = S.dt)
    S.Energy = S.EnergyL + S.EnergyR

    # torque calculation
    # This should include capability to have different resistances for each motor. AP 9/26/2014
    S.TorqueR = (S.DCR/100.0)*S.Kt*(S.VBatt - S.RBEMF)/S.RMotor # \Tau = Kt i_m x duty cycle
    S.TorqueL = (S.DCL/100.0)*S.Kt*(S.VBatt - S.LBEMF)/S.RMotor # \Tau = Kt i_m x duty cycle
        
    # Motor Voltage, R,L
    S.VMotorR = S.VBatt*S.DCR
    S.VMotorL = S.VBatt*S.DCL
    
    S.numSamples = data.shape[0]
    print "Got",S.numSamples,"samples"
    
    return S
    
    
class TelemetryData:

    #Constants saved inside structure, for completeness
    
    legScale = 95.8738e-6 # 16 bit to radian
    vref = 3.3 # for voltage conversion
    vdivide = 3.7/2.7  # for battery scaling
    vgain = 15.0/47.0  # gain of differential amplifier
    RMotor = 3.3   # resistance for SS7-3.3 ** need to check **
    Kt = 1.41 #  motor toriqe constant mN-m/A  ** SS7-3.3 **

    #acelerometer scale in mpu6000.c set to +- 8g
    # +- 32768 data
    xlScale = (1/4096.0) * 9.81

    # gyro in mpu6000.c scale set to +-2000 degrees per second
    # +- 32768
    gyroScale = (1/16.384) * (np.pi/180.0)  

    length = 16
    width = 8
    
    # Metadata
    filename = ""
    dateStamp = None
    timeStamp = None
    rightStrideFreq = None
    leftStrideFreq = None
    phaseFractional = None
    script = None
    motorGains = None
    
    # Recorded data
    time = None
    rightLegPos = None
    leftLegPos = None
    commandedRightLegPos = None
    commandedLeftLegPos = None
    DCR = None
    DCL = None
    GyroX = None
    GyroY = None
    GyroZ = None
    AX = None
    AY = None
    AZ = None
    RBEMF = None
    LBEMF = None
    VBatt = None
    PowerR = None
    PowerL = None
    dt = None
    TorqueR = None
    TorqueL = None
    VMotorR = None
    VMotorL = None
    