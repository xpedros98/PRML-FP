import os
import glob
from datetime import datetime
from conversor import tcx2csv


def loadData(in_path, out_path):
    counter = 0
    timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    for root, dirs, files in os.walk(in_path):
        for file in files:
            curr_file = root + "/" + file
            if curr_file.split(".")[-1] == "tcx":
                counter = counter + 1
                tcx2csv(curr_file, out_path + "/out_#" + str(counter) + "_" + timestamp + ".csv")