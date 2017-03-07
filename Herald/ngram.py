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

    parent.value = value_entry
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
        sp = line.split(", ")
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

def search(parent, key):
    list = []
    for x in parent.children:
        if(x.key == key):
            list = getChildren(x)
    s = sorted(list,key=len,reverse=True)
    return s

def findValue(parent, key):
    i=0
    num=0
    sp = key.split(" ")
    child_num = len(parent.children)
    while 1:
        ch = parent.children[num]
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

'''
root = makeNgramTree("test.csv")
print("make done")
print(search(root,"젤다의"))
print(findValue(root,"코카콜라"))
print(findValue(root,"젤다의 전설: 브레스 오브 더 와일드"))
'''
#search(root, "FM")
#search(root, "느무르")
