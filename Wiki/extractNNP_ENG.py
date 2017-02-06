#!/usr/bin/python
# -*- coding:utf-8 -*-
from nltk.tag import pos_tag
def extractNNP_ENG(i):
    f = open("../../data/Wiki/sample/header/eng/"+str(i)+".txt","rU",encoding='UTF8')
    e_list = []
    while 1:
        sentence = f.readline()
        if not sentence:
            break;
        tagged_sent = pos_tag(sentence.split())
        propernouns = [word for word,pos in tagged_sent if pos == 'NNP' or pos == 'NN' or pos == 'NNS']
        e_list.append(propernouns)

    return e_list
extractNNP_ENG(1)
