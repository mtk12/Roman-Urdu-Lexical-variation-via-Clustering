class UrduPhone:
     
    def clean(self,word):
        e = word[0]
        j = len(word)
        for i in range(1,len(word)):
            
            if word[i]=='A' or word[i]=='I' or word[i]=='O' or word[i]=='U'  or word[i]=='E':
                continue
            if i+1 < j and word[i] == word[i+1]:
                continue
            e = e + word[i]
        
        return e
            
    
    def urduphone(self, word):
        word = word.upper()
        encoding = ""
        x = self.clean(word)
        x = x.replace("_", "")
        substring = self.subString(x[1:],len(x)-1)
        
        if x != "" :
            encoding += "|" + x[0]
            
            dictionary = {"BH" : 20, "PH" : 21,"TH" : 22, "JH" : 23, "DH" : 24, "RH" : 25, "GH" : 26, "ZH" : 16, "CH" : 5, "KH" : 6, "SH" : 1}
            dictionary1 = {"C" : 1, "S" : 1 , "T" : 2, "Z" : 3, "X" : 3, "J" : 4, "K" : 7, "Q" : 7, "D" : 8, "B" : 9, "P" : 10, "N" : 11, "M" : 12, "G" : 13, "R" : 14, "F" : 15, "L" : 17, "W" : 18, "H" : 19, "Y" : 20, "AEIOUH":"."}
            for char in substring:
                for key in dictionary.keys():
                    if char == key:
                        code = dictionary[key]
                        if code != encoding[-1]:
                            encoding += "|" + str(code)
                            x = x.replace(char,"")
                            
            for char in x[1:]:
                for key in dictionary1.keys():
                    if char == key:
                        code = dictionary1[key]
                        if code != encoding[-1]:
                            encoding += "|" + str(code)
                            
            encoding = encoding.replace(".", "")
            count = 0
            for i in encoding:
                if(i == '|'):
                    count += 1
            
            for i in range(0,6 - count):
                encoding += "|0"
            
            code = ""
            encoding = encoding.split("|")
            count = 0
            for i in encoding:
                if count == 7:
                    break
                else:
                    code = code + "|" + i
                count += 1
            code = code[1:]
        else:
             code = "|_|0|0|0|0|0"
        
        return code
    
    def subString(self, word, n):
        bigram_substr = []
        for l in range(0,n-1): 
            bigram_substr.append(word[l] + word[l+1])
        
        return bigram_substr