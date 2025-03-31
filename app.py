import os
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat_history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for storing chat history
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500))
    bot_response = db.Column(db.String(500))

    def __repr__(self):
        return f"ChatHistory('{self.user_message}', '{self.bot_response}')"

# DevOps tool options
tool_options = {
    'jenkins': {
        'options': ['Build Job', 'Pipeline', 'Plugins'],
        'Build Job': ['Create New Job', 'List All Jobs', 'Configure Job'],
        'Pipeline': ['Create Pipeline', 'View Pipeline', 'Delete Pipeline'],
        'Plugins': ['Install Plugin', 'List Installed Plugins', 'Update Plugin']
    },
    'bitbucket': {
        'options': ['Repositories', 'Pull Requests', 'Branches'],
        'Repositories': ['Create Repo', 'Clone Repo', 'List Repositories'],
        'Pull Requests': ['Create PR', 'Merge PR', 'View PRs'],
        'Branches': ['Create Branch', 'Delete Branch', 'View Branches']
    },
    'jira': {
        'options': ['Issues', 'Boards', 'Projects'],
        'Issues': ['Create Issue', 'View Issues', 'Assign Issues'],
        'Boards': ['Create Board', 'View Boards', 'Manage Boards'],
        'Projects': ['Create Project', 'View Projects', 'Manage Projects']
    },
    'confluence': {
        'options': ['Spaces', 'Pages', 'Templates'],
        'Spaces': ['Create Space', 'View Spaces', 'Manage Spaces'],
        'Pages': ['Create Page', 'Edit Page', 'View Pages'],
        'Templates': ['Create Template', 'List Templates', 'Use Template']
    }
}

# Route to render the chatbot interface
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to handle tool selection and provide tool-specific options
@app.route('/get_options', methods=['POST'])
def get_options():
    tool = request.json.get('tool')
    if tool in tool_options:
        return jsonify({'options': tool_options[tool]['options']})
    else:
        return jsonify({'options': []})

# API endpoint to get sub-options for a specific choice
@app.route('/get_sub_options', methods=['POST'])
def get_sub_options():
    tool = request.json.get('tool')
    choice = request.json.get('choice')
    if tool in tool_options and choice in tool_options[tool]:
        return jsonify({'sub_options': tool_options[tool][choice]})
    else:
        return jsonify({'sub_options': []})

# API endpoint to save chat history
@app.route('/save_chat', methods=['POST'])
def save_chat():
    user_message = request.json.get('user_message')
    bot_response = request.json.get('bot_response')
    new_chat = ChatHistory(user_message=user_message, bot_response=bot_response)
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({"status": "success"})

# API endpoint to fetch chat history
@app.route('/chat_history', methods=['GET'])
def chat_history():
    history = ChatHistory.query.all()
    chat_data = [{"user": chat.user_message, "bot": chat.bot_response} for chat in history]
    return jsonify({"history": chat_data})

# Function to simulate bot response (e.g., connect to APIs like Jenkins, Jira, etc.)
def generate_bot_response(message):
    # Simulate bot response based on message (can be replaced with actual API calls)
    return f"Bot response to: {message}"

# Endpoint to handle messages sent to the chatbot
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    bot_response = generate_bot_response(user_message)
    save_chat(user_message, bot_response)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    db.create_all()  # Creates the database file
    app.run(debug=True)
