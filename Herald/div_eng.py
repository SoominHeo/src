from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
def div_english_sentence(content,filenumber):
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
    for x in content:
        flag=0
        x = str(x).replace(".” ",".”\n")
        x = str(x).replace(".\" ",".\"\n")
        for y in range(len(x)):
            if(flag==1 and (x[y]=='.'or x[y]=='?') and y+1<len(x)):
                if(x[y+1]!='”' and x[y+1]!='＂' and x[y+1]!=')'):
                    if(x[y]=='?'):
                        x=str(x).replace('?',"@#$")
                    elif(x[y]=='.'):
                        x=str(x).replace('.',"%^&*")
            if(flag==1 and (x[y]=='”' or x[y]=='＂' or x[y]==')')):
                flag=0
            elif(flag==0 and (x[y]=='“' or x[y]=='＂' or x[y]=='(') ):
                flag=1

        tokens = sent_tokenize(x)
        for m in range(len(tokens)):
            tmp = str(tokens[m]).replace('@#$','?')
            tmp = str(tmp).replace('%^&*','.')
            f.write(tmp+"\n")

    f.close()


def div_eng(start, end):
    for i in range(start, end):
        f = open("../../data/Herald/sample/eng/"+str(i)+".txt","rU",encoding="UTF8")
        content = f.readlines()
        div_english_sentence(content,i) 
   


