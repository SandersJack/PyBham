import numpy as np 
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)
from random import seed
from random import random
from random import randint
import seaborn as sns
from scipy.stats import poisson

def Efficiency(photons):
    return (1-np.exp(-photons))

def Eff8Fold(photons):
    return Efficiency(photons)**8

def Eff7Fold(photons):
    return Eff8Fold(photons) + (8*Efficiency(photons)**7)*(1-Efficiency(photons))

def Eff6Fold(photons):
    return Eff7Fold(photons) + (28*Efficiency(photons)**6)*(1-Efficiency(photons))**2

def Eff5Fold(photons):
    return Eff6Fold(photons) + (56*Efficiency(photons)**5)*(1-Efficiency(photons))**3

def Eff4Fold(photons):
    return Eff5Fold(photons) + (70*Efficiency(photons)**4)*(1-Efficiency(photons))**4

def Eff3Fold(photons):
    return Eff4Fold(photons) + (56*Efficiency(photons)**3)*(1-Efficiency(photons))**5

def Eff2Fold(photons):
    return Eff3Fold(photons) + (28*Efficiency(photons)**2)*(1-Efficiency(photons))**6

def Eff1Fold(photons):

    return Eff2Fold(photons) + (8*Efficiency(photons))*(1-Efficiency(photons))**7

photons = 18.534 #19*0.9215665458029813

#print(Eff6Fold(photons))

_Eff1Fold = Eff1Fold(photons/8)
_Eff2Fold = Eff2Fold(photons/8)
_Eff3Fold = Eff3Fold(photons/8)
_Eff4Fold = Eff4Fold(photons/8)
_Eff5Fold = Eff5Fold(photons/8)
_Eff6Fold = Eff6Fold(photons/8)
_Eff7Fold = Eff7Fold(photons/8)
_Eff8Fold = Eff8Fold(photons/8)

print("8Fold Effciency {}".format(_Eff8Fold))
print("7Fold Effciency {}".format(_Eff7Fold))
print("6Fold Effciency {}".format(_Eff6Fold))
print("5Fold Effciency {}".format(_Eff5Fold))
print("4Fold Effciency {}".format(_Eff4Fold))
print("3Fold Effciency {}".format(_Eff3Fold))
print("2Fold Effciency {}".format(_Eff2Fold))
print("1Fold Effciency {}".format(_Eff1Fold))

print("{}, {}, {} ,{} , {}, {} ,{}, {}".format(_Eff1Fold,_Eff2Fold,_Eff3Fold,_Eff4Fold,_Eff5Fold,_Eff6Fold,_Eff7Fold,_Eff8Fold))

exit(0)


photons = np.linspace(0,30)

_Eff1Fold = Eff1Fold(photons/8)
_Eff2Fold = Eff2Fold(photons/8)
_Eff3Fold = Eff3Fold(photons/8)
_Eff4Fold = Eff4Fold(photons/8)
_Eff5Fold = Eff5Fold(photons/8)
_Eff6Fold = Eff6Fold(photons/8)
_Eff7Fold = Eff7Fold(photons/8)
_Eff8Fold = Eff8Fold(photons/8)


fig, axs = plt.subplots(figsize=(20,20))

axs.plot(photons,_Eff1Fold, label="1 Fold Efficiency",linestyle='--', marker='o')
axs.plot(photons,_Eff2Fold, label="2 Fold Efficiency",linestyle='--', marker='o')
axs.plot(photons,_Eff3Fold, label="3 Fold Efficiency",linestyle='--', marker='o')
axs.plot(photons,_Eff4Fold, label="4 Fold Efficiency",linestyle='--', marker='o')
axs.plot(photons,_Eff5Fold, label="5 Fold Efficiency",linestyle='--', marker='o')
axs.plot(photons,_Eff6Fold, label="6 Fold Efficiency",linestyle='--', marker='o')
axs.plot(photons,_Eff7Fold, label="7 Fold Efficiency",linestyle='--', marker='o')
axs.plot(photons,_Eff8Fold, label="8 Fold Efficiency",linestyle='--', marker='o')

axs.set_xlabel("Number of Photons")
axs.legend()

seed(987665)
mu = [21] #np.linspace(15,30,31)

nSectors_ = []
nHits_ = []
totalrings = 10000000
for l in range(len(mu)):
    nSectors = []
    nHits = []
    for ring in range(totalrings):
        nphotons = poisson.rvs(mu[l])
        octantHits = [0,0,0,0,0,0,0,0]
        octantbool = [0,0,0,0,0,0,0,0]
        if nphotons < 4:
            continue
        for photon in range(nphotons):
            octant = randint(0,7)
            cont = randint(0,10)
            #if cont == 0 or cont == 1:
            #    continue
            octantHits[octant] += 1
            octantbool[octant] = 1
        nSectors.append(sum(octantbool))
        nHits.append(sum(octantHits))
    nSectors_.append(nSectors)
    nHits_.append(nHits)

n8Sectors_ = []
n7Sectors_ = []
n6Sectors_ = []
n5Sectors_ = []
n4Sectors_ = []
n3Sectors_ = []
n2Sectors_ = []

n8Sectors_r = []
n7Sectors_r = []
n6Sectors_r = []
n5Sectors_r = []
n4Sectors_r = []
n3Sectors_r = []
n2Sectors_r = []
n1Sectors_r = []

for v in range((len(mu))):
    n8Sectors = n7Sectors = n6Sectors = n5Sectors = n4Sectors = n3Sectors = n2Sectors = n1Sectors = 0
    for t in range(len(nSectors)):
        if nSectors_[v][t] > 7:
            n8Sectors += 1
        if nSectors_[v][t] > 6:
            n7Sectors += 1
        if nSectors_[v][t] > 5:
            n6Sectors += 1
        if nSectors_[v][t] > 4:
            n5Sectors += 1
        if nSectors_[v][t] > 3:
            n4Sectors += 1
        if nSectors_[v][t] > 2:
            n3Sectors += 1
        if nSectors_[v][t] > 1:
            n2Sectors += 1
        if nSectors_[v][t] > 0:
            n1Sectors += 1
    
    n2Sectors_.append(n2Sectors)
    n3Sectors_.append(n3Sectors)
    n4Sectors_.append(n4Sectors)
    n5Sectors_.append(n5Sectors)          
    n6Sectors_.append(n6Sectors)
    n7Sectors_.append(n7Sectors)
    n8Sectors_.append(n8Sectors)   
    
    n1Sectors_r.append(n1Sectors/totalrings)
    n2Sectors_r.append(n2Sectors/totalrings)
    n3Sectors_r.append(n3Sectors/totalrings)
    n4Sectors_r.append(n4Sectors/totalrings)
    n5Sectors_r.append(n5Sectors/totalrings)          
    n6Sectors_r.append(n6Sectors/totalrings)
    n7Sectors_r.append(n7Sectors/totalrings)
    n8Sectors_r.append(n8Sectors/totalrings) 
    
     
    print("********************************")
    print("For mu of {}".format(mu[v]))
    print("Number of at least 1 coincidence = {} . fraction of total rings {} ".format(n1Sectors, n1Sectors/totalrings))
    print("Number of at least 2 coincidence = {} . fraction of total rings {} ".format(n2Sectors, n2Sectors/totalrings))
    print("Number of at least 3 coincidence = {} . fraction of total rings {} ".format(n3Sectors, n3Sectors/totalrings))
    print("Number of at least 4 coincidence = {} . fraction of total rings {} ".format(n4Sectors, n4Sectors/totalrings))
    print("Number of at least 5 coincidence = {} . fraction of total rings {} ".format(n5Sectors, n5Sectors/totalrings))
    print("Number of at least 6 coincidence = {} . fraction of total rings {} ".format(n6Sectors, n6Sectors/totalrings))
    print("Number of at least 7 coincidence = {} . fraction of total rings {} ".format(n7Sectors, n7Sectors/totalrings))
    print("Number of at least 8 coincidence = {} . fraction of total rings {} ".format(n8Sectors, n8Sectors/totalrings))

fig, ax0 = plt.subplots(1, 1,figsize=(20,20))

y_val = [1-n1Sectors_r[0],1-n2Sectors_r[0],1-n3Sectors_r[0],1-n4Sectors_r[0],1-n5Sectors_r[0],1-n6Sectors_r[0],1-n7Sectors_r[0],1-n8Sectors_r[0]]
x_val = [1,2,3,4,5,6,7,8]

ax0.scatter(x_val, y_val)
ax0.set_yscale("log")
plt.show()
'''
fig0 = plt.figure()
ax0 = fig0.add_subplot(111)
r87 = []
r76 = []
for v in range((len(mu))):
    sns.histplot(x=nSectors_[v],discrete=True,fill=False,ax=ax0,label="mu={}".format(mu[v]),weights=np.full(totalrings,1/totalrings))
    r87.append(float(n8Sectors_[v])/n7Sectors_[v])
    r76.append(float(n7Sectors_[v]/n6Sectors_[v]))
    
ax0.set(xlabel='N Coincidences', ylabel='Fraction of Total Triggers',title="Exactly N Fold Coincidences")
ax0.legend()

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(mu,r87, label="R87",linestyle='--', marker='o', color='r')
ax1.plot(mu,r76, label="R76", linestyle='--', marker='o', color='b')
ax1.set_xlim(16,30)
ax1.legend()
ax1.set_xlabel(r"Mean number of photoelectrons ($\lambda$)")
ax1.set_title("Ratio of cumulative coincidence probabilities")

fig = plt.figure()
ax2 = fig.add_subplot(111)

ax2.plot(mu,n8Sectors_r, label="8 Sectors",linestyle='--', marker='o')
ax2.plot(mu,n7Sectors_r, label="7 Sectors",linestyle='--', marker='o')
ax2.plot(mu,n6Sectors_r, label="6 Sectors",linestyle='--', marker='o')
ax2.plot(mu,n5Sectors_r, label="5 Sectors",linestyle='--', marker='o')
ax2.plot(mu,n4Sectors_r, label="4 Sectors",linestyle='--', marker='o')

ax2.legend()
ax2.set_xlabel(r"Mean number of photoelectrons ($\lambda$)")
ax2.set_title("Efficiency of NFold coincidences")
ax2.set_ylim(0.6,1.1)
save_file = "NFold Effciency.png"
plt.savefig(save_file)
'''
plt.show()

