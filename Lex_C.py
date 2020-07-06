import Similarity as s
import numpy as np

class LexC:
    
    d = s.Similarity()
    sim_dict = {}
    
    def calculate_centroid(self, c, features, weights, prev_dict, next_dict):
        
        clusters = c
        centroid = []
        
        print("Calculating Centroids------")
        for wordi in clusters:
            r = []
            for wordj in clusters[wordi]:
                self.sim_dict.setdefault(wordj,{})
                rj = 0
                for word in clusters[wordi]:
                    di =  self.d.calculate_distance(wordj, word, features, weights, prev_dict, next_dict)
                    self.sim_dict[wordj][word] = di
                    rj = rj + di
                r.append(rj)
            m = np.argmax(r)
            centroid.append(clusters[wordi][m])
        print("Centroids Calculated------")
        return centroid
    
    def make_clusters(self,initial_clusters, max_iteration, threshold, features, weights, prev_dict, next_dict):
        
        words = list(prev_dict.keys())
        c = initial_clusters
        
        for it in range(max_iteration):
            print("Iteration Number:" + str(it) + "-----")
            centroid = self.calculate_centroid(c, features, weights, prev_dict, next_dict)
            cluster = {}
            for i in centroid:
                cluster.setdefault(i,[])
            
            print("Making Clusters----")
            for w in words:
                print(w)
                closest = 0
                maxSim = 0
                x = list(self.sim_dict[w].keys())
                inter = list(set(x).intersection(set(centroid)))
                for ci in inter:
                    try:
                        if(w[0]==ci[0] and w[1]==ci[1]):
                            if self.sim_dict[w][ci] > threshold and self.sim_dict[w][ci] > maxSim:
                                maxSim = self.sim_dict[w][ci]
                                closest = ci
                    except:
                        if(w[0]==ci[0]):
                            if self.sim_dict[w][ci] > threshold and self.sim_dict[w][ci] > maxSim:
                                maxSim = self.sim_dict[w][ci]
                                closest = ci
                                
                if closest != 0:
                    cluster[closest].append(w)
                else:
                    key = w
                    cluster.setdefault(key,[])
                    centroid.append(key)
                
            clusters = {}
            x = 0
            for i in cluster:
                clusters[x] = cluster[i]
                if(i not in clusters[x]):
                    clusters[x].append(i)
                x += 1
            c = clusters
        
        print("Writing CLusters in file-----")
        self.write_results(clusters,features,weights)
                
        return clusters
    
    def write_results(self,clusters,features,weights):
        filename = features + str(weights[0]) + "_" + str(weights[1]) + "_" + str(weights[2]) + "_" + str(weights[3])
        file = open("Result/" + filename + " Cluster.txt","w")
        for i in clusters:
            file.write(str(i)+" ")
            for j in clusters[i]:
                file.write(j+",")
            file.write("\n")