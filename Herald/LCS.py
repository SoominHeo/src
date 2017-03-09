import lcslib
import special_feature

original_url = "./../../data/Herald/sample/{lang}/{idx}.txt"
number_url = "./../../data/Herald/NUM/{lang}/{idx}.txt"
result_url = "./../../data/Herald/LCS/{subtype}/{lang}/{distance_value}/{jaccard_value}/{idx}.txt"

maintype = "word"
subtype = "word_fill"
# noun_url = "./../data/NNP"

#make dictionary
#dic = lcslib.make_dict()
# total =0
# get original_text
def LCS(idx,root,maintype,subtype,distance_value,jaccard_value):
	print(idx)
	jaccard_value = float(jaccard_value) / 10.0 # for control line_lcs jaccard value
	print("distance value : ",distance_value)
	print("jaccard value :",jaccard_value)
	lcslib.check_directory(subtype,distance_value,jaccard_value) # make directory
	kor_file = open(original_url.format(lang ="kor",idx = idx),'r',encoding='utf8')
	eng_file = open(original_url.format(lang ="eng",idx = idx),'r',encoding='utf8')
	kor_number = open(number_url.format(lang="kor",idx=idx),'r')
	eng_number = open(number_url.format(lang="eng",idx=idx),'r')
	result_kor_file = open(result_url.format(subtype = subtype, lang = 'kor',distance_value = distance_value, jaccard_value = jaccard_value, idx=idx),'w',encoding='utf8')
	result_eng_file = open(result_url.format(subtype = subtype, lang = 'eng',distance_value = distance_value, jaccard_value = jaccard_value, idx=idx),'w',encoding='utf8')
	result = []
	kor_text = kor_file.readlines()
	eng_text = eng_file.readlines()
	# total += len(kor_text)
	# print("kor")
	# for line in kor_text:
	# 	print(line)

	# print("\neng")
	# for line in eng_text:
	# 	print(line)
	if len(kor_text) == 0 or len(eng_text) == 0:
		return -1,-1,-1,-1
	special = special_feature.special_feature(kor_text, eng_text)	
	trans_set = lcslib.trans_list(kor_text,root)
	# get noun and number feature list
	kor_list = lcslib.add_list(lcslib.number_list(kor_number),trans_set)
	eng_list = lcslib.add_list(lcslib.number_list(eng_number),lcslib.noun_list(eng_text,trans_set))
	if maintype == 'word':
		result = lcslib.word_lcs(kor_list,eng_list,special)
	if maintype == 'line':
		result = lcslib.line_lcs(kor_list,eng_list,jaccard_value)

	if distance_value > 1 :
		result = lcslib.fill_line(result,distance_value) # for filling the line
	if result == None:
		return len(kor_text),-1,-1,-1
	human,machine,answer = lcslib.check_answer(result,idx,subtype,distance_value,jaccard_value)
	human,machine,answer = -1,-1,-1
	#write resu	print("kor : ",len(kor_text))
	for element in result:
		result_kor_file.write(kor_text[element[0]-1]+'\n')
		result_eng_file.write(eng_text[element[1]-1]+'\n')
	print(result_url.format(subtype = subtype, lang = 'kor',distance_value = distance_value, jaccard_value = jaccard_value, idx=idx))
	kor_file.close()
	eng_file.close()
	kor_number.close()
	eng_number.close()
	result_kor_file.close()
	result_eng_file.close()
	return len(kor_text), human,machine,answer
# print(total) # total articles size
def run(start,end,root,distance_start,distance_end,jaccard_start,jaccard_end):
    total_text = 0
    total = open("./../../data/Herald/ANS/result/{subtype}/result.csv".format(subtype=subtype),'w',encoding='utf8')
    score = open("./../../data/Herald/ANS/result/{subtype}/score.csv".format(subtype=subtype),'w',encoding='utf8')
    total.write("\n")
    score.write("\n")
    
    count = end-start+1
    for distance_value in [1,5]:
            total.write("{distance},".format(distance=distance_value))
            score.write("{distance},".format(distance=distance_value))
            total.write(",Human,Machine,Answer"*(count+1))
            score.write(",Precison,Recall,Score"*(count+1))
            total.write("\n")
            score.write("\n")
            for jaccard_value in range(jaccard_start,jaccard_end+1):
                    total_human= 0
                    total_machine= 0
                    total_answer =0
                    total.write(",{jaccard},".format(jaccard=jaccard_value))
                    score.write(",{jaccard},".format(jaccard=jaccard_value))
                    #for idx in index_list:			
                    for idx in range(start,end+1):
                            text,human,machine,answer = LCS(idx,root,maintype,subtype,distance_value,jaccard_value)
                            if text == -1 or human == -1 or machine == -1 or answer == -1:
                                continue
                            if machine ==0:
                                    precision = 0
                            else :
                                    precision = answer / machine
                            recall = answer / human
                            if(answer == 0):
                                    f1_score = 0
                            else:
                                    f1_score = precision * recall / (precision + recall)
                            total.write("{human},{machine},{answer},".format(human=human,machine=machine,answer=answer))
                            score.write("{precision},{recall},{score},".format(precision=precision,recall=recall,score=f1_score))
                            total_human += human
                            total_machine += machine
                            total_answer += answer
                            total_text += text
                    total.write("{human},{machine},{answer}\n".format(human=total_human,machine=total_machine,answer=total_answer))
                    if total_machine == 0 or total_human ==0:
                        score.write("0,0,0\n")
                    else:
                        print("{precision},{recall},{score}\n".format(precision=(total_answer / total_machine),recall=(total_answer/total_human),score= (total_answer / (total_human + total_machine))))
                        score.write("{precision},{recall},{score}\n".format(precision=(total_answer / total_machine),recall=(total_answer/total_human),score= (total_answer / (total_human + total_machine))))
            total.write("\n")
            score.write("\n")
    total.close()
    score.close()
def run2(distance_start,distance_end,jaccard_start,jaccard_end):
    for distance_value in range(distance_start,distance_end+1):
        for jaccard_value in range(jaccard_start,jaccard_end+1):
            for idx in range(62,1832):
                #try:
                LCS(idx,maintype,subtype,distance_value,jaccard_value)
                #except:
                #    print("error!! idx:",idx)
