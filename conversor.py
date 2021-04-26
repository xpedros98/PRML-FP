import re
import xml.etree.ElementTree as et


# takes in a TCX file and outputs a CSV file
def tcx2csv(input, output):
    tree = et.parse(input)
    root = tree.getroot()
    m = re.match(r'^({.*})', root.tag)
    if m:
        ns = m.group(1)
    else:
        ns = 'NaN'
    if root.tag != ns + 'TrainingCenterDatabase':
        print('Unknown root found: ' + root.tag)
        return
    activities = root.find(ns + 'Activities')
    if not activities:
        print('Unable to find Activities under root')
        return
    activity = activities.find(ns + 'Activity')
    if not activity:
        print('Unable to find Activity under Activities')
        return
    columnsEstablished = False
    for lap in activity.iter(ns + 'Lap'):
        if columnsEstablished:
            fout.write('New Lap\n')
        for track in lap.iter(ns + 'Track'):
            # pdb.set_trace()
            if columnsEstablished:
                fout.write('New Track\n')
            for trackpoint in track.iter(ns + 'Trackpoint'):
                try:
                    time = trackpoint.find(ns + 'Time').text.strip()
                except:
                    time = 'NaN'
                try:
                    latitude = trackpoint.find(ns + 'Position').find(ns + 'LatitudeDegrees').text.strip()
                except:
                    latitude = 'NaN'
                try:
                    longitude = trackpoint.find(ns + 'Position').find(ns + 'LongitudeDegrees').text.strip()
                except:
                    longitude = 'NaN'
                try:
                    altitude = trackpoint.find(ns + 'AltitudeMeters').text.strip()
                except:
                    altitude = 'NaN'
                try:
                    bpm = trackpoint.find(ns + 'HeartRateBpm').find(ns + 'Value').text.strip()
                except:
                    bpm = 'NaN'

                counter = 0
                for el in trackpoint.find(ns + 'Extensions'):
                    counter = counter + 1
                    element = el

                if counter > 0:
                    ns2 = re.match(r'^({.*})', element.tag).group(1)
                    try:
                        spd = trackpoint.find(ns + 'Extensions').find(ns2 + 'TPX').find(ns2 + 'Speed').text.strip()
                    except:
                        spd = 'NaN'
                    try:
                        rcd = trackpoint.find(ns + 'Extensions').find(ns2 + 'TPX').find(ns2 + 'RunCadence').text.strip()
                    except:
                        rcd = 'NaN'
                if not columnsEstablished:
                    fout = open(output, 'w+')
                    fout.write(','.join(('Time', 'LatitudeDegrees', 'LongitudeDegrees', 'AltitudeMeters', 'heartratebpm/value', 'Speed','RunCadence')) + '\n')
                    columnsEstablished = True
                fout.write(','.join((time, latitude, longitude, altitude, bpm, spd, rcd)) + '\n')

    fout.close()
