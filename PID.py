def PID(Kp, Ki, Kd, MV_bar=0, beta=1, gamma=0):
    P=0
    I=0
    D=0
    eD_prev=0
    t_prev=0


    while True:
        t,PV,SP,TR = yield MV

        I=TR-MV_bar-P-D

        P=Kp*(beta*SP - PV)
        I=I+Ki*(SP-PV)*(t-t_prev)


        D=Kd*(eD-eD_prev)/(t-t_prev)
        MV=MV_bar + P + I + D


        eD_prev = eD_prev
        t_prev=t




print(PID())


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.filters import gaussian_filter1d

# Update the t_end and n_steps values for 10 iterations
t_start = 0
t_end = 500
n_steps = 50
dt = (t_end - t_start) / n_steps
time_values = [t_start + i*dt for i in range(n_steps)]
# We will use a constant target value (10)
setpoint_values = [10 for _ in time_values]

# Our starting value is 0, it will be updated in the next steps with the values coming from the PID control
measurements = [0]
errors = [setpoint_values[0] - measurements[0]]

def baptiste(alexandre):
    return 1+alexandre

def PID2(Kp,Ki,Kd):
    val_P=[0]
    val_I=[0]
    val_D=[0]
    val_PID=[0]

    I=0
    erreur_ant=0



    for i in range(1,n):
        e=erreur[-1]
        I=I+dt*e
        