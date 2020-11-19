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
