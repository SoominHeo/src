import os
import zipfile
current_path = os.getcwd()

data_path = "/../data/"
wiki_path = "/../data/Herald/"
ANS_path = "/../data/Herald/ANS/result/{subtype}/{distance}/{value}/"
LCS_path = "/../data/Herald/LCS/{subtype}/{lang}/{distance}/{value}/"
NUM_path = "/../data/Herald/NUM/{lang}/"
original_path = "/../data/Herald/resource/{lang}/"
sample_path = "/../data/Herald/sample/{lang}/"
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
	#NUM_path
	make_directory(current_path+NUM_path.format(lang="eng"))
	make_directory(current_path+NUM_path.format(lang="kor"))

	make_directory(current_path+original_path.format(lang="eng"))
	make_directory(current_path+original_path.format(lang="kor"))
	make_dicrectory(current_path+sample_path.format(lang="eng")
	make_dicrectory(current_path+sample_path.format(lang="kor"))
check_directory("word_fill","5","0.3")
zip_ref = zipfile.ZipFile("./resource.zip", 'r')
zip_ref.extractall("../data/Herald/")
zip_ref.close()
