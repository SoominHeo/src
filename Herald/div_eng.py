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
<<<<<<< HEAD
    #f = open("../../data/Herald/sample/eng/"+str(filenumber)+".txt","w",encoding="UTF8")
    f = open("./result.txt","w",encoding="UTF8")
=======
    f = open("../../data/Herald/sample/eng/"+str(filenumber)+".txt","w",encoding="UTF8")
    #f = open("./result.txt","w",encoding="UTF8")
>>>>>>> c5190002ec2538457a6c47c1aa4772f56f93b905
    for x in content:
        flag=0
        x = str(x).replace(".” ",".”\n")
        x = str(x).replace(".\" ",".\"\n")
        x = str(x).replace("U.S.","U.S")
        x = str(x).replace("No.","No")
        for y in range(len(x)):
            
            
            if(flag==1 and (x[y]=='.'or x[y]=='?') and y+1<len(x)):
                if(x[y+1]!='”' and x[y+1]!='＂' and x[y+1]!=')'):
                    if(x[y]=='?'):
                        x = x[:y]+"@#$"+x[y+1:]
                        #x=str(x).replace('?',"@#$")
                    elif(x[y]=='.'):
                        x = x[:y]+"%^&*"+x[y+1:]
                        #x=str(x).replace('.',"%^&*")
            if(flag==1 and (x[y]=='”' or x[y]=='＂' or x[y]==')')):
                flag=0
            elif(flag==0 and (x[y]=='“' or x[y]=='＂' or x[y]=='(') ):
                flag=1

        tokens = sent_tokenize(x)
        print(tokens)
        for m in range(len(tokens)):
            tmp = str(tokens[m]).replace('@#$','?')
            tmp = str(tmp).replace('%^&*','.')
            f.write(tmp+"\n")
        f.write("\n")

    f.close()


def div_eng(start, end):
    for i in range(start, end):
<<<<<<< HEAD
        #f = open("../../data/Herald/resource/eng/"+str(i)+".txt","rU",encoding="UTF8")
        f = open("./test.txt","rU",encoding="UTF8")
        content = f.readlines()
        div_english_sentence(content,i) 
   
div_eng(0,1)

=======
        f = open("../../data/Herald/resource/eng/"+str(i)+".txt","rU",encoding="UTF8")
        #f = open("./test.txt","rU",encoding="UTF8")
        content = f.readlines()
        div_english_sentence(content,i) 
>>>>>>> c5190002ec2538457a6c47c1aa4772f56f93b905
