def special_number_div(index): 
    k = open("./NUM/kor/"+str(index)+".txt","r",encoding="utf8")
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
            if(y != "\n" and y!='①' and y!= '②' and y.isdigit()==True and float(y)>=10 and float(y)%10 != 0 ):
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
            if(y != "\n" and y.isdigit()==True and float(y)>=10 and float(y)%10 != 0):
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
    return result
