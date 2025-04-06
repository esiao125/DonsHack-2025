from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
import numpy as np
from DBSCAN import DBScan

model = SentenceTransformer('all-MiniLM-L6-v2')
db = DBScan(3, 0.38)

def add(location, issue):
    line = "This issue is happening at " + location + ". " + issue

    with open("Log.txt", 'a') as f:
        f.write(issue + "\n")

    embedding = model.encode(line)
    embedding /= np.linalg.norm(embedding)

    db.add(embedding)

    db.save()


def get_ranking():
    issues = []

    with open("Log.txt", 'r') as f:
        for line in f:
            issues.append(line.strip())

    rankings = []

    for i in db.labels:
        if i == -1:
            continue

        if i > len(rankings):
            diff = i - len(rankings)
            rankings += [0] * diff

        rankings[i - 1] += 1

    print(f"Rankings: {rankings}")

    # val = popularity
    # val_idx = cluster label
    top = 0
    top_idx = 0

    mid = 0
    mid_idx = 0

    low = 0
    low_idx = 0

    for i in range(len(rankings)):
        if rankings[i] > top:
            low = mid
            low_idx = mid_idx

            mid = top
            mid_idx = top_idx

            top = rankings[i]
            top_idx = i

        elif rankings[i] > mid:
            low = mid
            low_idx = mid_idx

            mid = rankings[i]
            mid_idx = i

        elif rankings[i] > low:
            low = rankings[i]
            low_idx = i

    if mid_idx == top_idx:
        mid = -1
        mid_idx = -1

        low = -1
        low_idx = -1

    elif low_idx == mid_idx:
        low = -1
        low_idx = -1

    print(f"Top: {top}, {top_idx}\nMid: {mid}, {mid_idx}\nLow: {low}, {low_idx}")

    #find representatives
    found_a = False
    found_b = False
    found_c = False

    a = ("NONE", -1)
    b = ("NONE", -1)
    c = ("NONE", -1)

    for i in range(len(issues)):
        print(f"Searching {i}: isCore = {db.isCore[i]}")
        if found_a and found_b and found_c:
            print("BROKE")
            break

        if not found_a and db.labels[i] == top_idx + 1 and db.isCore[i]:
            found_a = True
            a = (issues[i], str(top))
            print("FOUND A")

        elif not found_b and db.labels[i] == mid_idx + 1 and db.isCore[i]:
            found_b = True
            b = (issues[i], str(mid))
            print("FOUND B")

        elif not found_c and db.labels[i] == low_idx + 1 and db.isCore[i]:
            found_c = True
            c = (issues[i], str(low))
            print("FOUND C")

    return [a, b, c]


app = Flask(__name__)
CORS(app)


@app.route('/submit', methods=['POST'])
def submit():
    print("PYTHON SUBMIT")
    location = request.form.get('location')
    issue = request.form.get('issue').replace("\n", "").replace("\r", "")

    print(f"Location: {location}\nIssue: {issue}")

    add(location, issue)

    message = {"message": "Added!"}
    return jsonify(message), 200


@app.route('/view', methods=['GET'])
def view():
    print("Doing View")

    print(f"--------------------\n{db.labels}\n--------------------")

    rankings = get_ranking()

    #rankings = [("a", 1), ("b", 2), ("c", 3)]

    #get top 3 (representative, cardinality)
    message = {"top_message": rankings[0][0],
               "top_ranking": rankings[0][1],
               "mid_message": rankings[1][0],
               "mid_ranking": rankings[1][1],
               "low_message": rankings[2][0],
               "low_ranking": rankings[2][1]}

    print(jsonify(message))

    return jsonify(message), 200



if __name__ == "__main__":
    db.load()

    app.run(debug=True)