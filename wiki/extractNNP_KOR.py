from konlpy.tag import Kkma


kkma = Kkma()


'''
get ith file noun list
'''
def extractNNP_KOR(i):
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

