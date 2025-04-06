from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/run-script", methods=["GET"])

def run_script():
    param1 = request.args.get("param1")
    param2 = request.args.get("param2")

    result = f"Thing 1: {param1}\nThing 2: {param2}"
    return jsonify(result=result)

if __name__ == "__main__":
    app.run(debug=True)

"""
Javascript Side:

window.onload = function() {
    const data = {
        param1: 'value1',
        param2: 'value2'
    };

    fetch('/run-script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)  // Send data as JSON
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.result);  // Process the output
        document.getElementById('output').innerText = data.result;
    })
    .catch(error => console.error('Error:', error));
};
"""