import uproot
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.ROOT)
import pandas as pd
from csv import writer
from scipy.stats import norm
import argparse
import seaborn as sns

def DecodeChannel(chID):
    #print(chID)
    if chID == 0:
        return [0,0,0]
    SectorID = np.floor((chID)/ 100)
    RowID = np.floor((chID-SectorID*100)/10)
    ConeID = np.floor((chID-SectorID*100-RowID*10))
    #print(SectorID,RowID,ConeID)
    return [SectorID,RowID,ConeID]

fchannel = [0]*3065
chun = 0
with open('cedar.conf') as f:
    lines = f.readlines()

line_count = []

for i in range(len(lines)):
    ru = lines[i].split()
    #print(ru)
    if len(ru) == 0: 
        continue
    if ru[0] == '#' or ru[0] == '#Cable':
        continue
    else:
        line_count.append(int(ru[1]))
        line_count.append(int(ru[9]))

for t in range(len(line_count)):
    fchannel[chun] = line_count[t]
    chun += 8

fDecodedChDec = []
for i in range(len(fchannel)):
    fDecodedChDec.append(DecodeChannel(fchannel[i]))

file_name = "na62om_1684500862-06-013135-0061.ds10.root"

try: 
    inFile = uproot.open(file_name)
except ValueError:
    pass
except OSError:
    pass



h_NTime = inFile["CedarMonitor/DigiTimeRawFineVsROChannel"]

bins_sel = h_NTime.axis(0).edges()
weight_sel = h_NTime.counts()

cut_res = []

for i in range(len(bins_sel[1:])):
    if int(np.floor(bins_sel[1:][i])) > 3064:
        break
    channel_count = sum(weight_sel[i])
    if channel_count == 0.0:
        continue
    #print(int(np.floor(bins_sel[1:][i])))
    #print(int(np.floor(bins_sel[i])),channel_count)
    cut_res.append([int(np.floor(bins_sel[1:][i])),sum(weight_sel[i])])
    if channel_count < 500:
        cut_res.append([int(np.floor(bins_sel[1:][i])),sum(weight_sel[i])])
        
        
Sec2 = []

Sec_x = [[],[],[],[],[],[],[],[]]
Sec_y = [[],[],[],[],[],[],[],[]]
for v in cut_res:
    tmp_x = []
    tmp_y = []
    comp = 0
    #print(v)
    tmp = fDecodedChDec[v[0]]
    comp = tmp
    Sec_x[int(comp[0])-1].append(comp[2] - 0.5*(comp[1]%2))
    Sec_y[int(comp[0])-1].append(-comp[1])
    
#print(Sec_y[5])

for i in range(len(Sec_x)):
    plt.subplots(figsize=(10,10))
    plt.hist2d(Sec_x[i], Sec_y[i], cmin=1, bins=(20,18), range=[[0,10],[-9,0]],cmap='jet')
    plt.xlabel("Cone")
    plt.ylabel("Row")
    plt.title("2D Channel Profile in Sector {}".format(i))
    save_file = "ChannelID{}".format(i)
    plt.savefig(save_file)

plt.show()
#weights=Sec2[3])


'''
df = pd.DataFrame(Sec2,columns =['Sec','Row', 'ConeID','NHits'])
print(df)

pivot = df.pivot(index='Row', columns='ConeID', values='NHits')
print(pivot)
sns.heatmap(pivot,cmap='coolwarm',annot=True)
plt.show()
'''