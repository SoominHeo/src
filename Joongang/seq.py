from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize, word_tokenize, pos_tag

import copy
import time
import datetime
import codecs

def seq(b,i):
    a = [[1,3],[3,5],[5,8],[12,15],[16,13]]
    kor = []
    eng = []
    for x in range(len(a)-1):
        if(a[x+1][0]-a[x][0] == a[x+1][1]-a[x][1]):
            kor.append([a[x][0],a[x+1][0]])
            eng.append([a[x][1],a[x+1][1]])

    x=0
    while 1:
        if x>=len(kor)-1:
            break
        else:
            if(kor[x+1][0]==kor[x][1]):
                kor[x+1][0]==kor[x][0]
                kor.pop(x)
            else:
                x=x+1


    while 1:
        if x>=len(eng)-1:
            break
        else:
            if(eng[x+1][0]==eng[x][1]):
                eng[x+1][0]==eng[x][0]
                eng.pop(x)
            else:
                x=x+1

    print(kor)
    print(eng)
    f_ko = open("0.kor.txt","rU")
    f_en = open("0.eng.txt","rU")
    f_total_kor = open("kor.txt","w")
    f_total_eng = open("eng.txt","w")
    i_ko=0
    k=0


    while 1:
        if(k==len(kor)):
            break;
        if(len(kor)==0):
            break;

        if(i_ko==kor[k][0]):
            while 1:
                f_total_kor.write(f_ko.readline())
                
                if(i_ko==kor[k][1]):
                    f_total_kor.write("\n")
                    break;
                i_ko=i_ko+1
            k=k+1
            
            if(k==len(kor)):
                break;
        f_ko.readline()
        i_ko=i_ko+1

    i_en=0
    e=0
    while 1:
        if(e==len(eng)):
            break;
        if(len(eng)==0):
            break;
        
        if(i_en==eng[e][0]):
            while 1:
                f_total_eng.write(f_en.readline())
                if(i_en==eng[e][1]):
                    f_total_eng.write("\n")
                    break;
                i_en=i_en+1
            e=e+1
            if(e==len(eng)):
                break;
        f_en.readline()
        i_en=i_en+1
    f_ko.close()
    f_en.close()
    f_total_kor.close()
    f_total_eng.close()

seq(1,2)



