from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
#from konlpy.tag import Kkma
#from konlpy.utils import pprint
import time
#import datetime

data_number=0
#csv = open("html_attribute.csv","w")
csv2 = open("match_attribute.csv","w")

def remove_tags(data):
    p=re.compile(r'<.*?>')
    return p.sub('', data)


def TimeAndEngScript(url_last):
    insert_transcript = "https://www.ted.com"+url_last
    asdf = insert_transcript.split('/')
    d = insert_transcript.split('?')
    eee = d[0]+"/transcript?language=en"
    address1 = urlopen(eee)
    data1 = BeautifulSoup(address1,"html.parser")
    source_time1 = data1.findAll('span',attrs={'class':'talk-transcript__fragment'})
    source1 = []
    for x in range(len(source_time1)):
        tmp = source_time1[x]
        tmp = str(tmp).split('>')
        tmp[1]=tmp[1].replace(' \n',' ')
        tmp[1]=tmp[1].replace('\n',' ')
        #print(tmp)
        source1.append(tmp)
        #print(tmp[2])

    return source1

def TimeAndKorScript(url_last):
    insert_transcript = "https://www.ted.com"+url_last
    asdf = insert_transcript.split('/')
    d = insert_transcript.split('?')
    kkk = d[0]+"/transcript?language=ko"
    address1 = urlopen(kkk)
    data1 = BeautifulSoup(address1,"html.parser")
    source_time1 = data1.findAll('span',attrs={'class':'talk-transcript__fragment'})
    source1 = []
    for x in range(len(source_time1)):
        tmp = source_time1[x]
        tmp = str(tmp).split('>')
        tmp[1]=tmp[1].replace(' \n',' ')
        tmp[1]=tmp[1].replace('\n',' ')
        #print(tmp)
        source1.append(tmp)
        #print(tmp[2])

    return source1

def sub_kor(p):
    temp=""
    st=[]
    start = 0
    finish = 0
    s_start=0
    s_finish=0
    prev=""

    for z in range(len(p)):

              if z==0 and p[z]=="\"" or p[z]=="“":
                       temp=temp+p[z]
                       start=1
                       continue
              elif z==0:
                       temp=temp+p[z]
                       continue
                
              elif z>0:
                       prev=p[z-1]


              # next word
              if z==len(p)-1:
                       next_word=""
              else:
                       next_word=p[z+1]


              # double quotes beginning and ending
              if p[z]=="\"":
                      if start==1:
                          finish=1
                      else:
                          start=1

              elif p[z]=="“":
                      start=1
                  
              elif p[z]=="”" and start==1:
                      finish=1


              # single quotes beginning and ending 
              if p[z]=="\'":
                      if s_start==1:
                          s_finish=1
                      else:
                          s_start=1
              elif p[z]=="‘":
                      s_start=1

              elif p[z]=="’" and s_start==1:
                      s_finish=1

                      
               # separate sentences
              if p[z]=="." or p[z]=="!" or p[z]=="?":
                      if prev=="가" or prev== "나" or prev== "다" or prev== "라" or prev== "까" or prev== "지" or prev== "요" or prev=="죠":
                              if start==1 and finish==0:
                                      temp=temp+p[z]

                              elif start==1 and finish==1:
                                      if next_word=="":
                                              temp=temp+p[z]+"\n"
                                              st.append(temp)
                                              temp=""
                                              start=0
                                              finish=0

                                      elif next_word!=" " and next_word!="\n":
                                              temp=temp+p[z]

                                      elif next_word==" " or next_word=="\n":
                                              temp=temp+p[z]+"\n"
                                              st.append(temp)
                                              temp=""
                                              start=0
                                              finish=0

                              
                              #single case
                              elif s_start==1 and s_finish==0:
                                      temp=temp+p[z]
                        
                              elif s_start==1 and s_finish==1:
                                      if next_word=="":
                                              temp=temp+p[z]+"\n"
                                              st.append(temp)
                                              temp=""
                                              s_start=0
                                              s_finish=0

                                      elif next_word!=" " and next_word!="\n":
                                              temp=temp+p[z]
                           
                        
                                      elif next_word==" " or next_word=="\n":
                                              temp=temp+p[z]+"\n"
                                              st.append(temp)
                                              temp=""
                                              s_start=0
                                              s_finish=0

                              else:
                                      temp=temp+p[z]+"\n"
                                      st.append(temp)
                                      temp=""
                                      start=0
                                      finish=0

                      elif prev==")":
                              if p[z-2]=="다" or p[z-2]=="나" or p[z-2]=="가" or p[z-2]=="라" or p[z-2]=="까" or p[z-2]=="지"or p[z-2]=="요"or p[z-2]=="죠":
                                      temp=temp+p[z]+"\n"
                                      st.append(temp)
                                      temp=""
                                      start=0
                                      finish=0

                      else:
                              temp=temp+p[z]

              else:
                     temp=temp+p[z]                  

    for index in range(len(st)):
       ct=0
       for w in range(len(st[index])):

           if st[index][w]==" " or st[index][w]=="\n":
               ct=ct+1
           else:
               break

       st[index]=st[index][ct:len(st[index])]


    return st                          





def kor(url_last):
    insert_transcript = "https://www.ted.com"+url_last
    d = insert_transcript.split('?')
    s = d[0]+"/transcript?"+d[1]
    address1 = urlopen(s)
    data = BeautifulSoup(address1, "html.parser")
    script = data.findAll('span',attrs={'class':'talk-transcript__para__text'})

    ttt=TimeAndKorScript(url_last)

    f = open("Ted_ko/Ted_kor."+str(data_number)+".txt","w",encoding='UTF8')
    paragraph = len(script)
    y=0
    
    for y in range(paragraph):
        data = str(script[y])
        data = remove_tags(data)
        data = data.replace("\n"," ")
        data = data.replace("  "," ")

        final_par=sub_kor(data)

        if final_par==[]:
            continue
           
        b=len(final_par)
        for m in range(b):
            tmp=""
            p=re.compile("[\n]*")
            final_par[m]=p.sub('',final_par[m])
            #print("문장: ",final_par[m])
            #print()

            for n in ttt:
                
                time=str(n[0]).split(' ')
                if n[1][0:-6]==final_par[m][0:len(n[1][0:-6])]:
             
                  tmp=time[3]+"&&"+str(final_par[m])
                  
                  break
                else:
                  continue
                
            f.write(tmp)
            f.write("\n")
            #print(tmp)
                  
        f.write("\n")
      
      
    f.close()
    



def en(url_last):
    insert_transcript = "https://www.ted.com"+url_last
    d = insert_transcript.split('?')
    s = d[0]+"/transcript?language=en"
    address1 = urlopen(s)
    data = BeautifulSoup(address1, "html.parser")
    script = data.findAll('span',attrs={'class':'talk-transcript__para__text'})

    ttt=TimeAndEngScript(url_last)
    
    f = open("Ted_en/Ted_eng."+str(data_number)+".txt","w",encoding='UTF8')
    paragraph = len(script)
    y=0
    for y in range(paragraph):
        data = str(script[y])
        data = remove_tags(data)
        data = data.replace("\n"," ")
        data = data.replace("  "," ")
       
        sen = sent_tokenize(data)
        
        l = len(sen)
        q = 0
        for q in range(l):
            
            if(sen[q][0]==" "):
                d = len(sen[q])
                u = 1
                tmp=""
                for u in range(d):
                    if(u==d-1):
                        break;

                    tmp=tmp+sen[q][u+1]

                for n in ttt:
                    time=str(n[0]).split(' ')
                    if n[1][0:-6]==tmp[0:len(n[1][0:-6])]:
                       tmp=time[3]+"&&"+str(tmp)
                       break
                    else:
                       continue
                f.write(tmp)
            else:
                for n in ttt:
                    time=str(n[0]).split(' ')
                    if n[1][0:-6]==sen[q][0:len(n[1][0:-6])]:
                       tmp=time[3]+"&&"+str(sen[q])
                       break
                    else:
                       continue
                
                f.write(tmp)
            
            f.write("\n")
    
        f.write("\n")
             
    f.close()




def diff_percent(url_last):
    
    insert_transcript = "https://www.ted.com"+url_last
    asdf = insert_transcript.split('/')
    d = insert_transcript.split('?')
    eee = d[0]+"/transcript?language=en"
    kkk = d[0]+"/transcript?language=ko"

    address1=urlopen(eee)
    address2=urlopen(kkk)
    data1 = BeautifulSoup(address1,"html.parser")
    data2 = BeautifulSoup(address2,"html.parser")
    source_time1 = data1.findAll('span',attrs={'class':'talk-transcript__fragment'})
    source_time2 = data2.findAll('span',attrs={'class':'talk-transcript__fragment'})
    source1 = []
    source2 = []
    for x in range(len(source_time1)):
        tmp = source_time1[x]
        tmp = str(tmp).split(' ')
        source1.append(tmp[2])
    for y in range(len(source_time2)):
        tmp = source_time2[y]
        tmp = str(tmp).split(' ')
        source2.append(tmp[2])
    
    diff=0;
    diff2=0
    for j in source2:
        chk=0
        for i in source1:
            if(i==j):
                chk=1
                break;
        if(chk!=1):
            diff=diff+1

    for j in source1:
        chk=0
        for i in source2:
            if(i==j):
                chk=1
                break;
        if(chk!=1):
            diff2=diff2+1


    aver1=(float)(diff+diff2)/2
    aver2=(float)(len(source1)+len(source2))/2
    per=aver1/aver2

    return per*100

def matching():
    f_eng= open("Ted_en/Ted_eng."+str(data_number)+".txt","r",encoding='UTF8')
    f_kor = open("Ted_ko/Ted_kor."+str(data_number)+".txt","r",encoding='UTF8')
    f_ENmat = open("Ted_ENmatch/Ted_ENmat."+str(data_number)+".txt","w",encoding='UTF8')
    f_KOmat = open("Ted_KOmatch/Ted_KOmat."+str(data_number)+".txt","w",encoding='UTF8')

    to_write=''
    now = time.localtime()
    tt = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    to_write=to_write+tt+"\n"
    csv2.write(to_write)

    eng=f_eng.readlines()
    kor=f_kor.readlines()

    for x in range(len(eng)):
        if eng[x]=='\n':
            continue
            
        tmp1=str(eng[x]).split('&&')
        for y in range(len(kor)):
            if kor[y]=="\n":
                continue
            tmp2=str(kor[y]).split('&&')
            chk=0
            if tmp1[0]==tmp2[0]:
                chk=1
                next_tmp1=str(eng[x+1]).split('&&')
                next_tmp2=str(kor[y+1]).split('&&')
                if next_tmp1[0]==next_tmp2[0]:
                    f_ENmat.write(tmp1[1])
                    f_KOmat.write(tmp2[1])
                    f_ENmat.write("\n")
                    f_KOmat.write("\n")

    f_eng.close()
    f_kor.close()
    f_ENmat.close()
    f_KOmat.close()

def save_html(url_last):
    insert_transcript = "https://www.ted.com"+url_last
    asdf = insert_transcript.split('/')
    ddd = asdf[4].split('?')
    to_write = str(ddd[0])+","+insert_transcript+","
    d = insert_transcript.split('?')
    s = d[0]+"/transcript?language=en"
    s1 = d[0]+"/transcript?language=ko"
    
    now = time.localtime()
    tt = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    to_write=to_write+tt+"\n"
    csv.write(to_write)

    '''
    f = open("html/eng/html"+str(data_number),"w")
    address=urlopen(s)
    data=BeautifulSoup(address,"html.parser")
    f.write(str(data))
    f.close()
    
    f1 = open("html/kor/html"+str(data_number),"w")
    address1=urlopen(s1)
    data1=BeautifulSoup(address1,"html.parser")
    f1.write(str(data1))
    f1.close()
    '''
    
i=0
while i<=61:
    number = str(i)
    address = urlopen('https://www.ted.com/talks?language=ko&page='+number+'&sort=newest')
    sources = BeautifulSoup(address,"html.parser")
    list_audio = sources.findAll('a',attrs={'lang':'ko'})
    x=0
    list_number_audio = len(list_audio)
    #부분적으로는 쓰고, 전체는 없애고
    data_number=i*36
    for x in range(list_number_audio):
        tmp = str(list_audio[x])
        sp = tmp.split('href="')
        y=0
        url_last=""
        while 1:
            if(sp[1][y]=='"'):
                break;

            url_last = url_last + sp[1][y]
            y=y+1
    
        insert_transcript = "https://www.ted.com"+url_last
        print("[",data_number,"] lecture")

        sss=diff_percent(url_last)

        print("퍼센트:",sss)
        if sss<=50:
            kor(url_last)
            en(url_last)
            matching()
            #save_html(url_last)
        data_number=data_number+1

            

    #time.sleep(3.00)

    i=i+1
    
#csv.close()
csv2.close()
