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

count = 40


#get MONTH, ORDINAL NUMBER






def en_NUM(start,end):
    for index in range(start, end+1):
        try:
            write_en_File = open(output_url.format(lang='eng',idx=index), 'w', encoding= 'utf-8')
            # file_name = "er\\" + str(index) + ".eng.txt"
            en = open(input_url.format(lang='eng',idx=index, 'r',encoding='utf8'))
        except: FileNotFoundError:
            print(There is no input_url.format(lang='eng',idx=index))
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

