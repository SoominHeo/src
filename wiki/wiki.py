# -*- coding: utf-8 -*-
import ssl
from urllib.request import urlopen
#import requests
from bs4 import BeautifulSoup
import time
import sys
import os
sys.path.append(os.getcwd()+"/metric/")
sys.path.append(os.getcwd()+"/extract/")
from urllib import parse
import urllib
import zss
import re
import metric
import reference
import photo_check
import check_translate_pair
import paragraph
import reading
import tree_compare
import header
import header_for_link
import translate_k_to_e
import extract_num_KOR
import extract_num_ENG
import extractNNP_KOR
import extractNNP_ENG


csv_path = "../../data/wiki/{csv}.csv"
html_path = "../../data/wiki/{lang}_html/{idx}.html"
header_path = "../../data/header/{lang}/{idx}.txt"
list_path = "../../data/wiki/{attr}/{lang}/{idx}.txt"

def remove_tags(data):
    p=re.compile(r'<.*?>')
    return p.sub('', data)

def save_list(newlist,csv):
    for x in newlist:
        s=x.split(' ')
        url=""
        title=""
        for y in s:
            if(y[0:5]=="href="):
                url = "https://ko.wikipedia.org"+y[6:len(y)-1]
    
        s=x.split('"')
        nextistitle=0
        for y in s:
            if(nextistitle==1):
                title=y
                break;
            if(y[len(y)-6:]=="title="):
                nextistitle=1
                continue;
        now = time.localtime()
        tt = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
        save_csv(url,title,tt,csv)
    if(url=="https://ko.wikipedia.org/wiki/%F0%9F%98%BC"):
        return -1

    return 1

def save_csv(url,title,tt,csv):
    print(str(url)+",\t"+str(title)+",\t"+str(tt)+"\n")
    csv.write(str(url)+",\t"+str(title)+",\t"+str(tt)+"\n")


def make_list_csv():#680000개 전체 데이터 url
    csv = open(csv_path.format(csv='urlindex'),"w",encoding='UTF8')

    nexturl = 'https://ko.wikipedia.org/w/index.php?title=%ED%8A%B9%EC%88%98:%EB%AA%A8%EB%93%A0%EB%AC%B8%EC%84%9C&from=%21';

    i=0
    tmp=nexturl
    chk=0

    while 1:
        print(str(i)+ " page")
        i+=1
        if(chk==1):
            chk=0
        if(chk==2):
            chk=0
        try:
            address = urlopen(nexturl)
            sources = BeautifulSoup(address,"html.parser")
            list_audio = sources.findAll('li')
            next = sources.findAll('div',attrs={'class':'mw-allpages-nav'})
            if(next==-1):
                break;
        except:
            print("ERROR")
            chk=2
            continue

        for x in next:
            d = str(x).split('|')
            s = str(x).split(' ')
            if(len(d)==1):
                for y in s:
                    if(y[0:5]=="href="):
                        d = y[6:len(y)-1].replace("amp;","")
                        tmp=nexturl
                        nexturl = 'https://ko.wikipedia.org'+d
                        break;

            if(len(d)==2):
                dd = 0
                for y in s:
                    if(y[0:5]=="href=" and dd==0):
                        dd=1
                        continue
                    elif(y[0:5]=="href=" and dd==1):
                        print("next")
                        dd=0
                        d = y[6:len(y)-1].replace("amp;","")
                        tmp=nexturl
                        nexturl = 'https://ko.wikipedia.org'+d
                        break;
                            
        newlist = []
        for x in list_audio:
            if(str(x).find('pt-anonuserpage')<0):
                newlist.append(str(x))
            else:
                break;
    
        if(save_list(newlist,csv)==-1):
            break;
    csv.close()



def pair_dic(): #pair있는 인덱스 만들기
    f = readcsv();
    p = open(csv_path.format(csv='pair470000'),"w",encoding='UTF8')

    while 1:
        line = f.readline()
        if not line: break
        s = line.split(',\t')
        try:
            address = urlopen(s[0])
        except:
            print("URL_OPEN_ERROR!")
            continue
        sources = BeautifulSoup(address,"html.parser")
        list_audio = sources.findAll('a',attrs={'lang':'en'})
        if(len(list_audio)==1):
            for x in list_audio:
                d = str(x).split(' ')
                for y in d:
                    if(y[0:5]=="href="):
                        try:
                            url=parse.unquote(y[6:len(y)-1])
                            t=url.split('/')
                            print(s[0]+",\t"+str(y[6:len(y)-1])+",\t"+s[1]+",\t"+str(t[-1])+"\n")
                            p.write(s[0]+",\t"+str(y[6:len(y)-1])+",\t"+s[1]+",\t"+str(t[-1])+"\n")
                        except:
                            break;
    p.close()


def pair_cro():#noredirect 부분만 저장
    p = open(csv_path.format(csv='pair470000'),"r",encoding='UTF8')
    f = open(csv_path.format(csv='data'),"w",encoding='UTF8')
    log = open(csv_path.format(csv='log'),"w",encoding='UTF8')

    filenumber = 0
    while 1:
        line = p.readline()
        if not line: break
        s = line.split(',\t')
        print("------------------")
        print("original : ",s[2])
        try:
            address_kor = urlopen(s[0])
        except:
            log.write(line)
            continue
        sources_kor = BeautifulSoup(address_kor,"html.parser")
        
        list = sources_kor.findAll('title')
        notag = remove_tags(str(list[0]))
        sp = notag.split(' - 위키백과')
        print("response : ",sp[0])
        if(sp[0]==s[2]):
            print("SAME!")
            kor = open(html_path.format(lang='kor',idx='filenumber'),"w",encoding='UTF8')
            eng = open(html_path.format(lang='eng',idx='filenumber'),"w",encoding='UTF8')
            try:
                address_eng = urlopen(s[1])
                f.write(line)
            except:
                log.write(line)
                print("URL OPEN ERROR!")
                continue
            sources_eng = BeautifulSoup(address_eng,"html.parser")
            kor.write(str(sources_kor))
            eng.write(str(sources_eng))
            kor.close()
            eng.close()
            filenumber = filenumber+1
    log.close()
    p.close()
    f.close()

def check_all_pair(dic, i):
    k = open(html_path.format(lang='kor',idx=i),"r",encoding='UTF8')
    sources_k = BeautifulSoup(k,"html.parser")
    e = open(html_path.format(lang='eng',idx=i),"r",encoding='UTF8')
    sources_e = BeautifulSoup(e,"html.parser")
    
    k.close()
    e.close()
    #Metric 평가요소
    t1=reference.reference(sources_k, sources_e)
    t2=tree_compare.tree_compare(sources_k,sources_e)
    t3=photo_check.photo_check(sources_k,sources_e)
    t4=check_translate_pair.check_translate_pair(sources_k)
    t5=paragraph.paragraph(sources_k,sources_e)
    t6=reading.reading(sources_k,sources_e)
    
    ck_link_list = [[]]
    e_link_list = [[]]
    
    if(t5==-1):
        return -1,-1,-1
    
    #Metric
    metric_result=metric.metric(t1,t2,t3,t4,t5,t6)
    #print (metric_result)

    ck = header.header(sources_k, sources_e, i, metric_result)
    if ck == -1:
        return -1,-1,-1
    else:
        k_link_list, e_link_list = header_for_link.header_for_link(sources_k, sources_e, i, metric_result)
        if k_link_list==-1:
            return -1,-1,-1
    ck_link_list = translate_k_to_e.translate_k_to_e(dic,k_link_list)

    return ck_link_list, e_link_list, metric_result

def make_file_for_LCS(ck_link_list, e_link_list,dic ,i):
    if(ck_link_list==-1):
        return -1
    k_num_list = extract_num_KOR.extract_num_KOR(i)
    e_num_list = extract_num_ENG.extract_num_ENG(i)

    #k_NNP_list = []
    k_NNP_list = extractNNP_KOR.extractNNP_KOR(dic,i)
    e_NNP_list = extractNNP_ENG.extractNNP_ENG(i)
    '''
    print("k_link: " + str(ck_link_list))
    print("k_num: " + str(k_num_list))
    print("k_NNP: " + str(k_NNP_list))
    print("e_link: " + str(e_link_list))
    print("e_num: " + str(e_num_list))
    print("e_NNP: " + str(e_NNP_list) + "\n")
    '''
    write_file(ck_link_list, e_link_list, "result/link_list", i)
    write_file(k_NNP_list, e_NNP_list, "result/NNP_list", i)
    write_file(k_num_list, e_num_list, "result/num_list", i)

def write_file(k_list, e_list, path, index):
    k_file = open(list_path.format(attr=path,lang='kor',idx=index), "w", encoding="UTF8")
    e_file = open(list_path.format(attr=path,lang='eng',idx=index), "w", encoding="UTF8")

    for i in range (len(k_list)):
        for j in range (len(k_list[i])):
            k_file.write(k_list[i][j] + ", ")
        k_file.write("\n")

    for i in range (len(e_list)):
        for j in range (len(e_list[i])):
            e_file.write(e_list[i][j] + ", ")
        e_file.write("\n")
    k_file.close()
    e_file.close()
