from flask import Flask, render_template, jsonify, request
import requests
from requests.auth import HTTPBasicAuth

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

# Jenkins API Integration
JENKINS_URL = "http://your-jenkins-server-url"
JENKINS_API_TOKEN = "your-api-token"
JENKINS_USER = "your-jenkins-username"

def get_jenkins_jobs():
    url = f"{JENKINS_URL}/api/json"
    response = requests.get(url, auth=(JENKINS_USER, JENKINS_API_TOKEN))
    if response.status_code == 200:
        jobs = response.json().get('jobs', [])
        return [job['name'] for job in jobs]
    return []

# Jira API Integration
JIRA_URL = "https://your-jira-instance.atlassian.net"
JIRA_EMAIL = "your-email"
JIRA_API_TOKEN = "your-jira-api-token"

def get_jira_projects():
    url = f"{JIRA_URL}/rest/api/3/project"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        projects = response.json()
        return [project['name'] for project in projects]
    return []

# Bitbucket API Integration
BITBUCKET_URL = "https://api.bitbucket.org/2.0"
BITBUCKET_USER = "your-bitbucket-username"
BITBUCKET_APP_PASSWORD = "your-app-password"

def get_bitbucket_repositories():
    url = f"{BITBUCKET_URL}/repositories/{BITBUCKET_USER}"
    response = requests.get(url, auth=(BITBUCKET_USER, BITBUCKET_APP_PASSWORD))
    if response.status_code == 200:
        repos = response.json().get('values', [])
        return [repo['name'] for repo in repos]
    return []

# Confluence API Integration
CONFLUENCE_URL = "https://your-confluence-instance.atlassian.net/wiki"
CONFLUENCE_EMAIL = "your-email"
CONFLUENCE_API_TOKEN = "your-confluence-api-token"

def get_confluence_pages(space_key):
    url = f"{CONFLUENCE_URL}/rest/api/content"
    params = {"spaceKey": space_key, "limit": 50}
    auth = HTTPBasicAuth(CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)
    response = requests.get(url, auth=auth, params=params)
    if response.status_code == 200:
        pages = response.json().get('results', [])
        return [page['title'] for page in pages]
    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message'].lower()
    bot_response = generate_bot_response(user_message)
    return jsonify({'response': bot_response})

def generate_bot_response(message):
    if "jenkins" in message:
        if "list jobs" in message:
            jobs = get_jenkins_jobs()
            return f"Here are the Jenkins jobs: {', '.join(jobs)}" if jobs else "No Jenkins jobs found."

    elif "jira" in message:
        if "projects" in message:
            projects = get_jira_projects()
            return f"Here are the Jira projects: {', '.join(projects)}" if projects else "No Jira projects found."

    elif "bitbucket" in message:
        if "repositories" in message:
            repos = get_bitbucket_repositories()
            return f"Here are your Bitbucket repositories: {', '.join(repos)}" if repos else "No Bitbucket repositories found."

    elif "confluence" in message:
        if "pages" in message:
            pages = get_confluence_pages("SPACE_KEY")  # replace with actual space key
            return f"Here are the Confluence pages: {', '.join(pages)}" if pages else "No Confluence pages found."

    return "I'm sorry, I couldn't understand your request. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
