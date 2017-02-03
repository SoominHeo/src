import make_dictionary
import wiki
import LCS

#wiki.make_list_csv()
#wiki.pair_dic()
dic = make_dictionary.make_dictionary()
#wiki.pair_cro()

i = 0
while 1:
    print (str(i)+".txt")
    ck_link_list, e_link_list = wiki.check_all_pair(dic, i)
    wiki.make_file_for_LCS(ck_link_list, e_link_list, i)
    LCS.using_LCS(i)
    i = i + 1

