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
from scipy.optimize import curve_fit
 
time = []
hitpevnt = []

_Arg_count = []

_sec_8 = []
_sec_7 = []
_sec_6 = []
_sec_5 = []

_sec_8_comp = []
_sec_7_comp = []
_sec_6_comp = []
_sec_5_comp = []

_sec_5_comp_PiK = []

r76 = []
r87 = []
r86 = []
r85 = []

p_sec_8 = []
p_sec_7 = []
p_sec_6 = []
p_sec_5 = []

h_sec_0 = []
h_sec_1 = []
h_sec_2 = []
h_sec_3 = []
h_sec_4 = []
h_sec_5 = []
h_sec_6 = []
h_sec_7 = []

_mu = []
_presure = []
_presure_comp = []

_temp_Dia = []
_temp_Front = []
_temp_Back = []
_temp_Dia = []

#190, 600
ref_time = ["new_H_PRES","__"] 
ref_P = [2.2,1.61]

file_name = "Testing"


directory = '/afs/cern.ch/work/r/romano/public/013703/'

c = 0

for filename in os.scandir(directory):
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
        except OSError:
            continue
        
        h_NRecoHits = inFile["CedarMonitor/NRecoHits"]
        
        NEvnts = inFile['SpecialTrigger;1']['EventHeader/fEventNumber']
        
        h_NSectorsInCandidate = inFile["CedarMonitor/NSectorsInCandidate"]
        
        h_NRecoHitsInSector = inFile["CedarMonitor/NRecoHitsInSector"].values()
        
        presure = inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fPressure'].array()
        
        h_NSectorsInSelectedCandidate = inFile["CedarMonitor/NSectorsInSelectedCandidate"]
        
        h_NRecoHitsInSelectedCandidate = inFile["CedarMonitor/NRecoHitsInSelectedCandidate"]

        nsecCand = h_NSectorsInCandidate.values()
        
        
        Arg = inFile['SpecialTrigger;1']['Beam/fARGONION']
        
        burst = inFile['SpecialTrigger;1']['EventHeader/fBurstID'].array()[0]

        time_stamp = file_name[-35:-25]
        
        pres = 0
        
        pres = file_name[-9:-5]
        
        
        try:
            pres = max(presure)
        except ValueError:
            continue
        print(burst)
        
        print("-----------------------")
        print("Pressure: ", pres)
        print("Time Stamp: ", time_stamp)
        print("Burst Number: ", burst)
        
       
        Arg_count = 1
        try:
            Arg_count = max(Arg["fARGONION.fCounts"].array())
        except ValueError:
            continue
        
        print("ArgCount: ", Arg_count)
        
        THits = h_NRecoHits.member('fTsumwx')
        
        temp_D = max(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fTempDiaph'].array())
        temp_B = max(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fTempRear'].array())
        temp_F = max(inFile['SpecialTrigger;1']['Cedar/fDIMInfo/fDIMInfo.fTempFront'].array())
        
        print("Temperature at Dia: ", temp_D)
        
        _temp_Back.append(temp_B)
        _temp_Dia.append(temp_D)
        _temp_Front.append(temp_F)
        
        _presure.append(float(pres))
        time.append(burst)
        hitpevnt.append(0)
        
        _Arg_count.append(Arg_count)
        
        _sec_8.append((nsecCand[-1])/Arg_count)
        _sec_7.append((nsecCand[-2]+nsecCand[-1])/Arg_count)
        _sec_6.append((nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
        _sec_5.append((nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)

        r76.append((nsecCand[-2]+nsecCand[-1])/(nsecCand[-3]+nsecCand[-2]+nsecCand[-1]))
        r87.append((nsecCand[-1])/(nsecCand[-2]+nsecCand[-1]))
        r86.append((nsecCand[-1])/(nsecCand[-3]+nsecCand[-2]+nsecCand[-1]))
        r85.append((nsecCand[-1])/(nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1]))
        
        if 3.850 < round(pres*1000)/1000 < 3.890:
            print("R85 = {}".format(r85[-1]))
            print("R87 = {}".format(r87[-1]))
            print("R76 = {}".format(r76[-1]))

        
        p_sec_8.append(((nsecCand[-1])/sum(nsecCand)))
        p_sec_7.append((nsecCand[-2]+nsecCand[-1])/sum(nsecCand))
        p_sec_6.append((nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/sum(nsecCand))
        p_sec_5.append((nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/sum(nsecCand))
        
        print("NEntries in Reco: ", h_NRecoHits.member('fEntries'))
        
        
        if float(pres) < 3.8:  
            pres -= 3.72
            pres *= -1
            pres += 3.72
            
            pres += 0.01
            
        _sec_8_comp.append((nsecCand[-1])/Arg_count)
        _sec_7_comp.append((nsecCand[-2]+nsecCand[-1])/Arg_count)
        _sec_6_comp.append((nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
        _sec_5_comp.append((nsecCand[-4]+nsecCand[-3]+nsecCand[-2]+nsecCand[-1])/Arg_count)
            
        _presure_comp.append(pres)
        
        h_sec_0.append(h_NRecoHitsInSector[0])
        h_sec_1.append(h_NRecoHitsInSector[1])
        h_sec_2.append(h_NRecoHitsInSector[2])
        h_sec_3.append(h_NRecoHitsInSector[3])
        h_sec_4.append(h_NRecoHitsInSector[4])
        h_sec_5.append(h_NRecoHitsInSector[5])
        h_sec_6.append(h_NRecoHitsInSector[6])
        h_sec_7.append(h_NRecoHitsInSector[7])
            
            
        try:
            mu1 = h_NRecoHitsInSelectedCandidate.member("fTsumwx")/h_NRecoHitsInSelectedCandidate.member("fEntries")
        except ZeroDivisionError:
            mu1 = 0
            
        if 3.850 < round(pres*1000)/1000 < 3.890:
            print(file_name)
            print(mu1)
            
        _mu.append(mu1)
        
        c += 1
        

plt.rcParams['figure.constrained_layout.use'] = True

fig, axs = plt.subplots(figsize=(10,10))

axs.scatter(time,hitpevnt,marker="x")
axs.set_ylabel("Averge NHits per event")
axs.set_xlabel("Burst")
axs.xaxis.set_major_locator(plt.MaxNLocator(20))
axs.tick_params(axis='x', labelrotation = 90)

save_file = "output/PressureScans/{}-{}.Hits_Arg.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file)


ratio_8 = []
ratio_7 = []
ratio_6 = []
ratio_5 = []
ratio_pres = []


for i in range(len(_presure_comp)):
    for t in range(len(_presure_comp)):  
        if round(_presure_comp[i]*1000)/1000 == round(_presure_comp[t]*1000)/1000 and (i != t):
            print("-------PION CONTAMINATION--------")
            print(_presure_comp[i],_presure_comp[t])
            print("5FOLD {}".format(_sec_5_comp[i]))
            print("6FOLD {}".format(_sec_6_comp[i]))
            print("7FOLD {}".format(_sec_7_comp[i]))
            print("8FOLD {}".format(_sec_8_comp[i]))
            print("=================================")
            print("5FOLD {}".format(_sec_5_comp[t]))
            print("6FOLD {}".format(_sec_6_comp[t]))
            print("7FOLD {}".format(_sec_7_comp[t]))
            print("8FOLD {}".format(_sec_8_comp[t]))
            print("-------PION DONE--------")
            if _sec_6_comp[i] == 0 or _sec_6_comp[t] == 0:
                continue
            if _sec_8_comp[t] > 1e-5:
                continue
            if 3.8 < round(_presure_comp[i]*1000)/1000 < 3.9:
                pass
            else:
                continue
            if _sec_8_comp[i] > _sec_8_comp[t] :
                ratio_8.append(_sec_8_comp[t]/_sec_8_comp[i])
                ratio_7.append(_sec_7_comp[t]/_sec_7_comp[i])
                ratio_6.append(_sec_6_comp[t]/_sec_6_comp[i])
                ratio_5.append(_sec_5_comp[t]/_sec_5_comp[i])
            else: 
                ratio_8.append(_sec_8_comp[i]/_sec_8_comp[t])
                ratio_7.append(_sec_7_comp[i]/_sec_7_comp[t])
                ratio_6.append(_sec_6_comp[i]/_sec_6_comp[t])
                ratio_5.append(_sec_5_comp[i]/_sec_5_comp[t])
            
            if 3.84 < round(_presure_comp[i]*1000)/1000 < 3.92:
                print("-------PION CONTAMINATION--------")
                print(_presure_comp[i],_presure_comp[t])
                print("5FOLD {}".format(_sec_5_comp[i]))
                print("6FOLD {}".format(_sec_6_comp[i]))
                print("7FOLD {}".format(_sec_7_comp[i]))
                print("8FOLD {}".format(_sec_8_comp[i]))
                print("=================================")
                print("5FOLD {}".format(_sec_5_comp[t]))
                print("6FOLD {}".format(_sec_6_comp[t]))
                print("7FOLD {}".format(_sec_7_comp[t]))
                print("8FOLD {}".format(_sec_8_comp[t]))
                print("-------PION DONE--------")
            
            ratio_pres.append(round(_presure_comp[i]*1000)/1000)
        
output1 = uproot.recreate("{}-{}.root".format(ref_time[0],ref_time[1]))

fig0, axs0 = plt.subplots(figsize=(10,10))

output1["Coin_ratio"] = {"ratio_pres": np.array(ratio_pres), "ratio_8": np.array(ratio_8), "ratio_7": np.array(ratio_7), "ratio_6": np.array(ratio_6), "ratio_5": np.array(ratio_5)}

axs0.scatter(ratio_pres,ratio_8,marker="x",label="At Least 8 Sectors")
axs0.scatter(ratio_pres,ratio_7,marker="x",label="At Least 7 Sectors")
axs0.scatter(ratio_pres,ratio_6,marker="x",label="At Least 6 Sectors")
axs0.scatter(ratio_pres,ratio_5,marker="x",label="At Least 5 Sectors")
#axs0.set_ylabel("NFold Coincidences per Event Normalised to Argonian")
axs0.set_xlabel("Pressure")
#axs0.set_xlim(1.5,2.2)
axs0.set_yscale('log')
axs0.set_ylim(1e-5,1)
axs0.xaxis.set_major_locator(plt.MaxNLocator(20))
axs0.tick_params(axis='x', labelrotation = 90)
axs0.legend()
save_file = "output/PressureScans/{}-{}.Coin_log_ratio.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig01, axs01 = plt.subplots(figsize=(10,10))

output1["Coin_ratio_comp_arg"] = {"presure_comp": np.array(_presure_comp), "sec_8_comp": np.array(_sec_8_comp), "sec_7_comp": np.array(_sec_7_comp), "sec_6_comp": np.array(_sec_5_comp), "sec_5_comp": np.array(_sec_5_comp)}

axs01.scatter(_presure_comp,_sec_5_comp,marker="x",label="At Least 5 Sectors")
axs01.scatter(_presure_comp,_sec_6_comp,marker="x",label="At Least 6 Sectors")
axs01.scatter(_presure_comp,_sec_7_comp,marker="x",label="At Least 7 Sectors")
axs01.scatter(_presure_comp,_sec_8_comp,marker="x",label="At Least 8 Sectors")
axs01.set_ylabel("Coincidences per Event Normalised to Argonian")
axs01.set_xlabel("Pressure")
#axs01.set_xlim(1.5,2.2)
axs01.set_xlim(3.65,4.4)
axs01.set_yscale('log')
axs01.set_ylim(1e-7,1)
axs01.xaxis.set_major_locator(plt.MaxNLocator(20))
axs01.tick_params(axis='both', which='major', pad=10)
axs01.tick_params(axis='x', labelrotation = 90)
axs01.legend(prop={'size': 30})
save_file = "output/PressureScans/{}-{}.Coin_log_compare.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file, bbox_inches="tight")

fig1, axs1 = plt.subplots(figsize=(10,10))
size_marker = 40
output1["Coin_ratio_arg"] = {"presure": np.array(_presure), "sec_8": np.array(_sec_8), "sec_7": np.array(_sec_7), "sec_6": np.array(_sec_6), "sec_5": np.array(_sec_5)}


'''_presure.pop(432)
_sec_8.pop(432)
_sec_7.pop(432)
_sec_6.pop(432)
_sec_5.pop(432)'''



axs1.scatter(_presure,_sec_5,marker="d",label="5-fold",c='orange',s=size_marker)
axs1.scatter(_presure,_sec_6,marker="s",label="6-fold",c='DarkBlue',s=size_marker)
axs1.scatter(_presure,_sec_7,marker="^",label="7-fold",c='red',s=size_marker)
axs1.scatter(_presure,_sec_8,marker="o",label="8-fold",c='green',s=size_marker)
axs1.set_ylabel("Arbitrary scale", fontsize=30)
axs1.set_xlabel("Pressure [bar]", fontsize=30)
axs1.set_xlim(3.6,4.4)
axs1.set_yscale('log')
axs1.set_ylim(1e-7,0.01)
axs1.tick_params(axis='both', which='major', pad=10)
#axs1.set_ylim(1e-8,10)
#axs1.xaxis.set_major_locator(plt.MaxNLocator(20))
#axs1.tick_params(axis='x', labelrotation = 90)

fold5_R1 = []
fold5_R2 = []
fold5_R3 = []
pres_R1 = []
pres_R1_p = []
pres_R2 = []
pres_R2_p = []
pres_R3 = []
pres_R3_p = []


for i in range(len(_presure)):
    if 3.87 < _presure[i] < 3.89:
        print(i , " ============= ", _presure[i],_sec_8[i])
        
    if 3.78 < _presure[i] < 3.88:
        pres_R1_p.append(_presure[i])
        
    if 3.79 < _presure[i] < 3.82:
        pres_R1.append(_presure[i])
        fold5_R1.append(_sec_5[i])
       
    #if 3.66 < _presure[i] < 3.97:
    #    pres_R1.append(_presure[i])
    #    fold5_R1.append(_sec_5[i])
     
    if 3.9 < _presure[i] < 3.965:
        pres_R2_p.append(_presure[i])
        
    if 3.90 < _presure[i] < 3.965:
        pres_R2.append(_presure[i])
        fold5_R2.append(_sec_5[i])
        
    if 4.12 < _presure[i] < 4.30:
        pres_R3_p.append(_presure[i])
        
    if 4.172 < _presure[i] < 4.30:
        pres_R3.append(_presure[i])
        fold5_R3.append(_sec_5[i])

def sup_gauss(x, a, x0, sigma,p):
    return a * np.exp(-((x - x0) ** 2 / (2 * sigma ** 2))**p)


def double_sup(x, a1, x01, sigma1,p1, a2, x02, sigma2,p2):
    return sup_gauss(x, a1, x01, sigma1,p1) * sup_gauss(x, a2, x02, sigma2,p2)


x = np.linspace(3.8, 3.97, 100)

popt5_1,pcov6_1 = curve_fit(sup_gauss,pres_R1,fold5_R1,p0=[1e-3,3.72,0.3,1])
axs1.plot(x,sup_gauss(x,*popt5_1),'--',c="orange")
#popt5_1,pcov6_1 = curve_fit(double_sup,pres_R1,fold5_R1,p0=[1e-3,3.72,0.3,1,1e-3,3.88,0.3,1])
#axs1.plot(x,double_sup(x,*popt5_1),'--',c="orange")

popt5_2,pcov6_2 = curve_fit(sup_gauss,pres_R2,fold5_R2,p0=[1e-3,3.88,0.3,1])
#axs1.plot(pres_R2_p,sup_gauss(pres_R2_p,*popt5_2),'b--')

popt5_3,pcov6_3 = curve_fit(sup_gauss,pres_R3,fold5_R3,p0=[1e-3,4.3,0.3,1])
#axs1.plot(pres_R3_p,sup_gauss(pres_R3_p,*popt5_3),'b--')

print(popt5_1)
print("fitval")
print(sup_gauss(3.88,*popt5_1))
#print(popt5_2)
#print(sup_gauss(pres_R2_p,*popt5_2))
#print(popt5_3)
#print(sup_gauss(pres_R3_p,*popt5_3))
#

#print(sup_gauss(3.88,*popt5_1))
#print(sup_gauss(3.88,*popt5_2))
#print(sup_gauss(3.88,*popt5_1)/sup_gauss(3.88,*popt5_2))

#fig01000, axs01000 = plt.subplots(figsize=(10,10))
#axs01000.scatter(_presure,_Arg_count,marker="o",c='green')
#axs01000.set_ylabel("Argonian")

#axs1.legend(prop={'size': 30})
save_file = "output/PressureScans/{}-{}.Coin_log.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file, bbox_inches="tight")

fig01, axs01 = plt.subplots(figsize=(10,10))




axs01.scatter(_presure,_sec_5,marker="d",label="5-fold",c='orange',s=size_marker)
axs01.scatter(_presure,_sec_6,marker="s",label="6-fold",c='DarkBlue',s=size_marker)
axs01.scatter(_presure,_sec_7,marker="^",label="7-fold",c='red',s=size_marker)
axs01.scatter(_presure,_sec_8,marker="o",label="8-fold",c='green',s=size_marker)
axs01.set_ylabel("Arbitrary scale", fontsize=30)
axs01.set_xlabel("Pressure [bar]", fontsize=30)
axs01.set_xlim(3.6,4.4)
#axs01.yscale("log")
axs01.set_ylim(0,0.004)
axs01.tick_params(axis='both', which='major', pad=10)
#axs01.xaxis.set_major_locator(plt.MaxNLocator(20))
#axs01.tick_params(axis='x', labelrotation = 90)
axs01.legend(prop={'size': 30})
save_file = "output/PressureScans/{}-{}.Coin.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file, bbox_inches="tight")

fig2, axs2 = plt.subplots(figsize=(10,10))

output1["Coin_prob"] = {"presure": np.array(_presure), "sec_8": np.array(p_sec_8), "sec_7": np.array(p_sec_7), "sec_6": np.array(p_sec_6), "sec_5": np.array(p_sec_5)}

axs2.scatter(_presure,p_sec_8,marker="x",label="At Least 8 Sectors")
axs2.scatter(_presure,p_sec_7,marker="x",label="At Least 7 Sectors")
axs2.scatter(_presure,p_sec_6,marker="x",label="At Least 6 Sectors")
axs2.set_ylabel("Probabilty of NFold Conicidences per Burst")
axs2.set_xlabel("Pressure")
#axs2.set_xlim(1.5,2.2)
#axs2.set_ylim(0,0.3)
axs2.legend()
axs2.set_xlim(3.6,4.4)
#axs2.xaxis.set_major_locator(plt.MaxNLocator(20))
#axs2.tick_params(axis='x', labelrotation = 90)

save_file = "output/PressureScans/{}-{}.CoinpEvnt.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

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
#axs3.set_xlim(1.5,2.25)
axs3.xaxis.set_major_locator(plt.MaxNLocator(20))
axs3.tick_params(axis='x', labelrotation = 90)
axs3.legend()
save_file = "output/PressureScans/{}-{}.SecHits.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig4, axs4 = plt.subplots(figsize=(10,10))

axs4.scatter(_presure,_mu,marker="x")
axs4.set_ylabel("Number of Hits in Selected Candidate")
axs4.set_xlabel("Presure")
axs4.xaxis.set_major_locator(plt.MaxNLocator(20))
axs4.tick_params(axis='x', labelrotation = 90)

save_file = "output/PressureScans/{}-{}.NHits_Sel.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file)


fig5, axs5 = plt.subplots(figsize=(10,10))

axs5.scatter(_presure,r76,marker="x",label="R76")
axs5.scatter(_presure,r87,marker="x",label="R87")
axs5.set_ylabel("Ratios")
axs5.set_xlabel("Pressure")
#axs5.set_xlim(1.5,2.2)
axs5.set_yscale('log')
#axs5.set_ylim(1e-4,1)
axs5.xaxis.set_major_locator(plt.MaxNLocator(20))
axs5.tick_params(axis='x', labelrotation = 90)
axs5.legend()
save_file = "output/PressureScans/{}-{}.Ratio_log.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig6, axs6 = plt.subplots(figsize=(10,10))

axs6.scatter(_presure,r76,marker="x",label="R76")
axs6.scatter(_presure,r87,marker="x",label="R87")
axs6.scatter(_presure,r86,marker="x",label="R86")
axs6.scatter(_presure,r85,marker="x",label="R85")
axs6.set_ylabel("Ratios")
axs6.set_xlabel("Pressure")
#axs6.set_xlim(1.5,2.2)
axs6.set_ylim(0,1)
axs6.xaxis.set_major_locator(plt.MaxNLocator(20))
axs6.tick_params(axis='x', labelrotation = 90)
axs6.legend()
save_file = "output/PressureScans/{}-{}.Ratio_log.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file)

fig7, axs7 = plt.subplots(figsize=(10,10))

axs7.scatter(_presure,_temp_Back,marker="x",label="Rear")
axs7.scatter(_presure,_temp_Front,marker="x",label="Front")
axs7.scatter(_presure,_temp_Dia,marker="x",label="Diaphragm")
axs7.set_ylabel("Temperature")
axs7.set_xlabel("Pressure")
#axs6.set_xlim(1.5,2.2)
#axs7.set_ylim(0,1)
axs7.xaxis.set_major_locator(plt.MaxNLocator(20))
axs7.tick_params(axis='x', labelrotation = 90)
axs7.legend()
save_file = "output/PressureScans/{}-{}.Temp.pdf".format(ref_time[0],ref_time[1])
plt.savefig(save_file)


plt.show()
