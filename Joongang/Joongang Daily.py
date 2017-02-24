from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
#from konlpy.tag import Kkma
#from konlpy.utils import pprint
import time
import copy
#import datetime
import number_ko
import number_en
import LCS
def remove_br_tags(data):
    newstr = data.replace("<br/>","=br=")
    newstr = newstr.replace("<br>\n<br>","=br=")
    
    return newstr

def div_english_korean(data):
    newstr = data.replace("</font><br/><br/>","!div_eng_kor!")
    newstr = newstr.replace("</b></font>=br= =br=","!div_eng_kor!")
    newstr = newstr.replace("</b></font>=br==br=","!div_eng_kor!")
    newstr = newstr.replace("</b></font>=br=","!div_eng_kor!")
    newstr = newstr.replace("</b><font>","!div_eng_kor!")
    newstr = newstr.replace("</font><br><br><font class=\"txt\">","!div_eng_kor!")
    newstr = newstr.replace("<div class=\"article_dvright\"><div class=\"article_content\">","!div_eng_kor!")
    newstr = newstr.replace("</b></font>=br==br==br=","!div_eng_kor!")
    newstr = newstr.replace("</html>=br==br=","!div_eng_kor!")
    newstr = newstr.replace("</b></font>=br= =br=","!div_eng_kor!")
    newstr = newstr.replace("</b></font>=br==br=","!div_eng_kor!")
    newstr = newstr.replace("</b></font> =br==br=","!div_eng_kor!")
    newstr = newstr.replace("</b></font>","!div_eng_kor!")
    return newstr

#remove tags
def remove_tags(data):
    p=re.compile(r'<.*?>')
    return p.sub('', data)

def div_english_sentence(bodies_split,filenumber,csv2):
    p = re.compile('[0-9\.\'\`]?[ㄱ-ㅣ가-힣]+.*[ㄱ-ㅣ가-힣]+')
    bodies_split[0] = p.sub('',bodies_split[0])
        
        
    
    #div enlish sentence
    bodies_split[0]=bodies_split[0].replace(". \n",".**next**")
    bodies_split[0]=bodies_split[0].replace(".\n", ".**next**")
    bodies_split[0]=bodies_split[0].replace("” \n","”**next**")
    bodies_split[0]=bodies_split[0].replace("”\n", "”**next**")
    bodies_split[0]=bodies_split[0].replace("＂\n","＂**next**")
    bodies_split[0]=bodies_split[0].replace("＂\n","＂**next**")
    mun_split=bodies_split[0].split("**next**")
    a = len(mun_split)
    for h in range(a):
        flag=0
        for y in range(len(mun_split[h])):
            if(flag==1 and mun_split[h][y]=='.' and y+1<len(mun_split[h])):
                if(mun_split[h][y+1]!='”' and mun_split[h][y+1]!='＂'):
                    mun_split[h] = mun_split[h][:y] + " " + mun_split[h][y+1:]
            if(flag==1 and (mun_split[h][y]=='”' or mun_split[h][y]=='＂')):
                flag=0
            elif(flag==0 and (mun_split[h][y]=='“' or mun_split[h][y]=='＂') ):
                flag=1
    f = open("../../data/Joongang/original_text/en/"+str(filenumber)+".txt","w",encoding="UTF8")
    tmp=""
    for n in range(a):
        tokens = sent_tokenize(mun_split[n])
        b = len(tokens)
        for m in range(b):
            p = re.compile("[\n]*")
            tokens[m] = p.sub('',tokens[m])
            tokens[m]=tokens[m].replace(".” ",".”");
            tokens[m]=tokens[m].replace(".”",".”\n");
            '''
            p = re.compile('JoongAng Ilbo.*\s*\n*')
            tokens[m] = p.sub('',tokens[m])
            p = re.compile('The author is.*\s*\n*')
            tokens[m] = p.sub('',tokens[m])
            p = re.compile('The writer is .*\s*\n*')
            tokens[m] = p.sub('',tokens[m])
            p = re.compile('by .+[ ]*.*-.+')
            tokens[m] = p.sub('',tokens[m])
            '''
            tmp=tmp+tokens[m]
            tmp=tmp+"\n"
        tmp = tmp+"\n"
    '''
    tokens = tmp.split("\n\n\n")
    
    s = len(tokens[0])
    for p in range(s):
        if tokens[0][s-1-p]=="\n":
            tokens[0] = tokens[0][0:s-1-p]
        else:
            break
    '''
    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    csv2.write(str(s)+"\n")
    f.write(tmp)

    f.close()


def sub_div_korean_sentence(p):
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
                      if prev=="가" or prev== "나" or prev== "다" or prev== "라" or prev== "까" or prev== "지":
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
                              if p[z-2]=="다" or p[z-2]=="나" or p[z-2]=="가" or p[z-2]=="라" or p[z-2]=="까" or p[z-2]=="지":
                                      temp=temp+p[z]+"\n"
                                      st.append(temp)
                                      temp=""
                                      start=0
                                      finish=0

                      else:
                              temp=temp+p[z]
                        
                                
              else:
                     temp=temp+p[z]   




    
    #remove space in front of sentences
    for index in range(len(st)):
       ct=0
       for w in range(len(st[index])):

           if st[index][w]==" " or st[index][w]=="\n":
               ct=ct+1
           else:
               break

       st[index]=st[index][ct:len(st[index])]


    return st

    
    
def div_korean_sentence(bodies_split,filenumber,csv2):
    bodies_split[1]=bodies_split[1].replace(". \n",".**next**")
    bodies_split[1]=bodies_split[1].replace(".\n",".**next**")
    bodies_split[1]=bodies_split[1].replace("\n\n\n\n","**next**")
        
    mun_split=bodies_split[1].split("**next**")

    a = len(mun_split)
        
    f = open("../../data/Joongang/original_text/ko/"+str(filenumber)+".txt","w",encoding="UTF8")
    for n in range(a): 
        tokens=sub_div_korean_sentence(mun_split[n])

        if tokens==[]:
            continue
        
        if n!= a-1:
            next_tokens=sub_div_korean_sentence(mun_split[n+1])

        b = len(tokens)
        for m in range(b):
            p = re.compile("[\n]*")
            tokens[m] = p.sub('',tokens[m])
                    
            f.write(tokens[m])
            
            if n==a-1:
                if m!=b-1:
                     f.write("\n")

            else:
                if next_tokens!=[] or m!=b-1:
                     f.write("\n")
                
                    
        if n!=a-1:
            if next_tokens!=[]:
                f.write("\n")
            
    
    f.close()
    

def store_html_csv(address, data, filenumber,csv,id):
    f = open("../../data/Joongang/original_html/html/"+str(filenumber)+".html","w",encoding='UTF8')
    date = str(data.findAll('span',attrs={'class':'date'}))
    p = re.compile('\[')
    date = p.sub('',date)
    p = re.compile('\]')
    date = p.sub('',date)
    date = remove_tags(date)

    tokens=id.split("aid=")

    now = time.localtime()
    s = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    attribute = str(tokens[1])+","+str(address)+","+str(date)+","+str(s)+"\n"
    #print(attribute)
    csv.write(attribute)
    f.write(str(data))
    f.close()

def get_html_csv():

    #Begging page number
    i=1
    filenumber=i*10-10;
    csv = open("../../data/Joongang/original_html/attribute.csv","w",encoding="UTF8")
    while i<=822:    #Ending page number
        print(str(i)+" page")
    
        # Get articles from joongangdaily
        number = str(i)
        address = urlopen('http://koreajoongangdaily.joins.com/news/list/list.aspx?gCat=060201&pgi='+number)
        sources = BeautifulSoup(address,"html.parser")
        test0 = sources.findAll('a',attrs={'class':'title_cr'})
        x=0
    
        while 1:
            print("\t"+str(filenumber)+" article")
            if(x==10): #10 online articles in one page
                break;
        
            ddd = str(test0[x])
            test1 = ddd.split('href="')
            y=0
            url_last =""
        
            while 1:
                if(test1[1][y]=='"'):
                    break;
            
                url_last = url_last + test1[1][y]
                y = y+1
            id = str(url_last)
            urladdress = "http://koreajoongangdaily.joins.com"+id
            address = urlopen('http://koreajoongangdaily.joins.com/'+id)
            data = BeautifulSoup(address,"html.parser")
            store_html_csv(urladdress, data, filenumber,csv,id)
            filenumber = filenumber+1
            x = x+1
            
        i = i+1

    csv.close()



def save_content(start,end):
    filenumber = start
    csv2 = open("../../data/Joongang/original_text/attribute.csv","w",encoding="UTF8")
    while filenumber <= end:
        print(filenumber)
        file = open("../../data/Joongang/original_html/html/"+str(filenumber)+".html","rU",encoding='UTF8')
        data = BeautifulSoup(file,"html.parser")
        #for raw data that contains a lot of tags and space.
        f = open("raw_data.txt","w",encoding='UTF8')
        f.write(str(data.prettify))
        f.close()
        s = open("raw_data.txt","r",encoding='UTF8')
        tmp=""
        chk=0
            
        #Get specific parts of raw data. Beginng note, that is for cutting contents, is "<span class="data">", and Ending note is "id="language">" in the raw data.
        for st in s :
            if chk==2:
                break
            if st[0:19]=="<span class=\"date\">":
                chk=1
            elif chk==1:
                tmp=tmp+st
                toSplit = st.split()
                for u in range(len(toSplit)):
                    if toSplit[u]=="id=\"language\">":
                        chk=2
                        break
    
    
        #Get more valuable contens by cutting tags and space
        tmp = remove_br_tags(tmp)
        tmp = div_english_korean(tmp)
        bodies=remove_tags(tmp)
            
        bodies=bodies.replace("=br=","\n\n")
            
        bodies_split=bodies.split("!div_eng_kor!")
            
        if len(bodies_split)<2:
            #x=x+1
            filenumber = filenumber+1
            continue;
            
        div_english_sentence(bodies_split,filenumber,csv2)
        div_korean_sentence(bodies_split,filenumber,csv2)
        filenumber = filenumber + 1
        
    csv2.close()

#get_html_csv()
print("save_content")
save_content(0,8217)
'''
print("number_ko")
number_ko.number_ko(0,8217)
print("number_en")
number_en.number_en(0,8217)
print("LCS")
LCS.run(0,8217)
'''
