from inspector import loadData, summarize
import os

loadData(os.path.dirname(__file__) + "/Data", os.path.dirname(__file__) + "/Outs")

counter = 0
for file in os.listdir(os.path.dirname(__file__) + "/Outs"):
    out_dict = summarize(os.path.dirname(__file__) + "/Outs/" + file)
    ds = open(os.path.dirname(__file__) + "/dataset.csv", "w+")
    if counter == 0:
        for field in out_dict.keys():
            ds.write(field)

        ds.write("\n")
    else:
        for field in out_dict.keys():
            ds.write(out_dict[field])

        ds.write("\n")

    print("nice")



