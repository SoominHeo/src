import sqlite3
import make_dictionary
import operator
# cursor.execute("CREATE TABLE NNP(kor text, eng text, count int)")
# cursor.execute("INSERT INTO NNP VALUES('사과', 'apple', 1)")
# cursor.execute("INSERT INTO NNP VALUES('바나나', 'banana', 1)")
# con.commit()
# cursor.execute("SELECT * FROM NNP")
# for row in cursor:
#    print (row)
# cursor.execute("DROP TABLE NNP")

def create_table(table_name):
    print("[create table] " + table_name)
    con = sqlite3.connect("NNP.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE " + table_name + "(kor text, eng text, count int)")
    con.commit()
    con.close()
    print ("[create table done]")

def drop_table(table_name):
    print("[drop table] " + table_name)
    con = sqlite3.connect("NNP.db")
    cursor = con.cursor()
    cursor.execute("DROP TABLE " + table_name)
    con.commit()
    con.close()
    print("[drop table done]")

def insert_link_dictionary(table_name):
    print("[insert] fill with link dictionary")
    dic = make_dictionary.make_dictionary()
    i = 0
    for word in dic.keys():
        if i % 100 == 0:
            print (i)
        i = i + 1
        if '\"' in dic[word]:
            continue
        dic[word] = dic[word].replace("_", " ")

        con = sqlite3.connect("NNP.db")
        cursor = con.cursor()
        #cursor.execute("INSERT INTO " + table_name + " VALUES('" + str(word) + "', '" + str(dic[word]) + "', 1)")
        cursor.execute('INSERT INTO ' + table_name + ' VALUES("' + str(word) + '", "' + str(dic[word]) + '", 1)')
        #time.sleep(0.1)
        con.commit()
        con.close()
    print("[insert link dictionary done]")

def print_table(table_name):
    con = sqlite3.connect("NNP.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM " + table_name)
    for row in cursor:
       print (row)
    con.close()

def add_new_word(table_name, word, language):
    con = sqlite3.content("NNP.db")
    cursor = con.cursor()
    if language == "k":
        cursor.execute('INSERT INTO ' + table_name + ' VALUES("' + str(word) + '", NULL, 1)')
    if language == "e":
        cursor.execute('INSERT INTO ' + table_name + ' VALUES(NULL, "' + str(word) + '", 1)')
    con.commit()
    con.close()

def add_count(table_name, word, language):
    con = sqlite3.content("NNP.db")
    cursor = con.cursor()
    if language == "k":
        cursor.execute("UPDATE NNP_DIC SET count=count+1 WHERE kor = '"+word+"'") # count + 1
    if language == "e":
        cursor.execute("UPDATE NNP_DIC SET count=count+1 WHERE eng = '"+word+"'") # count + 1
    pass

def insert_word_to_dictionary(table_name, kor_2d, eng_2d):
    dic = make_dictionary()
    for i in range(len(kor_2d)):
        for j in range(len(kor_2d[i])):
            if kor_2d[i][j] in dic.keys():
                add_count(table_name, kor_2d[i][j], "k")
            else:
                add_new_word(table_name, kor_2d[i][j], "k") #매칭되는 영어단어가 없음
    for i in range(len(eng_2d)):
        for j in range(len(eng_2d[i])):
            if eng_2d[i][j] in dic.values():
                add_count(table_name, eng_2d[i][j], "e")
            else:
                add_new_word(table_name, eng_2d[i][j], "e") #매칭되는 한글 단어가 없음

#drop_table("NNP_DIC")
create_table("NNP_DIC")
insert_link_dictionary("NNP_DIC")
#print_table("NNP_DIC")
#insert_word_to_dictionary("NNP_DIC", [['한국 경제']], [['apple']['banana']])