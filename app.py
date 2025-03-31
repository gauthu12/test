from flask import Flask, render_template, jsonify, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Example API endpoints (Replace with actual credentials and URLs)
JENKINS_URL = 'http://your-jenkins-url/api/json'
JIRA_URL = 'https://your-jira-instance/rest/api/2/search'
BITBUCKET_URL = 'https://api.bitbucket.org/2.0/repositories/your-team'
CONFLUENCE_URL = 'https://your-confluence-instance/wiki/rest/api/content'

# Authentication details (replace with actual keys or tokens)
JENKINS_USER = 'your-username'
JENKINS_PASS = 'your-password'
JIRA_API_TOKEN = 'your-jira-api-token'
BITBUCKET_TOKEN = 'your-bitbucket-api-token'
CONFLUENCE_TOKEN = 'your-confluence-api-token'

def fetch_data_from_api(url, headers=None, auth=None):
    """General function to fetch data from APIs."""
    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()  # Raises exception for 4xx/5xx responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f'Error: {str(e)}'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_jenkins_jobs', methods=['GET'])
def get_jenkins_jobs():
    auth = HTTPBasicAuth(JENKINS_USER, JENKINS_PASS)
    data = fetch_data_from_api(JENKINS_URL, auth=auth)
    return jsonify(data)

@app.route('/get_jira_issues', methods=['GET'])
def get_jira_issues():
    headers = {'Authorization': f'Bearer {JIRA_API_TOKEN}'}
    data = fetch_data_from_api(JIRA_URL, headers=headers)
    return jsonify(data)

@app.route('/get_bitbucket_repos', methods=['GET'])
def get_bitbucket_repos():
    headers = {'Authorization': f'Bearer {BITBUCKET_TOKEN}'}
    data = fetch_data_from_api(BITBUCKET_URL, headers=headers)
    return jsonify(data)

@app.route('/get_confluence_pages', methods=['GET'])
def get_confluence_pages():
    headers = {'Authorization': f'Bearer {CONFLUENCE_TOKEN}'}
    data = fetch_data_from_api(CONFLUENCE_URL, headers=headers)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
