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

name = "tuto01_mf6"
# hidraulic heads
h1 = 100
h2 = 90
# number of layers
Nlay = 10 
# Mesh dimensions
N = 101
L = 400
H = 50
# number of stress periods
k = 1.0


# creating the simulation

sim = flopy.mf6.MFSimulation(
    sim_name = name, exe_name="C:/WRDAPP/mf6.2.0/bin/mf6", version="mf6",
    sim_ws=".")

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
flopy.mf6.ModflowGwfnpf( gwf, icelltype=1, k=k,
                        save_flows=True,save_specific_discharge=True)


# Creating boundary conditions

# Creating constat head package

chd_rec=[]
chd_rec.append(((1 , int(3*N / 4),int(N / 4)), h2))
for layer in range(0, Nlay):
    for row_col in range(0, N):
        chd_rec.append(((layer, row_col, 0), h1))
        chd_rec.append(((layer, row_col, N - 1), h1))
        if row_col !=0 and row_col!= N - 1:
            chd_rec.append(((layer, 0, row_col), h1))
            chd_rec.append(((layer, N - 1, row_col), h1))

chd = flopy.mf6.ModflowGwfchd(gwf, maxbound=len(chd_rec), 
                              stress_period_data=chd_rec,
                              save_flows=True)

# For looking the chd array

iper = 0
ra = chd.stress_period_data.get_data(key=iper)
print(ra)




# creating output control file OC

headfile = f"{name}.hds"
head_filerecord = [headfile]
budgetfile = f"{name}.bud"
budget_filerecord = [budgetfile]
saverecord = [("HEAD", "ALL"), ("BUDGET", "ALL")]
printrecord = [("HEAD", "LAST")]
oc = flopy.mf6.ModflowGwfoc(gwf, saverecord=saverecord,
                            head_filerecord=head_filerecord
                            , budget_filerecord=budget_filerecord,
                            printrecord=printrecord)

# create the model
sim.write_simulation()

# run the simulation
success, buff= sim.run_simulation()
if not success:
    raise Exception("MODFLOW 6 did not terminate normally.")
    
# Plot map layer 1
# import results
hds = flopy.utils.binaryfile.HeadFile(headfile)
# Take from first stress period
h = hds.get_data(kstpkper=(0,0))
# create the mesh for the graph
x = y = np.linspace(0 , L, N)
fig = plt.figure(figsize=(6,6))
ax=fig.add_subplot(1,1,1, aspect="equal")
c=ax.contour(x, y, h[0], np.arange(90, 100.1, 0.2), colors="black")
plt.clabel(c, fmt="%2.1f")


# Plot map layer 10
# import results
hds = flopy.utils.binaryfile.HeadFile(headfile)
# Take from first stress period
h = hds.get_data(kstpkper=(0,0))
# create the mesh for the graph
x = y = np.linspace(0 , L, N)
fig = plt.figure(figsize=(6,6))
ax=fig.add_subplot(1,1,1, aspect="equal")
c=ax.contour(x, y, h[9], np.arange(90, 100.1, 0.2), colors="black")
plt.clabel(c, fmt="%2.1f")


# plot a cross section along a row
# z = np.linspace(-H / Nlay /2, -H + H/ Nlay / 2,  Nlay)
z = np.linspace(-H/Nlay, -H,  Nlay) #prueba oscar
fig = plt.figure(figsize=(5, 2.5))
ax = fig.add_subplot(1, 1, 1, aspect="auto")
c = ax.contour(x, z , h[:,int( 3*N/4), :], np.arange(0, 100, 0.2), colors="black")#take care about the cell number, not distance!
plt.clabel(c, fmt="%1.1f")

# using pltmapview capabilities
plt.figure()   
bud = flopy.utils.CellBudgetFile(budgetfile, precision="double")
spdis = bud.get_data(text='DATA-SPDIS')[0]
pmv=flopy.plot.PlotMapView(gwf)
pmv.plot_grid(colors='white')
pmv.contour_array(h, levels=[.2, .4, .6, .8], linewidths=3.)
pmv.plot_specific_discharge(spdis, color='black')

