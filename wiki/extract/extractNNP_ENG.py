#!/usr/bin/python
# -*- coding:utf-8 -*-
from nltk.tag import pos_tag
header_path = "../../data/wiki/header/{lang}/{idx}.txt"
def extractNNP_ENG(i):
    try:
        f = open(header_path.format(lang='eng',idx=i),"rU",encoding='UTF8')
    except:
        return -1
    e_list = []
    while 1:
        sentence = f.readline()
        if not sentence:
            break;
        tagged_sent = pos_tag(sentence.split())
        propernouns = [word for word,pos in tagged_sent if pos == 'NNP' or pos == 'NN' or pos == 'NNS']
        e_list.append(propernouns)

    return e_list
