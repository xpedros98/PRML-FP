import os
from datetime import datetime
from conversor import tcx2csv, latlon2dist
import re
import xml.etree.ElementTree as et
import math
import statistics as st


# Convert the input .tcx file and return a .csv file.
def tcx2csv(input, output):
    # Parse the XML data.
    tree = et.parse(input)
    root = tree.getroot()
    m = re.match(r"^({.*})", root.tag)
    if m:
        ns = m.group(1)
    else:
        ns = "NaN"
    if root.tag != ns + "TrainingCenterDatabase":
        print("Unknown root found: " + root.tag)
        return
    activities = root.find(ns + "Activities")
    if not activities:
        print("Unable to find Activities under root")
        return
    activity = activities.find(ns + "Activity")
    if not activity:
        print("Unable to find Activity under Activities")
        return
    columnsEstablished = False
    for lap in activity.iter(ns + "Lap"):
        if columnsEstablished:
            fout.write("New Lap\n")
        for track in lap.iter(ns + "Track"):
            # pdb.set_trace()
            if columnsEstablished:
                fout.write("New Track\n")
            for trackpoint in track.iter(ns + "Trackpoint"):
                try:
                    time = trackpoint.find(ns + "Time").text.strip()
                except:
                    time = "NaN"
                try:
                    latitude = trackpoint.find(ns + "Position").find(ns + "LatitudeDegrees").text.strip()
                except:
                    latitude = "NaN"
                try:
                    longitude = trackpoint.find(ns + "Position").find(ns + "LongitudeDegrees").text.strip()
                except:
                    longitude = "NaN"
                try:
                    altitude = trackpoint.find(ns + "AltitudeMeters").text.strip()
                except:
                    altitude = "NaN"
                try:
                    bpm = trackpoint.find(ns + "HeartRateBpm").find(ns + "Value").text.strip()
                except:
                    bpm = "NaN"

                counter = 0
                for el in trackpoint.find(ns + "Extensions"):
                    counter = counter + 1
                    element = el

                if counter > 0:
                    ns2 = re.match(r"^({.*})", element.tag).group(1)
                    try:
                        spd = trackpoint.find(ns + "Extensions").find(ns2 + "TPX").find(ns2 + "Speed").text.strip()
                    except:
                        spd = "NaN"
                    try:
                        rcd = trackpoint.find(ns + "Extensions").find(ns2 + "TPX").find(ns2 + "RunCadence").text.strip()
                    except:
                        rcd = "NaN"
                if not columnsEstablished:  # For the first iteration.
                    # Create the output file.
                    fout = open(output, "w+")

                    # Save the headers
                    fout.write(",".join(("Time", "LatitudeDegrees", "LongitudeDegrees", "AltitudeMeters", "HeartRatebpm", "Speed", "RunCadence")) + "\n")

                    # Indicate that the headers are added.
                    columnsEstablished = True

                # Save the data.
                fout.write(",".join((time, latitude, longitude, altitude, bpm, spd, rcd)) + "\n")

    # Close the file.
    fout.close()


# Convert two latitude and longitude points into distance measure.
def latlon2dist(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius [km]

    # Convert the latitude and longitude in deg to rad.
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # Compute the speed (copied algorithm from internet).
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c / 1000  # Distance [m]
    return d


# Inspect all .tcx files of the first specified directory (in_path), including its subdirectories; and saves the homologs in the second specified directory (out_path) as .csv.
def loadData(in_path, out_path):
    counter = 0

    # Save a timestamp fro the files name to identify them easily.
    timestamp = "" #datetime.now().strftime("%d-%m_%H:%M")

    # Scans the entire input directory to convert all the files.
    for root, dirs, files in os.walk(in_path):
        for file in files:
            # Save the current file path.
            curr_file = root + "/" + file

            # Check if it is a .tcx file.
            if curr_file.split(".")[-1] == "tcx":
                counter = counter + 1

                # Save the enough path parts to interpret which sport was recorded in each file.
                split_path = curr_file.split("/")
                # split_path = split_path[-1].split("\\")
                indx = split_path.index("Data")

                # Convert TCX data into CSV data.
                tcx2csv(curr_file, out_path + "/" + "#" + str(counter) + "_" + timestamp + "_" + "_".join(split_path[indx:-1]) + ".csv")


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
                        else:
                            dict[field].append("NaN")

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
            if dict[field][0] != "NaN":
                # Compute some statistics properties.
                dict2[field + "_max"] = max(dict[field])
                dict2[field + "_min"] = min(dict[field])
                dict2[field + "_mean"] = st.mean(dict[field])
                quant = st.quantiles(dict[field], n=4)
                dict2[field + "_q1"] = quant[0]
                dict2[field + "_q2"] = quant[1]
                dict2[field + "_q3"] = quant[2]
            else:
                # Fill the gaps.
                dict2[field + "_max"] = "NaN"
                dict2[field + "_min"] = "NaN"
                dict2[field + "_mean"] = "NaN"
                dict2[field + "_q1"] = "NaN"
                dict2[field + "_q2"] = "NaN"
                dict2[field + "_q3"] = "NaN"

    # Add a label for each activity.
    main_label = "ERROR"
    act_folders = activity.split("/")[-1]
    if -1 < act_folders.find("Run") or -1 < act_folders.find("Trail") or -1 < act_folders.find("Asfalt") or -1 < act_folders.find("run"):
        main_label = "run"
    elif -1 < act_folders.find("Cycling") or -1 < act_folders.find("Bici") or -1 < act_folders.find("Bycicle") or -1 < act_folders.find("BTT") or -1 < act_folders.find("bici"):
        main_label = "bike"
    elif -1 < act_folders.find("Walk"):
        main_label = "walk"
    elif -1 < act_folders.find("Car") or -1 < act_folders.find("Bus") or -1 < act_folders.find("Cotxe") or -1 < act_folders.find("Metro") or -1 < act_folders.find("Tramvia"):
        main_label = "vehicle"
    elif -1 < act_folders.find("Test"):
        main_label = "test"
    else:
        print("No label detected for: " + act_folders)
        print("Indicate the main label manually: ", end="")
        main_label = input()

    dict2["label"] = main_label

    # Add checksums at the end of each summarizing dictionary.
    dict2["fields_num"] = len(dict.keys())  # Number of assessed fields.
    dict2["props_num"] = 6  # Number of statistics properties considered.
    dict2["#ref"] = act_folders.split("_")[0]

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

