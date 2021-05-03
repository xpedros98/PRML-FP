from inspector import loadData, summarize
import os

# Convert all .tcx files of the "Data" folder of the project to .csv files in the "Outs" folder of the project.
loadData(os.path.dirname(__file__) + "/Data", os.path.dirname(__file__) + "/Outs")


# Initialize the dataset file.
ds = open(os.path.dirname(__file__) + "/dataset.csv", "w+")

# Merge all information of the .csv files of the "Outs" folder of the project into a single .csv dataset.
counter = 0
for file in os.listdir(os.path.dirname(__file__) + "/Outs"):
    # Compress the information for each activity into statistical data.
    out_dict = summarize(os.path.dirname(__file__) + "/Outs/" + file)

    line = ""
    if counter == 0:  # For the first iteration.
        # Save the headers.
        for field in out_dict.keys():
            line = line + field + ","

        # Remove the last comma to avoid a confusion of an extra field.
        line = line[0:-1]

        # Add entry to the dataset.
        ds.write(line + "\n")

        line = ""

        # Save the information.
        for field in out_dict.keys():
            line = line + str(out_dict[field]) + ","

        # Remove the last comma to avoid a confusion of an extra field.
        line = line[0:-1]

        # Add entry to the dataset.
        ds.write(line + "\n")
    else:
        # Save the information.
        for field in out_dict.keys():
            line = line + str(out_dict[field]) + ","

        # Remove the last comma to avoid a confusion of an extra field.
        line = line[0:-1]

        # Add entry to the dataset.
        ds.write(line + "\n")

    counter = counter + 1

ds.close()



