import os
import zipfile
current_path = os.getcwd()

data_path = "/../data/"
Joongang_path = "/../data/Joongang/"
original_text_path = "/../data/Joongang/original_text/{lang}/"
original_html_path = "/../data/Joongang/original_html/html/"
no_single_space_path = "/../data/Joongang/no_single_space_text/{lang}/"
num_path = "/../data/Joongang/NUM/{lang}/"

def make_directory(path):
	if not os.path.exists(path):
		os.makedirs(path)

def check_directory(subtype, distance,value):
	#data_path
	make_directory(current_path+data_path)
	#Joongang_path
	make_directory(current_path+Joongang_path)
	#original_text
	make_directory(current_path+original_text_path.format(lang="eng"))
	make_directory(current_path+original_text_path.format(lang="kor"))
	#original_html
	make_directory(current_path+original_html_path)
	#no_single_space
	make_directory(current_path+no_single_space_path.format(lang="eng"))
	make_directory(current_path+no_single_space_path.format(lang="kor"))
	#num
	make_directory(current_path+num_path.format(lang="eng"))
	make_directory(current_path+num_path.format(lang="kor"))
check_directory("word_fill","5","0.3")

zip_ref = zipfile.ZipFile("./original_html.zip", 'r')
zip_ref.extractall("../data/Joongang")
zip_ref.close()
