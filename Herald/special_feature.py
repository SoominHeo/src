


kor_path="kor/kor/"
eng_path="eng/eng/"

def special_feature(filenumber):

    feature=['!','?','\"','\'','@','#','$','%','&','“','”','’']
    
    
    f_kor=open(kor_path+str(filenumber)+".txt","r",encoding="UTF8")
    f_eng=open(eng_path+str(filenumber)+".txt","r",encoding="UTF8")

    kor=f_kor.readlines()
    eng=f_eng.readlines()

    kor_feature=[[] for i in range(len(kor))]
    for i in range(len(kor)):
        for j in range(len(kor[i])):
            if kor[i][j] in feature:
                kor_feature[i].append(kor[i][j])

    eng_feature=[[] for i in range(len(eng))]
    for i in range(len(eng)):
        for j in range(len(eng[i])):
            if eng[i][j] in feature:
                eng_feature[i].append(eng[i][j])

    feature_table=[[] for i in range(len(kor))]
    for i in range(len(kor_feature)):
        if len(kor_feature[i])==0:
            for k in range(len(eng_feature)):
                feature_table[i].append(0)
            continue

        for k in range(len(eng_feature)):
            if len(eng_feature[k])==0:
                    feature_table[i].append(0)
                    continue
            for j in range(len(kor_feature[i])):
                if kor_feature[i][j] in eng_feature[k]:
                    if j==len(kor_feature[i])-1:
                        if len(kor_feature[i])==len(eng_feature[k]):
                            feature_table[i].append(str(i)+str(' ')+str(k))
                            break
                        else:
                            feature_table[i].append(0)
                    else:
                        continue
                else:
                    feature_table[i].append(0)
                    break

    '''                
    print("["+str(filenumber)+" text ]")
    print(len(kor_feature), len(eng_feature))
    for i in range(len(feature_table)):
        print(feature_table[i])
    '''
    


        
    

    
