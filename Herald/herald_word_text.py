import re

kor_path = "../../data/Herald/resource/kor/"
eng_path = "../../data/Herald/resource/eng/"
input_path = "../../data/Herald/"
index = 0
def make_file(file_num):
	f = open(input_path+str(file_num) + ".txt", "r", encoding="UTF8")
	line = f.readline()

	count = len(re.findall("[A-Za-z]", str(line)))
	percent = count/len(line)

	global index
	isEng = True
	wf = open(eng_path + str(index) + ".txt", "w", encoding="UTF8")

	if line[:3] != "No.":
		wf.write(line)

	while True:
		line = f.readline()
		line = re.sub(r'\[\d\]',"",line)
		if not line: 
			wf.close()
			break
		if line[:3] == "No.": 
			continue
		new_line = line
		exception = re.compile("\s*did you know[?]?\s*$|\s*알고 있었나요[?]?\s*$")
		check = exception.match(new_line.lower())
                
		for num in range(10):
			new_line = new_line.replace(str(num), "")
		new_line = new_line.replace("\n", "")

		if len(re.findall("[\w]", str(new_line))) == 0: continue

		count = len(re.findall("[A-Za-z.,\?\!\$\^\&\*\;\<\>\/]", str(new_line)))

		percent = count/(len(new_line))

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
	f.close()

def herald_word_text(start, end):
    for i in range (start,end+1):
        make_file(i)
    global index
    return index
