from flask import Flask, render_template, request, jsonify
from main import process_ai_response, get_chemicals, get_columns  # Import chatbot functions
from flask_cors import CORS

app = Flask(__name__, template_folder='login/templates')
CORS(app) 

@app.route('/')
def home():
    return render_template('login/chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    action = data.get('action')
    additional_data = data.get('data')

    response = process_ai_response(action, additional_data)
    return jsonify(response)

@app.route('/get_chemicals')
def chemicals():
    return jsonify(get_chemicals())

@app.route('/get_columns')
def columns():
    return jsonify(get_columns())

if __name__ == '__main__':
    app.run(debug=True)