from nltk.tokenize import word_tokenize
from nltk import pos_tag

read_file_name = "./../sample/eng/"
write_file_name = "./../data/NVA/eng/"

for i in range(1,21):
	print (i)
	read_page = open(read_file_name + str(i) +".txt",'r')
	write_page = open(write_file_name + str(i) +".txt",'w')
	for line in read_page:
		tokens = word_tokenize(line)
		tagged = pos_tag(tokens)
		for element in tagged:
			if(element[1].find('NN') is not -1 or element[1].find('VB') is not -1 or element[1].find('JJ') is not -1):
				write_page.write(element[0] + ', ')
		write_page.write('\n')
# 		if(len(noun_list) == 0):
# 			pass
# 		for noun in noun_list:
# 			write_page.write(noun + ', ')
# 		write_page.write('\n')	
# 		#write_page.write(str(noun_list)+'\n')

	read_page.close()
	write_page.close()


# sentence = """At eight o'clock on Thursday morning
# ... Arthur didn't feel very good."""
# >>> tokens = nltk.word_tokenize(sentence)
# >>> tokens
# ['At', 'eight', "o'clock", 'on', 'Thursday', 'morning',
# 'Arthur', 'did', "n't", 'feel', 'very', 'good', '.']
# >>> tagged = nltk.pos_tag(tokens)
# >>> tagged[0:6]
# [('At', 'IN'), ('eight', 'CD'), ("o'clock", 'JJ'), ('on', 'IN'),
# ('Thursday', 'NNP'), ('morning', 'NN')]
