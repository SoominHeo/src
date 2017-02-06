import make_dictionary
import translate_k_to_e
from konlpy.tag import Kkma
kkma = Kkma()

def extractNNP_KOR(i):
	dic = make_dictionary.make_dictionary()
	read_page = open("../../data/Wiki/sample/header/kor/"+str(i)+".txt","rU",encoding='UTF8')
	result = [] # all noun list
	for line in read_page: # if file is empty, skip
		if(len(line) < 2):
			continue
		dic_list = kkma.pos(line[:-1]) #delete '\n'
		for element in dic_list: # for each line, get noun
			tmp = []
			if(element[1] == 'NNP' or element[1] == 'NNG'): # only noun
				tmp.append(element[0])
			result.append(tmp)
	read_page.close()
	result1 = translate_k_to_e.translate_k_to_e(dic, result)
	return result1
