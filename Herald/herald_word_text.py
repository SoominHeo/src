korean = u'[\uac00-\ud7a3]'

#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

kor_path = "../../data/Herald/resource/kor/"
eng_path = "../../data/Herald/resource/eng/"
input_path = "../../data/Herald/"
#kor_path = "./jh/kor/"
#eng_path = "./jh/eng/"
#input_path = "./"
index = 0

def make_file(file_num):
	global index
	written_line = 0
	f = open(input_path + str(file_num) + ".txt", "r", encoding="UTF8")
	line = f.readline()
	line = line.replace("*", "")

	count = len(re.findall("[A-Za-z]", str(line)))
	percent = count/len(line)

	isEng = True
	wf = open(eng_path + str(index) + ".txt", "w", encoding="UTF8")
	number = re.match("[0-9]{3}", line)
	if line[:3].lower() != "no." and number == None and line != "\n":
		wf.write(line)

	while True:
		line = f.readline()
		if not line: 
			wf.close()
			break
		if line == '\n': continue
		if "http://" in line: continue
		number = re.match("[0-9]{3}$", line)
		if line[:3].lower() == "no." or number != None:
			#print (line)
			continue

		if "Fun Photos of the Week" in line: continue
		if "Fun Keywords of the Week" in line: continue
		line = re.sub(r"\[[0-9]+\]", "", line)
		line = re.sub(r"\([0-9]+\)", "", line)
		line = re.sub(r"\[[A-Za-z]+\]", "", line)
		line = re.sub(r"\sFun\s\(p\.\s[0-9]+\-[0-9]+\)", "", line)
		line = line.replace("*", "")

		new_line = line
		exception = re.compile("\s*did you know[?]?\s*$|\s*알고 있었나요[?]?\s*$")
		check = exception.match(new_line.lower())
		if check != None:
			#print(line)
			continue
		new_line = re.sub(r"면\)", "면면면면면", new_line)
		new_line = re.sub(r"\([0-9A-Za-zㄱ-ㅣ가-힣\s\?]+\)", "", new_line)
		new_line = re.sub(r"URL", "", new_line)
		new_line = re.sub(r"http://[\w\.\\]+", "", new_line)
		new_line = re.sub(r"www\.[\w\.\\]+", "", new_line)
		new_line = re.sub(r"1991 - 2NE1 CL", "투애니원 씨엘", new_line)
		new_line = re.sub(r"[0-9\-\.\,\?\!\$\^\&\;\<\>\/\s\(\)\"\“\”\n\'']+", "", new_line)
		count = len(re.findall("[A-Za-z]", str(new_line)))
		korean_count = len(re.findall(korean, str(new_line)))
		percent = korean_count/(len(new_line)+1)

		if len(re.findall("[\w]", str(new_line))) == 0: continue
		if line == " \n" or line == "\n": continue
		
		if percent >= 0.08 and percent < 0.3:
			written_line += 1
			wf.write(line)
		elif percent < 0.12 and isEng == True: # E->E 영어 계속
			written_line +=1
			wf.write(line)
		elif percent >= 0.12 and isEng == True: # E->K 영어 끝났고 한글이 새로 나옴
			isEng = False
			wf.close()
			written_line = 1
			wf = open(kor_path + str(index)+".txt", "w", encoding="UTF8")
			wf.write(line)
		elif percent >= 0.12 and isEng == False: # K->K한글 계속
			written_line += 1
			wf.write(line)
		elif percent < 0.12 and isEng == False: # K->E 한글 끝났고 영어가 새로 나옴
			# 한국어 그대로 지속
			if "www." in line or "http" in line:
				written_line += 1
				wf.write(line)
				continue
			# 영어 새로 쓰기
			isEng = True
			wf.close()
			index += 1
			written_line = 1
			wf = open(eng_path + str(index) + ".txt", "w", encoding="UTF8")
			wf.write(line)
	f.close()

def herald_word_text(start, end):
	for i in range(start, end+1):
		make_file(i)
	global index
	return index

