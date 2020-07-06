class Evaluation:
    
    tp = 0
    tr = 0

    def evaluate(self,actual_clusters,clusters):
        for w in actual_clusters:  
            print(w)
            for i in clusters:
                if w in clusters[i]:
                    e = clusters[i]
                    break
            l = actual_clusters[w]
            sim = list(set(e).intersection(set(l)))
            if(len(sim)!=0):
                precision = len(sim)/len(l)
                recall = len(sim)/len(e)
                self.tp = self.tp + precision
                self.tr = self.tr + recall
                        
            recall = 0
            precision = 0
        
        avt = self.tp/len(actual_clusters)
        avr = self.tr/len(actual_clusters)
        f_measure = (2*avt*avr)/(avr + avt)
        
        return avt,avr,f_measure