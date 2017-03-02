import re

kor_path = "../../data/Herald/resource/kor/"
eng_path = "../../data/Herald/resource/eng/"
input_path = "../../data/Herald/"
#kor_path = "jh/kor/"
#eng_path = "jh/eng/"
#input_path = ""
index = 0
def make_file(file_num):
	global index
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
		number = re.match("[0-9]{3}$", line)
		if line[:3].lower() == "no." or number != None:
			#print (line)
			continue
		new_line = line
		exception = re.compile("\s*did you know[?]?\s*$|\s*알고 있었나요[?]?\s*$")
		check = exception.match(new_line.lower())
		if check != None:
			#print(line)
			continue
                
		for num in range(10):
			new_line = new_line.replace(str(num), "")
		new_line = new_line.replace("\n", "")

		if len(re.findall("[\w]", str(new_line))) == 0: continue

		count = len(re.findall("[A-Za-z.,\?\!\$\^\&\*\;\<\>\/]", str(new_line)))

		percent = count/(len(new_line))
		line = re.sub(r"\[[0-9]+\]", "", line)
		line = line.replace("*", "")
		if percent >= 0.5 and isEng == True: #영어 계속
			wf.write(line)
		elif percent < 0.5 and isEng == True: #영어 끝났고 한글이 새로 나옴 
			isEng = False
			wf.close()
			wf = open(kor_path + str(index)+".txt", "w", encoding="UTF8")
			wf.write(line)
		elif percent < 0.5 and isEng == False: #한글 계속 
			wf.write(line)
		elif percent >= 0.5 and isEng == False: #한글 끝났고 영어가 새로 나옴
			if "www." in line or "http" in line:
				wf.write(line)
				continue
			isEng = True
			wf.close()
			index += 1
			wf = open(eng_path + str(index) + ".txt", "w", encoding="UTF8")
			wf.write(line)
		#print ("[" + str(index) + "] " + str(percent))
		#print (line)
	f.close()

def herald_word_text(start, end):
	for i in range(start, end+1):
		make_file(i)
	global index
	return index

