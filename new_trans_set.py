import ngram
def trans_list(l,root):
    trans_set = []
    kor_set = []
    article_word_index = 0
    article_line_index = 0

    while 1:
        if(article_line_index >= len(l)):
            break

        line = l[article_line_index].replace("\n","")

        split_one_line = line.split()
        print(line)
        if(len(split_one_line)==0):
            article_line_index += 1
            trans_set.append([])
            kor_set.append([])
            continue
        line_set = []
        kortmp_set = []
        while 1:
            if(len(split_one_line[article_word_index])!=1):
                search_result_list = ngram.search(root,split_one_line[article_word_index])
                if(search_result_list != "none"):
                    for x in search_result_list:
                        length = len(x.split())
                        to_find_string = ""

                        if(article_word_index + length < len(split_one_line)):
                            for y in range(length):
                                to_find_string = to_find_string + " " + split_one_line[article_word_index+y]
                        if(to_find_string[1:].find(x)==0):
                            print("find : ",x)
                            c = ngram.findValue(root,x)
                            kortmp_set.append(x)
                            print("ngram result : ",c)
                            article_word_index = article_word_index + length-1
                            sp = c.split(" & ")
                            for i in sp:
                                line_set.append(i)
                            break
            article_word_index +=1
            if(article_word_index >= len(split_one_line)):
                trans_set.append(line_set)
                kor_set.append(kortmp_set)
                article_line_index +=1
                article_word_index = 0
                break;
    return trans_set,kor_set
'''
root = ngram.getRoot("../dictionary.csv")
f = open("test.txt","r",encoding="UTF8")

l = f.readlines()
print("start")
s = trans_list(l,root)
print(s)
print("end")
'''
