import make_dictionary
import wiki

#wiki.make_list_csv()
#wiki.pair_dic()
dic = make_dictionary.make_dictionary()
#wiki.pair_cro()

i = 0
while 1:
    print (str(i)+".txt")
    wiki.check_all_pair(dic, i)
    if i == 10: break
    i = i + 1

#LCS()