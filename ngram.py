import sys
class Ngram:
    key=""
    value=""
    children=[]
    level=0

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children=[]
    def toChild(self, Ngram):
        Ngram.children.append(self)


def checkIsChild(s,Ngram):
    for x in Ngram.children:
        if(x.key == s):
            return x
    return NULL
def findParent(parent,key_entry_split,i):
    tmp = parent
    for x in parent.children:
        if(x.key == key_entry_split[i]):
            
            i = i+1
            if(i<len(key_entry_split)):
                tmp = findParent(x,key_entry_split,i)
            else:
                break;
    return tmp
def insert(root,key_entry,value_entry):
    key_entry_split = key_entry.split(" ")
    parent = findParent(root,key_entry_split,0)
    
    flag = False
    for idx,x in enumerate(key_entry_split):
        if parent.key == "root":
            flag = True
        elif x == parent.key:
            flag= True
            continue
        if flag == True :
            child = Ngram(key_entry_split[idx],"none")
            child.toChild(parent)
            parent = child
    nullchild = Ngram("","")
    nullchild.toChild(parent)
    value_entry = value_entry.replace("\t","")
    parent.value = value_entry.replace("\n","")
    #print(parent.key)
    #print(parent.value)
    

def makeNgramTree(filename, limit):
    print("makeNgramTree")
    f = open(filename,"rU",encoding='UTF8')
    root = Ngram("root","root")
    count = 0
    while 1:
        if(count%10000==0):
            print("count : ", count)
        if(limit==count):
            break
        line = f.readline()
        if not line:
            break;
        #print(line)
        sp = line.split(",\t")
        key_entry = sp[0]
        value_entry = sp[1]
        insert(root,key_entry, value_entry)
        count = count + 1
    #printChild(root)
    return root
def printChild(parent):
    print(parent.key)
    for x in parent.children:
        printChild(x)
def getChildren(parent):
    descendant = []
    if parent.children == []:
        return [parent.key]
    for child in parent.children:
        #print("child : ",child.key)
        tmp = getChildren(child)
        #print("tmp : ",tmp)
        for idx,family in enumerate(tmp):
            family = parent.key + " " + family
            #print("family : ",family)
            descendant.append(family)
    return descendant

def binarysearch(l,key, left, right):
    if(left <= right):
        mid = int((left+right)/2)
        if(mid >= len(l)): return -1
        mid_value = bytes(l[mid].key,'utf-8').hex()
        
        if(mid_value == key): return mid
        elif(mid_value < key): return binarysearch(l,key,mid+1,right)
        elif(mid_value > key): return binarysearch(l,key,left,mid-1)

    return -1
def search(parent, key):
    list = []
    # to do
    child_num = len(parent.children)
    
    s = binarysearch(parent.children,bytes(key,'utf-8').hex(),0,child_num)
    if(s==-1): return "none"
    
    list = getChildren(parent.children[s]) 
    '''
    for x in parent.children:
        if(x.key == key):
            list = getChildren(x)
    '''
    for x in range(len(list)):
        list[x]=list[x][:-1]
    s = sorted(list,key=len,reverse=True)
    return s
def findValue(parent, key):
    i=0
    num=0
    sp = key.split(" ")
    child_num = len(parent.children)-1
    
    s = binarysearch(parent.children,bytes(sp[i],'utf-8').hex(),0,child_num)
    
    if(s==-1): return "none"
    
    num = s
    # to do
    while 1:
        ch = parent.children[num]
        #print(ch.key)
        #print(sp[i])
        if(ch.key==sp[i]):
            if(i+1 >= len(sp)):
                return ch.value.replace("\n","")
            parent = ch
            child_num = len(parent.children)
            num=0
            i=i+1
            continue
        if(num+1>=child_num):
            return "none"
        num=num+1
def writeTree(parent, f, depth):
    if(parent.children==[]):
        f.write("#\n")
    else:
        f.write(parent.key+"\t"+parent.value+"\t"+str(depth)+"\n")
        for x in parent.children:
            writeTree(x,f,depth+1)

def readTree(parent, f):
    stacklist = []
    tmp = []
    tmp.append(parent)
    tmp.append(0)
    stacklist.append(tmp)
    while 1:
        line = f.readline()
        if not line: break
        line = line.replace("\n","")
        sp = line.split("\t")
        key = ""
        value = ""
        level = 0
        if(len(sp)==3):
            key = sp[0]
            value = sp[1]
            level = int(sp[2])
            #print("stacklist : ", stacklist)
            if(level==0): continue
            if(stacklist[-1][1] > level):
                while (level-1) != (stacklist[-1][1]):
                    tmp_child = stacklist.pop()[0]
                    tmp_list = stacklist.pop()
                    tmp_parent = tmp_list[0]
                    tmp_level = tmp_list[1]
                    tmp = []
                    tmp_child.toChild(tmp_parent)
                    tmp.append(tmp_parent)
                    tmp.append(tmp_level)
                    stacklist.append(tmp)
                tmp_node = Ngram(key,value)
                tmp = []
                tmp.append(tmp_node)
                tmp.append(level)
                stacklist.append(tmp)
            elif(stacklist[-1][1] == level):
                tmp_child=stacklist.pop()[0]
                tmp_list = stacklist.pop()
                tmp_parent = tmp_list[0]
                tmp_level = tmp_list[1]
                tmp = []
                tmp_child.toChild(tmp_parent)
                tmp.append(tmp_parent)
                tmp.append(tmp_level)
                stacklist.append(tmp)
                tmp_node = Ngram(key,value)
                tmp = []
                tmp.append(tmp_node)
                tmp.append(level)
                stacklist.append(tmp)
            elif(stacklist[-1][1]<level):
                tmp_node = Ngram(key,value)
                tmp = []
                tmp.append(tmp_node)
                tmp.append(level)
                stacklist.append(tmp)
        if(len(sp)==1 and sp[0]=="#"):
            tmp_list = stacklist.pop()
            tmp_parent = tmp_list[0]
            tmp_level = tmp_list[1]
            nullchild = Ngram("","")
            nullchild.toChild(tmp_parent)
            tmp = []
            tmp.append(tmp_parent)
            tmp.append(tmp_level)
            stacklist.append(tmp)
    while len(stacklist)>1:
        tmp_child = stacklist.pop()[0]
        tmp_list = stacklist.pop()
        tmp_parent = tmp_list[0]
        tmp_level = tmp_list[1]
        tmp_child.toChild(tmp_parent)
        tmp = []
        tmp.append(tmp_parent)
        tmp.append(tmp_level)
        stacklist.append(tmp)
    return stacklist.pop()[0]
def storeDictionary(fromfile, tofile, limit):
    file = open(tofile,"w",encoding="utf8")
    root = makeNgramTree(fromfile,limit)
    writeTree(root,file,0)
    file.close()
#storeDictionary()
def getRoot(fromfile):
    file2 = open(fromfile,"r",encoding="utf8")
    tmp_root = Ngram("root","root")
    tmp_root = readTree(tmp_root,file2)
    return tmp_root
#file2.close()
#testfile = open("test.csv","w",encoding="utf8")
#writeTree(tmp_root,testfile,0)
#testfile.close()
#print("make done")
#print(search(tmp_root,"니호늄"))
#print(findValue(tmp_root,"니호늄"))

#print(search(tmp_root,"닛산"))
#print(findValue(tmp_root,"닛산 GT-R"))
#search(root, "FM")
#search(root, "느무르")
#r = getRoot("dictionary.csv")
#print(search(r,"유인"))
'''
print(r.children[72181].key)
print(r.children[72182].key)
print(r.children[72183].key)
print(r.children[72184].key)
print(r.children[72185].key)
print(r.children[72186].key)
count = 0
for x in r.children:
    print(x.key)
    if(x.key=="유인"):
        print(x.key)
        break
    count+=1
print(count)
print(r.children[116801].key)
print(r.children[116802].key)
print(r.children[116803].key)
print(r.children[116804].key)
print(r.children[116805].key)
'''