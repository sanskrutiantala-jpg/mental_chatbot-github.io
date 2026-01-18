from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_response(msg):
    try:
        db = mysql.connector.connect(host="localhost", user="root", password="@12345", database="college_event")
        cursor = db.cursor()
        # % ke liye double %% use karein Python mein
        query = "SELECT response FROM admin_knowledge WHERE %s LIKE CONCAT('%%', trigger_word, '%%')"
        cursor.execute(query, (msg,)) # Yahan brackets (msg,) sahi se check karein
        data = cursor.fetchone()
        cursor.close()
        db.close()
        return data[0] if data else "I am here to listen. Tell me more."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    reply = get_response(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)