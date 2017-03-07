import re
import os
import copy
import NNP_dictionary
import ngram
current_path = os.getcwd()

def long(list1, list2):
	return  list1 if len(list1) >= len(list2) else list2

def short(list1, list2):
	return  list1 if len(list1) < len(list2) else list2

def make_dict():
	dictionary = open("./../../data/Herald/dic_revised.csv",'r',encoding ='utf8')
	#new_dictionary = open("./../../data/Herald/data2.csv",'w',encoding='utf8') 
	#special_character_list = ['.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '\\', '|', '(', ')']
	lines = dictionary.readlines()
	#bracket = re.compile(r'\(.*?\)')
	#special_character=re.compile('\.|\^|\$|\*|\+|\?|\{|\}|\[|\]|\\|\||\(|\)')
	dic={}
	for idx, line in enumerate(lines):
		#line =bracket.sub("",line)
		#special_character.sub("",line)
		splt = re.split("\t|\n",line)
		#new_dictionary.write("{kor}\t{eng}\n".format(kor=NNP_dictionary.special_character(splt[2]),eng=NNP_dictionary.special_character(splt[3])))
	sorted(dic,key=len ,reverse =True)
	dictionary.close()
	return dic
#return translate NNP
def trans_list(text,root):
	trans_set = []

	for line in text:
		tmp = []
		word = line.split(" ")
		flag = 0
		for x in range(len(word)):
			flag = 0
			if word[x] == " ":
				continue
			word_length = len(word[x])
			# find the word match
			while word_length > 1 and flag == 0:
				# find ngram search
				result_list = ngram.search(root,word[x][:word_length])

				#if match
				if result_list != []:
					for result in result_list:
						value = result.split(" ")
						arr = []
						count = 0
						for i in range(len(value)):
							arr.append("0")
						for next_word_index in range(len(value)):
							if next_word_index == 0:
								arr[next_word_index] == "1"
								continue
							if next_word_index + x < len(word) and word[x+next_word_index] == value[next_word_index] and arr[next_word_index-1] == "1":
								arr[next_word_index]="1"
								count = count +1
							if count != 0 and count == len(value)-1 and arr[len(arr)-1] =="1":
								val = ngram.findValue(root,result)
								tmp.append(val)
								for i in range(len(value)):
									word[x+i]= " "
								flag = 1
								break
				word_length= word_length - 1
		trans_set.append(tmp)
	return trans_set

# return number list1
def number_list(file):
	text = file.readlines()
	number_list = []
	for line in (text):
		tmp =[]

		#append all number in csv file
		for element in line.split(', '):
			if(element == "\n"):
				continue
			tmp.append(element)
		number_list.append(tmp)
	return number_list		

def noun_list(text,trans_set):
	noun_list = []
	count = 0
	for line in text:
		tmp = []
		for value in trans_set[count]:
			if line.lower().find(value.lower()) != -1:
				tmp.append(value)
		count = count+1
		if count == len(trans_set):
			break
		noun_list.append(tmp)

	return noun_list

# add two list
def add_list(list1, list2):
	longer = long(list1,list2)
	shorter = short(list1,list2)
	
	#append shorter on to longer one
	for idx in range(len(shorter)):
		longer[idx].extend(shorter[idx])

	# for idx,element in enumerate(longer):
	return longer

def common_set_table(list1,list2):
	table = []

	for element_1 in range(len(list1)):
		tmp = []
		for element_2 in range(len(list2)):
			#append len(intersection)
			tmp.append(len(list(set(list1[element_1]) & set(list2[element_2]))))
		table.append(tmp)
	# for idx,line in enumerate(list1):
	# for idx,line in enumerate(list2):
	return table

def make_candidate(table,x,y):
	candidate = []
	for tmp_x in range(x):
		candidate += table[tmp_x][:y]
	
	return candidate

def get_max_pair(table,x,y):
	candidate = make_candidate(table,x,y)
	candidate = candidate[:-1]
	index = candidate.index(max(candidate))
	new_x, new_y = divmod(index,y)
	if new_x == x-1 and new_y==y:
		return new_x,new_y
	elif new_x == x and new_y == y:
		return new_x,new_Y
	elif new_x == x-1 or new_y ==y-1:
		candidate = make_candidate(table,x-1,y-1)
		index = candidate.index(max(candidate))
		new_x, new_y = divmod(index,y)

	return new_x,new_y
def jaccard(kor, eng):
    deno=0
    numer=0
    aver=0
    
    tmp_d=[]
    tmp_k=[]
    

    if kor=='\n' or eng=='\n':
        return 0.0

    for kk in range(len(kor)):
        if kor[kk]:
            if kor[kk] not in tmp_k:
                tmp_k.append(kor[kk])
        else:
            continue
    
    
    tmp_d=copy.deepcopy(tmp_k)
    for ee in range(len(eng)):
        if eng[ee]:
            if eng[ee] not in tmp_k:
                tmp_d.append(eng[ee])
        else:
            continue


    deno=len(tmp_d)

    
    for x in tmp_k:
        if x=='':
            continue
        
        for y in eng:
            if y=='':
                continue
            
            elif x==y:
                numer=numer+1
                break
                
    if deno==0:
        return 0.0
    else:
      
        aver=numer/deno
        
        return aver

def LCS_TraceBack(m, n, LCStable,lcs):
    new_list =[]
    
    if m==0 or n==0:
        return lcs
    
    if (LCStable[m][n] > LCStable[m][n-1]) and (LCStable[m][n] > LCStable[m-1][n]) and (LCStable[m][n] > LCStable[m-1][n-1]):
        new_list.append(m)
        new_list.append(n)
        lcs.append((m,n))
        result = LCS_TraceBack(m-1, n-1, LCStable, lcs)
    
    elif (LCStable[m][n] > LCStable[m-1][n]) and (LCStable[m][n] == LCStable[m][n-1]):
        result = LCS_TraceBack(m, n-1, LCStable, lcs)
    
    else:
        result = LCS_TraceBack(m-1, n, LCStable, lcs)
    result.sort()
    return result

def LCSS_TraceBack(m, n, LCStable,limit,distance_x,distance_y):
    result = []
    len_ko = len(LCStable)
    len_en = len(LCStable[0])
    if len(result) > 1:
        prev = result[-1]
    else:
        prev= (0,0)
    if m==0 or n==0:
        return result
    if (LCStable[m][n] > LCStable[m][n-1]) and (LCStable[m][n] > LCStable[m-1][n]) and (LCStable[m][n] > LCStable[m-1][n-1]):
        result.append((len_ko-m,len_en-n))
        result += LCSS_TraceBack(m-1, n-1, LCStable,limit,0,0)
    else:
        if m+prev[0]-len_ko > limit: # distance_x > 5
            result += LCSS_TraceBack(len_ko-prev[0]-1,len_en-prev[1]-2,LCStable,limit,0,0)
        elif n+prev[1]-len_en > limit: # distance_y >5
            result += LCSS_TraceBack(len_ko-prev[0]-2,len_en-prev[1]-1,LCStable,limit,0,0)
        elif (LCStable[m][n] > LCStable[m-1][n]) and (LCStable[m][n] == LCStable[m][n-1]): # ko
            result = LCSS_TraceBack(m, n-1, LCStable,limit,distance_x ,distance_y+1)
        else:
            result = LCSS_TraceBack(m-1, n, LCStable,limit,distance_x+1,distance_y) # en
    #result.sort()
    return result

def fill_line(frame,distance):
	length = len(frame)
	frame.append((0,0))
	limitX = len(frame)
	limitY = len(frame[limitX -1])
	frame.append((limitX,limitY))
	for idx in range(length-1):
		ko_diff = frame[idx + 1][0] - frame[idx][0]
		en_diff = frame[idx + 1][1] - frame[idx][1]
		if(ko_diff == en_diff and en_diff <= distance):
			for fill_idx in range(1,ko_diff):
				frame.append(((frame[idx][0] + fill_idx), (frame[idx][1] + fill_idx)))
	# print(result)
	frame.remove((0,0))
	frame.remove((limitX,limitY))
	frame.sort()
	return frame

def line_lcs(kor,eng,jaccard_value):
	#kor.reverse()
	#eng.reverse()
	k_len = len(kor)
	e_len = len(eng)
	LCStable = []
	for kor_idx in range(k_len+1):
		LCStable.append([])
		LCStable[kor_idx].append(0)
		for eng_idx in range(e_len):
			if kor_idx==0:
				LCStable[kor_idx].append(0)
			else:
				LCStable[kor_idx].append(-1)
                

	for kor_idx in range(k_len):
		for eng_idx in range(e_len):
			k = kor[kor_idx]
			e = eng[eng_idx]
			#print("kor:{k}\neng:{e}\n===================".format(k=k,e=e))
			if jaccard(k,e)>= jaccard_value:
				LCStable[kor_idx+1][eng_idx+1]=LCStable[kor_idx][eng_idx]+1
			else:
				if LCStable[kor_idx+1][eng_idx]>=LCStable[kor_idx][eng_idx+1]:
					LCStable[kor_idx+1][eng_idx+1]=LCStable[kor_idx+1][eng_idx]
				else:
					LCStable[kor_idx+1][eng_idx+1]=LCStable[kor_idx][eng_idx+1]
	length = LCStable[k_len][e_len]
	result = []	
	a = LCS_TraceBack(len(kor),len(eng),LCStable,result)
	#result = LCSS_TraceBack(len(kor),len(eng),LCStable,5,0,0)
	return result

def word_lcs(kor, eng):
	#start idx = 1,1
	#kor.reverse()
	#eng.reverse()
	if len(kor) == 0 or len(eng) == 0:
		return None
	lengths = [[0 for y in range(len(eng)+1)] for x in range(len(kor)+1)] 

	table = common_set_table(kor, eng)
	result = []
	length_kor = len(table)
	length_eng = len(table[0])



	result.append((1,1))
	result.append((length_kor,length_eng))

	#make LCS table
	for  x in range(length_kor):
		for y in range(length_eng):
			if x == 0 or y == 0:
				lengths[x+1][y+1] += table[x][y]
			else:	
				candidate = []
				for tmp_x in range(x):
					candidate += lengths[tmp_x +1][:y +1]
				lengths[x+1][y+1] += max(candidate) + table[x][y]
	#for x in range(length_kor):
	#	for y in range(length_eng):
	#		if x == 0 or y == 0:
	#			lengths[x][y] += table[x][y]
	#		else:
	#			candidate = []
	#			for tmp_x in range(x):
	#				candidate+=lengths[tmp_x][:y]
	#			lengths[x][y] += max(candidate) + table[x][y]
		
	#trace
	#for make first candidate = whole lengths table
	while(True):
		length_kor += 1
		length_eng += 1
		(length_kor,length_eng) = get_max_pair(lengths,length_kor,length_eng)
		if(length_kor <= 1 or length_eng <=1):
			break;
		#result.append((len(kor)-length_kor+1,len(eng)-length_eng+1))
		result.append((length_kor,length_eng))
	result.sort()

	return list(set(result))

def check_answer(result,idx,subtype,distance_value,jaccard_value):
	answer_file = open("./../../data/Herald/ANS/answer_{0}.csv".format(idx),'r',encoding='utf8')
	check_file = open("./../../data/Herald/ANS/result/{subtype}/{distance_value}/{jaccard_value}/{index}.txt".format(subtype=subtype,index=idx, distance_value = distance_value, jaccard_value =jaccard_value),'w',encoding='utf8')
	check_file.write(str(idx) + "\n")
	check_file.write("[한글,영어]\n")
	answer = answer_file.readlines()
	answer_list = []
	machine_number = len(result)
	answer_number  = 0
	right = 0
	wrong = 0
	score = 0
	#erase " symbol and , symbol
	for line in answer:
 		
		# remove " ,' ', '\n' symbol
		line = line.replace(",K","\t")
		line = line.replace("E","")
		line = line.replace('"',"")
		line = line.replace(' ',"")
		line = line.replace('\n',"")
 		# split eng and kor
		line = line.split('\t')
 		
 		#ignore two-to-one and no-to-one
		if(len(line[0]) != 0 and len(line[0].split(','))==1):
			answer_list.append((int(line[1].split(',')[0]),int(line[0])))
			answer_number += 1
	# print(result)
	# print(len(set(result) & set(answer_list)))
	# print(len(set(result) - set(answer_list)))

	precision = 0
	recall = 0
	right = set(result) & set(answer_list)

	if answer_number == 0:
		score = -1
	elif machine_number == 0:
		score = 0

	else:
		assert machine_number != 0 or answer_number != 0
		precision = len(right) / machine_number
		recall = len(right) / answer_number
		if(len(right) == 0):
			score = 0
		else:
			score = precision * recall / (precision + recall)


	#write result to file
	check_file.write("사람 : " + str(answer_number) + '\n')
	check_file.write(str(answer_list) + '\n')
	check_file.write("기계 : " + str(machine_number) + '\n')
	check_file.write(str(result) + '\n')
	check_file.write("교집합 : " + str(len(right)) + '\n')
	check_file.write(str(sorted(right)) + '\n')
	check_file.write("precision : " + str(precision) + '\n')
	check_file.write("recall : " + str(recall) +'\n')
	check_file.write("score : " + str(score) +'\n')
	answer_file.close()
	check_file.close()
	return answer_number, machine_number,len(right)

def make_directory(path):
	if not os.path.exists(path):
		os.makedirs(path)

def check_directory(subtype, distance,value):
	ANS_path = "/../../data/Herald/ANS/result/{subtype}/{distance}/{value}/"
	LCS_path = "/../../data/Herald/LCS/{subtype}/{lang}/{distance}/{value}/"
	#ANS/line/{value}/line_{}Fill/{lang}
	make_directory(current_path+(ANS_path.format(value=value, distance = distance,subtype= subtype)))
	#LCS/line/{value}{line_{}Fill/lang}
	make_directory(current_path+(LCS_path.format(value=value, distance = distance,subtype=subtype,lang="eng")))
	make_directory(current_path+(LCS_path.format(value=value, distance = distance,subtype=subtype,lang="kor")))
