from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["notesdb"]
notes_collection = db["notes"]


@app.route("/")
def home():
    return "Notes API running with MongoDB 🚀"


# Get all notes
@app.route("/notes", methods=["GET"])
def get_notes():

    notes = []

    for note in notes_collection.find():
        notes.append({
            "id": str(note["_id"]),
            "title": note["title"],
            "content": note["content"]
        })

    return jsonify(notes)


# Add new note
@app.route("/notes", methods=["POST"])
def add_note():

    data = request.json

    note = {
        "title": data["title"],
        "content": data["content"]
    }

    result = notes_collection.insert_one(note)

    return jsonify({
        "id": str(result.inserted_id),
        "title": note["title"],
        "content": note["content"]
    })


# Delete note
@app.route("/notes/<id>", methods=["DELETE"])
def delete_note(id):

    notes_collection.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({"message": "Deleted"})


if __name__ == "__main__":
    app.run(debug=True)