import LCS
header_path = "../../data/wiki/header/{lang}/{idx}.txt"
result_path = "../../data/wiki/result/{lang}/{idx}.txt"
def run_3LCS(index):
    a = [[5,6], [10,11], [11,12], [12,13]]
    b = [[4,6], [5,7], [6,8]]
    c = []

    k_lst = []
    e_lst = []

    for i in range(len(a)):
        k_lst.append(a[i][0])
        e_lst.append(a[i][1])

    for i in range(len(b)):
        if (b[i][0] not in k_lst) and (b[i][1] not in e_lst):
            k_lst.append(b[i][0])
            e_lst.append(b[i][1])

    for i in range(len(c)):
        if (c[i][0] not in k_lst) and (c[i][1] not in e_lst):
            k_lst.append(c[i][0])
            e_lst.append(c[i][1])

    print(k_lst)
    print(e_lst)

    try:
        f_ko = open(header_path.format(lang='kor',idx=index),"rU", encoding="UTF8")
        f_en = open(header_path.format(lang='eng',idx=index),,"rU", encoding="UTF8")
    except:
        return -1

    k_result = open(result_path.format(lang='kor',idx=index),"w", encoding="UTF8")
    e_result = open(result_path.format(lang='eng',idx=index),"w", encoding="UTF8")

    k_contents = f_ko.readlines()
    e_contents = f_en.readlines()

    print (len(k_contents), len(e_contents))
    for i in range(len(k_lst)):
        print (k_lst[i], e_lst[i])
        k_result.write(k_contents[i])
        e_result.write(e_contents[i])

run_3LCS(1)
