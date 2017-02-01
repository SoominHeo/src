# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize, word_tokenize, pos_tag

import copy
import time
import datetime
import codecs

cs = open("attribute.csv","w")

# 자카드 함수에는 한 라인의 숫자가 들어감
def jj(k,e): #자카드 함수, 반환형은 퍼센트
    k_tmp = [] # 일단 비어있는 temp list를 만들고
    e_tmp = [] 

    s_k = k.split(', ') # s_k는 숫자 list
    s_e = e.split(', ') # s_e도 숫자 list

    for x in range(len(s_k)): # 각각의 한글 숫자 list에 대해서 아무것도 없으면 continue, 뭔가 있으면 위에서 만들 temp list에 append
        if(s_k[x]==''): 
            continue
        k_tmp.append(s_k[x])

    for y in range(len(s_e)): # 영어도 똑같이
        if(s_e[y]==''):
            continue
        e_tmp.append(s_e[y])

    # 그럼 여기서 이제 k_tmp랑 e_tmp라는 list에 각각의 숫자가 들어가있음

    # 합집합을 만들고
    tmp = copy.deepcopy(k_tmp) 
    for x in range(len(e_tmp)): 
        chk=0
        for y in range(len(tmp)): 
            if(tmp[y]==e_tmp[x]):
                chk=1
        if(chk==0): 
            tmp.append(e_tmp[x]) 

    # 교집합을 만들어서
    kyo = []
    for x in range(len(k_tmp)): 
        for y in range(len(e_tmp)):
            if(k_tmp[x]==e_tmp[y]):
                kyo.append(k_tmp[x])
                break;

    # 자카드 확률을 반환한다. 
    if(len(tmp)!=0):
        return float(len(kyo))/float(len(tmp))
    else:
        return 0

def seq(i):
    arr_k =[] #처음에 빈 리스트를 만들고
    arr_eng=[]

    f = open("./6/"+str(i)+".kor.txt","rU") # 한글에 개행x num
    cnt=0 # 라인의 수
    while 1:
        s = f.readline()
        a = s[0:-1] # a에 한 line의 처음부터 끝까지 집어 넣는다. 
    
        if(s=="\n"): # 개행되면, cnt(라인의 수)를 1 증가시키고, 다시 for문으로 돌아간다. 
            cnt=cnt+1
            continue;

        tmp = a.split(', ') # \n이 아니면 ', '로 split을 시켜 tmp에 저장한다. 
        if(len(tmp)==2 and tmp[0]=="1"): # split된 개수가 1개이고 첫 번째 letter가 1이면 cnt를 1 증가시키고 for문으로 돌아간다. 
            cnt=cnt+1
            continue;
        arr_k.append([a,cnt]) # 중간에 돌아가지 않은 것들은 arr_k에 split된 list와 자신의 line 수의 list를 append시키고 line수를 +1한다. 
        cnt=cnt+1
        if not s: #s에 아무것도 없으면 break;
            break;

    f = open("./7/"+str(i)+".txt","rU") #영어는 한글과 같다. 
    cnt=0
    while 1:
        s = f.readline()
        a = s[0:-1]
        
        if(s=="\n"):
            cnt=cnt+1
            continue;
        tmp = a.split(', ')
        if(len(tmp)==2 and tmp[0]=="1"):
            cnt=cnt+1
            continue;
        arr_eng.append([a,cnt])
        cnt=cnt+1
        if not s:
            break;

    #맨 마지막 요소는 뺀다. 왜???????????????????????????????????????????????????
    arr_k.pop(len(arr_k)-1)
    arr_eng.pop(len(arr_eng)-1)
    
    # 한글 array 출력
    for x in arr_k:
        print(x)
    
    # 영어 array 출력
    print("=============")
    for x in arr_eng:
        print(x)

    # sd는 라인 정보를 담을 것!
    sd_k = []
    sd_e = []
    print("!!!!!!!!!!!!!!")
    for x in range(len(arr_k)): # 한글 기준으로
        for y in range(len(arr_eng)): # 영어를 한번 쭉 돌리기
            print(arr_k[x][0]) #[x][0]에는 숫자 list가 들어있음!
            print(arr_eng[y][0]) 
            '''자카드 함수 호출'''
            print(jj(arr_k[x][0],arr_eng[y][0])) # 각 라인의 숫자 list들을 넣어서 자카드로 보냄 ==> 자카드 확률을 반환한다. 
            
            if(jj(arr_k[x][0],arr_eng[y][0])>=0.5 and x!=len(arr_k)-1 and y != len(arr_eng)-1): #한글~영어 자카드 확률이 0.5보다 높고
                if(jj(arr_k[x+1][0],arr_eng[y+1][0])>=0.5): # 한글~영어+1 자카드 확률이 0.5보다 높으면
                    dif_kor_line = arr_k[x+1][1]-arr_k[x][1] # dif_kor_line = 한글에서 line 사이의 개수
                    dif_eng_line = arr_eng[y+1][1]-arr_eng[y][1] # dif_eng_line = 영어에서 line 사이의 개수
                    if(dif_kor_line==dif_eng_line): # 같으면
                        print("KOR")
                        print(arr_k[x])
                        print(arr_k[x+1])
                        sd_k.append([arr_k[x][1],arr_k[x+1][1]]) # 시작과 끝 line을 저장하고
                        print("ENG")
                        print(arr_eng[y])
                        print(arr_eng[y+1])
                        sd_e.append([arr_eng[y][1],arr_eng[y+1][1]]) # 영어도 마찬가지로
    print(sd_k)
    print(sd_e)
    ss = 0

    # ex. 0~3이 같고 3~4같으면 0~4로 만들어주는 작업
    x=0
    while 1:
    #for x in range(len(sd_k)-1):
        if x>=len(sd_k)-1:
            break
        else:
            if(sd_k[x+1][0]==sd_k[x][1]):
                sd_k[x+1][0]=sd_k[x][0]
                sd_k.pop(x)
            else:
                x=x+1
    print(sd_k)
    
    x=0
    while 1:
        #for x in range(len(sd_k)-1):
        if x>=len(sd_e)-1:
            break;
        else:
            if(sd_e[x+1][0]==sd_e[x][1]):
                sd_e[x+1][0]=sd_e[x][0]
                sd_e.pop(x)
            else:
                x=x+1

    print(sd_e)

    f_en = open("./new/new_en/"+str(i)+".eng.txt","rU") # 개행 없는 영어 text 파일
    f_ko = open("./new/new_kr/"+str(i)+".kor.txt","rU") # 개행 없는 한글 text 파일
    f_total = open("./total/total"+str(i)+".txt","w") # 뽑아내서 출력

    i_ko = 0
    k___=0
    while 1:
        if(k___==len(sd_k)):
            break;
        if(len(sd_k)==0):
            break;

        if(i_ko==sd_k[k___][0]):
            while 1:
                f_total.write(f_ko.readline())
                if(i_ko==sd_k[k___][1]):
                    break;
                i_ko=i_ko+1
            k___=k___+1
            if(k___==len(sd_k)-1):
                break;
        f_ko.readline()
        i_ko=i_ko+1

    i_en = 0
    e___=0
    while 1:
        print(len(sd_e))
        if(e___==len(sd_e)):
            break;
        if(len(sd_e)==0):
            break;

        if(i_en==sd_e[e___][0]):
            while 1:
                print("i "+ str(i_en))
                print("k__ " + str(e___))
                f_total.write(f_en.readline())
                if(i_en==sd_e[e___][1]):
                    break;
                i_en=i_en+1
            e___=e___+1
            if(e___==len(sd_e)-1):
                break;
        f_en.readline()
        i_en=i_en+1

    f_en.close()
    f_ko.close()
    f_total.close()
    f.close()

i=0
while i<=10: #개수가 10개
    cs.write(str(i)+"article\n") # csv에 쓰는 것
    print("\t"+str(i))
    seq(i)
    i=i+1

cs.close()