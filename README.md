# PRML final project
This repository contains the complementary programs commented on the final project report as well as the data needed to run them. The files correspond to:
 - auxiliar_fucntions.py: there are auxiliar functions to convert and compute the data.
 - ds_creator.py: it is the main program, the only that it is needed to run in order to obtain the dataset.

It also includes the "dataset.csv" file; this is the data set with which we obtained the results of the report. This can also be generated again by these programs mentioned above. However, we realized that we only achived to run it properly on Ubuntu OS. On Windows returns an error, and the reason seems to be that it reads the paths in a different way, not easy to manage with; but it is required when accessing to the "Data" folder with the original data files.

## Requirements
 - All .py files from the repository must be saved in the same folder.

 - To execute the ds_creator.py, a folder called "Data" (with all the .tcx files desired to convert to .csv), and another empty folder called "Outs" (where all converted .csv files will be stored) must exist in the same folder as the file in question.
