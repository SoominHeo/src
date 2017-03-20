import LCS
import en_Num
import ko_Num
import no_single_space
import JoongangDaily
import ngram
import lcslib
#count = no_single_space.no_single_space(0,6)
#print(count)



#lcslib.check_answer([],1,"word_fill",5,0.3)

#ngram.storeDictionary("final_dic.csv","dictionary.csv",266081)

#LCS2.run(0,1831,dic,5,5,3,9)
#LCS.run2(1,5,3,3)

# JoongangDaily.save_content(0,10)
# no_single_space.no_single_space(0,10)

#print("number_ko")

#ko_Num.ko_Num(0,10)
#print("number_en")

#en_Num.en_Num(0,10)
#print("LCS")
#8217
root = ngram.getRoot("dictionary.csv")
LCS.run(1,1,root,5,5,3,3)
