import os
from datetime import datetime
from conversor import tcx2csv, latlon2dist


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
    time = []
    lat = []
    lon = []
    alt = []
    bpm = []
    speed = []
    cad = []

    file = open(activity, 'r')
    lines = file.readlines()
    file.close()

    counter = 0
    for line in lines:
        if counter > 0:
            split_line = line.split(',')
            if len(split_line) == 7:
                curr_seconds = int(datetime.fromisoformat(split_line[0][0:-1]).strftime("%s"))
                time.append(curr_seconds)
                lat.append(split_line[1])
                lon.append(split_line[2])
                alt.append(split_line[3])
                bpm.append(split_line[4])
                speed.append(split_line[5])
                cad.append(split_line[6])
            else:
                print("ERROR summarize: 7 fields are expected for each line.")

        counter = counter + 1

        gps_speed = gpsSpeed(time, lat, lon)


# Inspect a set of latitudes and longitudes points to get the speed.
def gpsSpeed(time, lat, lon):
    gps_speed = [0]
    if len(time) == len(lat) == len(lon):
        for i in range(len(lat)-1):
            curr_dist = latlon2dist(lat[i], lon[i], lat[i+1], lon[i+1])
            curr_speed = curr_dist / (time[i+1] - time[i])
            gps_speed.append(curr_speed)

        # Save last speed equal to the last value since there are not enough information to calculate it properly.
        gps_speed.append(curr_speed)
    else:
        print("ERROR gpsSpeed: the number of timestamps, latitudes and longitudes must be the same.")

    return gps_speed
