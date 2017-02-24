import lcslib
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from konlpy.tag import Kkma
import re
import copy
import extract_num_KOR
import extract_num_ENG
count = 10

original_url = "./../sample/{lang}/{idx}.txt"
number_url = "./../data/NUM/{lang}/{idx}.txt"
result_url = "./../data/LCS/{subtype}/{lang}/0/{value}/{idx}.txt"


subtype = "sequence"
# noun_url = "./../data/NNP"

#make dictionary
dic = lcslib.make_dict()

def eng_NVA(line):
	tokens = word_tokenize(line)
	tagged = pos_tag(tokens)
	
	result = []
	for element in tagged:
		# if(element[1].find('NN') is not -1 or element[1].find('VB') is not -1 or element[1].find('JJ') is not -1):
		if(element[1].find('NN') is not -1):
			result.append(element)
	
	return len(result)

def kor_NVA(line):
	kkma = Kkma()
	if(len(line)<2):
		pass
	dic_list = kkma.pos(line[:-1])
	result = []
	for element in dic_list:
		# if element[1] == 'NNG' or element[1] == 'NNP' or element[1] == 'VA' or element[1] == 'VV':
		if element[1] == 'NNG' or element[1] == 'NNP':
			result.append(element)

	return len(result)
def common_word(kor_line,kor_idx,eng_line,eng_idx,value):
	kor_noun = []
	kor_trans = []
	eng_noun = []
	common_noun = []
	kor_number = []
	eng_number = []
	common_number = []
	count_noun = 0
	count_number = 0
	count_rest = 0
	for entry in dic.keys():
		for word in re.findall(entry,kor_line):
			kor_trans.append(dic[word])
			kor_noun.append(word)
	
	for entry in dic.values():
		for word in re.findall(entry,eng_line):
			eng_noun.append(word)
	
	common_noun = (set(kor_trans) & set(eng_noun))
	for noun in kor_noun:
		kor_line = kor_line.replace(noun,"")
	for noun in eng_noun:
		eng_line = eng_line.replace(noun,"")

	kor_number = extract_num_KOR.extract_num_KOR(kor_line)
	eng_number = extract_num_ENG.extract_num_ENG(eng_line)
	common_number = (set(kor_number) & set(eng_number))

	for number in kor_number:
		kor_line = kor_line.replace(number,"")
	for number in eng_number:
		eng_line = eng_line.replace(number,"")

	count_noun = len(common_noun)
	count_number = len(common_number)
	# count_rest = len(kor_line.split()) + len(eng_line.split())
	count_rest = eng_NVA(eng_line) + kor_NVA(kor_line)
	#print("noun : " , count_noun)
	#print("number : " , count_number)
	#print("rest : ", count_rest)
	if(count_noun + count_number + count_rest == 0):
		return (-1,-1)
	score = float(count_noun + count_number) / float(count_noun + count_number +count_rest)
	if(score > value):
		return (kor_idx,eng_idx)
	else:
		return (-1,-1)
			


# get original_text
for idx in range(1, count + 1):
	print("index : ",idx)

	#control value
	for control_value in range(1,10):
		control_value = float(control_value) / 10.0
		print("control value :",control_value)
		lcslib.check_directory(subtype,0,control_value) # make directory
		kor_file = open(original_url.format(lang ="kor",idx = idx),'r',encoding='utf8')
		eng_file = open(original_url.format(lang ="eng",idx = idx),'r',encoding='utf8')
		kor_number = open(number_url.format(lang="kor",idx=idx),'r')
		eng_number = open(number_url.format(lang="eng",idx=idx),'r')
		result_kor_file = open(result_url.format(subtype = subtype, lang = 'kor',value = control_value, idx=idx),'w',encoding='utf8')
		result_eng_file = open(result_url.format(subtype = subtype, lang = 'eng',value = control_value, idx=idx),'w',encoding='utf8')

		kor_text = kor_file.readlines()
		eng_text = eng_file.readlines()

	# print("kor")
	# for line in kor_text:
	# 	print(line)

	# print("\neng")
	# for line in eng_text:
	# 	print(line)

		tmp_kor_text = copy.deepcopy(kor_text)
		tmp_eng_text = copy.deepcopy(eng_text)
	# get noun and number feature list

	#LCS
		result = []
		for kor_idx, kor_line in enumerate(tmp_kor_text):
			for eng_idx, eng_line in enumerate(tmp_eng_text):
				pair = (common_word(kor_line,kor_idx,eng_line,eng_idx,control_value))
				#print("kor idx : ",kor_idx,"\neng idx : ",eng_idx,"\nresult : ",pair)
				if(pair == (-1,-1)):
					continue
				result.append(pair)
		#result = lcslib.fill_line(result,1)
		lcslib.check_answer(result,idx,subtype,0,control_value)
	#write result_file
		for element in result:
			result_kor_file.write(kor_text[element[0]]+'\n')
			result_eng_file.write(eng_text[element[1]]+'\n')

		kor_file.close()
		eng_file.close()
		kor_number.close()
		eng_number.close()
		result_kor_file.close()
		result_eng_file.close()



