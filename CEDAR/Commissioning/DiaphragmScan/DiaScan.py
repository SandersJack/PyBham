import numpy as np
import sys
import os
import uproot as up
import boost_histogram as bh
import hist 
from hist import Hist
import matplotlib.pyplot as plt
import mplhep as hep
hep.style.use(hep.style.ROOT)

VERSION = 1.0

def process_command_line_args(args):
    ''' Process command line arguments from user '''
    arguments = {
        "directory": "",
        "wantsHelp": False,
        "saveFigures": False,
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
    print(f"CEDAR Diaphragm Scan Tool (v{VERSION})\n---------------------------\nArguments:\n--help\tDisplay this help menu.\n--dir <directory>\tPath to the directory with the reconstructed ROOT files to process.\n\n")


if __name__ == "__main__":
    args = process_command_line_args(sys.argv[1:]) # First argument is the name of the file which we don't need
    if(args["wantsHelp"]):
        display_help()
    else:
        if not os.path.isdir(args["directory"]):
            print("[Error] The provided directory does not exist.")
            exit()

        mu_Hits = []
        mu_CandHits = []
        mu_SelCandHits = []

        mu_Hits_Arg = []
        mu_CandHits_Arg = []
        mu_SelCandHits_Arg = []

        cand = [] # Number of candidates

        _burst = []
        burst = []
        cand_Arg = [] # Candidates per argonion hit

        name = "CLICKS"

        # Only look for ROOT files in the provided directory
        files = [filename for filename in os.scandir(args["directory"]) if filename.is_file and "tar" not in filename.path and ".root" in filename.path]

        for filename in files:
            with up.open(filename) as f:
                # Get the stuff i need here....
                burst = f['SpecialTrigger;1']['EventHeader/fBurstID'].array()
                try:
                    burst = burst[1]
                except ValueError:
                    continue

                h_NRecoCand = f["CedarMonitor/NCandidates"].to_hist()
                h_NRecoHits = f["CedarMonitor/NRecoHits"].to_hist()
                h_NHitsInCandidate = f["CedarMonitor/NRecoHitsInCandidate"].to_hist()
                h_NRecoHitsInSelectedCandidate = f["CedarMonitor/NRecoHitsInSelectedCandidate"].to_hist()
                burst = f['SpecialTrigger;1']['EventHeader/fBurstID'].array()
                run_number = f['SpecialTrigger;1']['EventHeader/fRunID'].array()
                argonion = f['SpecialTrigger;1']['Beam/fARGONION'] # Was Arg
                argonion_counts = argonion["fARGONION.fCounts"].array()
                
            arg_count = -99
            try:
                arg_count = argonion_counts[1]
            except ValueError:
                continue
        
            burst = burst[0]
            print(f"Burst Number: {burst}")
            if run_number[0] > 12925:
                burst += 100
        
            _burst.append(burst)
            print(f"Argonion Count: {arg_count}")
            # Calculate the average number of reco candidates as a weighted sum
            can = np.sum((h_NRecoCand.axes[0].centers * h_NRecoCand.values())) / h_NRecoCand.values().sum()
            cand.append(can)
            cand_Arg.append(can / arg_count)    

            mu1 = np.sum((h_NRecoHits.axes[0].centers * h_NRecoHits.values())) / h_NRecoHits.values().sum()
            mu_Hits.append(mu1)
            mu_Hits_Arg.append(mu1 / arg_count)
            
            mu2 = np.sum((h_NHitsInCandidate.axes[0].centers * h_NHitsInCandidate.values())) / h_NHitsInCandidate.values().sum()
            mu_CandHits.append(mu2)
            mu_CandHits_Arg.append(mu2 / arg_count)

            try:
                mu3 = np.sum((h_NRecoHitsInSelectedCandidate.axes[0].centers * h_NRecoHitsInSelectedCandidate.values())) / h_NRecoHitsInSelectedCandidate.values().sum()
            except ZeroDivisionError:
                mu3 = 0
            mu_SelCandHits.append(mu3)
            mu_SelCandHits_Arg.append(mu3 / arg_count)
            print("---------------------")
        

    fig, ax = plt.subplots(1, 1, figsize=(10,10))
    ax.scatter(_burst, mu_Hits, marker="x", label="Reco.")
    ax.scatter(_burst, mu_CandHits, marker="x", label="Cand.")
    ax.scatter(_burst, mu_SelCandHits, marker="x", label="Sel. Cand.")

    ax.set_ylabel("Number of Hits")
    ax.set_xlabel("Aperature [mm]")
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.tick_params(axis='x', labelrotation = 90)
    ax.legend()
    plt.tight_layout()
    if(args["saveFigures"]):
        if not os.path.exists('output'):
                os.makedirs("output")
        plt.savefig(f"output/DiaScan_{name}.1.pdf")
    plt.close()

    fig, ax = plt.subplots(1, 1, figsize=(10,10))
    ax.scatter(_burst, mu_Hits_Arg, marker="x", label="Reco")
    ax.scatter(_burst, mu_CandHits_Arg, marker="x", label="Cand")
    ax.scatter(_burst, mu_SelCandHits_Arg, marker="x", label="Sel Cand")

    ax.set_ylabel("Number of Hits Normalise to Argonion")
    ax.set_xlabel("Aperature [mm]")
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.tick_params(axis='x', labelrotation = 90)
    ax.set_ylim(0,0.1e-6)
    ax.legend()
    plt.tight_layout()
    if(args["saveFigures"]):
        if not os.path.exists('output'):
                os.makedirs("output")
        plt.savefig(f"output/DiaScan_{name}.2.pdf")
    plt.close()

    fig, ax = plt.subplots(figsize=(10,10))
    ax.scatter(_burst,mu_Hits,marker="x",label="Reco")
    ax.scatter(_burst,mu_CandHits,marker="x",label="Cand")
    ax.scatter(_burst,mu_SelCandHits,marker="x",label="Sel Cand")
    ax.set_ylabel("Number of Hits")
    ax.set_xlabel("Aperature [mm]")
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.tick_params(axis='x', labelrotation = 90)
    ax.set_ylim(11,13)
    ax.legend()
    plt.tight_layout()
    if(args["saveFigures"]):
        if not os.path.exists('output'):
                os.makedirs("output")
        plt.savefig(f"output/DiaScan_{name}.3.pdf")
    plt.close()

    fig, ax = plt.subplots(figsize=(10,10))
    ax.scatter(_burst,mu_Hits_Arg,marker="x",label="Reco")
    ax.scatter(_burst,mu_CandHits_Arg,marker="x",label="Cand")
    ax.scatter(_burst,mu_SelCandHits_Arg,marker="x",label="Sel Cand")

    ax.set_ylabel("Number of Hits Normalise to Argonion")
    ax.set_xlabel("Aperature [mm]")
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.tick_params(axis='x', labelrotation = 90)
    ax.set_ylim(11,13)
    ax.legend()
    plt.tight_layout()
    if(args["saveFigures"]):
        if not os.path.exists('output'):
                os.makedirs("output")
        plt.savefig(f"output/DiaScan_{name}.4.pdf")
    plt.close()

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
    plt.tight_layout()
    if(args["saveFigures"]):
        if not os.path.exists('output'):
                os.makedirs("output")
        plt.savefig(f"output/DiaScan_{name}.5.pdf")
    plt.close()


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
    plt.tight_layout()
    if(args["saveFigures"]):
        if not os.path.exists('output'):
                os.makedirs("output")
        plt.savefig(f"output/DiaScan_{name}.6.pdf")
    plt.close()


    fig11, axs11 = plt.subplots(figsize=(10,10))
    axs11.scatter(_burst,cand,marker="x",label="NCandidates")
    axs11.set_ylabel("Number of Can_bursttes")
    axs11.set_xlabel("Aperature [mm]")
    axs11.xaxis.set_major_locator(plt.MaxNLocator(20))
    axs11.tick_params(axis='x', labelrotation = 90)
    axs11.legend()
    plt.tight_layout()
    if(args["saveFigures"]):
        if not os.path.exists('output'):
                os.makedirs("output")
        plt.savefig(f"output/DiaScan_{name}.7.pdf")
    plt.close()

    fig12, axs12 = plt.subplots(figsize=(10,10))
    axs12.scatter(_burst,cand_Arg,marker="x",label="NCandidates")
    axs12.set_ylabel("Number of Can_bursttes Normlised to Argonian")
    axs12.set_xlabel("Aperature [mm]")
    axs12.xaxis.set_major_locator(plt.MaxNLocator(20))
    axs12.tick_params(axis='x', labelrotation = 90)
    axs12.legend()
    if(args["saveFigures"]):
        if not os.path.exists('output'):
                os.makedirs("output")
        plt.savefig(f"output/DiaScan_{name}.8.pdf")
    plt.close()
