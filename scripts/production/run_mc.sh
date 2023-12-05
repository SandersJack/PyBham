#!/bin/bash
source /afs/cern.ch/work/j/jsanders/Software/na62fw/NA62MC/scripts/env.sh
mkdir mc
burst=$(printf "%06i" "$1")
NA62MC -n 1000 -o pluto._dr030000_r$burst.root -s $RANDOM -r 30000
source /afs/cern.ch/work/j/jsanders/Software/na62fw/NA62Reconstruction/scripts/env.sh
ls -lh
mkdir config
xrdcp /afs/cern.ch/work/j/jsanders/Software/na62fw/NA62Reconstruction/config/* config/
ls -lh
mkdir reco
NA62Reco -i pluto._dr030000_r$burst.root -o reco/pluto_reco._dr030000_$burst.root -c config/NA62Reconstruction.MC.NoOverlay.HIKE-Phase2.conf -e2