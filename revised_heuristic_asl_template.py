'''
    Heuristic file for BIDS classification of legacy data collected by the Penn 
    Frontotemporal Degeneration Center on the HUP 3T MRI scanner. The main
    function, infotodict, is defined below and takes sequence information from
    dicom headers; you can see which information is extracted by running
    fw-heudiconv-tabulate on the session directory, which writes the sequence
    info to a tsv file that can subsequently be read in as a Pandas dataframe.
    Each row of seqinfo corresponds to one series/acquisition in an imaging 
    session.
    
    See complete version history with comments by getting in touch with FTDC 
'''

# trimmed to ASL for TS - CO - 6/13/23

import datetime
import numpy as np

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes


#ASL
asl = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_asl')
asl_mz = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_m0scan')
asl_mp = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_cbf')
pcasl_3d = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_acq-3D_asl')
pcasl_3d_mz = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_acq-3D_m0scan')
pcasl_3d_mp = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_acq-3D_cbf')
# Should we use the acq entity like this? How specific should filenames strive to be?
pasl = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_acq-pasl_asl')
pasl_mp = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_acq-pasl_cbf')
casl = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_acq-casl_asl')
casl_mz = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_acq-casl_m0scan')
fairest = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_acq-fairest_asl')
fairest_mz = create_key('sub-{subject}/{session}/asl/sub-{subject}_{session}_acq-fairest_m0scan')

from collections import defaultdict
def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
        allowed template fields - follow python string module:
        index: index within category
        subject: participant id
        seqindex: run number during scanning
        subindex: sub index within group
    """

    info = {
        asl: [], asl_mz: [], asl_mp: [],
        pcasl_3d: [], pcasl_3d_mz: [], pcasl_3d_mp: [],
        pasl: [], pasl_mp: [], 
        casl: [], casl_mz: [],
        fairest: [], fairest_mz: []
    }
    
    for s in seqinfo:
        protocol = s.protocol_name.lower().replace(" ","_").replace("__","_")
        desc = s.series_description.lower().replace(" ","_").replace("__","_")
        id = s.series_id
        if s.date is not None:
            mydatetime = datetime.datetime.strptime(s.date, '%Y-%m-%dT%H:%M:%S.%f')
        else:
            mydatetime = None
        if "ep2d_se_pcasl_m0" in protocol:
            info[asl_mz].append(id)
        elif "3d_pasl" in protocol and "perfusion_weighted" in desc:
            info[pasl_mp].append(id)
        elif "3d_pasl" in protocol and "3d_pasl" in desc:
            info[pasl].append(id)
        elif "3d_pcasl" in protocol and "perfusion_weighted" in desc:
            info[pcasl_3d_mp].append(id)
        elif "3d_pcasl" in protocol and "3d_pcasl" in desc:
            info[pcasl_3d].append(id)
        elif "pcasl" in protocol and not "moco" in protocol:
            info[asl].append(id)
        elif "ep2d_casl_ui_1500ms" in protocol and not "moco" in protocol:
            info[casl].append(id)
        elif "ep2d_casl_am_ui_1500ms" in protocol and not desc == 'mocoseries':
            info[casl].append(id)
        elif "ep2d_casl_1500ms" in protocol and not desc == 'mocoseries':
            info[casl].append(id)
        elif "ep2d_casl_1500ms" in protocol and not "MOSAIC" in s.image_type:
            info[casl_mz].append(id)
        elif "spiral_v20_hcp" in protocol and "m0" in desc:
            info[asl_mz].append(id)
        elif "spiral_v20_hcp" in protocol and "meanperf" in desc:
            info[asl_mp].append(id)
        elif "spiral_v20_hcp" in protocol:
            info[asl].append(id)
        elif "asl_3dspiral_4shot_2.5mm_1daccel_v20" in protocol and "m0" in desc:
            info[asl_mz].append(id)
        elif "asl_3dspiral_4shot_2.5mm_1daccel_v20" in protocol and "meanperf" in desc:
            info[asl_mp].append(id)
        elif "asl_3dspiral_4shot_2.5mm_1daccel_v20" in protocol:
            info[asl].append(id)
        elif "ep2d_fairest_ui_m0" in protocol and not "moco" in protocol:
            info[fairest_mz].append(id)
        elif "fairest" in protocol and not "moco" in protocol:
            info[fairest].append(id)
        else:
            print("Series not recognized!: ", protocol, s.dcm_dir_name)

    # Get timestamp info to use as a sort key.
    # This helps when same sequence is run multiple times in a session (either false starts or repeats a la DTI
    def get_date(series_info):
        try:
            sortval = datetime.datetime.strptime(series_info.date, '%Y-%m-%dT%H:%M:%S.%f')
        except:
            sortval = series_info.series_uid
        return(sortval)
    
    # Before returning the info dictionary, 1) get rid of empty dict entries; and
    # 2) for entries that have more than one series, differentiate them by run-{index}.
    def update_key(series_key, runindex):
        series_name = series_key[0]
        s = series_name.split("_")
        nfields = len(s)
        s.insert(nfields-1, "run-" + str(runindex))
        new_name = "_".join(s)
        return((new_name, series_key[1], series_key[2]))

    newdict = {}
    delkeys = []
    for k in info.keys():
        ids = info[k]
        if len(list(set(ids))) > 1:
            series_list = [s for s in seqinfo if (s.series_id in ids)]
            uids = list(set([s.series_uid for s in series_list]))
            if len(uids) > 1:
                uids.sort()
                runnumb = 1
                for uid in uids:
                    series_matches = [s for s in series_list if s.series_uid == uid]
                    newkey = update_key(k, runnumb)
                    print("New key: ", uid, newkey, runnumb)
                    newdict[newkey] = [s.series_id for s in series_matches]
                    runnumb += 1
            elif None in uids:
            # Some sessions don't have UID info. In that case, sort by dcm_dir_name.
                dcm_dirs = list(set([s.dcm_dir_name for s in series_list]))
                dcm_dirs.sort()
                runnumb = 1
                for d in dcm_dirs:
                    series_matches = [s for s in series_list if s.dcm_dir_name == d]
                    newkey = update_key(k, runnumb)
                    newdict[newkey] = [s.series_id for s in series_matches]
                    runnumb += 1
            delkeys.append(k)
    # Merge the two dictionaries.
    info.update(newdict)
    

    # Delete keys that were expanded on in the new dictionary.
    for k in delkeys:
        info.pop(k, None)

    return info

def ReplaceSession(sesname):
    return sesname[:13].replace("-", "x").replace(".","x").replace("_","x")

def ReplaceSubject(subjname):
    return subjname[:10].replace("-", "x").replace(".","x").replace("_","x")

MetadataExtras = {

   fm_phasediff1: {
       "EchoTime1": 0.00255,
       "EchoTime2": 0.00501
   },

   fm_phasediff2: {
       "EchoTime1": 0.00406,
       "EchoTime2": 0.00652
   },

   fm_phasediff3: {
       "EchoTime1": 0.00411,
       "EchoTime2": 0.00657
   },

   fm_phasediff4: {
       "EchoTime1": 0.00492,
       "EchoTime2": 0.00738
   },

   fm_phasediff5: {
       "EchoTime1": 0.00412,
       "EchoTime2": 0.00658
   },

   fm_phasediff6: {
       "EchoTime1": 0.00519,
       "EchoTime2": 0.00765
   }

}       

IntendedFor = {

   # sorry really thought we'd sorted this out for M0s

}