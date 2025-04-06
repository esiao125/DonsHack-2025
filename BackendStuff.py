from sentence_transformers import SentenceTransformer
import numpy as np
import DBSCAN
from DBSCAN import DBScan

model = SentenceTransformer('all-MiniLM-L6-v2')
db = DBScan(3, 0.38)

thing_to_do = 0

if thing_to_do == 0:
    with open("Log.txt", 'r') as f:
        for line in f:
            if line == "":
                continue

            embedding = model.encode(line)
            embedding /= np.linalg.norm(embedding)

            db.add(embedding)

        db.save()

else:
    db.load()

    print(db.labels)
    print(db.isCore)
    print("--------------------------------------------------------")

    for i in range(len(db.mat)):
        for j in range(i + 1, len(db.mat)):
            print(f"{i + 1} ({db.labels[i]}) : {j + 1} ({db.labels[j]}) = {DBSCAN.cos_distance(db.mat[i], db.mat[j])}")
