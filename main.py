import Processing as process
import Evaluation as evaluation
import Lex_C as lexc
import time

#process.store_tokens()
#process.token_ID()
#process.write_actual_clusters()
#process.Vocab_UrduPhone()
#process.UrduPhone_ID()
#process.Prev5("WordID")
#process.Next5("WordID")
#
#process.Prev5("UrduID")
#process.Next5("UrduID")


'''
Gold standard clusters
'''
gold = process.get_actual_clusters()

'''
Previous and Next based on WordID
'''
prev_dict = process.get_prev("WordID")
next_dict = process.get_next("WordID")

'''
Previous and Next based on UrduID
'''
#prev_dict = process.get_prev("UrduID")
#next_dict = process.get_next("UrduID")

'''
Making Intial Clusters based on UrduPhone
'''
words = list(prev_dict.keys())
urdu_dict = process.get_Urduphone_ID()


initial_clusters = {}

for i in urdu_dict:
    try:
        initial_clusters[urdu_dict[i]].append(i)
    except:
        key = urdu_dict[i]
        initial_clusters.setdefault(key, [])
        initial_clusters[urdu_dict[i]].append(i)

ic = {}
x = 0
for i in initial_clusters:
    ic.setdefault(x,[])
    ic[x] = initial_clusters[i]
    x = x+1
    
features = "URDUPHONE_EDITDISTANCE_WORDID"
weights = [1,1,1,1]

st= time.time()
sd = lexc.LexC()

clusters = sd.make_clusters(ic,2,0.4,features,weights,prev_dict,next_dict)

es = evaluation.Evaluation()
tp,tr,f = es.evaluate(gold,clusters)
print(tp)
print(tr)
print(f)

filename = features + str(weights[0]) + "_" + str(weights[1]) + "_" + str(weights[2]) + "_" + str(weights[3])
file = open("Result/" + filename + "Evaluation_Results.txt","w")
file.write("Precision:" + str(tp))
file.write("\n")
file.write("Recall:" + str(tr))
file.write("\n")
file.write("F Score:" + str(f))
print(time.time() -st)
file.close()