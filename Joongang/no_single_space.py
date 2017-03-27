

def no_single_space(start, end):
    for i in range(start, end):
        try:
            print(i)
            f_kor = open("../../data/Joongang/original_text/kor/"+str(i)+".txt","r",encoding="UTF8")
            f_eng = open("../../data/Joongang/original_text/eng/"+str(i)+".txt","r",encoding="UTF8")
            f_no_kor = open("../../data/Joongang/no_single_space_text/kor/"+str(i)+".txt","w",encoding="UTF8")
            f_no_eng = open("../../data/Joongang/no_single_space_text/eng/"+str(i)+".txt","w",encoding="UTF8")


            kor=f_kor.readlines()
            eng=f_eng.readlines()
            
            for k in range(len(kor)):
                if kor[k]=="\n" or kor[k]==" \n" or kor[k]=="  \n":
                    continue
                else:
                   f_no_kor.write(kor[k])

            for j in range(len(eng)):
                if eng[j]=="\n":
                    continue
                else:
                   f_no_eng.write(eng[j])
            f_no_eng.close()
            f_no_kor.close()
            f_kor.close()
            f_eng.close()
        except:
            print("no_single_spac error")
