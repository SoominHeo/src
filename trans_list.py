import ngram
#return translate NNP
def trans_list(l,root):
    trans_set = []
    article_word_index = 0
    article_line_index = 0
    korset = []
    while 1:
        if(article_line_index >= len(l)):
            break

        line = l[article_line_index].replace("\n","")

        split_one_line = line.split()
        if(len(split_one_line)==0):
            korset.append([])
            trans_set.append([])
            article_line_index += 1
            continue
        line_set = []
        korTmp = []
        while 1:
            if(len(split_one_line[article_word_index])!=1):
                search_result_list = ngram.search(root,split_one_line[article_word_index])
                #print(split_one_line[article_word_index])
                #print(search_result_list)
                if(len(search_result_list)!=0):
                    for x in search_result_list:
                        length = len(x.split())
                        to_find_string = ""

                        if(article_word_index + length < len(split_one_line)):
                            for y in range(length):
                                to_find_string = to_find_string + " " + split_one_line[article_word_index+y]
                        if(to_find_string[1:].find(x)==0):
                            c = ngram.findValue(root,x)
                            article_word_index = article_word_index + length-1
                            sp = c.split(" & ")
                            korTmp.append(x)
                            for i in sp:
                                line_set.append(i)
                            break
                length = len(split_one_line[article_word_index])-1
                #print(split_one_line[article_word_index][:length])
                if length > 3:
                    wordLimit = length -3
                else:
                    wordLimit = 1
                while length > wordLimit:
                    candi = ngram.findValue(root,split_one_line[article_word_index][:length])
                    #print(candi)
                    if candi == "none":
                        length -= 1
                        continue
                    else:
                        sp = candi.split(" & ")
                        for i in sp:
                            line_set.append(i)
                        korTmp.append(split_one_line[article_word_index][:length])
                        break
                        

            article_word_index +=1
            if(article_word_index >= len(split_one_line)):
                korset.append(korTmp)
                trans_set.append(line_set)
                article_line_index +=1
                article_word_index = 0
                break;
    return trans_set, korset

f = open("0.txt","r",encoding="UTF8")
s = f.readlines()
r = ngram.getRoot("dictionary.csv")
print("done")
print(trans_list(s,r))