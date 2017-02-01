from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import time
import copy

csv1=open("jaccard_attribute.csv","w")

def jaccard(kor, eng):

    deno=0
    numer=0
    aver=0

    tmp_d=[]
    tmp_k=[]
    
    
    #중복없는 kor
    for kk in range(len(kor)):
        if kor[kk]:
            if kor[kk][0]==' ':
                kor[kk]=str(kor[kk]).replace(' ','')
                
            if kor[kk] not in tmp_k:
                tmp_k.append(kor[kk])
        else:
            continue
    
    #deno 갯수
    tmp_d=copy.deepcopy(tmp_k)
    for ee in range(len(eng)):
        
        if eng[ee]:
            '''
            if eng[ee][0]==' ':
                eng[ee]=str(eng[ee]).replace(' ','')
            '''
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


def matching(kl,el,i):
    f_eng=open("new_en/"+str(i)+".eng.txt","rU",encoding='UTF8')
    f_kor=open("new_kr/"+str(i)+".kor.txt","rU",encoding='UTF8')
    #f_mat=open("match_joong/"+str(i)+".txt","w",encoding='UTF8')

    kkkk=f_kor.readlines()
    eeee=f_eng.readlines()
    #print(kkkk)
    #print(len(eeee))
    for tt in range(len(kkkk)):
        if kl==tt:
            f_mat.write("[k-"+str(kl)+"] ")
            f_mat.write(kkkk[tt])
            #f_mat.write("\n")
                    
    for gg in range(len(eeee)):
        if el==gg:
            f_mat.write("[e-"+str(el)+"] ")
            f_mat.write(eeee[gg])
            #f_mat.write("\n")

    f_mat.write("\n")

i=0

while i<= 10:
    print()
    print("[",str(i),"] article")

    try:
        ##문단 구분이 있는 텍스트로 뽑은 숫자 feature
        f_kor=open("ko_num/num"+str(i)+".kor.txt","r",encoding='UTF8')
        f_eng=open("en_num/"+str(i)+".txt","r",encoding='UTF8')

        ##문단 구분이 없는 텍스트로 뽑은 숫자 feature 

    except FileNotFoundError as e:

        i=i+1

    else:
        f_mat=open("match_joong/"+str(i)+".txt","w",encoding='UTF8')
        ko=f_kor.readlines()
        en=f_eng.readlines()

        '''
        for ee in range(len(en)):
            tmp=str(en[ee]).split(']')
            if tmp[0]=='\n':
                continue
            
            en[ee]=tmp[1]
        '''
        
        to_write=''
        to_write="--- ["+str(i)+"] article ---"+"\n"
        csv1.write(to_write)
        for x in range(len(ko)):
        
            if ko[x]=='' or ko[x]=='\n':
                continue
            k=str(ko[x]).replace(' \n','')
            k=k.split(',')
            
            if k==['']:
                continue
            elif k[0]=='1' and k[1]=='':
                continue
            
        
            for y in range(len(en)):
                if en[y]=='' or en[y]=='\n':
                    continue

            
                e=str(en[y]).replace(' \n','')
                e=e.split(',')

                for ee in range(len(e)):
                    if e[ee]:
                        if e[ee][0]==' ':
                            e[ee]=str(e[ee]).replace(' ','')
            
                if e==['']:
                    continue
                elif e[0]=='1' and e[1]=='':
                    continue
               
            
                ##########여기서 함수 돌리면 됩니다. 여기부터는 한글, 영어에서 빈라인을 취급하지 않습니다. 아래는 어떻게 넘어가는지 확인용 프린트 
                #print("e:",e)
                #print("k:",k)
            
                aver=jaccard(k,e)


                ##############0부터 하는걸로 수정하기
                
                to_write="kor"+str(x)+" -- eng"+str(y)+","+str(round(aver,2))+"\n"
                  
                      
                if aver>=0.8:
                    #print("[ kor",x+1," -- eng",y+1,"]"," jaccard: "+str(round(aver,2)))
                    matching(x,y,i)
               
                #print("인덱스:",x)
                #print("내용:",k)
                #print()

                csv1.write(to_write)
                
                
     
        i=i+1
        f_kor.close()
        f_eng.close()
        f_mat.close()

csv1.close()

            


    
