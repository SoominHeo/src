import re
import os
import copy
current_path = os.getcwd()
original_url = "./../sample/{lang}/{idx}.txt"
number_url = "./../data/NUM/{lang}/{idx}.txt"
result_url = "./../data/LCS/{subtype}/{lang}/{distance_value}/{jaccard_value}/{idx}.txt"
total_result_path = "./../data/ANS/result/{subtype}/"
total_score_path = "./../data/ANS/result/{subtype}/"

def long(list1, list2):
	return  list1 if len(list1) >= len(list2) else list2

def short(list1, list2):
	return  list1 if len(list1) < len(list2) else list2

def make_dict():
	dictionary = open("./../data/Dict.csv",'r',encoding ='utf8')
	dic = {}
	for line in dictionary:
		# seperate entry and value
		entry = line.split(",")
		
		# put dictionary entry and value(delete '\n' symbol)
		dic[entry[0]] = entry[1].replace("\n","")

	dictionary.close()
	return dic
#return translate NNP
def trans_list(text,dic):
	trans_set = []

	for line in text:
		tmp = []

		#if there is key in kor_text, append dic[key]
		for key in dic.keys():
			find_list = re.findall(key,line)
			for element in find_list:
				tmp.append(dic[element])
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

def noun_list(text,dic):
	noun_list = []

	for line in text:
		tmp = []
		# if line == "\n\n":
		# 	noun_list.append(tmp)
		# 	continue

		#if there is value in eng_text, append value
		for value in dic.values():
			find_list = re.findall(value,line)
			for element in find_list:
				tmp.append(element)
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
	# 	print(idx," : ",element)
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
	# 	print(str(idx+1)+" : ",line)
	# for idx,line in enumerate(list2):
	# 	print(str(idx+1)+" : ",line)
	return table

def make_candidate(table,x,y):
	candidate = []
	for tmp_x in range(x):
		candidate += table[tmp_x][:y]
	return candidate

def get_max_pair(table,x,y):
	candidate = make_candidate(table,x,y)
	index = candidate.index(max(candidate))
	# print("***")
	# print(candidate)
	# for element in candidate:
	# 	print (element)
	# print (index)
	# print (divmod(index,y))
	# print (y)
	return divmod(index,y)

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
	for idx in range(length-1):
		ko_diff = frame[idx + 1][0] - frame[idx][0]
		en_diff = frame[idx + 1][1] - frame[idx][1]
		if(ko_diff == en_diff and en_diff <= distance):
			for fill_idx in range(1,ko_diff):
				frame.append(((frame[idx][0] + fill_idx), (frame[idx][1] + fill_idx)))
	# print(result)
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
	lengths = [[0 for y in range(len(eng)+1)] for x in range(len(kor)+1)] 

	table = common_set_table(kor, eng)
	result = []

	length_kor = len(table)
	length_eng = len(table[0])

	# make LCS table
	for  x in range(length_kor):
		for y in range(length_eng):
			if x == 0 or y == 0:
				lengths[x+1][y+1] += table[x][y]
			else:	
				candidate = []
				for tmp_x in range(x):
					candidate += lengths[tmp_x +1][:y +1]
				lengths[x+1][y+1] += max(candidate) + table[x][y]
		

	#trace
	#for make first candidate = whole lengths table
	length_kor += 1
	length_eng += 1
	while(True):
		(length_kor,length_eng) = get_max_pair(lengths,length_kor,length_eng)
		# print(length_kor)
		# print(length_eng)
		# print("================")
		if(length_kor == 0 or length_eng ==0):
			break;
		result.append((length_kor,length_eng))

		
	#print(result)
	#result = fill_line(result)
	result.sort()

	# for line in table:
	# 	print(line)
	# print("===================="*5)
	# for idx, line in enumerate(lengths):
	# 	print(idx," : ",line)
	# print(result)
	return result

def check_answer(result,idx,subtype,distance_value,jaccard_value):
	answer_file = open("./../data/ANS/answer_{0}.csv".format(idx),'r',encoding='utf8')
	check_file = open("./../data/ANS/result/{subtype}/{distance_value}/{jaccard_value}/{index}.txt".format(subtype=subtype,index=idx, distance_value = distance_value, jaccard_value =jaccard_value),'w',encoding='utf8')
	check_file.write(str(idx) + "\n")
	check_file.write("[한글,영어]\n")
	answer = answer_file.readlines()
	answer_list = []
	machine_number = len(result)
	answer_number  = 0
	right = 0
	wrong = 0
	score = 0
	print(idx)
	#erase " symbol and , symbol
	for line in answer:
 		
		# remove " ,' ', '\n' symbol
		line = line.replace(",K","\t")
		line = line.replace("E","")
		line = line.replace('"',"")
		line = line.replace(' ',"")
		line = line.replace('\n',"")
 		# split eng and kor
		line = line.split("\t")
 		
 		#ignore two-to-one and no-to-one
		if(len(line[0]) != 0 and len(line[0].split(','))==1):
			answer_list.append((int(line[1]),int(line[0])))
			answer_number += 1
	# print(answer_list)
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
	ANS_path = "/../data/ANS/result/{subtype}/{distance}/{value}/"
	LCS_path = "/../data/LCS/{subtype}/{lang}/{distance}/{value}/"
	#ANS/line/{value}/line_{}Fill/{lang}
	make_directory(current_path+(ANS_path.format(value=value, distance = distance,subtype= subtype)))
	#LCS/line/{value}{line_{}Fill/lang}
	make_directory(current_path+(LCS_path.format(value=value, distance = distance,subtype=subtype,lang="eng")))
	make_directory(current_path+(LCS_path.format(value=value, distance = distance,subtype=subtype,lang="kor")))
def method(idx,maintype,subtype,distance_value,jaccard_value,dic):

	jaccard_value = float(jaccard_value) / 10.0 # for control line_lcs jaccard value
	check_directory(subtype,distance_value,jaccard_value) # make directory
	kor_file = open(original_url.format(lang ="kor",idx = idx),'r',encoding='utf8')
	eng_file = open(original_url.format(lang ="eng",idx = idx),'r',encoding='utf8')
	kor_number = open(number_url.format(lang="kor",idx=idx),'r')
	eng_number = open(number_url.format(lang="eng",idx=idx),'r')
	result_kor_file = open(result_url.format(subtype = subtype, lang = 'kor',distance_value = distance_value, jaccard_value = jaccard_value, idx=idx),'w',encoding='utf8')
	result_eng_file = open(result_url.format(subtype = subtype, lang = 'eng',distance_value = distance_value, jaccard_value = jaccard_value, idx=idx),'w',encoding='utf8')

	kor_text = kor_file.readlines()
	eng_text = eng_file.readlines()

	# get noun and number feature list
	kor_list = add_list(number_list(kor_number),trans_list(kor_text,dic))
	eng_list = add_list(number_list(eng_number),noun_list(eng_text,dic))
	if maintype == 'word':
		common_set_table(kor_list,eng_list) # for word_lcs
		result = word_lcs(kor_list,eng_list)
	if maintype == 'line':
		result = line_lcs(kor_list,eng_list,jaccard_value)

	result = fill_line(result,distance_value) # for filling the line

	human,machine,answer = check_answer(result,idx,subtype,distance_value,jaccard_value)
	#write result_file
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
def run(count,maintype,subtype,distance_start,distance_end,jaccard_start,jaccard_end):
    total_text = 0
    dic = make_dict()
    make_directory(total_result_path.format(subtype=subtype))
    make_directory(total_score_path.format(subtype=subtype))

    total = open(total_result_path.format(subtype=subtype)+"result.csv",'w',encoding='utf8')
    score = open(total_score_path.format(subtype=subtype)+"score.csv",'w',encoding='utf8')
    total.write("\n")
    score.write("\n")
    for distance_value in range(distance_start,distance_end+1):
            total.write("{distance},".format(distance=distance_value))
            score.write("{distance},".format(distance=distance_value))
            total.write(",Human,Machine,Answer"*(count+1))
            score.write(",Precison,Recall,Score"*(count+1))
            total.write("\n")
            score.write("\n")
            for jaccard_value in range(jaccard_start,jaccard_end +1):
                    total_human= 0
                    total_machine= 0
                    total_answer =0
                    total.write(",{jaccard},".format(jaccard=jaccard_value))
                    score.write(",{jaccard},".format(jaccard=jaccard_value))
                    for idx in range(1,count+1):			
                            text,human,machine,answer = method(idx,maintype,subtype,distance_value,jaccard_value,dic)
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
                    score.write("{precision},{recall},{score}\n".format(precision=(total_answer / total_machine),recall=(total_answer/total_human),score= (total_answer / (total_human + total_machine))))
            total.write("\n")
            score.write("\n")
    print(total_text)
    total.close()
    score.close()
