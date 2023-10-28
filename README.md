# Four_Papaver_HiFi
The analysis scripts used in four Papaver HiFi centromere satellites analysis projects.
There are 13 scripts, and the introduction and description as following:

1_buildingSatellites.sh   `the script used to build satellite library`

2_processTRFforlastz.py   `the script used to filter TRF results to get tandem repeat regions`

3_filterNamelist.py       `the script used to filter the TRF overlapping results`

4_splitNamelist.py        `the script used to split the files for parallel`

5.1_runSD_batch.sh        `the script used to run StringDecomposer`

5.2_checkSD.py            `the script used to checke the StringDecomposer results`

6_getSDContinueRegion.py  `the script used to obtain the continues regions from StringDecomposer results`

7_run_batch_lastz.sh      `the script used to run lastZ`

8_run_batch_edge.sh       `the script used to get the edges between satellites`

9_mergeEdge.py            `the script used to merge the edges for final edge list`

10_buildSatellates.py     `the script used to obtain satellites and name them, like Prh168S1`

11_panLastz.py            `the script used to obtain the satellites shared in multip-species`

12_panEdge.py             `the script used to construct edge list of cross species satellites`

13_getLastzRegion.py      `the script used to obtain the lastZ alignment regions given a specific satellite`

