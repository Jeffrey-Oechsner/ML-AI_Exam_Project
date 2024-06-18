from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['EksamensProjekt_DB']
collection = db['climate_risk_assessments_2023']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert():
    data = request.json
    collection.insert_one(data)
    return jsonify(message="Document Inserted"), 201

@app.route('/retrieve', methods=['GET'])
def retrieve():
    print("Retrieve function called")
    documents = list(collection.find().limit(10))
    print("Documents retrieved:", documents)
    for doc in documents:
        doc['_id'] = str(doc['_id'])
    return jsonify(documents), 200

@app.route('/update', methods=['POST'])
def update():
    query = request.json.get('query')
    update = request.json.get('update')
    collection.update_one(query, {"$set": update})
    return jsonify(message="Document Updated"), 200

@app.route('/delete', methods=['POST'])
def delete():
    query = request.json
    collection.delete_one(query)
    return jsonify(message="Document Deleted"), 200

@app.route('/aggregate', methods=['GET'])
def aggregate():
    pipeline = [
        {"$group": {"_id": "$country", "totalPopulation": {"$sum": "$population"}}}
    ]
    result = list(collection.aggregate(pipeline))
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
