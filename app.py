import os
import json
import sqlite3
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace with your actual API credentials and URLs
JIRA_API_URL = 'https://your-jira-instance.atlassian.net/rest/api/3'
JIRA_API_TOKEN = 'your-jira-api-token'
JIRA_EMAIL = 'your-jira-email'
BITBUCKET_API_URL = 'https://api.bitbucket.org/2.0'
BITBUCKET_USERNAME = 'your-bitbucket-username'
BITBUCKET_APP_PASSWORD = 'your-bitbucket-app-password'
JENKINS_API_URL = 'http://your-jenkins-instance.com/api/json'
JENKINS_API_TOKEN = 'your-jenkins-api-token'
CONFLUENCE_API_URL = 'https://your-confluence-instance.atlassian.net/wiki/rest/api/content'
CONFLUENCE_API_TOKEN = 'your-confluence-api-token'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                        id INTEGER PRIMARY KEY,
                        user_message TEXT,
                        bot_response TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Function to save chat history in SQLite
def save_chat_history(user_message, bot_response):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_message, bot_response) VALUES (?, ?)", 
                   (user_message, bot_response))
    conn.commit()
    conn.close()

# Route to render the chatbot interface
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to get available options for a tool
@app.route('/get_options', methods=['POST'])
def get_options():
    tool = request.json.get('tool')
    
    # Dynamic tool options and sub-options
    if tool == 'jenkins':
        options = ['Build Job', 'Pipeline', 'Plugins']
    elif tool == 'bitbucket':
        options = ['Repositories', 'Pull Requests', 'Branches']
    elif tool == 'jira':
        options = ['Issues', 'Boards', 'Projects']
    elif tool == 'confluence':
        options = ['Spaces', 'Pages', 'Templates']
    else:
        options = []

    return jsonify({'options': options})

# API endpoint to get sub-options for a tool and choice
@app.route('/get_sub_options', methods=['POST'])
def get_sub_options():
    tool = request.json.get('tool')
    choice = request.json.get('choice')

    if tool == 'jenkins':
        if choice == 'Build Job':
            sub_options = ['Create New Job', 'List All Jobs', 'Configure Job']
        elif choice == 'Pipeline':
            sub_options = ['Create Pipeline', 'View Pipeline', 'Delete Pipeline']
        elif choice == 'Plugins':
            sub_options = ['Install Plugin', 'List Installed Plugins', 'Update Plugin']
    elif tool == 'bitbucket':
        if choice == 'Repositories':
            sub_options = ['Create Repo', 'Clone Repo', 'List Repositories']
        elif choice == 'Pull Requests':
            sub_options = ['Create PR', 'Merge PR', 'View PRs']
        elif choice == 'Branches':
            sub_options = ['Create Branch', 'Delete Branch', 'View Branches']
    elif tool == 'jira':
        if choice == 'Issues':
            sub_options = ['Create Issue', 'View Issues', 'Assign Issues']
        elif choice == 'Boards':
            sub_options = ['Create Board', 'View Boards', 'Manage Boards']
        elif choice == 'Projects':
            sub_options = ['Create Project', 'View Projects', 'Manage Projects']
    elif tool == 'confluence':
        if choice == 'Spaces':
            sub_options = ['Create Space', 'View Spaces', 'Manage Spaces']
        elif choice == 'Pages':
            sub_options = ['Create Page', 'Edit Page', 'View Pages']
        elif choice == 'Templates':
            sub_options = ['Create Template', 'List Templates', 'Use Template']
    else:
        sub_options = []

    return jsonify({'sub_options': sub_options})

# API endpoint for Jira to fetch projects
@app.route('/jira/projects', methods=['GET'])
def get_jira_projects():
    response = requests.get(
        f'{JIRA_API_URL}/project',
        auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )
    projects = response.json()
    return jsonify(projects)

# API endpoint for Bitbucket to list repositories
@app.route('/bitbucket/repositories', methods=['GET'])
def get_bitbucket_repositories():
    response = requests.get(
        f'{BITBUCKET_API_URL}/repositories/{BITBUCKET_USERNAME}',
        auth=(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD)
    )
    repos = response.json()
    return jsonify(repos)

# API endpoint for Jenkins to get job list
@app.route('/jenkins/jobs', methods=['GET'])
def get_jenkins_jobs():
    response = requests.get(
        f'{JENKINS_API_URL}/api/json',
        auth=('your-jenkins-username', JENKINS_API_TOKEN)
    )
    jobs = response.json()['jobs']
    return jsonify(jobs)

# API endpoint for Confluence to get spaces
@app.route('/confluence/spaces', methods=['GET'])
def get_confluence_spaces():
    response = requests.get(
        f'{CONFLUENCE_API_URL}/space',
        auth=('your-confluence-email', CONFLUENCE_API_TOKEN)
    )
    spaces = response.json()['results']
    return jsonify(spaces)

# API endpoint to fetch chat history
@app.route('/chat_history', methods=['GET'])
def get_chat_history():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_history ORDER BY id DESC")
    history = cursor.fetchall()
    conn.close()

    chat_history = []
    for row in history:
        chat_history.append({
            'user': row[1],
            'bot': row[2]
        })
    
    return jsonify({'history': chat_history})

# API endpoint to handle sending user messages and saving chat history
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    bot_response = "Sorry, I didn't get that."

    # Process message based on the user input (e.g., tool, options)
    if 'Jenkins' in user_message:
        bot_response = "Here are the Jenkins options: Build Job, Pipeline, Plugins."
    elif 'Jira' in user_message:
        bot_response = "Here are the Jira options: Issues, Boards, Projects."
    elif 'Bitbucket' in user_message:
        bot_response = "Here are the Bitbucket options: Repositories, Pull Requests, Branches."
    elif 'Confluence' in user_message:
        bot_response = "Here are the Confluence options: Spaces, Pages, Templates."

    # Save to chat history
    save_chat_history(user_message, bot_response)

    return jsonify({'response': bot_response})

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
