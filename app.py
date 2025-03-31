from flask import Flask, render_template, jsonify, request

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

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
