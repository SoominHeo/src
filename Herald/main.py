import LCS
import en_Num
import ko_Num
import div_eng
import div_kor
import herald_word_text
import lcslib
#count = herald_word_text.herald_word_text(0,0)
#print(count)
#div_eng.div_eng(0,1831)
#div_kor.div_kor(0,1831)
#en_Num.en_Num(0,1831)
#ko_Num.ko_Num(0,1831)
dic = lcslib.make_dict()
LCS.run(1831,dic,1,5,3,9)
#LCS.run2(1,1,3,3)
