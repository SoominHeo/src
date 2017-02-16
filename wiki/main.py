import make_dictionary
import wiki
import LCS

#wiki.make_list_csv()
#wiki.pair_dic()
#wiki.pair_cro()
dic = make_dictionary.make_dictionary()
start_idx = 0 
end_idx = 250000 
error_list = []
i = start_idx
while 1:
    if i > end_idx:
        break
    print(i)
    ck_link_list, e_link_list, percent = wiki.check_all_pair(dic, i)
    a = wiki.make_file_for_LCS(ck_link_list, e_link_list, dic, i)
    if a == -1 or percent==-1:
        i = i + 1
        print("makefileforLCS error")
        continue
    LCS.run_3LCS(i, percent)
    i = i + 1
