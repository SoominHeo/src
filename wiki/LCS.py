from unicodedata import name
import copy
import re
from unicodedata import name
from nltk import sent_tokenize, word_tokenize, pos_tag
import copy
import time
import datetime
import codecs

count=0
LCStable=[]

def jaccard(kor, eng):
    deno=0
    numer=0
    aver=0

    tmp_d=[]
    tmp_k=[]

    if kor=='\n' or eng=='\n':
        return 0.0

    for kk in range(len(kor)):
        if kor[kk]:
            if kor[kk] not in tmp_k:
                tmp_k.append(kor[kk])
        else:
            continue

    tmp_d=copy.deepcopy(tmp_k)
    for ee in range(len(eng)):
        if eng[ee]:
            if eng[ee] not in tmp_k:
                tmp_d.append(eng[ee])
        else:
            continue

    deno=len(tmp_d)
    
    for x in tmp_k:
        if x=='':
            continue
        
        for y in eng:
            if y=='':
                continue
            
            elif x==y:
                numer=numer+1
                break
                
    if deno==0:
        return 0.0
    else:
        aver=numer/deno
        return aver

def LCS(k_art, e_art, k_len, e_len):
    m=0
    n=0

    for m in range(k_len+1):
        LCStable.append([])
        LCStable[m].append(0)
        for n in range(e_len):
            if m==0:
                LCStable[m].append(0)
            else:
                LCStable[m].append(-1)
                
    for mm in range(k_len):
        for nn in range(e_len):
            k = k_art[mm].split(', ')
            e = e_art[nn].split(', ')
            if jaccard(k,e)>=0.6:
                LCStable[mm+1][nn+1]=LCStable[mm][nn]+1
            else:
                if LCStable[mm+1][nn]>=LCStable[mm][nn+1]:
                    LCStable[mm+1][nn+1]=LCStable[mm+1][nn]
                else:
                    LCStable[mm+1][nn+1]=LCStable[mm][nn+1]

    return LCStable[k_len][e_len]

def LCS_TraceBack(m, n, lcs):
    new_list =[]
    
    if m==0 or n==0:
        return lcs
    
    if (LCStable[m][n] > LCStable[m][n-1]) and (LCStable[m][n] > LCStable[m-1][n]) and (LCStable[m][n] > LCStable[m-1][n-1]):
        new_list.append(m)
        new_list.append(n)
        lcs.insert(0,new_list)
        result = LCS_TraceBack(m-1, n-1, lcs)
    
    elif (LCStable[m][n] > LCStable[m-1][n]) and (LCStable[m][n] == LCStable[m][n-1]):
        result = LCS_TraceBack(m, n-1,  lcs)
    
    else:
        result = LCS_TraceBack(m-1, n,  lcs)

    return result


def seq(i,a, k_path, e_path):
    global cnt
    kor = []
    eng = []
    p_kor=[]
    p_eng=[]
    for x in range(len(a)-1):
        if(a[x+1][0]-a[x][0] == a[x+1][1]-a[x][1] and (a[x+1][1]-a[x][1])<=5):
            kor.append([a[x][0],a[x+1][0]])
            eng.append([a[x][1],a[x+1][1]])
        else:
            p_kor.append([a[x][0],a[x+1][0]])
            p_eng.append([a[x][1],a[x+1][1]])

    x=0
    while 1:
        if x>=len(kor)-1:
            break
        else:
            if(kor[x+1][0]==kor[x][1]):
                kor[x+1][0]=kor[x][0]
                kor.pop(x)
            else:
                x=x+1

    x=0
    while 1:
        if x>=len(eng)-1:
            break
        else:
            if(eng[x+1][0]==eng[x][1]):
                eng[x+1][0]=eng[x][0]
                eng.pop(x)
            else:
                x=x+1

    try:
        f_ko = open("../../data/wiki/sample/header/kor/"+str(i)+".txt","rU", encoding="UTF8")
        f_en = open("../../data/wiki/sample/header/eng/"+str(i)+".txt","rU", encoding="UTF8")
    except:
        return -1

    f_total_kor = open(k_path+str(i)+".txt","w", encoding="UTF8")
    f_total_eng = open(e_path+str(i)+".txt","w", encoding="UTF8")

    i_ko=0
    k=0
    while 1:
        if(k==len(kor)):
            break;
        if(len(kor)==0):
            break;
        
        if(i_ko==kor[k][0]-1):
            while 1:
                f_total_kor.write(f_ko.readline())
                cnt=cnt+1
                if(i_ko==kor[k][1]-1):
                    f_total_kor.write("\n")
                    break;
                i_ko=i_ko+1
            k=k+1
            
            if(k==len(kor)):
                break;
        f_ko.readline()
        i_ko=i_ko+1
    f_ko.close()

    f_ko = open("../../data/wiki/sample/header/kor/"+str(i)+".txt","rU", encoding="UTF8")
    i_ko=0
    k=0
    f_total_kor.write("\n")
    
    while 1:
        if(k==len(p_kor)):
            break;
        if(len(p_kor)==0):
            break;
        if(i_ko==p_kor[k][0]-1):
            tmp =f_ko.readline()
            f_total_kor.write(tmp)
            f_total_kor.write("\n")
            cnt=cnt+1
        elif(i_ko==p_kor[k][1]-1):
            tmp =f_ko.readline()
            f_total_kor.write(tmp)
            f_total_kor.write("\n")
            cnt=cnt+1
            k=k+1
        else:
            f_ko.readline()
        i_ko=i_ko+1

    i_en=0
    e=0
    while 1:
        
        if(e==len(eng)):
            break;
        if(len(eng)==0):
            break;
        
        if(i_en==eng[e][0]-1):
            while 1:
                f_total_eng.write(f_en.readline())
                if(i_en==eng[e][1]-1):
                    f_total_eng.write("\n")
                    break;
                i_en=i_en+1
            e=e+1
            if(e==len(eng)):
                break;
        f_en.readline()
        i_en=i_en+1
    f_en.close()
    f_en = open("../../data/wiki/sample/header/eng/"+str(i)+".txt","rU", encoding="UTF8")
    i_en=0
    e=0
    f_total_eng.write("\n")
    while 1:
        #print(i_en)
        if(e==len(p_eng)):
            break;
        if(len(p_eng)==0):
            break;
        if(i_en==p_eng[e][0]-1):
            tmp =f_en.readline()
            f_total_eng.write(tmp)
            f_total_eng.write("\n")
        elif(i_en==p_eng[e][1]-1):
            tmp =f_en.readline()
            f_total_eng.write(tmp)
            f_total_eng.write("\n")
            e=e+1
        else:
            f_en.readline()
        i_en=i_en+1

    f_ko.close()
    f_en.close()
    f_total_kor.close()
    f_total_eng.close()

def using_LCS(i, attr):
    try:
        f_eng = open("../../data/wiki/sample/list/" + attr + "/eng/" + str(i) + ".txt", "rU", encoding="UTF8")
        f_kor = open("../../data/wiki/sample/list/" + attr + "/kor/" + str(i) + ".txt", "rU", encoding="UTF8")
    except:
        #i=i+1
        return -1

    k_path = "../../data/wiki/sample/result/"+attr+"/kor/"
    e_path = "../../data/wiki/sample/result/"+attr+"/eng/"

    en=f_eng.readlines()
    ko=f_kor.readlines()

    for x in range(len(ko)):
        if ko[x][-1]=='\n':
            ko[x]=ko[x][:len(ko[x])-1]

    for y in range(len(en)):
        if en[y][-1]=='\n':
            en[y]=en[y][:len(en[y])-1]

    length=LCS(ko, en, len(ko), len(en))
    result=[]
    a = LCS_TraceBack(len(ko),len(en),result)

    #seq(i,a, k_path, e_path)

    return fill_line(a)


def fill_line(frame):
    length = len(frame)
    for idx in range(length-1):
        ko_diff = frame[idx + 1][0] - frame[idx][0]
        en_diff = frame[idx + 1][1] - frame[idx][1]
        if(ko_diff == en_diff and en_diff < 5):
            for fill_idx in range(1,ko_diff):
                frame.append([frame[idx][0] + fill_idx, frame[idx][1] + fill_idx])
    frame.sort()
    return frame

def run_3LCS(index):
    a = using_LCS(index, "link_list")
    b = using_LCS(index, "num_list")
    c = using_LCS(index, "NNP_list")

    print (a)
    print (b)
    print (c)

    k_lst = []
    e_lst = []

    for i in range(len(a)):
        k_lst.append(a[i][0])
        e_lst.append(a[i][1])

    for i in range(len(b)):
        if (b[i][0] not in k_lst) and (b[i][1] not in e_lst):
            k_lst.append(b[i][0])
            e_lst.append(b[i][1])

    for i in range(len(c)):
        if (c[i][0] not in k_lst) and (c[i][1] not in e_lst):
            k_lst.append(c[i][0])
            e_lst.append(c[i][1])

    try:
        f_ko = open("../../data/wiki/sample/header/kor/"+str(index)+".txt","rU", encoding="UTF8")
        f_en = open("../../data/wiki/sample/header/eng/"+str(index)+".txt","rU", encoding="UTF8")
    except:
        return -1

    k_result = open("../../data/wiki/sample/result/kor/"+str(index)+".txt","w", encoding="UTF8")
    e_result = open("../../data/wiki/sample/result/eng/"+str(index)+".txt","w", encoding="UTF8")

    k_contents = f_ko.readlines()
    e_contents = f_en.readlines()

    print (k_lst, e_lst)
    global count
    for i in range (len(k_contents)):
        if i in k_lst:
            count = count + 1
            k_result.write(k_contents[i])
    for i in range (len(e_contents)):
        if i in e_lst:
            e_result.write(e_contents[i])
    print (count)
    f_ko.close()
    f_en.close()
    k_result.close()
    e_result.close()
