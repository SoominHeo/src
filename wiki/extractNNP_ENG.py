#!/usr/bin/python
# -*- coding:utf-8 -*-
from nltk.tag import pos_tag
header_path = "../../data/wiki/header/{lang}/{idx}.txt"
def extractNNP_ENG(trans_set,i):
    try:
        f = open(header_path.format(lang='eng',idx=i),"rU",encoding='UTF8')
    except:
        return -1
    noun_list = []
    count = 0
    while 1:
        line = f.readline()
        if not line:
            break;

        tmp = []
        for value in trans_set:
            if line.lower().find(value.lower()) != -1:
                tmp.append(value)
        count = count+1

        if count == len(trans_set):
            break
        noun_list.append(tmp)


    return noun_list
