import re
def special_word_div(index):
    k = open("./ebook/kor/"+str(index)+".txt","r",encoding="UTF8")
    e = open("./ebook/eng/"+str(index)+".txt","r",encoding="UTF8")
    k_l = k.readlines()
    e_l = e.readlines()
    diff = 0
    if(len(k_l)<= len(e_l)):
        diff = len(e_l)-len(k_l)
        diff_by_line=diff/len(k_l)
    else:
        diff = len(k_l)-len(e_l)
        diff_by_line=diff/len(e_l)

    list_k = []
    list_e = []
    count_k= 0 
    result = []
    for x in k_l:
        l  = re.findall(r'[a-zA-Z]+[a-zA-Z\s\’]*[a-zA-Z\s]+',x)
        if(l!=[]):
            dif = count_k*diff_by_line
            index_value = []
            index_e = []
            for y in l:
                count_e = 0
                only_one = 0
                dd = 0
                for z in e_l:
                    if(z.find(y)!=-1):
                        index_value.append(y)
                        index_e.append(count_e)
                        only_one+=1
                    count_e +=1
            if(len(l)!=0):
                if(only_one==1 and len(l)==len(index_value)):
                    correct = 0
                    for q in range(len(index_e)):
                        if(q+1<len(index_e) and index_e[q+1]-index_e[q]>=3): 
                            correct=1 
                            break
                        if(index_e[q]>count_k+dif or index_e[q]< count_k-dif):
                            correct= 1
                            break
                    if(correct ==0):
                        #print("                      find : ",index_value,count_k,index_e[0])
                        tmp = []
                        tmp.append(count_k)
                        tmp.append(index_e[0])
                        result.append(tmp)
        count_k+=1
    return result
def special_number_div(index): 
    k = open("./NUM/kor/"+str(index)+".txt","r",encoding="UTF8")
    e = open("./NUM/eng/"+str(index)+".txt","r",encoding="UTF8")

    k_l = k.readlines()
    e_l = e.readlines()
    list_k = []
    list_e = []
    count = 0
    for x in k_l:
        s = x.split(", ")
    #    tmp = ""
        for y in s:
            if(y != "\n" and not (y>='\U00002460' and y<='\U00002473') and y.isdigit()==True and float(y)>=10 and float(y)%10 != 0 ):
                tmp = []
                tmp.append(count)
                tmp.append(float(y))
    #            tmp = str(y)+", " + tmp
    #    new_k.write(tmp+"\n")
                list_k.append(tmp)
        count+=1
    count = 0
    for x in e_l:
        s = x.split(", ")
    #    tmp = ""
        for y in s:
            if(y != "\n" and not (y>='\U00002460' and y<='\U00002473') and y.isdigit()==True and float(y)>=10 and float(y)%10 != 0):
                tmp = []
                tmp.append(count)
                tmp.append(float(y))
    #            tmp = str(y)+", " + tmp
    #    new_e.write(tmp+"\n")
                list_e.append(tmp)
        count+=1

    new_list_k = []
    new_list_e = []
    
    for x in range(0,len(list_k)):
        check = 0

        for y in range(0,len(list_k)):
            if(x != y and list_k[x][1]==list_k[y][1]):
                check = 1
        if(check == 0):
            new_list_k.append(list_k[x])
    for x in range(0,len(list_e)):
        check = 0
        for y in range(0,len(list_e)):
            if(x != y and list_e[x][1]==list_e[y][1]):
                check = 1
        if(check == 0):
            new_list_e.append(list_e[x])

    complete_k = []
    complete_e = []
    tmp = ""
    flag = 0
    for x in range(0,len(new_list_k)-1):
        tmp = str(new_list_k[x][1])
        if(new_list_k[x][0] == new_list_k[x+1][0]):
            tmp = tmp + ", " + str(new_list_k[x+1][1])
            flag = 1
        else:
            flag = 0
            d = []
            d.append(new_list_k[x][0])
            d.append(tmp)
            complete_k.append(d)
            tmp = ""
    if(flag == 1):
        d = []
        d.append(new_list_k[-1][0])
        d.append(tmp)
        complete_k.append(d)
    tmp = ""
    flag = 0
    for x in range(0,len(new_list_e)-1):
        tmp = str(new_list_e[x][1])
        if(new_list_e[x][0] == new_list_e[x+1][0]):
            tmp = tmp + ", " + str(new_list_e[x+1][1]) 
            flag = 1
        else:
            flag = 0
            d = []
            d.append(new_list_e[x][0])
            d.append(tmp)
            complete_e.append(d)
            tmp = ""
    if(flag == 1):
        d = []
        d.append(new_list_e[-1][0])
        d.append(tmp)
        complete_e.append(d)
    result = []
    for kk in complete_k:
        tmp = []
        flag = 0
        for ee in complete_e:
            k_s = kk[1].split(", ")
            e_s = ee[1].split(", ")
            for ks in k_s:
                if(ks in e_s):
                    flag = 1
                    break
            if(flag==1):
                tmp.append(kk[0])
                tmp.append(ee[0])
                result.append(tmp)
                tmp = []
                flag = 0
    k.close()
    e.close()
    sp_word_div = special_word_div(index)
    result = result+sp_word_div
    result = sorted(result,key=lambda l:l[0])
    to_del = []
    for x in range(len(result)-1):
        if(result[x][0] >= result[x+1][0] or result[x][1] >= result[x+1][1]):
            to_del.append(x+1)
    
    for x in sorted(to_del,reverse=True):
        result.pop(x)
    return result
for i in range(1,22):
    print(i)
    tmp=special_number_div(i)
    for x in tmp:
        print("               ",x)
