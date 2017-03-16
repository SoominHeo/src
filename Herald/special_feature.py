


kor_path="kor/kor/"
eng_path="eng/eng/"

def special_feature(kor,eng):
    feature=['!','?','\"','\'','@','#','$','%','&','“','”','’','(',')','[',']','{','}','<','>']
    
    # find feature in kor
    kor_feature=[[] for i in range(len(kor))]
    for i in range(len(kor)):
        for j in range(len(kor[i])):
            if kor[i][j] in feature:
                kor_feature[i].append(kor[i][j])

    # find feature in eng
    eng_feature=[[] for i in range(len(eng))]
    for i in range(len(eng)):
        for j in range(len(eng[i])):
            if eng[i][j] in feature:
                eng_feature[i].append(eng[i][j])
    
    feature_table = []
    kDomain = []
    eDomain = []
    #for i in range(len(kor_feature)):
    #    for k in range(len(eng_feature)):
    #        for j in range(len(kor_feature[i])):
    #            if kor_feature[i][j] in eng_feature[k]:
    #                if j==len(kor_feature[i])-1:
    #                    if len(kor_feature[i])==len(eng_feature[k]):
    #                        feature_table.append((i+1,k+1))
    
    #kIdx = 0
    #eIdx = 0
    #while kIdx < len(kor_feature):
    #    while eIdx < len(eng_feature):
    #        if len(kor_feature[kIdx]) == 0:
    #            kIdx += 1
    #        if kIdx == len(kor_feature):
    #            break
            
    #        for element in kor_feature[kIdx]:
    #            if element in eng_feature[eIdx]:
    #                feature_table.append((kIdx,eIdx))
    #                kIdx += 1
    #                eIdx += 1
    #            else:
    #                eIdx += 1
    for kIdx in range(len(kor_feature)):
        for eIdx in range(len(eng_feature)):
            for element in kor_feature[kIdx]:
                if element in eng_feature[eIdx]:
                    if kIdx not in kDomain:
                        kDomain.append(kIdx)
                    if eIdx not in eDomain:
                        eDomain.append(eIdx)


    kLength = len(kDomain)
    eLength = len(eDomain)
    
    if kLength == eLength:
        for i in range(kLength):
            feature_table.append((kDomain[i],eDomain[i]))
    #else:
    #    for kIdx in range(kLength):
    #        for eIdx in range(eLength):
    #            if kLength(kidx+1) == kLength(kidx) or kLength
    #            feature_table.append((kLength(kIdx),eLength(eIdx)))


        
        
    return feature_table

    '''                
    print("["+str(filenumber)+" text ]")
    print(len(kor_feature), len(eng_feature))
    for i in range(len(feature_table)):
        print(feature_table[i])
    '''
    


        
    

    
