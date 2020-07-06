import UrduPhone as UP
from similarity.levenshtein import Levenshtein
from similarity.longest_common_subsequence import LongestCommonSubsequence

class Similarity:
    
    def calculate_distance(self, word1, word2, features, weights, prev_dict, next_dict):
        if(features == "URDUPHONE_EDITDISTANCE_WORDID"):
            phonetic_sim = self.phonetic_similarity(word1, word2)
            string_sim = self.string_similarity(word1, word2)
            context_sim_prev, context_sim_next = self.contexual_similarity(word1, word2, prev_dict, next_dict)
#            print(phonetic_sim)
#            print(string_sim)
#            print(context_sim_prev)
#            print(context_sim_next)
#            
            distance = phonetic_sim * weights[0] + string_sim * weights[1] + context_sim_prev * weights[2] + context_sim_next * weights[3]
            distance = distance / (weights[0] + weights[1] + weights[2] + weights[3])
            return distance
        
    def LCS(self, X, Y, m, n):

        T = [[0 for x in range(n + 1)] for y in range(m + 1)]
    
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if X[i - 1] == Y[j - 1]:
                    T[i][j] = T[i - 1][j - 1] + 1
                else:
                    T[i][j] = max(T[i - 1][j], T[i][j - 1])
    
        return T[m][n]

        
    def editDistance(self, w1, w2, len1, len2): 
        m = len1
        n = len2
        d = []           
        for i in range(m+1):
            d.append([i])        
        del d[0][0]    
        for j in range(n+1):
            d[0].append(j)       
        for j in range(1,n+1):
            for i in range(1,m+1):
                if w1[i-1] == w2[j-1]:
                    d[i].insert(j,d[i-1][j-1])           
                else:
                    minimum = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+2)         
                    d[i].insert(j, minimum)
        ldist = d[-1][-1]
        #ratio = (lensum - ldist)/lensum
        return ldist
    
    def getContextSim(self, list1, list2):
        dist = 0
        for i in list1:
            p = 0
            if i in list2:
                p = (len(list1)+1) - min(list1.index(i),list2.index(i)) - 1
            dist = dist + p
            
        s = 0
        for i in range(0,len(list1)+1):
            s = s + i
            
        return dist/s
    
    def phonetic_similarity(self, word1, word2):
        u = UP.UrduPhone()
        encoding1 = u.urduphone(word1)
        encoding2 = u.urduphone(word2)
        
        sigma = 0
        if encoding1 == encoding2:
            sigma = 1
        else:
            sigma = 0
            
        return sigma
    
    def string_similarity(self, word1, word2):
        
        levenshtein = Levenshtein()
        lcs = LongestCommonSubsequence()

        ed = levenshtein.distance(word1, word2)
        if(ed == 0):
            sigma = (lcs.length(word1, word2)) / (
                    min(len(word1),len(word2)) * 1)
        else:
            sigma = (lcs.length(word1, word2)) / (
                    min(len(word1),len(word2)) * ed)
        return sigma
    
    def contexual_similarity(self, word1, word2, prev_dict, next_dict):
        prev1 = prev_dict[word1]
        prev2 = prev_dict[word2]
        
        next1 = next_dict[word1]
        next2 = next_dict[word2]

        a = len(prev1)
        b = len(prev2)
        c = len(next1)
        d = len(next2)
        
        if ((len(prev1) == 0) and (len(prev2) == 0)) or ((len(next1) == 0) and (len(next2) == 0)):
            prevWordDist = 0
            nextWordDist = 0
            return prevWordDist, nextWordDist
        
        if (a >= b):
            prevWordDist = self.getContextSim(prev1,prev2)
        else:
            prevWordDist = self.getContextSim(prev2,prev1)
        if (c >= d):
            nextWordDist = self.getContextSim(next1,next2)
        else:
            nextWordDist = self.getContextSim(next2,next1)
        
        return prevWordDist, nextWordDist
        
    