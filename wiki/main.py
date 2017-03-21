import LCS
import en_Num
import ko_Num
import wiki
import ngram
import lcslib
#count = herald_word_text.herald_word_text(0,6)
#print(count)
#div_eng.div_eng(0,1800)
#div_kor.div_kor(0,1800)
# en_Num.en_Num(0,1798)
# ko_Num.ko_Num(0,1798)

start_idx = 1;
end_idx = 1;
root = ngram.getRoot("dictionary.csv")
errorLogFile = open("log.txt",'w',encoding='utf8')
while 1:
	idx = start_idx;
	if idx > end_idx:
		break
	kLink, eLink, percent = wiki.check_all_pair(root,idx)
	check = wiki.make_file_for_LCS(kLink,eLink,root,r)
	if check == -1 or percent == -1:
		i += 1
		print("makefileforLCS error")
		continue
	
	en_Num.en_Num(idx,idx)
	ko_Num.ko_Num(idx,idx)
	LCS.run(idx,idx,root,5,5,3,3)
#LCS2.run(0,1831,dic,5,5,3,9)
#LCS.run2(1,5,3,3)
