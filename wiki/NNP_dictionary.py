import sqlite3
import make_dictionary
import re
from bs4 import BeautifulSoup
import header
import random
pair_list = []

'''
<각 함수에 대한 설명>
def insert_link_dictionary(table_name): 링크사전으로 DB 기반 만들기 (1회 사용)
def query_statement(query): 그냥 parameter에 쿼리 넣어주면 돌려줌
def insert_word_to_dictionary(language, word, count): 함수 dictionary_to_article_check에 사용되는 함수.
def special_character(key): 함수 dictionary_to_article_check에 사용되는 함수.
def dictionary_to_article_check(dic, index): 함수 dictionary에 있는 문자 하나하나 article에 집어 넣고(글자가 긴 순서로), 먼저 찾아진 단어는 삭제 후 다음 단어를 적용.
def run(start, end): 함수 dictionary_to_article_check를 돌리는 메인문 같은 역할.
def count_rows_larger_than(num): 함수 extract_NNP_DIC_in_LINK_DIC에서 나중에 num번 이상 나온 단어가 얼마나 있는지 계산하기 위해서 만듦.
def extract_NNP_DIC_in_LINK_DIC(num): num번 미만으로 나온 단어들로만 dictionary를 만들고 반환.
def make_index_kor_eng_list(): 예시가 이해가 더 잘 됨. ex) '전리수소영역'에서 '전리수소영역'이라는 단어는 빼고 돌려야되니까
'''
html_path = "../../data/wiki/{lang}_html/{idx}.html"
header_path = "../../data/wiki/header/{lang}/{idx}.txt"
csv_path = "../../data/wiki/data.csv"

randomList = [num for num in range(0,60000)]
random.shuffle(randomList)
# 링크사전으로 DB 기반 만들기 (1회 사용)
def insert_link_dictionary(table_name):
    con = sqlite3.connect("NNP.db")
    cursor = con.cursor()

    dic = make_dictionary.make_dictionary()
    i = 0
    for word in dic.keys():
        if i % 100 == 0:
            print (i)
        i = i + 1
        if '\"' in dic[word]:
            continue
        dic[word] = dic[word].replace("_", " ")

        cursor.execute('INSERT INTO ' + table_name + ' VALUES("' + str(word) + '", "' + str(dic[word]) + '", 0)')
        con.commit()
    print("[insert] fill with link dictionary")

def query_statement(query):
    con = sqlite3.connect("NNP.db")
    cursor = con.cursor()

    print(query)
    if query.split(" ")[0] == "SELECT":
        cursor.execute(query)
        for row in cursor:
            print(row)
    else:
        cursor.execute(query)
    con.commit()
    con.close()


# 한 문서에서 단어가 존재하는 만큼 DB의 count 올려주기
def insert_word_to_dictionary(con, language, word, count):
    cursor = con.cursor()
    if language == "k":
        print(word + " +" + str(count))
        cursor.execute('UPDATE NNP_DIC SET count=count+' + str(count) + ' WHERE kor="' + word + '"')
    if language == "e":
        print(word + " +" + str(count))
        cursor.execute('UPDATE NNP_DIC SET count=count+' + str(count) + ' WHERE eng="' + word + '"')
    con.commit()

# 정규표현식 쓸 때 의미 있는 글자들 앞에 escape character 붙이기 ex) + -> \+
def special_character(key):
    result = ""
    special_character_list = ['.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '\\', '|', '(', ')']
    for i in range(len(key)):
        if key[i] in special_character_list:
            result += "\\"+key[i]
        else:
            result += key[i]
    return result

# dictionary에 있는 문자 하나하나 article에 집어 넣고(글자가 긴 순서로), 먼저 찾아진 단어는 삭제 후 다음 단어를 적용
def dictionary_to_article_check(con, dic, pair_list):
    index = pair_list[0]
    print(str(index) + ".txt")
    k_file = open(header_path.format(lang='kor',idx=index), "rU", encoding='UTF8')
    e_file = open(header_path.format(lang='eng',idx=index), "rU", encoding='UTF8')

    k_header_list = str(k_file.readlines())
    e_header_list = str(e_file.readlines())

    k_header_list = k_header_list.replace(pair_list[1], "") #'전리수소영역'에서 '전리수소영역'빼기
    e_header_list = e_header_list.replace(pair_list[2], "")

    for k in sorted(dic, key=len, reverse=True):
        if k == '"': continue
        k = special_character(k)
        length = len(re.findall(k, k_header_list))
        if length > 0:
            insert_word_to_dictionary(con, "k", k, length)
            k_header_list = k_header_list.replace(k, "")

    for e in sorted(dic, key=len, reverse=True):
        if e == '"': continue
        e = special_character(e)
        length = len(re.findall(e, e_header_list))
        if length > 0:
            insert_word_to_dictionary(con, "e", e, length)
            e_header_list = e_header_list.replace(e, "")

    k_file.close()
    e_file.close()

def count_rows_larger_than(cursor, num):
    cursor.execute("SELECT COUNT(*) FROM NNP_DIC WHERE COUNT >= "+str(num))
    for row in cursor:
        return row[0]

def extract_NNP_DIC_in_LINK_DIC(num):
    con = sqlite3.connect("NNP.db")
    cursor = con.cursor()

    print ("빈도수가 " + str(num) + " 이상인 row의 수는 " + str(count_rows_larger_than(cursor, num)) + "개 이고, \n\t고유명사사전은 빈도수가 " + str(num) + " 미만인 것들로 만들고 반환합니다")
    dic = {}
    cursor.execute("SELECT * FROM NNP_DIC WHERE COUNT < " + str(num))
    for row in cursor:
        dic[row[0]] = row[1]
    con.commit()
    con.close()
    return dic

def run(start, end):
    log = open("log.txt",'w',encoding='utf8')
    con = sqlite3.connect("NNP.db")
    cursor = con.cursor()
    pair_list = make_index_kor_eng_list()
    dic = make_dictionary.make_dictionary()
    end = 3333
    index = 0
    # index = start
    while True:
        if index == end or index == 60000:
            break
        else:
            try:
                #if index == end+1: # 몇 개 돌리길 원하는지
                #    break
                dictionary_to_article_check(con, dic, pair_list[randomList[index]])
                #index = index+ 1
                index = index +1
            except:
                end += 1
                index += 1
                log.write("index : {idx}\n".format(idx=randomList[index]))
    con.commit()
    con.close()

def make_index_kor_eng_list():
    f = open(csv_path, "r", encoding='UTF8')
    lines = f.readlines()
    pair_list = []
    index = 0
    for line in lines:
        splt = re.split(",\t|\n", line)
        #print(splt[2], splt[3])
        pair_list.append([index, splt[2], splt[3]])
        index = index + 1
    f.close()
    return pair_list

def store_only_header():
    index=0
    while 1:
        ran_index=randomList[index]
        print (str(ran_index)+".txt")
        k = open(html_path.format(lang='kor',idx=ran_index), "r", encoding='UTF8')
        sources_k = BeautifulSoup(k, "html.parser")

        e = open(html_path.format(lang='eng',idx=ran_index), "r", encoding='UTF8')
        sources_e = BeautifulSoup(e, "html.parser")

        ck = header.header(sources_k, sources_e, ran_index, 0)
        if ck == -1:
            index = index + 1
            continue
        index = index + 1

def make_NNPDict():
    NNP_dict = {}
    test= sqlite3.connect("NNP.db")
    cursor= test.cursor()
    cursor.execute("SELECT * FROM NNP_DIC")
    for row in cursor:
        NNP_dict[row[0]] = row[1]
    return NNP_dict


#insert_link_dictionary("NNP_DIC")
#query_statement("CREATE TABLE NNP_DIC(kor text, eng text, count int)")
#query_statement("DROP TABLE NNP_DIC")
#query_statement("CREATE TABLE NNP_DIC(kor text, eng text, count int)")
#insert_link_dictionary("NNP_DIC")
#run(0,1)
#query_statement("SELECT * FROM NNP_DIC WHERE COUNT> 2") # n개 이상인 row만 print
#NNP_DICTIONARY = extract_NNP_DIC_in_LINK_DIC(1) #여기서 반환하는


#insert_link_dictionary("NNP_DIC")
# 이 모든 것들은 시간이 매우 오래 걸릴 예정이므로, 교수님 컴퓨터에서 돌리기를 권장합니다.

#step.0     NNP.db에서 NNP_DIC table은 (한글, 영어, 나타난 횟수)로 되어있습니다.
#           지윤이가 교수님 컴퓨터에서 받은 NNP.db가 초기 버전인지 확인한다. (초기 버전이 아닐 경우 꼭 초기버전-교수님컴퓨터에 있음-으로 다시 받아서 해놓길)
#step1.     header 부분만 일단 다 다운 받아야지 거기서 고유명사 사전을 만들 수 있습니다.
#           header는 html이 다 뽑혀야 뽑을 수 있는 것이고, 아마 월요일이면 다 받지 않을까 싶습니다.
'''           !!!!!!! 0.txt가 !(느낌표), Exclamation_mark 인지 꼭 확인하세요 !!!!!!!! 전리수소영역이면 안됩니다. 꼭 꼮 꼭
                그리고 경로는 이제 sample이 아니라 새로운 경로로 해야합니다!!!   '''
# step2.    그럼 html 파일에서 header만 뽑아 sample/header/eng와 sample/header/kor에 저장합니다. (html은 0.txt ~ 47xxxxx.txt로 저장해주세요)
#store_only_header()
#step3.     step2가 완성되면 run 함수를 돌립니다. 이 함수는 단어가 나타난 횟수를 증가시켜줍니다. 매~~우 오래 걸릴 예정입니다.
run(0,60000)
#step4.     앞의 작업이 끝나면 extract_NNP_DIC_in_LINK_DIC(num) 함수를 돌려서, 자주 나왔던 단어(예를들어 count-전체 글에서 단어가 나온 횟수-가 20보다 큰)가 몇 개 인지 확인하고
#           고유명사 사전에서 걸러내야할 빈도수는 어느정도인지 일일이 좀 봐야할 것 같습니다. 이 함수 돌리면 친절하게 한글이 나올 것 입니다.
#                       '빈도수가 20 이상인 row의 수는 300000개 이고,
#                       	고유명사사전은 빈도수가 20 미만인 것들로 만들고 반환합니다'
#           이렇게요. 친절하죠? 판단 방법: 여기서 저는 빈도수가 20 미만인 것들은 매우 드문 경우(17만개 밖에 안남았으니)라고 판단해서 여기서 반환된 dictionary를 사용하려 합니다.
'''             여기까지 딱 한번만 돌리는 거에요              '''
#query_statement("SELECT * FROM NNP_DIC")
#dic = extract_NNP_DIC_in_LINK_DIC(0)
#step5.     step4에서 만들어진 사전이 우리가 최종적으로 얻고자 하는 고유명사사전이 됩니다. 물론... 빈도수로만 했기 때문에 정확한 dictionary는 될 수 없겠지만,
#           우리가 고유명사사전을 만드려고 한 이유가 드물게 나오는 것들을 뽑아내는 것이므로, 취지에는 적합한 사전이 완성되었다 생각합니다.
#           아 그리고 이 함수는 이제 NNP_list를 만드는데 사용이 되겠죠? ㅎㅎㅎ Good Luck... 오빠들 사랑해여 지윤아 사랑해 ㅠㅠ 하루이틀은 꼭 쉬세여 ㅎㅎ 라뷰
