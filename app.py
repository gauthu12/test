import sqlite3
from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Tool options and sub-options
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

# Database setup
def init_db():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_message TEXT, bot_response TEXT)''')
    conn.commit()
    conn.close()

# Route to render the chatbot interface
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to handle tool selection and provide tool-specific options
@app.route('/get_options', methods=['POST'])
def get_options():
    tool = request.json.get('tool')
    if tool in tool_options:
        return jsonify({
            'options': tool_options[tool]['options']
        })
    else:
        return jsonify({'options': []})

# API endpoint to get sub-options for a specific choice
@app.route('/get_sub_options', methods=['POST'])
def get_sub_options():
    tool = request.json.get('tool')
    choice = request.json.get('choice')
    if tool in tool_options and choice in tool_options[tool]:
        return jsonify({
            'sub_options': tool_options[tool][choice]
        })
    else:
        return jsonify({'sub_options': []})

# API endpoint for chatbot to handle user messages and fetch bot response
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    bot_response = generate_bot_response(user_message)
    store_chat_history(user_message, bot_response)
    return jsonify({'response': bot_response})

# Function to generate a bot response based on the user input
def generate_bot_response(user_message):
    # Here, you can implement your chatbot logic based on user input.
    # For now, we'll simply return a greeting message or a message based on the tool selected.
    user_message = user_message.lower()
    
    if "hi" in user_message or "hello" in user_message:
        return "Hello! How can I assist you today? Choose a tool: Jenkins, Jira, Bitbucket, or Confluence."
    elif "jenkins" in user_message:
        return "You have selected Jenkins. Please choose an option: Build Job, Pipeline, or Plugins."
    elif "jira" in user_message:
        return "You have selected Jira. Please choose an option: Issues, Boards, or Projects."
    elif "bitbucket" in user_message:
        return "You have selected Bitbucket. Please choose an option: Repositories, Pull Requests, or Branches."
    elif "confluence" in user_message:
        return "You have selected Confluence. Please choose an option: Spaces, Pages, or Templates."
    else:
        return "Sorry, I didn't understand that. Please select a valid tool: Jenkins, Jira, Bitbucket, or Confluence."

# Function to store chat history in the database
def store_chat_history(user_message, bot_response):
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (user_message, bot_response) VALUES (?, ?)", 
              (user_message, bot_response))
    conn.commit()
    conn.close()

# API endpoint to retrieve chat history
@app.route('/chat_history', methods=['GET'])
def chat_history():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    c.execute("SELECT user_message, bot_response FROM chat_history ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({'user': row[0], 'bot': row[1]})
    
    return jsonify({'history': history})

# Main function to run the app
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
