


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
    for i in range(len(kor_feature)):
        for k in range(len(eng_feature)):
            for j in range(len(kor_feature[i])):
                if kor_feature[i][j] in eng_feature[k]:
                    if j==len(kor_feature[i])-1:
                        if len(kor_feature[i])==len(eng_feature[k]):
                            feature_table.append((i+1,k+1))
                            
    return feature_table

    '''                
    print("["+str(filenumber)+" text ]")
    print(len(kor_feature), len(eng_feature))
    for i in range(len(feature_table)):
        print(feature_table[i])
    '''
    


        
    

    
