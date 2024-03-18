#!/bin/bash

mkdir config
mkdir reco
############# Replace with local reco ######################
source /afs/cern.ch/work/j/jsanders/Software/bugfix/develop/na62fw/NA62Reconstruction/scripts/env.sh
xrdcp /afs/cern.ch/work/j/jsanders/Software/bugfix/develop/na62fw/NA62Reconstruction/config/* config/
IFS=$'\n' read -d '' -r -a lines < $3

NA62Reco -i ${lines[$1]} -o reco/Saturn.$2.$1.root -c config/NA62Reconstruction.conf -e1