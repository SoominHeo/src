import openpyxl as pyxl
import re
file_name = input("file name? ")
sheet_number = int(input("sheet number? "))
e = pyxl.load_workbook(file_name)

sheets = e.get_sheet_names()
#전체 한글 문장 수
count = 0

for x in range(0,sheet_number):
        
	try:
		sheet_b = e.get_sheet_by_name(str(x))
	except:
		continue
	for y in range(1,100):
		if(sheet_b['D'+str(y)].value!=None and sheet_b['D'+str(y)].value != "\n"):
			count += 1
print("전체 한글 문장수 : ",count)


#사람이 뽑은 전체 한글 문장 수
count = 0
for x in range(0,sheet_number):
        
	try:
		sheet_b = e.get_sheet_by_name(str(x))
	except:
		continue
	for y in range(1,100):
		if(sheet_b['B'+str(y)].value!=None):
			count+=1
		
print("사람이 뽑은 전체 한글 문장수 : ",count)
all_count = count
sum = 0




#사람이 뽑은 1대1 한글 문장 수
count = 0

for x in range(0,sheet_number):
        
	try:
		sheet_b = e.get_sheet_by_name(str(x))
	except:
		continue
	for y in range(1,100):
		if(sheet_b['B'+str(y)].value!=None):
			if(len(sheet_b['B'+str(y)].value.split(","))==1):
				if(y==1):
					if(sheet_b['B'+str(y)].value != sheet_b['B'+str(y+1)].value):
						count+=1
				else:
					if(sheet_b['B'+str(y)].value != sheet_b['B'+str(y+1)].value and sheet_b['B'+str(y)].value != sheet_b['B'+str(y-1)].value ):
						count+=1
print("사람이 뽑은 1대1 한글 문장수 : ",count)
sum += count
#사람이 뽑은 1대N 한글 문장 수
count = [0 for x in range(10)]
for x in range(0,sheet_number):
        
	try:
		sheet_b = e.get_sheet_by_name(str(x))
	except:
		continue
	for y in range(1,100):
		if(sheet_b['B'+str(y)].value!=None):
			lenght_N = len(sheet_b['B'+str(y)].value.split(","))
			if(lenght_N!=1):
				count[lenght_N] += 1
for x in range(2,len(count)):
	print("사람이 뽑은 1대"+str(x)+" 한글 문장수 : ",count[x])
	sum += count[x]
#사람이 뽑은 N대1 한글 문장 수
count = [0 for x in range(10)]
tmp = 1
for x in range(0,sheet_number):
        
	try:
		sheet_b = e.get_sheet_by_name(str(x))
	except:
		continue
	prev = "a"
	tmp = 1
	for y in range(1,100):
		if(sheet_b['B'+str(y)].value!=None):
			if(len(sheet_b['B'+str(y)].value.split(","))==1):
				if(y!=1):
					if(sheet_b['B'+str(y)].value == prev):
						tmp +=1
					elif(tmp!=1):
						count[tmp] += 1
						tmp = 1
					prev = sheet_b['B'+str(y)].value

for x in range(2,len(count)):
	print("사람이 뽑은 "+str(x)+"대1 한글 문장수 : ",count[x]*x)
	sum = sum+ count[x]*x

print("사람이 뽑은 N대N 한글 문장수 : ",all_count-sum)




## 사람 끝
#기계가 뽑은 전체 한글 문장 수
count = 0
for x in range(0,sheet_number):
        
	try:
		sheet_b = e.get_sheet_by_name(str(x))
	except:
		continue
	for y in range(1,100):
		if(sheet_b['A'+str(y)].value!=None):
			count+=1
		
print("기계가 뽑은 전체 한글 문장수 : ",count)
all_count = count
sum = 0

#기계가 뽑은 1대1 한글 문장 수
count = 0

for x in range(0,sheet_number):
        
	try:
		sheet_b = e.get_sheet_by_name(str(x))
	except:
		continue
	for y in range(1,100):
		if(sheet_b['B'+str(y)].value!=None):
			if(len(sheet_b['B'+str(y)].value.split(","))==1):
				if(y==1):
					if(sheet_b['B'+str(y)].value != sheet_b['B'+str(y+1)].value):
						if(sheet_b['A'+str(y)].value != None and sheet_b['A'+str(y)].value.replace(" ","") == sheet_b['B'+str(y)].value.replace(" ","")):
							count+=1
				else:
					if(sheet_b['B'+str(y)].value != sheet_b['B'+str(y+1)].value and sheet_b['B'+str(y)].value != sheet_b['B'+str(y-1)].value ):
						if(sheet_b['A'+str(y)].value != None and sheet_b['A'+str(y)].value.replace(" ","") == sheet_b['B'+str(y)].value.replace(" ","")):
							count+=1
print("사람이 뽑은 1대1 중 기계가 뽑은 1대1 한글 문장수 : ",count)
sum += count

#기계가 뽑은 1대N 한글 문장 수
count = [0 for x in range(10)]
for x in range(0,sheet_number):
        
	try:
		sheet_b = e.get_sheet_by_name(str(x))
	except:
		continue
	for y in range(1,100):
		if(sheet_b['B'+str(y)].value!=None):
			t=sheet_b['B'+str(y)].value.split(",")
			tmp = []
			for x in t:
				tmp.append(x.replace(" ",""))
			lenght_N = len(tmp)
			if(lenght_N!=1):
				if(sheet_b['A'+str(y)].value in tmp):
					count[lenght_N] += 1
for x in range(2,len(count)):
	print("사람이 뽑은 1대"+str(x)+ "중 기계가 뽑은 한글 문장수 : ",count[x])
	sum += count[x]

#사람이 뽑은 N대1 한글 문장 수
count = [0 for x in range(10)]
count_m=[0 for x in range(10)]
tmp = 1
for x in range(0,sheet_number):
        
	try:
		sheet_b = e.get_sheet_by_name(str(x))
	except:
		continue
	prev = "a"
	tmp = 1
	for y in range(1,100):
		if(sheet_b['B'+str(y)].value!=None):
			if(len(sheet_b['B'+str(y)].value.split(","))==1):
				if(y!=1):
					if(sheet_b['B'+str(y)].value == prev):
						tmp +=1
					elif(tmp!=1):
						for i in range(tmp,0,-1):
							if(sheet_b['A'+str(y)].value==sheet_b['B'+str(y-i+1)].value):
								count_m[tmp]+=1
								break
						count[tmp] += 1
						tmp = 1

					prev = sheet_b['B'+str(y)].value

for x in range(2,len(count_m)):
	print("사람이 뽑은 "+str(x)+"대1 중 기계가 뽑은 한글 문장수 : ",count_m[x])
	sum = sum+ count[x]

#print("사람이 뽑은 N대N 한글 문장수 : ",all_count-sum)
