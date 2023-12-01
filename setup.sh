#!/bin/bash

# Define Miniconda installation directory and filename
miniconda_dir="$HOME/miniconda"
miniconda_installer="Miniconda3-latest-Linux-x86_64.sh"

# Check if Miniconda is already installed
if [ -d "$miniconda_dir" ]; then
    echo "Miniconda is already installed in $miniconda_dir. Skipping installation."
else
    # Download and install Miniconda
    wget https://repo.anaconda.com/miniconda/$miniconda_installer -O /tmp/$miniconda_installer
    bash /tmp/$miniconda_installer -b -p $miniconda_dir
    rm /tmp/$miniconda_installer
    
    echo "Miniconda has been installed to $miniconda_dir."
    # Add Miniconda to the system PATH
    export PATH="$miniconda_dir/bin:$PATH"
fi

# Create a Python virtual environment named "na62"
conda create -n na62 python=3.8 -y

echo "Miniconda and the 'na62' virtual environment have been installed."
echo "Requiring packages..."

# Install required modules 
conda install -n na62 pandas -y
conda install -n na62 numpy -y
conda install -n na62 uproot -y
conda install -n na62 matplotlib -y
conda install -n na62 seaborn -y
conda install -n na62 mplhep -y
conda install -n na62 boot_histogram -y
conda install -n na62 numba -y

echo "Environment set up, your good to go! Use conda activate na62 to get going."
