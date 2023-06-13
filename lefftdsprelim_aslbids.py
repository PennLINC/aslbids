import sys
import numpy as np
import json 
import os
import pandas as pd

if len(sys.argv) == 4:
    infile = sys.argv[1]
    indir = sys.argv[2]
    outdir = sys.argv[3]
else:
    print('USAGE: python checkthedata.py <id,mr list> <exported fake-BIDS directory> <new BIDS valid directory')
    print(sys.argv)
    exit(2)

def readjson(jsonfile):
    import json
    with open(jsonfile) as f:
        data = json.load(f)
    return data

def writejson(data,outfile):
    import json
    with open(outfile, 'w') as outfile:
        json.dump(data, outfile,sort_keys=True,indent=2)
    outfile.close()


from glob import glob
import shutil

def editfiledir(bidsdir,newdir,subid,ses):
    # get directorory subjlist
    dirz=bidsdir + '/sub-'+subid +'/ses-'+ses
    subjdir=newdir + '/sub-'+subid +'/ses-'+ses
    os.makedirs(subjdir, exist_ok=True)
    anatdir=dirz+'/anat'
    perfdir= subjdir + '/perf'
    perfjson=glob(dirz+'/perf/*asl.json')
    # set a bunch of needed fields the same for everyone
    pldpcasl={"LabelingDuration": 1.450,"PostLabelingDelay": 2.025,"ArterialSpinLabelingType": "PCASL", "BackgroundSuppression": 'true', "RepetitionTimePreparation": 4.886 }
    for i in perfjson:
	    dataj=readjson(i)
	    dataj.update(pldpcasl)
	    # m0 set up right already so i got rid of the if statement but left this here
	    # dataj.update({"IntendedFor": "perf/sub-"+subid+'_ses-'+ses+"_acq-pcasl_asl.nii.gz"})
	    # writejson(dataj,perfdir+'/sub-'+subid+'_ses-'+ses+"_acq-pcasl_m0scan.json")
	    dataj.update({"M0Type": "Separate" })
	    writejson(dataj,perfdir+'/sub-'+subid+'_ses-'+ses+"_task-rest_asl.json")


subjl=pd.read_csv(infile, header=None)
for kk in range(0,len(subjl)):
    subid=str(subjl.iloc[kk][0]).zfill(6)
    sesid=str(subjl.iloc[kk][1])
    editfiledir(bidsdir=indir, newdir=outdir, subid=subid, ses=sesid)

    print(subid + sesid + " completed")


