from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
def div_english_sentence(content,filenumber):
    buffer = ""
    #div enlish sentence
    '''
    content=content.replace(". \n",".**next**")
    content=content.replace(".\n", ".**next**")
    content=content.replace("” \n","”**next**")
    content=content.replace("”\n", "”**next**")
    content=content.replace("＂\n","＂**next**")
    content=content.replace("＂\n","＂**next**")
    '''
    f = open("../../data/Herald/sample/eng/"+str(filenumber)+".txt","w",encoding="UTF8")
    #f = open("./result.txt","w",encoding="UTF8")
    for x in content:
        flag=0
        x = str(x).replace("\u3000\n","\n")
        x = str(x).replace(" \n","\n")
        x = str(x).replace(".” ",".”\n")
        x = str(x).replace(".\" ",".\"\n")
        x = str(x).replace("No.","No")
        x = str(x).replace("a.k.a.","HHHH1")
        x = str(x).replace("Jan.","Jan")
        x = str(x).replace("Feb.","Feb")
        x = str(x).replace("Mar.","Mar")
        x = str(x).replace("April.","April")
        x = str(x).replace("May.","May")
        x = str(x).replace("Jun.","Jun")
        x = str(x).replace("Jul.","Jul")
        x = str(x).replace("July.","July")
        x = str(x).replace("Aug.","Aug")
        x = str(x).replace("Sep.","Sep")
        x = str(x).replace("Oct.","Oct")
        x = str(x).replace("Nov.","Nov")
        x = str(x).replace("Dec.","Dec")
        
        p = re.compile("[A-Z]\.[ ]?")
        findlist = p.findall(x)
        '''
        if(findlist!=[]):
            print(findlist)
        '''
        s = 0
        for i in findlist:
            x = x.replace(i,"GGGG"+str(s))
            s = s+1
        t = 0
        while 1:
            t = str(x).find("?” ",t+1)
            if(t==-1):
                break;
            if(ord(x[t+3])>=65 and ord(x[t+3])<=90):
                x = x[:t+2]+"\n"+x[t+3:]
        for y in range(len(x)):
            
            if(flag==1 and (x[y]=='.'or x[y]=='?' or x[y]=='!') and y+1<len(x)):
                if(x[y+1]!='”' and x[y+1]!='＂' and x[y+1]!='"' and x[y+1]!=')'):
                    if(x[y]=='?'):
                        x = x[:y]+"@#$"+x[y+1:]
                        #x=str(x).replace('?',"@#$")
                    elif(x[y]=='.'):
                        x = x[:y]+"%^&*"+x[y+1:]
                        #x=str(x).replace('.',"%^&*")
                    elif(x[y]=='!'):
                        x = x[:y]+"%&%&"+x[y+1:]
            
            if(flag==1 and x[y]=='('):
                flag=2
            elif(flag==2 and x[y]==')'):
                flag=1
            elif(flag==1 and (x[y]=='”' or x[y]=='＂' or x[y]=='"' or x[y]==')')):
                flag=0
            elif(flag==0 and (x[y]=='“' or x[y]=='＂' or x[y]=='(' or x[y]=='"') ):
                flag=1
        
        tokens = sent_tokenize(x)
        for m in range(len(tokens)):
            s = 0
            tokens[m] = str(tokens[m]).replace("HHHH1","a.k.a")
            for i in findlist:
                tokens[m] = str(tokens[m]).replace("GGGG"+str(s),i)
                s = s+1
            tmp = str(tokens[m]).replace('@#$','?')
            tmp = str(tmp).replace('%^&*','.')
            tmp = str(tmp).replace('%&%&','!')
            buffer = buffer + tmp+"\n"
    buffer = buffer.replace("\n\n","\n")
    buffer = buffer.replace("\n\n","\n")
    buffer = buffer.replace("\n\n","\n")
    buffer = buffer.replace("\n\n","\n")
    buffer = buffer.replace("\n\n","\n")
    buffer = buffer.replace("\n\n","\n")
    
    f.write(buffer)
    f.close()


def div_eng(start, end):
    for i in range(start, end):
        f = open("../../data/Herald/resource/eng/"+str(i)+".txt","rU",encoding="UTF8")
        #f = open("./3.txt","rU",encoding="UTF8")
        content = f.readlines()
        div_english_sentence(content,i) 

f = open("8323.txt","r",encoding="UTF8")
l = f.readlines()
div_english_sentence(l,123123)
