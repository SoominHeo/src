# This Python file uses the following encoding: utf-8
import os, sys
from konlpy.tag import Kkma
from konlpy.utils import pprint
import codecs
import time
import nltk
import re

input_url = "./../sample/{lang}/{idx}.txt"
output_url = "./../data/NUM/{lang}/{idx}.txt"
start = 1
end = 40
kkma = Kkma()
POS = ["NR", "MDN"]
#POS = ["NNP"]
kor_unit = {
    '백':100, '천':1000,'만':10000,'십만':100000,'백만':1000000,'천만':10000000,'억':100000000,'십억':1000000000,'백억':10000000000,'천억':100000000000,'조':" ",'여':" "
}
num_ = {
    '하나':1, '둘':2, '셋':3, '넷':4, '다섯':5, '여섯':6, '일곱':7, '여덟':8, '아홉':9, '열':10, '세이':" ", '석':3,
    '일':1, '이':2, '삼':3, '사':4, '오':5, '육':6, '칠':7, '팔':8, '구':9, '십':10,
    '한':1, '두':2, '세':3, '네':4, '댓':5,
    '수십':10, '수백':100, '수천':1000, '수만':10000, '수십만':100000, '수백만':1000000, '수천만':10000000, '수억':100000000, '수십억':1000000000, '수백억':10000000000, '수천억':100000000000
}

MONTH = {'January' : 1, 'February' : 2,
         'March' : 3,   'April'    : 4,
         'May'   : 5,   'June'     : 6,
         'July'  : 7,   'August'   : 8,
         'September' : 9, 'October' : 10,
         'November' : 11, 'December' : 12}

Ordinal = {
    'first' : 1, 'second' : 2,
    'third' : 3, 'fourth' : 4, 'thirds' : 3,
    'fifth' : 5, 'sixth' : 6,
    'seventh' : 7, 'eighth' : 8,
    'ninth' : 9 , 'once' : 1
}

Cardinal = {
    'one' : 1, 'two' : 2,
    'three' : 3, 'four' : 4,
    'five' : 5, 'six' : 6,
    'seven' : 7, 'eight' : 8,
    'nine' : 9, 'ten' : 10,
    'eleven': 11, 'twelve' : 12, 'thirteen' :13, 'fourteen':14, 'fifteen':15, 'sixteen':16, 'sevneteen':17,
    'eighteen':18, 'ninteen':19,
    'twenty' : 20, 'thirty' : 30, 'fourty' : 40, 'fifty' : 50, 'sixty' : 60, 'seventy' : 70, 'eighty' : 80, 'ninty' :90
}

eng_unit = {
    'hundred' : 100,
    'thousand' : 1000,
    'million' : 1000000,
    'billion' : 1000000000,
    'trillion' : 1000000000000
}
def delete_symbol(line, symbol):

    flag = True

    while (flag):
        if (symbol in line):
            symbol_index = line.find(symbol)
            line = line[:symbol_index] + " " + line[symbol_index + 1:]
        else:
            flag = False
    return line

def exception_number(exception, number_list):
    if (exception in MONTH):
        number_list.append(str(MONTH[exception]))


    # get Ordinal number

    elif (exception.lower() in Ordinal):
        number_list.append(str(Ordinal[exception.lower()]))

    else:
        number_list.append(" ")

def nomalization(list):
    min = 0
    max = 0
    for i in range(len(list) - 1):
        if (list[i][0].isdigit() and list[i + 1].isdigit()):
            if(float(list[i]) < 100000 and float(list[i+1]) < 1000000):
                continue
            # print(list[i][0], list[i + 1][0])
            if i > max:
                min = i
            max = i
            while list[max + 1][0].isdigit():
                max += 1

            if i + 1 is max:
                sum = 0
                for i in range(min, max + 1):
                    if list[i] != " ":
                        sum += float(list[i])
                for i in range(min, max):
                    list[i] = " "
                if str(sum)[-1] != '0':
                    list[max] = str(float(sum))
                else:
                    list[max] = str(int(sum))

# get CD NUMBER
def getNumberList(element, number_list):
    if ('CD' in element):
        new_element = element[0]
        # one digit Cardinal to number
        if (new_element.lower() in Cardinal):
            new_element = (str(Cardinal[element[0].lower()]))

        elif (new_element in eng_unit):

            if (number_list[-1][0].isdigit() and number_list is not []):
                number_list[-1] = str(int(float(number_list[-1]) * eng_unit[new_element.lower()]))
                new_element = " "
            else:
                new_element = str(eng_unit[new_element.lower()])

            #new_element = (str(eng_unit[new_element.lower()]))

        else:
            # delete comma
            if ',' in new_element:
                comma = new_element.find(',')
                new_element= (new_element[:comma] + new_element[comma + 1:])

        # delete the alphabe after number
        '''
        change_key = re.compile("(?P<number>^a-zA-Z*)(?P<english>a-zA-Z*)")
        new_element = change_key.sub("\g<number>", new_element)
        number_list.append(new_element)
        '''
        new_element = re.findall('[\d]+[.]?[\d]*', new_element)
        if(len(new_element) > 0):
            number_list.append(new_element[0])

        # Month to number
    else:
        exception_number(element[0],number_list)

def kor_nomalization(list):
    min = 0
    max = 0
    new_list = [[] for i in range(len(list))]

    for i in range(len(list)):
        k = len(list[i])-1
        for j in range(k):
            if k<=j: break
            if list[i][j] == ',':
                string = list[i][:j] + list[i][j+1:]
                list[i] = str(string)
                k = k - 1
                continue
        find_all_list = re.findall('\d+', list[i])

        if len(find_all_list) > 0:
            for k in range(len(find_all_list)):
                if k == 0:
                    list[i + k] = find_all_list[k]
                else:
                    list.append(find_all_list[k])

    for i in range(len(list)-1):
        for j in range(len(list[i])):
            if list[i][j] == '-':
                if list[i] == '-':
                    break
                a = list[i].split('-')
                if(len(a)<2): break
                list[i] = a[0]
                list[i+1] = a[1]
                break

    #10억 같은 것을 다루는 애
    for i in range(len(list)-1):
        if len(list[i])>0 and len(list[i+1])>0 and list[i][0].isdigit() and list[i+1][0:3]=="100" and list[i][0] in ['1','2','3','4','5','6','7','8','9','0']:
            if i > max:
                min = i
            max = i
            while (list[max+1][0].isdigit()):
                max += 1
            if list[i-1] != " ":
                list[i+1] = str(float(list[i]) * float(list[i+1]))
                list[i] = " "
            if i+1 == max:
                sum = 0
                for i in range(min,max+1):
                    if list[i] != " ":
                        sum += float(list[i])
                for i in range(min,max):
                    list[i] = " "
                if str(sum)[-1] != '0':
                    list[max] = str(float(sum))
                else:
                    list[max] = str(int(sum))
    return list

total = 0
lines = 0
def ko_Num(start,end):
    for num in range(start,end+1):
    #for art_num in range(20):
        #new_input_url = input_url + n + ".txt"
        new_input_url = input_url.format(lang='kor',idx=num)
        new_output_url = output_url.format(lang='kor',idx=num)

        try:
            file = open(new_input_url, "rt")
        except IOError as e:
            print ("There is no",new_input_url)
            continue
        write_ko_File = open(new_output_url, 'w', encoding = 'utf-8')

        first_list = file.readlines()
        line_num = len(first_list)


        kkma_list = [ [] for j in range(line_num)]

        for i in range(line_num):
            if first_list[i] == "\n":
                kkma_list[i] = [(" "," ")]
            else:
                kkma_list[i] = kkma.pos(first_list[i])

        for i in range(line_num):
            for j in range(len(kkma_list[i])):
                list = [" "," "]
                list[0] = kkma_list[i][j][0]
                list[1] = kkma_list[i][j][1]
                kkma_list[i][j] = list

        for i in range(line_num):
            for j in range(len(kkma_list[i])):

                if kkma_list[i][j][1] in POS:
                    if kkma_list[i][j][0] in ['백','천','만','십만','백만','천만','억','십억','백억','천억','조','여']:
                        kkma_list[i][j][0] = str(kor_unit[kkma_list[i][j][0]])
                        #print ("#",kkma_list[i][j][0])
                    if kkma_list[i][j][0] in ['하나', '둘', '셋', '넷', '다섯', '여섯', '일곱', '여덟', '아홉', '열', '일', '이', '삼', '사', '오', '육',
                                      '칠', '팔', '구', '십', '한', '두', '세', '네', '댓', '수십', '수백', '수천', '수만', '수십만', '수백만', '수천만',
                                      '수억', '수십억', '수백억', '수천억', '세이', '석']:
                        kkma_list[i][j][0] = str(num_[(kkma_list[i][j][0])])

        num_list = [[] for i in range(line_num)]
        for i in range(line_num):
            for j in range(len(kkma_list[i])):
                num_list[i].append(kkma_list[i][j][0])

        fin_list = [[] for i in range(line_num)]
        for i in range(line_num):
            fin_list[i] = (kor_nomalization(num_list[i]))

        for i in range(line_num):
            for j in range(len(kkma_list[i])):
                if len(fin_list[i][j])>0 and fin_list[i][j][0].isdigit() and fin_list[i][j][0] in ['1','2','3','4','5','6','7','8','9','0']:
                    write_ko_File.write(str(fin_list[i][j]) + ", ")
            write_ko_File.write("\n")
        write_ko_File.close()
def en_Num(start,end):
    for index in range(start, end+1):
        try:
            write_en_File = open(output_url.format(lang='eng',idx=index), 'w', encoding= 'utf-8')
            # file_name = "er\\" + str(index) + ".eng.txt"
            en = open(input_url.format(lang='eng',idx=index), 'r',encoding='utf8')
        except FileNotFoundError:
            print("There is no input_url".format(lang='eng',idx=index))
            #count_en_line = 0
            #write_en_File.write(file_name + "\n")

        for line in en:
            #count_en_line += 1
            getList = []

            line = delete_symbol(line, '-')
            line = delete_symbol(line, ':')

            tokens = nltk.word_tokenize(line)
            tagged = nltk.pos_tag(tokens)
            

            # write_en_File.write("[" + str(count_en_line) + "] ")

            for element in tagged:
                getNumberList(element,getList)

            nomalization(getList)
            for element in getList:
                if(element is not " "):
                    write_en_File.write(str(element) +", ")
            write_en_File.write("\n")
        write_en_File.write("\n")


        en.close()
        write_en_File.close()

