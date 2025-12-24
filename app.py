from flask import Flask, render_template, request, jsonify
from datetime import datetime
import database  # Ensure database.py is in the same folder
import model_logic

app = Flask(__name__)

# Initialize DB on startup
database.init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history_page():
    return render_template('history.html')

# Endpoint to handle new analysis and saving
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    username = data.get('username')
    text = data.get('text')
    
    if not username or not text:
        return jsonify({"error": "Missing data"}), 400

    analysis = model_logic.analyze_review(text)
    
    record = {
        "username": username,
        "text": text,
        "entities": analysis['entities'],
        "keywords": analysis['keywords'],
        "score": analysis['score'],
        "label": analysis['label'],
        "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p")
    }
    
    # Save to SQLite
    database.save_review(record)
    return jsonify(analysis)

# FIXED: Ensure this route matches what the frontend calls
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = database.fetch_all_reviews()
    return jsonify(reviews)

# Route for deletion
@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    success = database.delete_review_by_id(review_id)
    if success:
        return jsonify({"message": "Deleted"}), 200
    return jsonify({"error": "Failed"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)