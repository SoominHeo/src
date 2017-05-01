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
                if(search_result_list != "none"):
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
                else:
                    length = len(split_one_line[article_word_index])-1
                    while length >2:
                        candi = ngram.findValue(root,split_one_line[article_word_index][:length])
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
    return trans_set