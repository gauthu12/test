from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# ---------------------- API CREDENTIALS ---------------------- #
JIRA_URL = os.getenv("JIRA_URL", "https://your-jira-instance.atlassian.net")
JIRA_USER = os.getenv("JIRA_USER", "your-email@example.com")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "your-api-token")

BITBUCKET_URL = os.getenv("BITBUCKET_URL", "https://api.bitbucket.org/2.0")
BITBUCKET_USERNAME = os.getenv("BITBUCKET_USERNAME", "your-username")
BITBUCKET_PASSWORD = os.getenv("BITBUCKET_PASSWORD", "your-password")

JENKINS_URL = os.getenv("JENKINS_URL", "http://your-jenkins-server:8080")
JENKINS_USER = os.getenv("JENKINS_USER", "your-jenkins-username")
JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN", "your-jenkins-api-token")

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL", "https://your-confluence-instance.atlassian.net/wiki")
CONFLUENCE_USER = os.getenv("CONFLUENCE_USER", "your-email@example.com")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN", "your-api-token")

# ---------------------- JENKINS INTEGRATION ---------------------- #
@app.route('/jenkins/jobs', methods=['GET'])
def get_jenkins_jobs():
    """Fetches the list of Jenkins jobs"""
    url = f"{JENKINS_URL}/api/json"
    auth = (JENKINS_USER, JENKINS_API_TOKEN)
    
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        jobs = response.json().get('jobs', [])
        return jsonify({'jobs': [job['name'] for job in jobs]})
    
    return jsonify({'error': 'Failed to fetch Jenkins jobs'}), response.status_code

@app.route('/jenkins/build', methods=['POST'])
def trigger_jenkins_build():
    """Triggers a Jenkins job"""
    job_name = request.json.get('job_name')
    if not job_name:
        return jsonify({'error': 'Job name is required'}), 400

    url = f"{JENKINS_URL}/job/{job_name}/build"
    auth = (JENKINS_USER, JENKINS_API_TOKEN)

    response = requests.post(url, auth=auth)
    if response.status_code == 201:
        return jsonify({'message': f'Jenkins job "{job_name}" triggered successfully!'})
    
    return jsonify({'error': f'Failed to trigger job "{job_name}"'}), response.status_code

# ---------------------- CONFLUENCE INTEGRATION ---------------------- #
@app.route('/confluence/pages', methods=['GET'])
def get_confluence_pages():
    """Fetches a list of Confluence pages in a given space"""
    space_key = request.args.get('space_key', 'YOUR_SPACE_KEY')
    
    url = f"{CONFLUENCE_URL}/rest/api/content"
    auth = (CONFLUENCE_USER, CONFLUENCE_API_TOKEN)
    params = {"spaceKey": space_key, "expand": "title"}

    response = requests.get(url, auth=auth, params=params)
    if response.status_code == 200:
        pages = response.json().get('results', [])
        return jsonify({'pages': [page['title'] for page in pages]})
    
    return jsonify({'error': 'Failed to fetch Confluence pages'}), response.status_code

@app.route('/confluence/create_page', methods=['POST'])
def create_confluence_page():
    """Creates a new Confluence page"""
    space_key = request.json.get('space_key', 'YOUR_SPACE_KEY')
    title = request.json.get('title', 'New Page')
    content = request.json.get('content', 'This is a test page.')

    url = f"{CONFLUENCE_URL}/rest/api/content"
    auth = (CONFLUENCE_USER, CONFLUENCE_API_TOKEN)
    headers = {"Content-Type": "application/json"}
    
    data = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }

    response = requests.post(url, auth=auth, headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        return jsonify({'message': f'Confluence page "{title}" created successfully!'})
    
    return jsonify({'error': 'Failed to create Confluence page'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)

