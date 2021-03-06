'''
다음에는
1.element를 리스트에 저장하고
나중에 다시 출력하는 것으로 바꿔야
unit을 적용시킬 수 있을 듯 함.
2. 숫자 끝에 붙은 알파벳들 ex)s 를 어떻게 제거할지 생각
3. hatred 이건 잘못 training 된 듯. 일딴 무시
'''
import re
import nltk

headerpath_en = "../../data/wiki/header/eng/"
def delete_symbol(line, symbol):

    flag = True

    while (flag):
        if (symbol in line):
            symbol_index = line.find(symbol)
            line = line[:symbol_index] + " " + line[symbol_index + 1:]
        else:
            flag = False
    return line

#get MONTH, ORDINAL NUMBER
def exception_number(exception, number_list):
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

    Unit = {
        'hundred' : 100,
        'thousand' : 1000,
        'million' : 1000000,
        'billion' : 1000000000,
        'trillion' : 1000000000000
    }

    if ('CD' in element):
        new_element = element[0]
        # one digit Cardinal to number
        if (new_element.lower() in Cardinal):
            new_element = (str(Cardinal[element[0].lower()]))

        elif (new_element in Unit):

            if (number_list[-1][0].isdigit() and number_list is not []):
                number_list[-1] = str(int(float(number_list[-1]) * Unit[new_element.lower()]))
                new_element = " "
            else:
                new_element = str(Unit[new_element.lower()])

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

def extract_num_ENG(index):
    result = []
    #en = open(url + str(index) + ".txt", 'r', encoding= 'utf8')
    try:
        en = open(headerpath_en + str(index) + ".txt", 'r', encoding='utf8')
        count_en_line = 0
        #write_en_File.write(file_name + "\n")
        for line in en:
            tmp = []
            count_en_line += 1
            getList = []
            line = delete_symbol(line, '-')
            line = delete_symbol(line, ':')

            tokens = nltk.word_tokenize(line)
            tagged = nltk.pos_tag(tokens)
            for element in tagged:
                getNumberList(element,getList)
            nomalization(getList)
            for element in getList:
                if(element is not " "):
                    tmp.append(element)
            result.append(tmp)

        en.close()
        return result
    except FileNotFoundError:
        pass
