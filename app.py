from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = 'chat_history.db'

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

# Chat history route
@app.route('/chat_history', methods=['GET'])
def get_chat_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response FROM chats ORDER BY id DESC LIMIT 10")
    chats = cursor.fetchall()
    conn.close()

    # Format history for frontend
    history = [{"user": c[0], "bot": c[1]} for c in chats]
    return jsonify({"history": history})

# Main route to render the chat window
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to get tool options
@app.route('/get_options', methods=['POST'])
def get_options():
    tool = request.json.get('tool')
    if tool in tool_options:
        return jsonify({'options': tool_options[tool]['options']})
    return jsonify({'options': []})

# API endpoint to get sub-options
@app.route('/get_sub_options', methods=['POST'])
def get_sub_options():
    tool = request.json.get('tool')
    choice = request.json.get('choice')
    if tool in tool_options and choice in tool_options[tool]:
        return jsonify({'sub_options': tool_options[tool][choice]})
    return jsonify({'sub_options': []})

# Start the app
if __name__ == '__main__':
    app.run(debug=True)
