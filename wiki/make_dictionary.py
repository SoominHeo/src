import re
csv_path = "../../data/wiki/dic.csv"
def make_dictionary():
    dict = {}
    f = open(csv_path, "r", encoding="UTF8")
    lines = f.readlines()
    for line in lines:
        splt = re.split(",\t|\n", line)
        dict[splt[2]] = splt[3]
    f.close()
    return dict
