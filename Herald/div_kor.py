
import kor_sentence

def div_korean_sentence(bodies_split,filenumber):
    bodies_split=bodies_split.replace(". \n",".**next**")
    bodies_split=bodies_split.replace(".\n",".**next**")
    bodies_split=bodies_split.replace("\n\n\n\n","**next**")
        
    mun_split=bodies_split.split("**next**")

    f = open("../../data/Herald/sample/kor/"+str(filenumber)+".txt","w",encoding="UTF8")
    buffer = ""
    tokens=[]
    for n in range(len(mun_split)):
        temp=kor_sentence.kor_sentence(mun_split[n])
        if temp!=[]:
            tokens.append(temp)

    for j in range(len(tokens)):
        for i in range(len(tokens[j])):
            if j==len(tokens)-1 and i==len(tokens[j])-1:
                buffer = buffer + tokens[j][i][:len(tokens[j][i])-1]
            else:
                buffer = buffer + tokens[j][i]
        if j!=len(tokens)-1:
            buffer = buffer + "\n"
    buffer = buffer.replace("\n\n","\n")
    buffer = buffer.replace("　\n","")
    f.write(buffer)
    f.close()    

def div_kor(start, end):
    for i in range(start, end):
        f = open("../../data/Herald/resource/kor/"+str(i)+".txt","rU",encoding="UTF8")
        list = f.readlines()
        tmp = ""
        for x in list:
            tmp = tmp+str(x)
        div_korean_sentence(tmp,i)



