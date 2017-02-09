import make_dictionary
import wiki
import LCS

#wiki.make_list_csv()
#wiki.pair_dic()
dic = make_dictionary.make_dictionary()
#wiki.pair_cro()
start_idx = 0
end_idx = 9999
error_list = []
i = start_idx
while 1:
    if i > end_idx:
        break
    try:
        print (str(i)+".txt")
        ck_link_list, e_link_list = wiki.check_all_pair(dic, i)
        a = wiki.make_file_for_LCS(ck_link_list, e_link_list, i)
        if a == -1:
            i = i + 1
            continue
        LCS.run_3LCS(i)
        i = i + 1
    except:
        error_list.append(i)
        i = i + 1



print(error_list)
