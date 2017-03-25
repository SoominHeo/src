import re
import os
import copy
import ngram
import special_feature
current_path = os.getcwd()

def long(list1, list2):
	return  list1 if len(list1) >= len(list2) else list2

def short(list1, list2):
	return  list1 if len(list1) < len(list2) else list2

def make_dict():
	dictionary = open("./../../data/Herald/dic_revised.csv",'r',encoding ='utf8')
	lines = dictionary.readlines()
	dic={}
	for idx, line in enumerate(lines):
		splt = re.split("\t|\n",line)
	sorted(dic,key=len ,reverse =True)
	dictionary.close()
	return dic

#return translate NNP
def trans_list(text,root):
	trans_set = []

	for line in text:
		tmp = []
		#print(line)
		line = line.replace("\n","")
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
						arr[0]="1"
						for next_word_index in range(len(value)):
							if next_word_index + x < len(word) and (word[x+next_word_index] == value[next_word_index] or next_word_index == 0 and word[x][:word_length] == value[next_word_index]) and ( next_word_index >= 1 and arr[next_word_index-1] == "1" or next_word_index==0 and arr[0]=="1"):
								arr[next_word_index]="1"
								count = count +1
							if count != 0 and (count!=1 and count == len(value) or len(value)==1 and count ==1) and arr[len(arr)-1] =="1":
								val = ngram.findValue(root,result)
								if val == 'none':
									continue
								val = val.lower()
								synoni=val.split(" & ")
								tmp+=synoni
								tmp = list(set(tmp))
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
		tmp += tmp
		number_list.append(tmp)
	return number_list		

def noun_list(text,trans_set):
	noun_list = []
	count = 0
	for line in text:
		tmp = []
		for value in trans_set:
			for element in value:
				element = " " + element
				line = " " + line
				if line.lower().find(element.lower()) != -1:
					if element[1:].lower() not in tmp:
						tmp.append(element[1:].lower())
		noun_list.append(tmp)

	return noun_list

# add two list
def add_list(list1, list2):
	longer = long(list1,list2)
	shorter = short(list1,list2)
	
	#append shorter on to longer one
	for idx in range(len(shorter)):
		longer[idx].extend(shorter[idx])

	return longer

def common_set_table(list1,list2):
	table = []
	
	for korLine in list1:
		tmp = []
		for engLine in list2:
			count = 0
			for korWord in korLine:
				if korWord in engLine:
					count += 1
			tmp.append(count)
		table.append(tmp)

	return table

def make_candidate(table,x,y):
	candidate = []
	for tmp_x in range(x):
		candidate += table[tmp_x][y:y+1]
	candidate += table[x][:y+1]
	
	return candidate
def get_max_pair(table,kor,eng,result,x,y):
	#get max pair
	#get next pair
	#if next pair's value is same as max pair's value
	#repeat
	candidate = make_candidate(table,x,y)
	index = candidate.index(max(candidate))
	if index >= x:
		new_x,new_y = x-1,index-x-1
	else:
		new_x,new_y = index-1,y-2
	next_x,next_y = new_x, new_y
	print(new_x,new_y)

	
	return new_x,new_y

	return new_x,new_y

def fill_line(frame,distance):
	length = len(frame)
	for idx in range(length-1):
		ko_diff = frame[idx + 1][0] - frame[idx][0]
		en_diff = frame[idx + 1][1] - frame[idx][1]
		if(ko_diff == en_diff and en_diff <= distance):
			for fill_idx in range(1,ko_diff):
				frame.append(((frame[idx][0] + fill_idx), (frame[idx][1] + fill_idx)))
	frame.sort()
	return frame

def word_lcs(kor, eng,special):
	longest = 0
	if len(kor) == 0 or len(eng) == 0:
		return None
	lengths = [[0 for y in range(len(eng)+1)] for x in range(len(kor)+1)] 

	table = common_set_table(kor, eng)
	longest = [] 
	for row in table:
		longest += row
	longest = max(longest)
	
	result = []
	length_kor = len(table)
	length_eng = len(table[0])

	for element in special:
		table[element[0]][element[1]] += longest

	result.append((1,1))
	result.append((length_kor,length_eng))

	#make LCS table 1:1
	for  x in range(length_kor):
		for y in range(length_eng):
			if x == 0 or y == 0:
				lengths[x+1][y+1] = table[x][y]
			else:	
				candidate = []
				for tmp_x in range(x):
					candidate += lengths[tmp_x+1][y:y+1]
				candidate += lengths[x][:y]
				lengths[x+1][y+1] += max(candidate) + table[x][y]

	
	print("lengths ")
	for idx,row in enumerate(lengths):
		print(idx,row)

	#trace
	#for make first candidate = whole lengths table
	while(True):
		(length_kor,length_eng) = get_max_pair(lengths,kor,eng,result,length_kor,length_eng)
		if(length_kor <= 1 or length_eng <=1):
			break;
		result.append((length_kor,length_eng))
	
	result.sort()
	print("result ",result)
	return result

def check_answer(result,idx,subtype,distance_value,jaccard_value):
	answer_file = open("./../../data/Herald/ANS/{idx}.csv".format(idx=idx),'r',encoding='utf8',errors='ignore')
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
 		
		if(len(line[0]) != 0 and len(line)>= 2):
			for eANS in line[0].split(','):
				answer_list.append((int(line[1].split(',')[0]),int(eANS))) 
				answer_number += 1

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
			score = score * 2


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
