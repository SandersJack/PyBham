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



directory = '/afs/cern.ch/work/j/jsanders/Software/CedarAlignment/clicks/pro/'

mu_Hits = []
mu_CandHits = []
mu_SelCandHits = []

mu_Hits_Arg = []
mu_CandHits_Arg = []
mu_SelCandHits_Arg = []

cand = []

_burst = []
burst = []
cand_Arg = []

name = "CLICKS"

for filename in os.scandir(directory):
    if filename.is_file():
        if ".root" not in filename.path:
            continue
        file_name = filename.path
        
        try: 
            inFile = uproot.open(file_name)
        except ValueError:
            continue
        except OSError:
            continue
        
        burst = inFile['SpecialTrigger;1']['EventHeader/fBurstID'].array()
        
        try:
            burst = burst[1]
        except ValueError:
            continue
        
        print("Burst Number: ", burst)
        
        h_NRecoCand = inFile["CedarMonitor/NCandidates"]
        
        h_NRecoHits = inFile["CedarMonitor/NRecoHits"]
        
        h_NHitsInCandidate = inFile["CedarMonitor/NRecoHitsInCandidate"]
        
        h_NRecoHitsInSelectedCandidate = inFile["CedarMonitor/NRecoHitsInSelectedCandidate"]
        
        burst = inFile['SpecialTrigger;1']['EventHeader/fBurstID'].array()
        
        runno = inFile['SpecialTrigger;1']['EventHeader/fRunID'].array()
        
        Arg = inFile['SpecialTrigger;1']['Beam/fARGONION']
        
        Arg_count = -99
        try:
            Arg_count = Arg["fARGONION.fCounts"].array()[1]
        except ValueError:
            continue
        
        burst = burst[0]
        
        if runno[0] > 12925:
            burst+=100
        
        
        
        _burst.append(burst)
        print("Arg Count: ", Arg_count)
        
        can = h_NRecoCand.member("fTsumwx")/h_NRecoCand.member("fEntries")
        cand.append(can)  
        cand_Arg.append(can/Arg_count)    

        mu1 = h_NRecoHits.member("fTsumwx")/h_NRecoHits.member("fEntries")
        mu_Hits.append(mu1)
        mu_Hits_Arg.append(mu1/(Arg_count))
        

        mu2 = h_NHitsInCandidate.member("fTsumwx")/h_NHitsInCandidate.member("fEntries")
        mu_CandHits.append(mu2)
        mu_CandHits_Arg.append(mu2/(Arg_count))

        try:
            mu3 = h_NRecoHitsInSelectedCandidate.member("fTsumwx")/h_NRecoHitsInSelectedCandidate.member("fEntries")
        except ZeroDivisionError:
            mu3 = 0
        mu_SelCandHits.append(mu3)
        mu_SelCandHits_Arg.append(mu3/(Arg_count))
        
        print("---------------------")
        


fig4, axs4 = plt.subplots(figsize=(10,10))

axs4.scatter(_burst,mu_Hits,marker="x",label="Reco")
axs4.scatter(_burst,mu_CandHits,marker="x",label="Cand")
axs4.scatter(_burst,mu_SelCandHits,marker="x",label="Sel Cand")

axs4.set_ylabel("Number of Hits")
axs4.set_xlabel("Aperature [mm]")
axs4.xaxis.set_major_locator(plt.MaxNLocator(20))
axs4.tick_params(axis='x', labelrotation = 90)
#axs4.set_ylim(15,18)
axs4.legend()
save_file = "output/DiaScan/{}.1.png".format(name)
plt.savefig(save_file)

fig5, axs5 = plt.subplots(figsize=(10,10))

axs5.scatter(_burst,mu_Hits_Arg,marker="x",label="Reco")
axs5.scatter(_burst,mu_CandHits_Arg,marker="x",label="Cand")
axs5.scatter(_burst,mu_SelCandHits_Arg,marker="x",label="Sel Cand")

axs5.set_ylabel("Number of Hits Normalise to Argonion")
axs5.set_xlabel("Aperature [mm]")
axs5.xaxis.set_major_locator(plt.MaxNLocator(20))
axs5.tick_params(axis='x', labelrotation = 90)
axs5.set_ylim(0,0.1e-6)
axs5.legend()

save_file = "output/DiaScan/{}.2.png".format(name)
plt.savefig(save_file)

fig6, axs6 = plt.subplots(figsize=(10,10))

axs6.scatter(_burst,mu_Hits,marker="x",label="Reco")
axs6.scatter(_burst,mu_CandHits,marker="x",label="Cand")
axs6.scatter(_burst,mu_SelCandHits,marker="x",label="Sel Cand")

axs6.set_ylabel("Number of Hits")
axs6.set_xlabel("Aperature [mm]")
axs6.xaxis.set_major_locator(plt.MaxNLocator(20))
axs6.tick_params(axis='x', labelrotation = 90)
axs6.set_ylim(11,13)
axs6.legend()

save_file = "output/DiaScan/{}.3.png".format(name)
plt.savefig(save_file)

fig8, axs8 = plt.subplots(figsize=(10,10))

axs8.scatter(_burst,mu_Hits_Arg,marker="x",label="Reco")
axs8.scatter(_burst,mu_CandHits_Arg,marker="x",label="Cand")
axs8.scatter(_burst,mu_SelCandHits_Arg,marker="x",label="Sel Cand")

axs8.set_ylabel("Number of Hits Normalise to Argonion")
axs8.set_xlabel("Aperature [mm]")
axs8.xaxis.set_major_locator(plt.MaxNLocator(20))
axs8.tick_params(axis='x', labelrotation = 90)
axs8.set_ylim(11,13)
axs8.legend()

save_file = "output/DiaScan/{}.4.png".format(name)
plt.savefig(save_file)

fig9, axs9 = plt.subplots(figsize=(10,10))

axs9.scatter(_burst,mu_Hits,marker="x",label="Reco")
axs9.scatter(_burst,mu_CandHits,marker="x",label="Cand")
axs9.scatter(_burst,mu_SelCandHits,marker="x",label="Sel Cand")

axs9.set_ylabel("Number of Hits")
axs9.set_xlabel("Aperature [mm]")
axs9.xaxis.set_major_locator(plt.MaxNLocator(20))
axs9.tick_params(axis='x', labelrotation = 90)
axs9.set_ylim(4,5)
axs9.legend()

save_file = "output/DiaScan/{}.5.png".format(name)
plt.savefig(save_file)

fig10, axs10 = plt.subplots(figsize=(10,10))

axs10.scatter(_burst,mu_Hits_Arg,marker="x",label="Reco")
axs10.scatter(_burst,mu_CandHits_Arg,marker="x",label="Cand")
axs10.scatter(_burst,mu_SelCandHits_Arg,marker="x",label="Sel Cand")

axs10.set_ylabel("Number of Hits Normalise to Argonion")
axs10.set_xlabel("Aperature [mm]")
axs10.xaxis.set_major_locator(plt.MaxNLocator(20))
axs10.tick_params(axis='x', labelrotation = 90)
axs10.set_ylim(4,5)
axs10.legend()

save_file = "output/DiaScan/{}.6.png".format(name)
plt.savefig(save_file)

fig11, axs11 = plt.subplots(figsize=(10,10))

axs11.scatter(_burst,cand,marker="x",label="NCandidates")

axs11.set_ylabel("Number of Can_bursttes")
axs11.set_xlabel("Aperature [mm]")
axs11.xaxis.set_major_locator(plt.MaxNLocator(20))
axs11.tick_params(axis='x', labelrotation = 90)
axs11.legend()

save_file = "output/DiaScan/{}.7.png".format(name)

plt.savefig(save_file)

fig12, axs12 = plt.subplots(figsize=(10,10))

axs12.scatter(_burst,cand_Arg,marker="x",label="NCandidates")

axs12.set_ylabel("Number of Can_bursttes Normlised to Argonian")
axs12.set_xlabel("Aperature [mm]")
axs12.xaxis.set_major_locator(plt.MaxNLocator(20))
axs12.tick_params(axis='x', labelrotation = 90)
axs12.legend()

save_file = "output/DiaScan/{}.8.png".format(name)
axs12.set_ylim(0,0.3e-7)
plt.savefig(save_file)


plt.show()