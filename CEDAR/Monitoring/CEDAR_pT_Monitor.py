# Author: Chandler Kenworthy
# Inspired by Adam's original script

# To get the Cedar_PTMonitor.txt file:
# 1. Log onto LXPLUS
# 2. ssh cctdaq@na62primitive.cern.ch (password same as username)
# 3. Copy the file from /home/sw/Cedar to wherever you are running this script
# 4. Run the script with python CEDAR_pT_Monitor.py

import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
#import mplhep as hep # May need to uncomment as LXPLUS doesn't have this package by default
#hep.style.use(hep.style.ROOT) # it is just used to make the plots look ROOT style and nice

OPTIMAL_P_T_REAR = 13.124 # mbar/K
OPTIMAL_PRESSURE_AT_T_ROOM = 3846 # mbar
ROOM_TEMPERATURE = 293.1 # kelvin

# Time, pressure, front, rear, diaphragm
df = pd.read_csv('Cedar_PTMonitor.txt', header=None, delimiter=' ')
df.columns = ["Timestamp", "Pressure", "Front", "Rear", "Diaphragm"]
df["DateTime"] = [datetime.fromtimestamp(time) for time in df["Timestamp"]] # There is a nicer pandas way to do this I just cant remember
df["Pressure"] *= 1e+3 # Convert bar -> mbar
df[["Front", "Rear", "Diaphragm"]] += 273
df["p_Tr"] = df["Pressure"]/df["Rear"] # p/T_rear
df["p_Tf"] = df["Pressure"]/df["Front"] # p/T_front

# Group data points by day for now, it is easy
df['TimestampFloor'] = pd.to_datetime(df['DateTime']).dt.floor("H") # Squash dates to nearest hour
g = df.groupby("TimestampFloor").mean() # Group data into hour chunks and average them

# Make plot of p/T (add second axis with actual pressure)
fig, ax = plt.subplots(1, 1, figsize=(10, 7))
plt.xticks(rotation=60, fontsize=16)
ax1 = ax.twinx()
a = ax.scatter(g.index, g["p_Tr"], color="blue", label=r"$p/T_{rear}$", s=8)
b = ax.scatter(g.index, g["p_Tf"], color="red", label=r"$p/T_{front}$", s=8)
c = ax1.scatter(g.index, g["Pressure"], color="green", label="Pressure", s=8)
ax1.set_ylabel("Pressure [mbar]")
ax.set_ylabel("Pressure / Temperature [mbar/K]") # Pressure (at 293.15 K) [bar]
ax.grid() # Draw grid lines
ax.hlines([OPTIMAL_P_T_REAR], xmin=g.index[0], xmax=g.index[-1], color="k", linestyle="--", label=r"$p/T{rear}|_{opt}$")
lines, labels = ax.get_legend_handles_labels() # Nicer legend
lines2, labels2 = ax1.get_legend_handles_labels() # Nicer legend
l = ax1.legend(lines + lines2, labels + labels2, frameon=True, edgecolor="#000", fancybox=False, fontsize=18, markerscale=3, loc="lower right")
l.get_frame().set_alpha(1)
fig.tight_layout()
plt.savefig("cedar_p_over_t.pdf")
plt.close()

# Make plot of p(at room temperature) (add second axis with actual pressure)
fig, ax = plt.subplots(1, 1, figsize=(10, 7))
plt.xticks(rotation=60, fontsize=16)
ax1 = ax.twinx()
a = ax.scatter(g.index, g["p_Tr"] * ROOM_TEMPERATURE, color="blue", label=r"$p/T_{rear}$", s=8)
b = ax.scatter(g.index, g["p_Tf"] * ROOM_TEMPERATURE, color="red", label=r"$p/T_{front}$", s=8)
c = ax1.scatter(g.index, g["Pressure"], color="green", label="Pressure", s=8)
ax1.set_ylabel("Pressure [mbar]")
ax.set_ylabel("Pressure (R.T) [mbar]") # Pressure (at 293.15 K) [mbar]
ax.grid() # Draw grid lines
ax.hlines([OPTIMAL_PRESSURE_AT_T_ROOM], xmin=g.index[0], xmax=g.index[-1], color="k", linestyle="--", label=r"$p_{RT}|_{opt}$")
lines, labels = ax.get_legend_handles_labels() # Nicer legend
lines2, labels2 = ax1.get_legend_handles_labels() # Nicer legend
l = ax1.legend(lines + lines2, labels + labels2, frameon=True, edgecolor="#000", fancybox=False, fontsize=18, markerscale=3, loc="lower right")
l.get_frame().set_alpha(1)
fig.tight_layout()
plt.savefig("cedar_p_over_t_rt.pdf")
plt.close()

ptroom_curr = (g["p_Tr"] * ROOM_TEMPERATURE)[-1]
delta_ptroom = ptroom_curr - OPTIMAL_PRESSURE_AT_T_ROOM

# Calculate the pressure order required | the current temperature at the CEDAR rear
delta_pt = ((OPTIMAL_P_T_REAR - g["p_Tr"][-1]) * g["Rear"][-1])
pressure_order = delta_pt + g["Pressure"][-1]
# pressure order is delta(p/T_rear) [mbar/K] * current temperature, average temperatures over last 12 hrs for accuracy

if(delta_ptroom < 0):
    print(f"CEDAR requires FILLING. Given the current rear temperature ({g['Rear'][-1]:.2f}K = {(g['Rear'][-1]-273):.2f}C) you need to issue a pressure order of {pressure_order:.2f} mbar (+{delta_pt:.2f} mbar)")
if(delta_ptroom > 0):
    print(f"CEDAR requires DRAINING. Given the current rear temperature ({g['Rear'][-1]:.2f}K = {(g['Rear'][-1]-273):.2f}C) you need to issue a pressure order of {pressure_order:.2f} mbar")
