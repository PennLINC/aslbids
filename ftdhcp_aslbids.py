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
    subjdir=newdir + '/sub-'+subid +ses
    os.makedirs(subjdir, exist_ok=True)
    anatdir=dirz+'/anat'
    os.makedirs(subjdir+'/anat/', exist_ok=True)
    tonenii=glob(anatdir+'/sub-'+subid+'_ses-'+ses+'_rec-norm*T1w.nii.gz')
    tonej=glob(anatdir+'/sub-'+subid+'_ses-'+ses+'_rec-norm*T1w.json')
    ttwonii=glob(anatdir+'/sub-'+subid+'_ses-'+ses+'_rec-norm*T2w.nii.gz')
    ttwoj=glob(anatdir+'/sub-'+subid+'_ses-'+ses+'_rec-norm*T2w.json')
    if tonenii and ttwonii:
       shutil.copyfile(tonenii[0],subjdir+'/anat/sub-'+subid+ses+'_rec-norm_T1w.nii.gz')
       shutil.copyfile(tonej[0],subjdir+'/anat/sub-'+subid+ses+'_rec-norm_T1w.json')
       shutil.copyfile(ttwonii[0],subjdir+'/anat/sub-'+subid+ses+'_rec-norm_T2w.nii.gz')
       shutil.copyfile(ttwoj[0],subjdir+'/anat/sub-'+subid+ses+'_rec-norm_T2w.json')
    else :
       print("check anat dir for " + subid + ses)

    perfdir= subjdir + '/perf'
    os.makedirs(perfdir, exist_ok=True)
    perfjson=glob(dirz+'/perf/*json')
    pldpcasl={"LabelingDuration": 1.8,"PostLabelingDelay": 1.8,"ArterialSpinLabelingType": "PCASL","LabelingEfficiency": 0.72, "TotalAcquiredPairs": 14, "BackgroundSuppression": True, "LookLocker": False, "RepetitionTimePreparation": 4.2 }

    for i in  perfjson:
        dataj=readjson(i)
        if "M0" in dataj["SeriesDescription"]:
            dataj.update(pldpcasl)
            dataj.update({"IntendedFor": "perf/sub-"+subid+ses+"_acq-pcasl_asl.nii.gz"})
#            dataj.update({"M0Type": "Separate" })
            writejson(dataj,perfdir+'/sub-'+subid+ses+"_acq-pcasl_m0scan.json")
            aslnii = i.replace('json', 'nii.gz')
            shutil.copyfile(aslnii,perfdir+'/sub-'+subid+ses+"_acq-pcasl_m0scan.nii.gz")
        elif "ASL" in dataj["SeriesDescription"]:
            dataj.update(pldpcasl)
#            dataj.update({"IntendedFor": "perf/sub-"+subid+ses+"_task-rest_asl.nii.gz"})
            dataj.update({"M0Type": "Separate" })
            writejson(dataj,perfdir+'/sub-'+subid+ses+"_acq-pcasl_asl.json")
            aslnii = i.replace('json', 'nii.gz')
            shutil.copyfile(aslnii,perfdir+'/sub-'+subid+ses+"_acq-pcasl_asl.nii.gz")
            df=pd.DataFrame(["label","control","label","control","label","control","label","control","label","control","label","control","label","control","label","control","label","control","label","control","label","control","label","control","label","control","label","control"],columns=['volume_type'])
            df.to_csv(perfdir+'/sub-'+subid+ses+"_acq-pcasl_aslcontext.tsv",index=None)
  #       elif "MOSAIC" in dataj["ImageType"] and "ASL" in dataj["SeriesDescription"]:
  #          dataj.update(pldasl)
  #          writejson(dataj,perfdir+'/'+subid+"_"+ses+"_task-rest_asl.json")
  #          aslnii = i.replace('json', 'nii.gz')
  #          shutil.copyfile(aslnii,perfdir+'/'+subid+"_"+ses+"_task-rest_asl.nii.gz")
  #          df=pd.DataFrame(["label","control"],columns=['volume_type'])
  #          df.to_csv(perfdir+'/'+subid+"_"+ses+"_task-rest_aslcontext.tsv",index=None)



subjl=pd.read_csv(infile, header=None)
for kk in range(0,len(subjl)):
    subid=str(subjl.iloc[kk][0]).zfill(6)
    sesid=str(subjl.iloc[kk][1])
    editfiledir(bidsdir=indir, newdir=outdir, subid=subid, ses=sesid)
    print(subid + sesid + " completed")


