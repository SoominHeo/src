import sqlite3
import make_dictionary
import re

#1 table 생성 (1회 사용)
def create_table(table_name):
    cursor.execute("CREATE TABLE " + table_name + "(kor text, eng text, count int)")
    con.commit()
    print("[create table] " + table_name)

#2 table 삭제 (1회 사용)
def drop_table(table_name):
    cursor.execute("DROP TABLE " + table_name)
    con.commit()
    print("[drop table] " + table_name)

#3 링크사전으로 DB 기반 만들기 (1회 사용)
def insert_link_dictionary(table_name):
    dic = make_dictionary.make_dictionary()
    i = 0
    for word in dic.keys():
        if i % 100 == 0:
            print (i)
        i = i + 1
        if '\"' in dic[word]:
            continue
        dic[word] = dic[word].replace("_", " ")

        cursor.execute('INSERT INTO ' + table_name + ' VALUES("' + str(word) + '", "' + str(dic[word]) + '", 1)')
        con.commit()
    print("[insert] fill with link dictionary")

#4 한 문서에서 count된 만큼 DB에 숫자 올려주기
def insert_word_to_dictionary(language, word, count):
    if language == "k":
        print(word + " +" + str(count))
        cursor.execute('UPDATE NNP_DIC SET count=count+' + str(count) + ' WHERE kor="' + word + '"')
    if language == "e":
        print(word + " +" + str(count))
        cursor.execute('UPDATE NNP_DIC SET count=count+' + str(count) + ' WHERE eng="' + word + '"')
    con.commit()

#5 정규표현식 쓸 때 의미 있는 글자들 앞에 \ 붙이기 ex) + -> \+
def special_character(key):
    result = ""
    special_character_list = ['.', '^', '$', '*', '+', '?', '{', '}', '[', ']', '\\', '|', '(', ')']
    for i in range(len(key)):
        if key[i] in special_character_list:
            result += "\\"+key[i]
        else:
            result += key[i]
    return result

#6 dictionary에 있는 문자 하나하나 article에 집어 넣고 비교 된 것은 삭제
def dictionary_to_article_check(dic, index):
    print(str(index) + ".txt")
    k_file = open("../../data/Wiki/sample/header/kor/" + str(index) + ".txt", "rU", encoding='UTF8')
    e_file = open("../../data/Wiki/sample/header/eng/" + str(index) + ".txt", "rU", encoding='UTF8')

    k_header_list = str(k_file.readlines())
    e_header_list = str(e_file.readlines())

    for k in sorted(dic, key=len, reverse=True):
        if k == '"': continue
        k = special_character(k)
        length = len(re.findall(k, k_header_list))
        if length > 0:
            insert_word_to_dictionary("k", k, length)
            k_header_list = k_header_list.replace(k, "")

    for e in sorted(dic, key=len, reverse=True):
        if e == '"': continue
        e = special_character(e)
        length = len(re.findall(e, e_header_list))
        if length > 0:
            insert_word_to_dictionary("e", e, length)
            e_header_list = e_header_list.replace(e, "")

    k_file.close()
    e_file.close()

#7
def run(start, end):
    dic = make_dictionary.make_dictionary()
    index = start
    while 1:
        if index == end+1: # 몇 개 돌리길 원하는지
            break
        dictionary_to_article_check(dic, index)
        index = index + 1

''' main 문 '''
con = sqlite3.connect("NNP.db")
cursor = con.cursor()
query = ""
'''########## 항상 코드는 이 뒤에 ##########'''

#drop_table("NNP_DIC") #1
#create_table("NNP_DIC") #2
#insert_link_dictionary("NNP_DIC") #3
#7<run> -> #6 -> (#5 & #4)

'''
아래의 run 함수 호출 시
몇 번 부터 몇 번 까지 돌려서 dictionary에 넣을지
(중복되면 안됨..그럼 DB에 2번 들어감..)
추천하는거는 (0,99), (100,199) 이렇게 해서 안겹치게 하는 것!
'''
run(0,1)

'''
여기에 쿼리 쓰면 됨 (쿼리는 지형오빠가 잘 알거같음_디비 들었으니ㅎㅎ)
'''
#query = "SELECT * FROM NNP_DIC WHERE COUNT> 2"

'''############### 이 전에 ###############'''
if query != "":
    print (query)
    if query.split(" ")[0] == "SELECT":
        cursor.execute(query)
        for row in cursor:
            print(row)
    else:
        cursor.execute(query)
        con.commit()

con.commit()
con.close()