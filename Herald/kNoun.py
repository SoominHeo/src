from konlpy.tag import Kkma


kkma = Kkma()
read_file_name = "./../sample/kor/"
write_file_name = "./../data/NVA/kor/"

for i in range(1,11):
	print (i)
	read_page = open(read_file_name + str(i) +".txt",'r')
	write_page = open(write_file_name + str(i) +".txt",'w', encoding = 'utf8')
	for line in read_page:
		if(len(line) < 2):
			pass
		dic_list = kkma.pos(line[:-1])
		for element in dic_list:
			#if(element[1] == 'NNP' or element[1] == 'NNG'): # only noun
			if(element[1] == 'NNG' or element[1] == 'NNP' or element[1]== 'VA' or element[1]== 'VV'): # noun, verb, adjective
				write_page.write(element[0] + ', ')
		# noun_list = kkma.nouns(line)
		# if(len(noun_list) == 0):
		# 	pass
		# for noun in noun_list:
			# write_page.write(noun + ', ')
		write_page.write('\n')	
		#write_page.write(str(noun_list)+'\n')

	read_page.close()
	write_page.close()

