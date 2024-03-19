import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)
import pandas as pd
from csv import writer
from scipy.stats import norm
import argparse
import os
 
time = []
hitpevnt = []



#190, 600
ref_time = ["H_1_5_NTemp_wFF",0] 
ref_P = [2.2,1.61]

coefficients = [0,0] #np.polyfit(ref_time, ref_P, 1)

directory = '/eos/user/j/jsanders/N2_H/pressure/reco/'

c = 0

direcs = ['/eos/user/j/jsanders/pressure/H_1_5_NTemp_wFF_new/kaon/reco','/eos/user/j/jsanders/pressure/H_1_5_NTemp_wFF/proton/reco','/eos/user/j/jsanders/pressure/H_1_5_NTemp_wFF/pip/reco']

A_sec_8 = []
A_sec_7 = []
A_sec_6 = []

Ap_sec_8 = []
Ap_sec_7 = []
Ap_sec_6 = []

Ah_sec_0 = []
Ah_sec_1 = []
Ah_sec_2 = []
Ah_sec_3 = []
Ah_sec_4 = []
Ah_sec_5 = []
Ah_sec_6 = []
Ah_sec_7 = []

A_mu = []
A_presure = []

for t in range(len(direcs)):
    t_sec_8 = []
    t_sec_7 = []
    t_sec_6 = []

    tp_sec_8 = []
    tp_sec_7 = []
    tp_sec_6 = []

    th_sec_0 = []
    th_sec_1 = []
    th_sec_2 = []
    th_sec_3 = []
    th_sec_4 = []
    th_sec_5 = []
    th_sec_6 = []
    th_sec_7 = []

    t_mu = []
    t_presure = []
    for filename in os.scandir(direcs[t]):
        if filename.is_file():
            if "tar" in filename.path:
                continue
            
            if ".root" not in filename.path:
                continue
            file_name = filename.path
            
            try: 
                inFile = uproot.open(file_name)
            except ValueError:
                continue
            
            h_NRecoHits = inFile["CedarMonitor/NRecoHits"]
            
            NEvnts = inFile['SpecialTrigger;1']['EventHeader/fEventNumber']
            
            h_NSectorsInCandidate = inFile["CedarMonitor/NSectorsInCandidate"]
            
            h_NRecoHitsInSector = inFile["CedarMonitor/NRecoHitsInSector"].values()
            
            presure = inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fPressure'].array()
            
            #print(presure)
            
            h_NSectorsInSelectedCandidate = inFile["CedarMonitor/NSectorsInSelectedCandidate"]
            
            h_NRecoHitsInSelectedCandidate = inFile["CedarMonitor/NRecoHitsInSelectedCandidate"]
            
            nsecCand = h_NSectorsInCandidate.values()
            
            
            Arg = inFile['SpecialTrigger;1']['Beam/fARGONION']
            
            
            burst = inFile['SpecialTrigger;1']['EventHeader/fBurstID'].array()
            
            
            time_stamp = file_name[-35:-25]
            
            pres = 0
            
            pres = file_name[-9:-5]
            
            burst = [0,0]
            
            print("-----------------------")
            print(pres)
            print(time_stamp)
            print(burst[0])
        
            Arg_count = 1
            
            print(Arg_count)
            THits = h_NRecoHits.member('fTsumwx')
            
            t_presure.append(float(pres))
            time.append(burst[0])
            hitpevnt.append(0)
            
            t_sec_8.append(nsecCand[-1])
            t_sec_7.append(nsecCand[-2]+nsecCand[-1])
            t_sec_6.append(nsecCand[-3]+nsecCand[-2]+nsecCand[-1])
            
            tp_sec_8.append((nsecCand[-1])/sum(nsecCand))
            tp_sec_7.append((nsecCand[-2]+nsecCand[-1])/sum(nsecCand))
            tp_sec_6.append((nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/sum(nsecCand))
            
            
            th_sec_0.append(h_NRecoHitsInSector[0])
            th_sec_1.append(h_NRecoHitsInSector[1])
            th_sec_2.append(h_NRecoHitsInSector[2])
            th_sec_3.append(h_NRecoHitsInSector[3])
            th_sec_4.append(h_NRecoHitsInSector[4])
            th_sec_5.append(h_NRecoHitsInSector[5])
            th_sec_6.append(h_NRecoHitsInSector[6])
            th_sec_7.append(h_NRecoHitsInSector[7])
            

            
            bins_sel = h_NRecoHitsInSelectedCandidate.axis().edges()
            weight_sel = h_NRecoHitsInSelectedCandidate.counts()
            
            value = []
            for i in range(len(bins_sel[1:])):
                for t in range(int(weight_sel[i])):
                    value.append(bins_sel[i])

            mu, std = norm.fit(value)
            t_mu.append(mu)
            
            #exit(0)
            print("NHits (Sel): mu = {}".format(mu))
            
    A_sec_8.append(t_sec_8)
    A_sec_7.append(t_sec_7)
    A_sec_6.append(t_sec_6)

    Ap_sec_8.append(tp_sec_8)
    Ap_sec_7.append(tp_sec_7)
    Ap_sec_6.append(tp_sec_6)

    Ah_sec_0.append(th_sec_0)
    Ah_sec_1.append(th_sec_1)
    Ah_sec_2.append(th_sec_2)
    Ah_sec_3.append(th_sec_3)
    Ah_sec_4.append(th_sec_4)
    Ah_sec_5.append(th_sec_5)
    Ah_sec_6.append(th_sec_6)
    Ah_sec_7.append(th_sec_7)
    
    A_presure.append(t_presure)

_sec_8 = []
_sec_7 = []
_sec_6 = []

p_sec_8 = []
p_sec_7 = []
p_sec_6 = []

h_sec_0 = []
h_sec_1 = []
h_sec_2 = []
h_sec_3 = []
h_sec_4 = []
h_sec_5 = []
h_sec_6 = []
h_sec_7 = []

_presure = []

triggers = 1000/0.06

for i in range(len(A_sec_8[0])):
    _sec_8.append((A_sec_8[0][i]+A_sec_8[1][i]*0.24/0.06+A_sec_8[2][i]*0.7/0.06)/triggers)
    _sec_7.append((A_sec_7[0][i]+A_sec_7[1][i]*0.24/0.06+A_sec_7[2][i]*0.7/0.06)/triggers)
    _sec_6.append((A_sec_6[0][i]+A_sec_6[1][i]*0.24/0.06+A_sec_6[2][i]*0.7/0.06)/triggers)
    _presure.append(A_presure[0][i])
    p_sec_8.append(Ap_sec_8[0][i]+Ap_sec_8[1][i]+Ap_sec_8[2][i])
    p_sec_7.append(Ap_sec_7[0][i]+Ap_sec_7[1][i]+Ap_sec_7[2][i])
    p_sec_6.append(Ap_sec_6[0][i]+Ap_sec_6[1][i]+Ap_sec_6[2][i])

fig1, axs1 = plt.subplots(figsize=(10,10))

axs1.scatter(_presure,_sec_8,marker="x",label="At Least 8 Sectors")
axs1.scatter(_presure,_sec_7,marker="x",label="At Least 7 Sectors")
axs1.scatter(_presure,_sec_6,marker="x",label="At Least 6 Sectors")
axs1.set_ylabel("NFold Coincidences per Trigger")
axs1.set_xlabel("Pressure")
axs1.xaxis.set_major_locator(plt.MaxNLocator(20))
axs1.tick_params(axis='x', labelrotation = 90)

save_file = "output/PressureScans/{}-{}.Coin.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig2, axs2 = plt.subplots(figsize=(10,10))


axs2.scatter(_presure,p_sec_8,marker="x",label="At Least 8 Sectors")
axs2.scatter(_presure,p_sec_7,marker="x",label="At Least 7 Sectors")
axs2.scatter(_presure,p_sec_6,marker="x",label="At Least 6 Sectors")
axs2.set_ylabel("Probabilty of NFold Conicidences per Burst")
axs2.set_xlabel("Pressure")
axs2.legend()
axs2.xaxis.set_major_locator(plt.MaxNLocator(20))
axs2.tick_params(axis='x', labelrotation = 90)

save_file = "output/PressureScans/{}-{}.CoinpEvnt.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig3, axs3 = plt.subplots(figsize=(10,10))

axs3.scatter(_presure,_sec_8,marker="x",label="At Least 8 Sectors")
axs3.scatter(_presure,_sec_7,marker="x",label="At Least 7 Sectors")
axs3.scatter(_presure,_sec_6,marker="x",label="At Least 6 Sectors")
axs3.set_ylabel("NFold Coincidences per Trigger")
axs3.set_xlabel("Pressure")
axs3.xaxis.set_major_locator(plt.MaxNLocator(20))
axs3.tick_params(axis='x', labelrotation = 90)
axs3.set_ylim(1e-5,1)
axs3.set_yscale('log')
save_file = "output/PressureScans/{}-{}.Coin_log.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig4, axs4 = plt.subplots(figsize=(10,10))


axs4.scatter(_presure,p_sec_8,marker="x",label="At Least 8 Sectors")
axs4.scatter(_presure,p_sec_7,marker="x",label="At Least 7 Sectors")
axs4.scatter(_presure,p_sec_6,marker="x",label="At Least 6 Sectors")
axs4.set_ylabel("Probabilty of NFold Conicidences per Burst")
axs4.set_xlabel("Pressure")
axs4.legend()
axs4.xaxis.set_major_locator(plt.MaxNLocator(20))
axs4.tick_params(axis='x', labelrotation = 90)
axs4.set_ylim(1e-5,1)
axs3.set_yscale('log')
save_file = "output/PressureScans/{}-{}.CoinpEvnt_log.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

'''
fig3, axs3 = plt.subplots(figsize=(10,10))


axs3.scatter(_presure,h_sec_0,marker="x",label="S_0")
axs3.scatter(_presure,h_sec_1,marker="x",label="S_1")
axs3.scatter(_presure,h_sec_2,marker="x",label="S_2")
axs3.scatter(_presure,h_sec_3,marker="x",label="S_3")
axs3.scatter(_presure,h_sec_4,marker="x",label="S_4")
axs3.scatter(_presure,h_sec_5,marker="x",label="S_5")
axs3.scatter(_presure,h_sec_6,marker="x",label="S_6")
axs3.scatter(_presure,h_sec_7,marker="x",label="S_7")


axs3.set_ylabel("Hits in Sector per Burst")
axs3.set_xlabel("Burst")
axs3.set_xlim(1.5,2.25)
axs3.xaxis.set_major_locator(plt.MaxNLocator(20))
axs3.tick_params(axis='x', labelrotation = 90)
axs3.legend()
save_file = "output/PressureScans/{}-{}.SecHits.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig4, axs4 = plt.subplots(figsize=(10,10))

axs4.scatter(_presure,_mu,marker="x")
axs4.set_ylabel("Number of Hits in Selected Candidate")
axs4.set_xlabel("Presure")
axs4.xaxis.set_major_locator(plt.MaxNLocator(20))
axs4.tick_params(axis='x', labelrotation = 90)

save_file = "output/PressureScans/{}-{}.NHits_Sel.png".format(ref_time[0],ref_time[1])
plt.savefig(save_file)
'''
plt.show()