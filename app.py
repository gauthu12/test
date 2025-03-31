from flask import Flask, render_template, jsonify, request
import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import os

app = Flask(__name__)

# ===========================
# API Credentials (Modify These)
# ===========================

# JIRA Credentials
JIRA_URL = "https://your-jira-url.atlassian.net"
JIRA_USER = "your-jira-email"
JIRA_TOKEN = "your-jira-api-token"

# Bitbucket Credentials
BITBUCKET_URL = "https://api.bitbucket.org/2.0"
BITBUCKET_USER = "your-bitbucket-username"
BITBUCKET_TOKEN = "your-bitbucket-api-token"

# Jenkins Credentials
JENKINS_URL = "http://your-jenkins-url"
JENKINS_USER = "your-jenkins-username"
JENKINS_TOKEN = "your-jenkins-api-token"

# Confluence Credentials
CONFLUENCE_URL = "https://your-confluence-url"
CONFLUENCE_USER = "your-confluence-username"
CONFLUENCE_TOKEN = "your-confluence-api-token"

# ===========================
# Database Setup (SQLite)
# ===========================

DB_PATH = "chat_history.db"

if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
    """)
    conn.commit()
    conn.close()

# ===========================
# Routes
# ===========================

@app.route('/')
def index():
    return render_template('index.html')

# ===========================
# JIRA API Endpoints
# ===========================

# Get Jira Projects
@app.route('/jira/projects', methods=['GET'])
def get_jira_projects():
    url = f"{JIRA_URL}/rest/api/3/project"
    response = requests.get(url, auth=HTTPBasicAuth(JIRA_USER, JIRA_TOKEN))
    if response.status_code == 200:
        projects = [{"id": p["id"], "name": p["name"]} for p in response.json()]
        return jsonify({"projects": projects})
    return jsonify({"error": "Failed to fetch Jira projects"}), 500

# Create a Jira Issue
@app.route('/jira/create_issue', methods=['POST'])
def create_jira_issue():
    data = request.json
    issue_data = {
        "fields": {
            "project": {"key": data["project_key"]},
            "summary": data["summary"],
            "description": data["description"],
            "issuetype": {"name": "Task"}
        }
    }
    url = f"{JIRA_URL}/rest/api/3/issue"
    response = requests.post(url, json=issue_data, auth=HTTPBasicAuth(JIRA_USER, JIRA_TOKEN))
    if response.status_code == 201:
        return jsonify({"message": "Jira issue created successfully"})
    return jsonify({"error": "Failed to create Jira issue"}), 500

# ===========================
# BITBUCKET API Endpoints
# ===========================

# Get Bitbucket Repositories
@app.route('/bitbucket/repos', methods=['GET'])
def get_bitbucket_repos():
    url = f"{BITBUCKET_URL}/repositories/{BITBUCKET_USER}"
    response = requests.get(url, auth=HTTPBasicAuth(BITBUCKET_USER, BITBUCKET_TOKEN))
    if response.status_code == 200:
        repos = [repo["name"] for repo in response.json().get("values", [])]
        return jsonify({"repositories": repos})
    return jsonify({"error": "Failed to fetch Bitbucket repositories"}), 500

# Create Bitbucket Branch
@app.route('/bitbucket/create_branch', methods=['POST'])
def create_bitbucket_branch():
    data = request.json
    repo_slug = data["repo_slug"]
    branch_name = data["branch_name"]
    base_branch = data["base_branch"]

    url = f"{BITBUCKET_URL}/repositories/{BITBUCKET_USER}/{repo_slug}/refs/branches"
    payload = {
        "name": branch_name,
        "target": {"hash": base_branch}
    }

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(BITBUCKET_USER, BITBUCKET_TOKEN))
    if response.status_code == 201:
        return jsonify({"message": "Branch created successfully"})
    return jsonify({"error": "Failed to create branch"}), 500

# ===========================
# JENKINS API Endpoints
# ===========================

# Get Jenkins Jobs
@app.route('/jenkins/jobs', methods=['GET'])
def get_jenkins_jobs():
    response = requests.get(f"{JENKINS_URL}/api/json", auth=(JENKINS_USER, JENKINS_TOKEN))
    if response.status_code == 200:
        jobs = [job["name"] for job in response.json().get("jobs", [])]
        return jsonify({"jobs": jobs})
    return jsonify({"error": "Failed to fetch Jenkins jobs"}), 500

# Trigger Jenkins Build
@app.route('/jenkins/build', methods=['POST'])
def trigger_jenkins_build():
    job_name = request.json.get("job_name")
    response = requests.post(f"{JENKINS_URL}/job/{job_name}/build", auth=(JENKINS_USER, JENKINS_TOKEN))
    if response.status_code == 201:
        return jsonify({"message": f"Build triggered for {job_name}"})
    return jsonify({"error": "Failed to trigger Jenkins job"}), 500

# ===========================
# CONFLUENCE API Endpoints
# ===========================

# Get Confluence Pages
@app.route('/confluence/pages', methods=['GET'])
def get_confluence_pages():
    response = requests.get(f"{CONFLUENCE_URL}/rest/api/content", auth=HTTPBasicAuth(CONFLUENCE_USER, CONFLUENCE_TOKEN))
    if response.status_code == 200:
        pages = [page["title"] for page in response.json().get("results", [])]
        return jsonify({"pages": pages})
    return jsonify({"error": "Failed to fetch Confluence pages"}), 500

# Create Confluence Page
@app.route('/confluence/create_page', methods=['POST'])
def create_confluence_page():
    data = request.json
    title = data["title"]
    content = data["content"]

    payload = {
        "type": "page",
        "title": title,
        "space": {"key": "YOUR_SPACE_KEY"},
        "body": {"storage": {"value": content, "representation": "storage"}}
    }

    response = requests.post(
        f"{CONFLUENCE_URL}/rest/api/content",
        json=payload,
        auth=HTTPBasicAuth(CONFLUENCE_USER, CONFLUENCE_TOKEN),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code in [200, 201]:
        return jsonify({"message": "Page created successfully"})
    return jsonify({"error": "Failed to create Confluence page"}), 500

# ===========================
# Chat History Storage
# ===========================

def store_chat(user_message, bot_response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user_message, bot_response) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()
    conn.close()

@app.route('/chat_history', methods=['GET'])
def get_chat_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response FROM chats ORDER BY id DESC LIMIT 10")
    chats = cursor.fetchall()
    conn.close()
    return jsonify({"history": [{"user": c[0], "bot": c[1]} for c in chats]})

# ===========================
# Run Flask App
# ===========================

if __name__ == '__main__':
    app.run(debug=True)
