import LCS
import en_Num
import ko_Num
import wiki
import ngram
import lcslib
import make_dictionary

#count = herald_word_text.herald_word_text(0,6)
#print(count)
#div_eng.div_eng(0,400)
#div_kor.div_kor(0,400)
#en_Num.en_Num(0,400)
#ko_Num.ko_Num(0,400)
dic = make_dictionary.make_dictionary()
start_idx = 0;
end_idx = 400;
root = ngram.getRoot("../../dictionary.csv")
errorLogFile = open("log.txt",'w',encoding='utf8')
idx = start_idx;
while 1:

	if idx > end_idx:
		break

	if(idx%10!=0):
		idx = idx+1
		continue
	
	print(str(idx)+".txt")
	kLink, eLink, percent = wiki.check_all_pair(dic,idx)

	print("check all pair end")
	#check = wiki.make_file_for_LCS(kLink,eLink,root,idx)
	#print("make file for lcs end")
	if percent == -1:
		i += 1
		idx = idx+1
		print("makefileforLCS error")
		continue

	en_Num.en_Num(idx,idx)
	print("en num end")
	ko_Num.ko_Num(idx,idx)
	print("ko num end")
	LCS.run(idx,idx,root,5,5,3,3,kLink,eLink)
	idx = idx+1
#LCS2.run(0,1831,dic,5,5,3,9)
#LCS.run2(1,5,3,3)
