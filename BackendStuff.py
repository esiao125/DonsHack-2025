#pip install sentence_transformers
#pip install torch
#(I don't remember if this one is required) pip install hf_xet
#from transformers import BertTokenizer, BertModel
from sentence_transformers import SentenceTransformer
import numpy as np

import DBSCAN
from DBSCAN import DBScan

model = SentenceTransformer('all-MiniLM-L6-v2')
db = DBScan(3, 0.37)


#FOR TESTING
thingy = 0

if not thingy:
    with open("TestReports.txt", 'r') as f:
        i = 1
        for line in f:
            print("\n----------\nINPUT:", i, "\n----------\n")
            embedding = model.encode(line)
            embedding /= np.linalg.norm(embedding)

            print(np.shape(embedding), ":\n", embedding)

            db.add(embedding)

            i += 1


    print("--------------------------------------------------------")
    db.save()
    print(db.mat)
    print(db.numClusters)
    print("--------------------------------------------------------")
    print(db.labels)

else:
    db.load()
    print(db.numClusters)
    print("--------------------------------------------------------")

    for i in range(len(db.mat)):
        for j in range(i + 1, len(db.mat)):
            print(f"{i + 1} ({db.labels[i]}) : {j + 1} ({db.labels[j]}) = {DBSCAN.cos_distance(db.mat[i], db.mat[j])}")
