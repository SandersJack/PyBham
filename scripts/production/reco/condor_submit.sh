filename=$1
# eg /afs/cern.ch/work/j/jsanders/Software/bugfix/develop/na62fw/NA62Reconstruction/2Pressure_H_4.list

executable            = run_reco.sh
arguments             = $(ProcId) $(ClusterId) $(filename)
output                = output/hello.$(ClusterId).$(ProcId).out
error                 = error/hello.$(ClusterId).$(ProcId).err
log                   = log/hello.$(ClusterId).log

###### Change this to your output Dir ###########
output_destination = root://eosuser.cern.ch//eos/user/j/jsanders/condorout/$(ClusterId)/
MY.XRDCP_CREATE_DIR = True

+JobFlavour = "espresso"

transfer_output_files = reco

lines=$(wc -l < "$filename")

queue $(lines)