from flask import Flask, request, jsonify,render_template, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
contacts = db.contacts


@app.route('/')
def index():
    # Fetch all contacts from the database
    all_contacts = list(contacts.find({}, {"_id": 0}))
    # Render the HTML template with the contacts data
    return render_template('index.html', contacts=all_contacts)

@app.route('/add', methods=['POST'])
def add_contact():
    contact = {
        "name": request.form.get("name"),
        "phone": request.form.get("phone")
    }
    contacts.insert_one(contact)
    return redirect("/")

@app.route('/contacts', methods=['GET'])
def get_contacts():
    all_contacts = list(contacts.find({}, {"_id": 0}))
    return jsonify(all_contacts)

@app.route('/delete', methods=['POST'])
def delete_contact():
    contact_name = request.form.get("name")
    contacts.delete_one({"name": contact_name})
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

