# aslbids

This code helps to convert ASL data to bids format as propopsed in  [ASLBIDS](https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c/edit#) 

First, the dicom files need to be convereted to bids with [heudiconv](https://github.com/nipy/heudiconv) and require heuristic file.

For example with sample heuritic file (`heuristic.py`) 

` heudiconv --files dicomdirectory  -s subjectid  -ss session_id -o  outputbidsdirectory  --bids  -f heuristic.py `

Second step is to edit ASL json files with  `edit_aslbids.py`. It require json files (see example [metadataextra.jon](https://github.com/PennLINC/aslbids/blob/master/metadataextra.json) that contain extra metadata for ASL,MO and mean CBF as proposed in [ASLBIDS](https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c/edit#). The [metadataextra.jon](https://github.com/PennLINC/aslbids/blob/master/metadataextra.json) also  has `asllabel` to be specify for each volume to write out the `aslcontext`.

The most important paremeters required for [ASLPREP](https://aslprep.readthedocs.io/en/latest/usage.html#command-line-arguments) are::  

            "LabelingType": labeling type, either PCASL or ASL
            "LabelingDuration": labeling duraion in seconds
            "PostLabelingDelay": post labeling delayin seconds
            "BackgroundSuppression": Yes or no
            "M0Scale": MO scale , defualt is 1
            "LabelingEfficiency": default are use depending on labeling type (PCASL or ASL)

`edit_aslbids.py  -s SUBJECT_ID -t SESSION_ID -b BIDS_DIR -j JSONTEMPLATE `

1. SUBJECT_ID > subject id e.g sub-XX, require
2. SESSION_ID > session id e.g ses-YY, require if the bids has seission
3. BIDS_DIR > bids output of  heudiconv 
4. JSONTEMPLATE > metadetata for asl,m0 and mean CBF, there is sample here (`metadataextra.json`) and should be edited as required 



On [flywheel](flywheel.io) using [fw-heudiconv](https://github.com/PennBBL/fw-heudiconv), the extra metadata and ASLContext files can be specified in your heuristic during curation.

1. Use the `tabulate` tool to extract your ASL parameters from DICOM headers
2. Use the `MetadataExtras` variable to hard code these parameters (see [example](https://fw-heudiconv.readthedocs.io/en/latest/heuristic.html#fw_heudiconv.example_heuristics.demo.MetadataExtras))
3. Dynamically create the ASLContext file in your heuristic (see [example](https://fw-heudiconv.readthedocs.io/en/latest/tips.html#arterial-spin-labelling-data))
4. Re-curate your dataset
