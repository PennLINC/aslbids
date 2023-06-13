# aslbids

This code helps to convert ASL data to BIDS format.

First, the dicom files need to be converted to BIDS with [heudiconv](https://github.com/nipy/heudiconv), which requires a heuristic file.

For example, using the sample heuritic file `heuristic.py`, you could call:

```
heudiconv --files dicomdirectory  -s subjectid  -ss session_id -o  outputbidsdirectory  --bids  -f heuristic.py
```

The second step is to edit the ASL json files with `edit_aslbids.py`.
This script requires json files
(see example [metadataextra.json](https://github.com/PennLINC/aslbids/blob/master/metadataextra.json))
that contains extra metadata for ASL, MO, and mean CBF scans.
The [metadataextra.json](https://github.com/PennLINC/aslbids/blob/master/metadataextra.json) also has `asllabel` to specify for each volume to write out the `aslcontext`.

The most important paremeters required for [ASLPrep](https://aslprep.readthedocs.io/en/latest/usage.html#command-line-arguments) are:

- "ArterialLabelingType": labeling type, either PCASL or ASL
- "LabelingDuration": labeling duraion in seconds
- "PostLabelingDelay": post labeling delay in seconds
- "BackgroundSuppression": true or false
- "LabelingEfficiency": default are use depending on labeling type (PCASL or ASL)

```
edit_aslbids.py  -s SUBJECT_ID -t SESSION_ID -b BIDS_DIR -j JSONTEMPLATE
```

1. SUBJECT_ID > subject id e.g sub-XX, require
2. SESSION_ID > session id e.g ses-YY, require if the bids has seission
3. BIDS_DIR > bids output of  heudiconv
4. JSONTEMPLATE > metadetata for asl,m0 and mean CBF, there is sample here (`metadataextra.json`) and should be edited as required

On [flywheel](flywheel.io) using [fw-heudiconv](https://github.com/PennBBL/fw-heudiconv), the extra metadata and ASLContext files can be specified in your heuristic during curation.

1. Use the `tabulate` tool to extract your ASL parameters from DICOM headers
2. Use the `MetadataExtras` variable to hard code these parameters (see [example](https://fw-heudiconv.readthedocs.io/en/latest/heuristic.html#fw_heudiconv.example_heuristics.demo.MetadataExtras))
3. Dynamically create the ASLContext file in your heuristic (see [example](https://fw-heudiconv.readthedocs.io/en/latest/tips.html#arterial-spin-labelling-data))
4. Re-curate your dataset
