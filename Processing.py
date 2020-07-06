import re
import UrduPhone as up

def store_tokens():
    with open("Dataset/Roman Urdu Dataset.txt") as f:
        tokens = f.read()
    
    tokens = tokens.lower()
    tokens = re.sub("[^A-Za-z]+"," ", tokens)
    tokens = tokens.split()
    
    file = open("Processed_Files/Total_vocabulary.txt","w")
    
    for i in range(len(tokens)):
        file.write(tokens[i] + "\n")
        
def retrieve_tokens():
    file = open("Processed_Files/Total_vocabulary.txt","r")
    tokens = file.read()
    tokens = tokens.split()
    return tokens

def get_gold_inter_vocab():
    words = retrieve_tokens()
    ff=open("Dataset/Roman Urdu Gold Standard.txt",encoding="utf8")
    text=ff.read()
    text = text.split()
    strwords=[]
    for t in text:
        strwords.append(t.split(",")[0].lower())
        strwords.append(t.split(",")[1].lower())
    
    new_list = set(words).intersection(set(strwords))
    print ("wordlist count = ",len(new_list))
    new_list = list(new_list)
    new_list.sort()
    
    return new_list

def get_gold_standard():
    ff=open("Dataset/Roman Urdu Gold Standard.txt",encoding="utf8")
    text=ff.read()
    text = text.split()
    gold = {}
    n = 0
    for t in text:
        s = t.split(",")
        w1 = s[0].lower()
        w2 = s[1].lower()
        key = str(n) + w1[0] + w2[0]
        gold[key] = [w1,w2]
        n += 1
        
    return gold

def token_ID():
    word = get_gold_inter_vocab()
    ID = {}
    x = 0
    for i in word:
        ID[i] = x
        x += 1
    
    file = open("Processed_Files/Tokens_ID.txt","w")
    for i in ID:
        file.write(i + " " + str(ID[i]) + "\n")

def get_tokens_ID():
    file = open("Processed_Files/Tokens_ID.txt","r")
    tokens = file.read()
    tokens = tokens.split("\n")
    
    ID = {}
    for i in range(0, len(tokens)-1):
        x = tokens[i].split()
        ID[x[0]] = x[1]
    return ID

def write_actual_clusters():
    actual_clusters = {}
    g = get_gold_standard()
    words = get_gold_inter_vocab()
    for w in words:
        l = []
        for i in g:
            if w[0] == i[-1] and w[0] == i[-2]:
                if w in g[i]:
                    #print(i)
                    l.extend(g[i])
                #l = list(set(l))
        l = list(set(l).intersection(set(words)))
        actual_clusters[w] = l
        
    file = open("Processed_Files/Actual_Clusters.txt","w")
    
    for i in actual_clusters:
        file.write(i)
        for j in actual_clusters[i]:
            file.write(" " + j)
        file.write("\n")
        
def get_actual_clusters():
    file = open("Processed_Files/Actual_Clusters.txt","r")
    clusters = file.read()
    clusters = clusters.split("\n")
    
    clu = {}
    for i in range(0,len(clusters)-1):
        tokens = clusters[i].split()
        clu[tokens[0]] = tokens[1:]
       
    return clu 

def get_Urduphone_ID():
    file = open("Processed_Files/UrduPhone_ID.txt","r")
    tokens = file.read()
    tokens = tokens.split("\n")
    
    ID = {}
    for i in range(0, len(tokens)-1):
        x = tokens[i].split()
        ID[x[0]] = x[1]
    return ID

def Vocab_UrduPhone():
    word = get_gold_inter_vocab()
    file = open("Processed_Files/UrduPhone_codes.txt","w")
    u = up.UrduPhone()
    for i in word:
        file.write(i + " " + u.urduphone(i) + "\n")
     
def get_UrduPhone_Vocab():
    file = open("Processed_Files/UrduPhone_codes.txt","r")
    tokens = file.read()
    tokens = tokens.split("\n")
    up = {}
    for i in range(0, len(tokens)-1):
        x = tokens[i].split()
        up[x[0]] = x[1]
    return up
    
def UrduPhone_ID():
#    ids = get_tokens_ID()
    urduphone = get_UrduPhone_Vocab()
    
    urduphone_dict = {}
    x = 0
    for i in urduphone:
        urduphone_dict[urduphone[i]] = x
        x += 1
#        try:
#            urduphone_dict[urduphone[i]].append(ids[i])
#        except:
#            key = urduphone[i]
#            urduphone_dict.setdefault(key, [])
#            urduphone_dict[key].append(ids[i])
    
    file = open("Processed_Files/UrduPhone_ID.txt","w")
    for i in urduphone:
        file.write(i + " " + str(urduphone_dict[urduphone[i]]) + "\n")
#        for j in urduphone_dict[i]:
#            file.write(" " + j)
#        file.write("\n")

def tokens_index_dict():
    tokens = retrieve_tokens()
    tokens_dict = {}
    for i in range(len(tokens)):
        try:
            tokens_dict[tokens[i]].append(i)
        except:
            key = tokens[i]
            tokens_dict.setdefault(key,[])
            tokens_dict[key].append(i)
    
    return tokens_dict

def Next5(feature):
    ff=open("Processed_Files/5 Next "+ feature + " List.txt","w")
    tokens = retrieve_tokens()
    words = get_gold_inter_vocab()
    if feature == "WordID":
        ids = get_tokens_ID()
    else:
        ids = get_Urduphone_ID()
        
    tokens_dict = tokens_index_dict()
    
    for w in words:
        indexes = []
        nextw = {}
        indexes = tokens_dict[w]
        for t in indexes:
            if tokens[t] == w:
                try:
                    #print(tokens[t+1])
                    nextw[tokens[t+1]] += 1
                except:
                    try:
                        #print(tokens[t+1])
                        nextw[tokens[t+1]] = 1
                    except:
                        print("+++++++++++++++++++++++++++++++++++++++++++d")
                    
        nextdict2 =sorted(nextw.items(), key=lambda x: x[1],reverse=True)
        
        i=0
        
        if feature == "UrduID":
            u = {}
            for j in range(len(nextdict2)):
                try:
                    key = ids[nextdict2[j][0]]
                    u.setdefault(key,[])
                    u[key].append(nextdict2[j][0])
                except:
                    print("")
            key = list(u.keys())
            ff.write(w)
            print(w)
            while i<5 and i<len(u):
                try:
                    ff.write(" "+str(key[i]))
                except: pass
                i+=1
            ff.write("\n")
        else:
            if len(nextdict2)>0:
                ff.write(w)
                print(w)
                while i<5 and i<len(nextdict2):
                    try:
                        ff.write(" "+str(ids[nextdict2[i][0]]))
                    except: pass
                    i+=1
                ff.write("\n")
            
def Prev5(feature):
    ff=open("Processed_Files/5 Prev "+ feature + " List.txt","w")
    tokens = retrieve_tokens()
    words = get_gold_inter_vocab()
    if feature == "WordID":
        ids = get_tokens_ID()
    else:
        ids = get_Urduphone_ID()
        
    tokens_dict = tokens_index_dict()

    for w in words:
        indexes = []
        prevw = {}
        indexes = tokens_dict[w]
        for t in indexes:
            if tokens[t] == w:
                try:
                    #print(tokens[t+1])
                    prevw[tokens[t-1]] += 1
                except:
                    try:
                        #print(tokens[t+1])
                        prevw[tokens[t-1]] = 1
                    except:
                        print("+++++++++++++++++++++++++++++++++++++++++++d")
                    
        prevdict2 =sorted(prevw.items(), key=lambda x: x[1],reverse=True)
        i=0
		
        if feature == "UrduID":
            u = {}
            for j in range(len(prevdict2)):
                try:
                    key = ids[prevdict2[j][0]]
                    u.setdefault(key,[])
                    u[key].append(prevdict2[j][0])
                except:
                    print("")
            key = list(u.keys())
            
            ff.write(w)
            print(w)
            while i<5 and i<len(u):
                try:
                    ff.write(" "+str(key[i]))
                except: pass
                i+=1
            ff.write("\n")
        else:
            if len(prevdict2)>0:
                ff.write(w)
                print(w)
                while i<5 and i<len(prevdict2):
                    try:
                        ff.write(" "+str(ids[prevdict2[i][0]]))
                    except: pass
                    i+=1
                ff.write("\n")

def get_prev(feature):
    file =open("Processed_Files/5 Prev "+ feature + " List.txt","r")
    tokens = file.read()
    tokens = tokens.split("\n")
    
    Dict = {}
    for i in range(0, len(tokens)-1):
        x = tokens[i].split()
        key = x[0]
        Dict.setdefault(key,[])
        for j in x[1:]:
            Dict[key].append(j)
            
    return Dict

def get_next(feature):
    file = open("Processed_Files/5 Next "+ feature + " List.txt","r")
    tokens = file.read()
    tokens = tokens.split("\n")
    
    Dict = {}
    for i in range(0, len(tokens)-1):
        x = tokens[i].split()
        key = x[0]
        Dict.setdefault(key,[])
        for j in x[1:]:
            Dict[key].append(j)
            
    return Dict
