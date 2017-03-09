
import ngram


header_path = "../../data/wiki/header/{lang}/{idx}.txt"
def extractNNP_KOR(root,i):
    try:
        read_page = open(header_path.format(lang='kor',idx=i),"rU",encoding='UTF8')
    except:
        return -1
    trans_set = []

    for line in read_page:
        tmp = []
        print(line)
        line = line.replace("\n","")
        word = line.split(" ")
        flag = 0
        for x in range(len(word)):
            flag = 0
            if word[x] == " ":
                continue
            word_length = len(word[x])
            # find the word match
            while word_length > 1 and flag == 0:
                #print("word[x] : ", word[x][:word_length])
                # find ngram search
                result_list = ngram.search(root,word[x][:word_length])
                if result_list != []:
                    for result in result_list:
                        value = result.split(" ")
                        #print("===============")
                        #print("value : ", value)
                        arr = []
                        count = 0
                        for i in range(len(value)):
                            arr.append("0")
                        arr[0]="1"
                        for next_word_index in range(len(value)):
                            if next_word_index + x < len(word) and (word[x+next_word_index] == value[next_word_index] or next_word_index == 0 and word[x][:word_length] == value[next_word_index]) and ( next_word_index >= 1 and arr[next_word_index-1] == "1" or next_word_index==0 and arr[0]=="1"):
                                arr[next_word_index]="1"
                                count = count +1
                            if count != 0 and (count!=1 and count == len(value) or len(value)==1 and count ==1) and arr[len(arr)-1] =="1":
                                val = ngram.findValue(root,result)
                                synoni=val.split(" & ")
                                tmp+=synoni
                                for i in range(len(value)):
                                    word[x+i]= " "
                                flag = 1
                                break
                word_length= word_length - 1
        print(tmp)
        trans_set.append(tmp)
    read_page.close()
    #print(trans_set)
    return trans_set
