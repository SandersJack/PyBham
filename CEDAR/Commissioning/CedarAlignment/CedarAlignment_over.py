import uproot
import numpy as np
import matplotlib.pyplot as plt
#import mplhep as hep
#plt.style.use(hep.style.ROOT)
import pandas as pd
from csv import writer
from scipy.stats import norm
import argparse
import os
import seaborn as sns

directory = '/eos/user/j/jsanders/cedar_roots/Alignment_Nitrogen/'

c = 0

Motor_x = []
Motor_y = []
Nhits = []

for filename in os.scandir(directory):
    if filename.is_file():
        
        if "tar" in filename.path:
            continue
        
        if ".root" not in filename.path:
            continue


        try: 
            inFile = uproot.open(filename)
        except ValueError:
            continue
        except OSError:
            continue

        h_NRecoHitsInSelectedCandidate = inFile["CedarMonitor/NRecoHitsInSelectedCandidate"]
        
        h_NSectorsInSelectedCandidate = inFile["CedarMonitor/NSectorsInSelectedCandidate"]
        
        cur_M_X = min(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fMotorPosX'].array())
        cur_M_Y = min(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fMotorPosY'].array())

        burst = inFile['SpecialTrigger;1']['EventHeader/fBurstID'].array()[0]


        fig, axs = plt.subplots(1, 1,figsize=(10,10))
        ax1 = axs

        # Plot 1

        bins_sel = h_NRecoHitsInSelectedCandidate.axis().edges()
        weight_sel = h_NRecoHitsInSelectedCandidate.counts()

        counts, bins, bars = ax1.hist(bins_sel[1:],bins_sel, weights=weight_sel)#, label="NHits (Sel): mu = {}".format(mu))

        value = []
        for i in range(len(bins[1:])):
            for t in range(int(counts[i])):
                value.append(bins[i])

        mu, std = norm.fit(value)
        
        if mu < 15:
            continue
        

        Nhits.append(mu)
        Motor_x.append((round(cur_M_X*1000)/1000))
        Motor_y.append((round(cur_M_Y*1000)/1000))
        
        print(burst, Motor_x[-1], Motor_y[-1])
        
        x = np.linspace(10, 30, 100)

        p = norm.pdf(x, loc=mu,scale=std)

        counts_sum = sum(counts)

        p = p*counts_sum

        ax1.plot(x, p, 'k', linewidth=2, label="NHits (Sel): mu = {}".format(mu))
        print("Fit Data: mu = {}".format(mu))

        ax1.set_xlim(0,40)
        ax1.legend()
        ax1.set_title("Number of Reco Hits in Candidate")
        
        plt.clf()
        plt.close()
        

fig, axs = plt.subplots(1, 1,figsize=(10,10))

axs.plot(Motor_x,Nhits)
axs.set_xlabel("X motor [mm]")
axs.set_ylabel("Nhits in Selected Candidate")

fig, axs2 = plt.subplots(1, 1,figsize=(10,10))

axs2.plot(Motor_y,Nhits)
axs2.set_xlabel("Y motor [mm]")
axs2.set_ylabel("Nhits in Selected Candidate")

fig, axs3 = plt.subplots(1, 1,figsize=(20,10))


#axs3.pcolormesh(Motor_x,Motor_y,Nhits)

Nhits = np.array(Nhits)
Motor_x = np.array(Motor_x)
Motor_y = np.array(Motor_y)


#df = pd.DataFrame(data=[Nhits], columns=Motor_x, index=Motor_y)
df = pd.DataFrame(list(zip(Motor_x, Motor_y,Nhits)),columns =['MotorX', 'MotorY','NHits'])

#print(df)
#print(df.groupby(['MotorX', 'MotorY'], as_index=False)['NHits'].mean())
error = df.groupby(['MotorX', 'MotorY'], as_index=False)['NHits'].sem()

df = df.groupby(['MotorX', 'MotorY'], as_index=False)['NHits'].mean()

pivot = df.pivot(index='MotorY', columns='MotorX', values='NHits')
sns.heatmap(pivot,cmap='coolwarm',annot=True, cbar_kws={'label': 'NHits in Selected Candidate'},fmt=".2f")
#sns.heatmap(df, cmap='coolwarm', square=True,annot=True)
#h1 = axs3.hexbin(df.MotorX, df.MotorY, C=df.NHits, gridsize=50,cmap='coolwarm')

axs3.set_xlabel("X motor [mm]")
axs3.set_ylabel("Y motor [mm]")
axs3.invert_yaxis()
save_file = "output/Align_N_2.png"
plt.savefig(save_file)

fig, axs3 = plt.subplots(1, 1,figsize=(10,10))

pivot = error.pivot(index='MotorY', columns='MotorX', values='NHits')
sns.heatmap(pivot,cmap='coolwarm',annot=True, cbar_kws={'label': 'NHits in Selected Candidate'},fmt=".2f")
#sns.heatmap(df, cmap='coolwarm', square=True,annot=True)
#h1 = axs3.hexbin(df.MotorX, df.MotorY, C=df.NHits, gridsize=50,cmap='coolwarm')

axs3.set_xlabel("X motor [mm]")
axs3.set_ylabel("Y motor [mm]")
save_file = "output/Align_N_2_error.png"
plt.savefig(save_file)
plt.show()