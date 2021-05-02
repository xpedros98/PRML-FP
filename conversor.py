import re
import xml.etree.ElementTree as et
import math


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
