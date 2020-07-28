# aslbids

This code helps to convert ASL data to bids format as propopsed in  [ASLBIDS](https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c/edit#) 

First, the dicom files need to be convereted to bids with [heudiconv](https://github.com/nipy/heudiconv) and require heuristic file.

For example with sample heuritic file (`heuristic.py`) 

` heudiconv --files dicomdirectory  -s subjectid  -ss session_id -o  outputbidsdirectory  --bids  -f heuristic.py `

Second step is to edit ASL json files with  `edit_aslbids.py`. It require json files (see example `metadataextra.jon`) that contain extra metadata for ASL,MO and mean CBF as proposed in [ASLBIDS](https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c/edit#). 


`edit_aslbids.py  -s SUBJECT_ID -t SESSION_ID -b BIDS_DIR -j JSONTEMPLATE -l ASL_LABEL] [--fieldmap]`

1. SUBJECT_ID > subject id e.g sub-XX, require
2. SESSION_ID > session id e.g ses-YY, require if the bids has seission
3. BIDS_DIR > bids output of  heudiconv 
4. JSONTEMPLATE > metadetata for asl,m0 and mean CBF, there is sample here (`metadataextra.json`) and should be edited as required 
5. ASL_LABEL > for asl tag, asl(`Label-Control` or `Control-Label`)
fieldmap > this is to include asl,m0 and cbf in fieldmap  if shims settings are the same 


On [flywheel](flywheel.io) using [fw-heudiconv](https://github.com/PennBBL/fw-heudiconv), the extra metadata and ASLContext files can be specified in your heuristic during curation.

1. Use the `tabulate` tool to extract your ASL parameters from DICOM headers
2. Use the `MetadataExtras` variable to hard code these parameters (see [example](https://fw-heudiconv.readthedocs.io/en/latest/heuristic.html#fw_heudiconv.example_heuristics.demo.MetadataExtras))
3. Dynamically create the ASLContext file in your heuristic (see [example](https://fw-heudiconv.readthedocs.io/en/latest/tips.html#arterial-spin-labelling-data))
4. Re-curate your dataset
