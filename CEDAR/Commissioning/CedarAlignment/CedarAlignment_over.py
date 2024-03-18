import numpy as np # The world's best library
import pandas as pd # File I/O
import time # Measure approximate execution time
from scipy.stats import norm # Gaussian fitting
import os # Scanning directories for files
import seaborn as sns # Plotting
import matplotlib.pyplot as plt # For plotting
import mplhep as hep # For prettier ROOT-style plots
hep.style.use(hep.style.ROOT)
import uproot as up # For ROOT file I/O
import boost_histogram as bh # Nicer histogram manipulation
from hist import Hist # Wrapper for boost histogram
from datetime import datetime
import sys # For processing of command line arguments

VERSION = 1.0

def process_command_line_args(args):
    ''' Process command line arguments from user '''
    arguments = {
        "directory": "",
        "wantsHelp": False,
        "saveFigures": False
    }
    for i, arg in enumerate(args):
        if(arg == "--dir"):
            if len(args) <= i + 1:
                print("[Warning] You must provide a valid directory")
                continue
            arguments["directory"] = args[i+1]            
        if(arg == "--help"):
            arguments["wantsHelp"] = True
        if(arg == "--save"):
            arguments["saveFigures"] = True
    return arguments

def display_help():
    print(f"CEDAR Alignment Tool (v{VERSION})\n---------------------------\nArguments:\n--help\tDisplay this help menu.\n--dir <directory>\tPath to the directory with the reconstructed ROOT files to process.\n\n")

if __name__ == "__main__":
    args = process_command_line_args(sys.argv[1:]) # First argument is the name of the file which we don't need
    if(args["wantsHelp"]):
        display_help()
    else:
        c = 0
        motor_x = []
        motor_y = []
        nhits = []
        
        if not os.path.isdir(args["directory"]):
            print(args["directory"])
            print("[Error] The provided directory does not exist.")
            exit()
        files = [filename for filename in os.scandir(args["directory"]) if filename.is_file and "tar" not in filename.path and ".root" in filename.path]
        start_time = time.time_ns() // 1.0E+6
        for n, filename in enumerate(files):
            with up.open(filename) as f:
                h_NRecoHitsInSelectedCandidate = f["CedarMonitor/NRecoHitsInSelectedCandidate"].to_hist()
                h_NSectorsInSelectedCandidate = f["CedarMonitor/NSectorsInSelectedCandidate"].to_hist()

                current_motor_x = np.min(f['SpecialTrigger']['Cedar/fDIMInfo/fDIMInfo.fMotorPosX'].array())
                current_motor_y = np.min(f['SpecialTrigger']['Cedar/fDIMInfo/fDIMInfo.fMotorPosY'].array())
                burst = f['SpecialTrigger;1']['EventHeader/fBurstID'].array()[0]
                
            # TODO: Document which plot this is
            fig, ax = plt.subplots(1, 1, figsize=(12, 10))
            bins_sel = h_NRecoHitsInSelectedCandidate.axes[0].edges
            weight_sel = h_NRecoHitsInSelectedCandidate.values()
            counts, bin_edges, bars = ax.hist(bins_sel[1:], bins_sel, weights=weight_sel, label="")

            # Construct a list of the "raw" histogram e.g. 22 would be repeated for the height of the 22 bin
            value = [bin_edges[i] for i in range(len(bin_edges[1:])) for t in range(int(counts[i]))]
            mu, std = norm.fit(value) # Fit a Gaussian to the hit distribution for reco candidates
        
            if mu < 15: # Fit was bad, skip
                continue
        
            nhits.append(mu)
            motor_x.append((round(current_motor_x*1000)/1000))
            motor_y.append((round(current_motor_y*1000)/1000))
        
            print(f"[Info] Burst ID = {burst}\tMotor position ({motor_x[-1]}, {motor_y[-1]})")
        
            x = np.linspace(10, 30, 100) # Number of hits
            p = norm.pdf(x, loc=mu, scale=std) # Gaussian PDF using the calculated mean and std.
            p *= np.sum(counts) # Scale by the total number of hits

            ax.plot(x, p, 'k', linewidth=2, label=f"NHits (Sel): mu = {mu:.2f}")
            #print(f"Fit Data: mu = {mu:.2f}")

            ax.set_xlim(0,40)
            ax.legend()
            ax.set_title("Number of Reco Hits in Candidate")
            ax.set_xlabel("Number of Hits")
            ax.grid()
            plt.clf()
            plt.close()

            current_time = time.time_ns() // 1.0E+6
            print(f"[Info] Processed {((n+1)/len(files))*100:.2f}% ({n}/{len(files)}) in {current_time - start_time} milliseconds")

        nhits = np.array(nhits).astype(np.int32)
        motor_x = np.array(motor_x).astype(np.float64)
        motor_y = np.array(motor_y).astype(np.float64)

        # Save data
        df = pd.DataFrame(list(zip(motor_x, motor_y, nhits)),columns =['MotorX', 'MotorY','NHits'])
        error = df.groupby(['MotorX', 'MotorY'], as_index=False)['NHits'].sem()
        df = df.groupby(['MotorX', 'MotorY'], as_index=False)['NHits'].mean()
        pivot = df.pivot(index='MotorY', columns='MotorX', values='NHits')
        plt.figure(figsize=(11, 9))
        sns.heatmap(pivot, cmap='jet', annot=True, cbar_kws={'label': 'NHits in Selected Candidate'}, fmt=".2f")
        plt.grid()
        plt.xlabel("X motor [mm]")
        plt.ylabel("Y motor [mm]")
        plt.tight_layout()
        if args["saveFigures"]:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%d_%m_%Y")
            # if output directory does not exist, create one
            if not os.path.exists('output'):
                os.makedirs("output")
            plt.savefig(f"output/x_vs_y_CEDARMotor_{formatted_date}.pdf")
        plt.show()
