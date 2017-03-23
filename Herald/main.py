import LCS
import en_Num
import ko_Num
import div_eng
import div_kor
import herald_word_text
import ngram
import lcslib
#count = herald_word_text.herald_word_text(0,6)
#print(count)
#div_eng.div_eng(0,1800)
#div_kor.div_kor(0,1800)
#en_Num.en_Num(0,1798)
#ko_Num.ko_Num(0,1798)

#lcslib.check_answer([],1,"word_fill",5,0.3)

#ngram.storeDictionary("../../final_dic.csv","../../dictionary.csv",266081)
root = ngram.getRoot("../../dictionary.csv")
LCS.run(1,1798,root,5,5,3,3)
#LCS2.run(0,1831,dic,5,5,3,9)
#LCS.run2(1,5,3,3)
