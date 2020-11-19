# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 08:30:24 2020

@author: Oscar
"""

import os 
import numpy as np
import matplotlib.pyplot as plt
import flopy


#parameters
name = "tutorial01_mf6"
h1 = 100
h2 = 90
Nlay = 10 
N = 101
L = 400
H = 50
k = 1.0


# creating the simulation

sim = flopy.mf6.MFSimulation(
    sim_name = name, exe_name="mf6", version="mf6",
    sim_ws="C:/WRDAPP/mf6.2.0/bin")

# Creating the temporal discretization
tdis = flopy.mf6.ModflowTdis(sim, pname="tdis",
                             time_units="DAYS"
                             , nper=1, perioddata=[(1,1,1)])
#creating the solver package

ims = flopy.mf6.ModflowIms(sim,
                           pname= "ims", complexity="SIMPLE")


#creating the groundwater model
model_nam_file = f'{name}.nam'
gwf = flopy.mf6.ModflowGwf(sim, modelname=model_nam_file)


# now we have to define the entire groundwater model

# Creating the discretization package

bot= np.linspace(-H/Nlay, -H, Nlay)
delrow = delcol = L / ( N - 1 )
dis = flopy.mf6.ModflowGwfdis(gwf, nlay=Nlay, nrow=N, ncol=N, 
                              delr=delrow, delc=delcol, top=0.0, 
                              botm=bot)
# Creating initial conditions

start = h1 * np.ones((Nlay, N, N))
ic = flopy.mf6.ModflowGwfic(gwf, pname="ic", strt=start )


# celltype 1 are unconfined thickness
flopy.mf6.ModflowGwfnpf( gwf, icelltype=1, k=k, save_flows=True)






ic = flopy.mf6.ModflowGwfnpf(gwf, icelltype=1, k=k, save_flows=True)
