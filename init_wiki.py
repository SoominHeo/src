import os
import zipfile
current_path = os.getcwd()

data_path = "/../data/"
wiki_path = "/../data/wiki/"
ANS_path = "/../data/wiki/ANS/result/{subtype}/{distance}/{value}/"
LCS_path = "/../data/wiki/LCS/{subtype}/{lang}/{distance}/{value}/"
HTML_path = "/../data/wiki/html/{lang}/"
FEATURE_path = "/../data/wiki/feature/"
HEADER_path = "/../data/wiki/header/{lang}/"
NUM_path = "/../data/wiki/NUM/{lang}/"
def make_directory(path):
	if not os.path.exists(path):
		os.makedirs(path)

def check_directory(subtype, distance,value):
	#data_path
	make_directory(current_path+data_path)
	#wiki_path
	make_directory(current_path+wiki_path)
	#ANS/line/{value}/line_{}Fill/{lang}
	make_directory(current_path+(ANS_path.format(value=value, distance = distance,subtype= subtype)))
	#LCS/line/{value}{line_{}Fill/lang}
	make_directory(current_path+(LCS_path.format(value=value, distance = distance,subtype=subtype,lang="eng")))
	make_directory(current_path+(LCS_path.format(value=value, distance = distance,subtype=subtype,lang="kor")))
	#HTML_path
	make_directory(current_path+(HTML_path.format(lang="eng")))
	make_directory(current_path+(HTML_path.format(lang="kor")))
	#FEATURE_path
	make_directory(current_path+FEATURE_path)
	#HEADER_path
	make_directory(current_path+HEADER_path.format(lang="eng"))
	make_directory(current_path+HEADER_path.format(lang="kor"))
	#NUM_path
	make_directory(current_path+NUM_path.format(lang="eng"))
	make_directory(current_path+NUM_path.format(lang="kor"))

check_directory("word_fill","5","0.3")
zip_ref = zipfile.ZipFile("./wiki.zip", 'r')
zip_ref.extractall("../data/wiki")
zip_ref.close()
