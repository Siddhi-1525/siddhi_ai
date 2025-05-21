import random
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string


class Chatbot:
    def __init__(self, name="ChatBot"):
        self.name = name
        self.patterns = {
            'greeting': {'patterns': ['hello', 'hi', 'hey', 'greetings', 'sup', 'howdy'], 'responses': ["Hello there! How can I help you today?", "Hi! Nice to chat with you.", "Hey! What's on your mind?"]},
            'bye': {'patterns': ['bye', 'goodbye', 'see you', 'exit', 'quit'], 'responses': ["Goodbye! Have a great day!", "See you later!", "Bye! Come back soon."]},
            'thanks': {'patterns': ['thank', 'thanks', 'appreciate'], 'responses': ["You're welcome!", "Happy to help!", "Anytime!"]},
            'name': {'patterns': ['your name', 'who are you', 'call you'], 'responses': [f"I'm {name}, your friendly chatbot.", f"My name is {name}.", f"You can call me {name}."]},
            'time': {'patterns': ['time', 'what time'], 'responses': ["The current time is {}.", "It's {} right now."]},
            'help': {'patterns': ['help', 'commands', 'features', 'what can you do', 'abilities'], 'responses': ["I can help with basic conversations. Try asking about my name or the time.", "I'm here to chat! What would you like to talk about?"]},
            'feeling': {'patterns': ['how are you', 'how do you feel', 'are you ok'], 'responses': ["I'm doing well, thanks for asking!", "I'm good! How about you?"]},
            'joke': {'patterns': ['joke', 'funny', 'make me laugh'], 'responses': ["Why don't scientists trust atoms? Because they make up everything!", "What do you call a fake noodle? An impasta!"]},
            'weather': {'patterns': ['weather', 'forecast', 'temperature'], 'responses': ["I don't have real-time weather data, but I hope it's nice where you are!"]},
            'date': {'patterns': ['date', 'what day', 'today is'], 'responses': ["Today is {}.", "The current date is {}."]},
            'facts': {'patterns': ['fact', 'tell me something', 'did you know'], 'responses': ["Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are still good to eat!", "Octopuses have three hearts, nine brains, and blue blood."]}
        }
        self.default_responses = ["I'm not sure I understand.", "Interesting! Tell me more.", "Can you try saying that differently?"]
    
    def get_response(self, user_input):
        user_input = user_input.lower()
        for intent, data in self.patterns.items():
            if any(word in user_input for word in data['patterns']):
                if intent == 'time': return data['responses'][0].format(datetime.now().strftime("%H:%M"))
                if intent == 'date': return data['responses'][0].format(datetime.now().strftime("%A, %B %d, %Y"))
                return random.choice(data['responses'])
        return random.choice(self.default_responses)

app = Flask(__name__)
chatbot = Chatbot("ChatBot")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatBot</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: sans-serif; background-color: #f0f4f8; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .app-container { background-color: #fff; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); overflow: hidden; max-width: 600px; width: 100%; height: 700px; display: flex; flex-direction: column; }
        .app-header { background: linear-gradient(to right, #4776E6, #8E54E9); color: white; padding: 15px; display: flex; align-items: center; }
        .logo { font-size: 20px; margin-right: 10px; }
        h1 { font-size: 20px; margin: 0; }
        .chat-container { flex-grow: 1; background-color: #f5f9fc; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; }
        .message { margin-bottom: 15px; max-width: 80%; display: flex; gap: 10px; align-items: flex-end; }
        .message-content { padding: 10px 15px; border-radius: 15px; font-size: 14px; word-wrap: break-word; }
        .message-time { font-size: 11px; margin-top: 4px; color: #888; align-self: flex-end; }
        .user-message { margin-left: auto; flex-direction: column; align-items: flex-end; }
        .user-message .message-content { background: linear-gradient(to right, #4776E6, #8E54E9); color: white; border-bottom-right-radius: 5px; }
        .bot-message { margin-right: auto; }
        .bot-avatar { width: 30px; height: 30px; background: linear-gradient(to right, #4776E6, #8E54E9); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; flex-shrink: 0; }
        .bot-message .message-content { background-color: #fff; border: 1px solid #eaeaea; color: #333; border-bottom-left-radius: 5px; }
        .chat-input-container { padding: 15px; background-color: white; border-top: 1px solid #eaeaea; }
        .suggestions { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 10px; scrollbar-width: none; -ms-overflow-style: none; }
        .suggestions::-webkit-scrollbar { display: none; }
        .suggestion-chip { background-color: #f0f2f5; padding: 8px 12px; border-radius: 15px; font-size: 12px; cursor: pointer; white-space: nowrap; flex-shrink: 0; }
        #chat-form { display: flex; width: 100%; gap: 8px; }
        #user-input { flex-grow: 1; padding: 10px 15px; border: 1px solid #ddd; border-radius: 20px; font-size: 14px; }
        #user-input:focus { outline: none; border-color: #4776E6; box-shadow: 0 0 0 3px rgba(71, 118, 230, 0.2); }
        button { width: 40px; height: 40px; background: linear-gradient(to right, #4776E6, #8E54E9); color: white; border: none; border-radius: 50%; cursor: pointer; font-size: 16px; display: flex; align-items: center; justify-content: center; }
        button:hover { transform: translateY(-2px); }
        .typing-indicator { display: none; align-items: center; margin-bottom: 15px; gap: 10px; }
        .typing-indicator .dots { display: flex; background-color: #fff; border: 1px solid #eaeaea; padding: 10px 15px; border-radius: 15px; gap: 4px; }
        .typing-indicator .dot { width: 8px; height: 8px; background-color: #aaa; border-radius: 50%; animation: bounce 1.5s infinite; }
        .typing-indicator .dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator .dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes bounce { 0%, 80%, 100% { transform: translateY(0); } 40% { transform: translateY(-5px); } }
        @media (max-width: 600px) { body { padding: 10px; } .app-container { height: 95vh; border-radius: 0; box-shadow: none; } .message { max-width: 95%; } }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="app-header">
            <div class="logo"><i class="fas fa-robot"></i></div>
            <h1>ChatBot</h1>
        </div>
        <div class="chat-container" id="chat-container">
            <div class="bot-message message">
                <div class="bot-avatar"><i class="fas fa-robot"></i></div>
                <div><div class="message-content">Hello! I'm ChatBot. How can I help you today?</div><div class="message-time">Just now</div></div>
            </div>
            <div class="typing-indicator" id="typing-indicator">
                <div class="bot-avatar"><i class="fas fa-robot"></i></div>
                <div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>
            </div>
        </div>
        <div class="chat-input-container">
            <div class="suggestions">
                <div class="suggestion-chip">What time is it?</div><div class="suggestion-chip">What's your name?</div>
                <div class="suggestion-chip">Tell me a joke</div><div class="suggestion-chip">Tell me a fact</div>
            </div>
            <form id="chat-form">
                <input type="text" id="user-input" placeholder="Type your message...">
                <button type="submit"><i class="fas fa-paper-plane"></i></button>
            </form>
        </div>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const chatContainer = document.getElementById('chat-container');
            const chatForm = document.getElementById('chat-form');
            const userInput = document.getElementById('user-input');
            const typingIndicator = document.getElementById('typing-indicator');
            const suggestionChips = document.querySelectorAll('.suggestion-chip');
            
            const getCurrentTime = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            document.querySelector('.bot-message .message-time').textContent = getCurrentTime();
            
            function addMessage(text, sender) {
                typingIndicator.style.display = 'none';
                const msgDiv = document.createElement('div');
                msgDiv.classList.add('message', `${sender}-message`);
                
                const contentDiv = document.createElement('div');
                contentDiv.classList.add('message-content');
                contentDiv.textContent = text;
                
                const timeDiv = document.createElement('div');
                timeDiv.classList.add('message-time');
                timeDiv.textContent = getCurrentTime();

                if (sender === 'user') {
                    msgDiv.append(contentDiv, timeDiv);
                } else {
                    const avatarDiv = document.createElement('div');
                    avatarDiv.classList.add('bot-avatar');
                    avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
                    const textContainer = document.createElement('div');
                    textContainer.append(contentDiv, timeDiv);
                    msgDiv.append(avatarDiv, textContainer);
                }
                chatContainer.appendChild(msgDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            const showTypingIndicator = () => { typingIndicator.style.display = 'flex'; chatContainer.scrollTop = chatContainer.scrollHeight; };
            
            chatForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const msg = userInput.value.trim();
                if (!msg) return;
                addMessage(msg, 'user');
                userInput.value = '';
                showTypingIndicator();
                setTimeout(() => {
                    fetch('/api/chat', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({message: msg}) })
                    .then(r => r.json()).then(data => addMessage(data.response, 'bot'))
                    .catch(error => { console.error('Error:', error); addMessage('Oops! Something went wrong.', 'bot'); });
                }, 800);
            });
            
            suggestionChips.forEach(chip => chip.addEventListener('click', function() {
                userInput.value = this.textContent;
                chatForm.dispatchEvent(new Event('submit'));
            }));
            userInput.focus();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    return jsonify({'response': chatbot.get_response(user_message)})

def run_console():
    print(f"{chatbot.name}: Hello! I'm {chatbot.name}. (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if not user_input.strip():
            print(f"{chatbot.name}: Say something!")
            continue
        response = chatbot.get_response(user_input)
        print(f"{chatbot.name}: {response}")
        if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']: break

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--console':
        run_console()
    else:
        print("Starting ChatBot web server at http://127.0.0.1:5000/")
        app.run(debug=True)