executable            = run_mc.sh
arguments             = $(ProcId) $(ClusterId)
output                = output/hello.$(ClusterId).$(ProcId).out
error                 = error/hello.$(ClusterId).$(ProcId).err
log                   = log/hello.$(ClusterId).log

output_destination = root://eosuser.cern.ch//eos/user/j/jsanders/condorout/441_1MEvent_30000_withNeutralKP/
MY.XRDCP_CREATE_DIR = True

+JobFlavour = "workday"
#when_to_transfer_output = ON_EXIT
#max_materialize = 2000

transfer_input_files    = NA62Reconstruction/bin-cc7/NA62Reco
transfer_input_files    = NA62Reconstruction/config
transfer_input_files    = NA62MC/bin-cc7/NA62MC
transfer_input_files    = NA62MC/macros

transfer_output_files = mc
transfer_output_files = reco

queue 1000