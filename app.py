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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_options', methods=['POST'])
def get_options():
    tool = request.json['tool']
    options = tool_options.get(tool, {}).get('options', [])
    return jsonify({'options': options})

@app.route('/get_sub_options', methods=['POST'])
def get_sub_options():
    tool = request.json['tool']
    option = request.json['option']
    sub_options = tool_options.get(tool, {}).get(option, [])
    return jsonify({'sub_options': sub_options})

if __name__ == '__main__':
    app.run(debug=True)
