import os
from datetime import datetime
from conversor import tcx2csv, latlon2dist
import statistics as st


# Inspect all .tcx files of the first specified directory (in_path), including its subdirectories; and saves the homologs in the second specified directory (out_path) as .csv.
def loadData(in_path, out_path):
    counter = 0

    # Save a timestamp fro the files name to identify them easily.
    timestamp = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

    # Scans the entire input directory to convert all the files.
    for root, dirs, files in os.walk(in_path):
        for file in files:
            # Save the current file path.
            curr_file = root + "/" + file

            # Check if it is a .tcx file.
            if curr_file.split(".")[-1] == "tcx":
                counter = counter + 1

                # Convert TCX data into CSV data.
                tcx2csv(curr_file, out_path + "/" + timestamp + "_out_#" + str(counter) + ".csv")


# Inspect a set of lines information and return it as single summarizing dictionary.
def summarize(activity):
    # Read all file lines.
    file = open(activity, "r")
    lines = file.readlines()
    file.close()

    # Initialize a dictionary to manage the data easily.
    counter = 0
    dict = {}
    fields = []
    for line in lines:
        if counter == 0:  # For the first iteration.
            # Create all the fields in the dictionary.
            split_line = line.split(",")
            for field in split_line:
                dict[field.replace("\n", "")] = []
                fields.append(field)

        elif counter > 0:
            # Save the information in the relevant field.
            split_line = line.split(",")

            # Check if the information provided matches with the information expected.
            if len(split_line) == len(dict):
                i = 0
                for field in dict.keys():
                    # Remove any new line to avoid errors.
                    curr_value = split_line[i].replace("\n", "")
                    if i == 0:  # For the first field (time expected).
                        # Convert the timestamps into seconds (unix time).
                        dict[field].append(int(datetime.fromisoformat(curr_value[0:-1]).strftime("%s")))
                    else:
                        # Do not save the empty fields in the dictionary.
                        if curr_value != "NaN":
                            dict[field].append(float(curr_value))

                    i = i + 1
            else:
                print("ERROR summarize: " + str(len(dict)) + " fields are expected but only " + str(len(split_line)) + " was detected.\nContent: '" + line + "'\n")

        counter = counter + 1

    # Add extra fields from existing ones.
    dict["gps_speed"] = gpsSpeed(dict[fields[0]], dict[fields[1]], dict[fields[2]])  # Speed [m/s]
    dict["gps_acc"] = gpsAcc(dict[fields[0]], dict["gps_speed"])  # Acceleration [m/s²]

    # Initialize the summarizing dictionary to be returned.
    dict2 = {}
    for field in dict.keys():
        # Check that the field is not empty.
        if len(dict[field]) > 0:
            # Compute some statistics properties.
            dict2[field + "_max"] = max(dict[field])
            dict2[field + "_min"] = min(dict[field])
            dict2[field + "_mean"] = st.mean(dict[field])
            quant = st.quantiles(dict[field], n=4)
            dict2[field + "_q1"] = quant[0]
            dict2[field + "_q2"] = quant[1]
            dict2[field + "_q3"] = quant[2]

    # Add checksums at the end of each summarizing dictionary.
    dict2["fields_num"] = len(dict.keys())  # Number of assessed fields.
    dict2["props_num"] = 6  # Number of statistics properties considered.

    return dict2


# Inspect a set of latitudes and longitudes points to get the speed.
def gpsSpeed(time, lat, lon):
    gps_speed = [0]  # The first sample of the speed is not representative due to there are no information about the previous one.

    # Check that the given data is coherent.
    if len(time) == len(lat) == len(lon):
        for i in range(len(time)-1):
            curr_dist = latlon2dist(lat[i], lon[i], lat[i+1], lon[i+1])
            if time[i+1] != time[i]:
                curr_speed = curr_dist / (time[i+1] - time[i])
            gps_speed.append(curr_speed)
    else:
        print("ERROR gpsSpeed: the number of timestamps, latitudes and longitudes must be the same.")

    return gps_speed


# Inspect a set of speeds to get the accelerations.
def gpsAcc(time, speed):
    gps_acc = [0]  # The first sample of the acceleration, as well as the speed, is not representative due to there are no information about the previous one.
    if len(time) == len(speed):
        for i in range(len(time)-1):
            if time[i+1] != time[i]:
                curr_acc = (speed[i+1] - speed[i]) / (time[i+1] - time[i])
            gps_acc.append(curr_acc)
    else:
        print("ERROR gpsAcc: the number of timestamps and speeds must be the same.")

    return gps_acc