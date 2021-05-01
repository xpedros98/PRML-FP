import os
from datetime import datetime
from conversor import tcx2csv, latlon2dist
import statistics as st


# Inspect all .tcx files of the first specified directory (in_path), including its subdirectories; and saves the homologs in the second specified directory (out_path) as .csv.
def loadData(in_path, out_path):
    counter = 0
    timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    for root, dirs, files in os.walk(in_path):
        for file in files:
            curr_file = root + "/" + file
            if curr_file.split(".")[-1] == "tcx":
                counter = counter + 1
                tcx2csv(curr_file, out_path + "/" + timestamp + "_out_#" + str(counter) + ".csv")


# Inspect a set of lines information into a single summarizing line.
def summarize(activity):

    file = open(activity, "r")
    lines = file.readlines()
    file.close()

    counter = 0
    dict = {}
    fields = []
    for line in lines:
        if counter == 0:
            split_line = line.split(",")
            for field in split_line:
                dict[field.replace("\n", "")] = []
                fields.append(field)
        elif counter > 0:
            split_line = line.split(",")
            if len(split_line) == len(dict):
                i = 0
                for field in dict.keys():
                    curr_value = split_line[i].replace("\n", "")
                    if i == 0:
                        dict[field].append(int(datetime.fromisoformat(curr_value[0:-1]).strftime("%s")))
                    else:
                        if curr_value != "NaN":
                            dict[field].append(float(curr_value))

                    i = i + 1
            else:
                print("ERROR summarize: 7 fields are expected for each line.")

        counter = counter + 1

    dict["gps_speed"] = gpsSpeed(dict[fields[0]], dict[fields[1]], dict[fields[2]])

    dict["gps_acc"] = gpsAcc(dict[fields[0]], dict["gps_speed"])

    dict2 = {}
    for field in dict.keys():
        if dict[field][0] != "NaN":
            dict2[field + "_max"] = max(dict[field])
            dict2[field + "_min"] = min(dict[field])
            dict2[field + "_mean"] = st.mean(dict[field])
            quant = st.quantiles(dict[field], n=4)
            dict2[field + "_q1"] = quant[0]
            dict2[field + "_q2"] = quant[1]
            dict2[field + "_q3"] = quant[2]

    dict2["fields_num"] = len(dict.keys())  # Number of fields assessed.
    dict2["props_num"] = 6  # Number of statistics properties considered.

    return dict2


# Inspect a set of latitudes and longitudes points to get the speed.
def gpsSpeed(time, lat, lon):
    gps_speed = [0]
    if len(time) == len(lat) == len(lon):
        for i in range(len(lat)-1):
            curr_dist = latlon2dist(lat[i], lon[i], lat[i+1], lon[i+1])
            curr_speed = curr_dist / (time[i+1] - time[i])
            gps_speed.append(curr_speed)
    else:
        print("ERROR gpsSpeed: the number of timestamps, latitudes and longitudes must be the same.")

    return gps_speed


# Inspect a set of latitudes and longitudes points to get the speed.
def gpsAcc(time, speed):
    gps_acc = [0]  # The first sample of the acceleration, as well as the speed, is not representative due to there are no information about the previous one.
    if len(time) == len(speed):
        for i in range(len(time)-1):
            curr_acc = (speed[i+1] - speed[i]) / (time[i+1] - time[i])
            gps_acc.append(curr_acc)
    else:
        print("ERROR gps: the number of timestamps, latitudes and longitudes must be the same.")

    return gps_acc