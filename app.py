<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Chatbot</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/js/all.min.js"></script>
    <style>
        /* Styling for chatbot UI */
        #chat-window {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 300px;
            height: 400px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            display: none;
            z-index: 9999;
            overflow-y: auto;
            padding: 10px;
        }

        #chat-header {
            background-color: #007bff;
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: bold;
            cursor: pointer;
            border-radius: 10px 10px 0 0;
        }

        .chat-btn {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px;
            margin: 5px 0;
            cursor: pointer;
            border-radius: 5px;
            width: 100%;
            text-align: left;
            transition: 0.3s;
        }

        .chat-btn:hover {
            background-color: #0056b3;
        }

        .show-chat-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 24px;
            cursor: pointer;
            z-index: 9999;
        }
    </style>
</head>
<body>

<!-- Chat Toggle Button -->
<button class="show-chat-btn" onclick="toggleChatWindow()">
    <i class="fas fa-comment"></i>
</button>

<!-- Chat Window -->
<div id="chat-window">
    <div id="chat-header" onclick="toggleChatWindow()">DevOps Chatbot</div>
    <div id="chat-body">
        <p>Hello! Choose a DevOps tool:</p>
        <div id="chat-options">
            <button class="chat-btn" onclick="showOptions('jenkins')">Jenkins</button>
            <button class="chat-btn" onclick="showOptions('jira')">Jira</button>
            <button class="chat-btn" onclick="showOptions('bitbucket')">Bitbucket</button>
            <button class="chat-btn" onclick="showOptions('confluence')">Confluence</button>
        </div>
    </div>
</div>

<script>
    const menuStructure = {
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
    };

    let chatHistory = [];

    function toggleChatWindow() {
        let chatWindow = document.getElementById('chat-window');
        chatWindow.style.display = chatWindow.style.display === 'block' ? 'none' : 'block';
    }

    function showOptions(tool) {
        chatHistory.push(tool);
        let options = menuStructure[tool]['options'];
        updateChatButtons(options, tool);
    }

    function showSubOptions(tool, category) {
        chatHistory.push(category);
        let options = menuStructure[tool][category];
        updateChatButtons(options, tool, category);
    }

    function updateChatButtons(options, tool, category = null) {
        let chatOptions = document.getElementById('chat-options');
        chatOptions.innerHTML = ''; // Clear previous options

        if (category) {
            chatOptions.innerHTML += `<button class="chat-btn" onclick="showOptions('${tool}')">⬅ Back</button>`;
        } else if (chatHistory.length > 1) {
            chatOptions.innerHTML += `<button class="chat-btn" onclick="resetChat()">🏠 Home</button>`;
        }

        options.forEach(option => {
            let onClickAction = category ? `executeAction('${tool}', '${category}', '${option}')` : `showSubOptions('${tool}', '${option}')`;
            chatOptions.innerHTML += `<button class="chat-btn" onclick="${onClickAction}">${option}</button>`;
        });
    }

    function resetChat() {
        chatHistory = [];
        document.getElementById('chat-options').innerHTML = `
            <button class="chat-btn" onclick="showOptions('jenkins')">Jenkins</button>
            <button class="chat-btn" onclick="showOptions('jira')">Jira</button>
            <button class="chat-btn" onclick="showOptions('bitbucket')">Bitbucket</button>
            <button class="chat-btn" onclick="showOptions('confluence')">Confluence</button>
        `;
    }

    function executeAction(tool, category, action) {
        let chatOptions = document.getElementById('chat-options');
        chatOptions.innerHTML = `<p>Executing: ${tool} > ${category} > ${action}</p>`;
        setTimeout(resetChat, 3000);
    }
</script>

</body>
</html>
