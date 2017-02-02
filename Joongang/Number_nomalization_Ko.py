# -*- coding: utf-8 -*-
import re

class WordsToNumbers():
    __ones__ = { 'il':   1,
                 'i':   2, 
                 'sam': 3,
                 'sa':  4, 
                 'o':  5, 
                 'yook':   6,
                 'chil': 7, 
                 'pal': 8, 
                 'goo':  9

                }
                 
    __groups__ = { 'sib':       10,
                   'bac':       100,
                   'cheon':     1000,
                   'man':       10000,
                   'uk':        100000000,
                   'jo':        1000000000000,
                   'kyeong':    10000000000000000,
                   'hae':       10000000000000000000}
                   
    __groups_re__ = re.compile(r'\s?([\w\s]+?)(?:\s((?:%s))|$)' % ('|'.join(__groups__)))

    __ones_re__ =  re.compile(r'((?:%s))(?:\s(.*)|$)')

    def parse(self, words):
        words = words.lower()       
        num = 0
  
        group_multiplier = 1
        for group in WordsToNumbers.__groups_re__.findall(words):
            
            if group[1] in WordsToNumbers.__groups__:
                
                #천만과 같이 뒤에 나오는 unit이 더 커질때
                if(WordsToNumbers.__groups__[group[1]] >= 10000 and group_multiplier <= 1000 ):
                    group_multiplier = WordsToNumbers.__groups__[group[1]]
                    num += (num % 10000 ) * (group_multiplier -1)
                            
                else:
                    group_multiplier = WordsToNumbers.__groups__[group[1]]
                    

            else:
                group_multiplier = 1
               

            
            group_num = 0
            
            
            ones = group[0]
            #unit을 나타내는 숫자만 있을 때
            if ones is None:
                num = num + (group_num * group_multiplier)
                continue
                
            #숫자로 표현되었을 때
            if(ones.isdigit()):
                group_num = group_num + int(ones)
            else:
                
                group_num = group_num + WordsToNumbers.__ones__[ones]
            num = num + (group_num * group_multiplier)


        return num
        
if __name__ == "__main__":
    nums = [
        "il","10", "100 man", "5 uk sa bac chil sib pal man 5 cheon chil bac", "5 sib 1 uk 3 sib","1 cheon 1 uk"]
    new_list = []
    for num in nums:
        output=""
        i=0
        for j in num:
            if j.isalpha() and num[i-1].isdigit():
                output += " "+j
            else: 
                output += j
            i=i+1
        new_list.append(output)
 
    wtn = WordsToNumbers()
    for num in new_list:
        print num, ": ", wtn.parse(num)