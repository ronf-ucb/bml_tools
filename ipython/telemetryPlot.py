# telemetry plotting function for overview state data
import numpy as np
import matplotlib.pyplot as plot
def telemetryPlot(S):
    #TODO: These should be moved to an "overview plot" function
    length = 16
    width = 8
    fig = plot.figure(figsize = (length,width))

    # gyro data
    plot.subplot(3,2,1)
    plot.plot(S.time, S.GyroX,'k--')
    plot.plot(S.time, S.GyroY, 'g.')
    plot.plot(S.time, S.GyroZ, 'b')
    xlabel('time [ms]')
    ylabel('Gyro rad/s')
    legend(['X', 'Y', 'Z'])

    # actual and commanded leg position
    plot.subplot(3,2,2)
    plot.plot(S.time, S.rightLegPos,'k')
    plot.plot(S.time, S.leftLegPos,'b--')
    plot.plot(S.time, S.commandedRightLegPos)
    plot.plot(S.time, S.commandedLeftLegPos)
    xlabel('time [ms]')
    ylabel('Leg Position')
    legend(['RPos','LPos','Rref','Lref'])

    # accelerometer data
    plot.subplot(3,2,3)
    plot.plot(S.time, S.AX,'k--')
    plot.plot(S.time, S.AY,'g.')
    plot.plot(S.time, S.AZ,'b')
    xlabel('time [ms]')
    ylabel('Accel $ m s^{-2}$')
    legend(['X', 'Y', 'Z'])

    #back EMF
    plot.subplot(3,2,4)
    plot.plot(S.time, S.RBEMF,'k')
    plot.plot(S.time, S.LBEMF,'b--')
    xlabel('time [ms]')
    ylabel('Back EMF (V)')
    legend(['Right', 'Left'])
    ax = fig.add_subplot(3,2,4)
    ax.axhline(linewidth=1, color='m')

    # Motor PWM 
    plot.subplot(3,2,5)
    plot.plot(S.time, S.DCR,'k')
    plot.plot(S.time, S.DCL,'b--')
    xlabel('time [ms]')
    ylabel('Duty Cycle (%)')
    legend(['Right', 'Left'])
    ax = fig.add_subplot(3,2,5)
    ax.axhline(linewidth=1, color='m')

    #battery voltage
    plot.subplot(3,2,6)
    plot.plot(S.time, S.VBatt)
    xlabel('time [ms]')
    ylabel('Battery Voltage (V)')
