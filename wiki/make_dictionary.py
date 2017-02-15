import re
csv_path = "../../data/wiki/data.csv"
def make_dictionary():
    dict = {}
    f = open(csv_path, "r", encoding="UTF8")
    lines = f.readlines()
    a = 0
    for line in lines:
        splt = re.split(",\t|\n", line)
        dict[splt[2]] = splt[3].replace("_"," ")
    f.close()
    return dict
