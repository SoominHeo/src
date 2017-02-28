from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from unicodedata import name
from nltk import sent_tokenize
import sys
import copy

def sub_kor_sentence(temp, word, st, start, finish):

    temp=temp+word+"\n"
    st.append(temp)
    temp=""
    start=0
    finish=0

    return temp, st, start, finish

def kor_sentence(p):
    temp=""
    st=[]
    start = 0
    finish = 0
    s_start=0
    s_finish=0
    prev=""

    endword=['가','나','다','라','자','까','지','요','죠','\"','%']
    endsign=['.','!','?']
    
    for z in range(len(p)):
        
              if z==0:
                  if p[z]=="\"" or p[z]=="“":
                       temp=temp+p[z]
                       start=1
                       continue
                  else:
                       temp=temp+p[z]
                       continue
                       
              elif z>0:
                       prev=p[z-1]

              # double quotes beginning and ending
              if p[z]=="\"":
                      if start==1 and finish==1:
                          finish=0
                      elif start==1 and finish==0:
                          finish=1
                      else:
                          start=1

              elif p[z]=="“":
                  if finish==1:
                      finish=0
                  else:
                      start=1
                  
              elif p[z]=="”" and start==1:
                      finish=1
                      
              # single quotes beginning and ending 
              if p[z]=="\'":
                      if s_start==1 and s_finish==1:
                          s_finish=0
                      elif s_start==1 and s_finish==0:
                          s_finish=1
                      else:
                          s_start=1
                          
              elif p[z]=="‘":
                  if s_finish==1:
                      s_finish=0
                  else:
                      s_start=1

              elif p[z]=="’" and s_start==1:
                      s_finish=1

              # separate sentences
              if p[z] in endsign:
                      if prev in endword:
                              if ( start==1 and finish==0 ) or ( s_start==1 and s_finish==0 ):
                                      temp=temp+p[z]
                              else:
                                      temp, st, start, finish = sub_kor_sentence(temp, p[z], st, start, finish)
                      elif prev==")":
                              if p[z-2] in endword: 
                                      temp, st, start, finish = sub_kor_sentence(temp, p[z], st, start, finish)
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
