import re

kor_path = "./jh/kor/"
eng_path = "./jh/eng/"
f = open("3.txt", "r")

line = f.readline()
count = len(re.findall("[A-Za-z]", str(line)))
percent = count/len(line)

isEng = True
wf = open(eng_path + "0.txt", "w", encoding="UTF8")
wf.write(line)
index = 0
while True:
	line = f.readline()
	new_line = line
	if not line: 
		wf.close()
		break
	for num in range(10):
		new_line = new_line.replace(str(num), "")
	new_line = new_line.replace("\n", "")
	if len(re.findall("[\w]", str(new_line))) == 0: continue
	count = len(re.findall("[A-Za-z]", str(new_line)))

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
		if "www." in line:
			wf.write(line)
			continue
		isEng = True
		wf.close()
		index += 1
		wf = open(eng_path + str(index) + ".txt", "w", encoding="UTF8")
		wf.write(line)
	print (index, count, len(new_line), percent, new_line)
f.close()
