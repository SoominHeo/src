import make_dictionary
import wiki
import LCS
import random
#wiki.make_list_csv()
#wiki.pair_dic()
#wiki.pair_cro()
dic = make_dictionary.make_dictionary()
start_idx = 0 
end_idx = 250000 
error_list = []
i = start_idx
random_list = []
for x in range(230000):
    random_list.append(x)

random.shuffle(random_list)
while 1:
    r = random_list[i]
    if i > end_idx:
        break
    print(str(i)+"\t"+str(r))
    ck_link_list, e_link_list, percent = wiki.check_all_pair(dic, r)
    print(percent)
    a = wiki.make_file_for_LCS(ck_link_list, e_link_list, dic, r)
    if a == -1 or percent==-1:
        i = i + 1
        print("makefileforLCS error")
        continue
    LCS.run_3LCS(r, percent)
    i = i + 1
