// Voice chat functionality
let recognition;
let synthesis;
let isListening = false;

// Initialize speech recognition and synthesis
function initSpeech() {
    try {
        window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        synthesis = window.speechSynthesis;
        
        setupRecognition();
        return true;
    } catch (e) {
        console.error('Speech recognition not supported:', e);
        return false;
    }
}

// Set up recognition handlers
function setupRecognition() {
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        sendMessage(transcript);
    };
    
    recognition.onerror = (event) => {
        console.error('Recognition error:', event.error);
        stopListening();
    };
    
    recognition.onend = () => {
        if (isListening) {
            recognition.start();
        }
    };
}

// Start listening for voice input
function startListening() {
    if (!recognition) {
        if (!initSpeech()) return;
    }
    isListening = true;
    recognition.start();
}

// Stop listening for voice input
function stopListening() {
    isListening = false;
    if (recognition) {
        recognition.stop();
    }
}

// Speak the response
function speakResponse(text) {
    if (!synthesis) {
        if (!initSpeech()) return;
    }
    
    // Cancel any ongoing speech
    synthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Get the character selection
    const character = document.getElementById('character-select').value;
    
    // Adjust voice settings based on character
    if (character) {
        const voices = synthesis.getVoices();
        // Try to find a suitable voice
        const englishVoices = voices.filter(voice => voice.lang.startsWith('en'));
        if (englishVoices.length > 0) {
            utterance.voice = englishVoices[0];
        }
        
        // Adjust pitch and rate based on character
        switch(character) {
            case 'You are a cybersecurity expert with deep knowledge of penetration testing and security assessments.':
                utterance.pitch = 1.0;
                utterance.rate = 0.9;
                break;
            case 'You are a helpful technical advisor who explains complex concepts in simple terms.':
                utterance.pitch = 1.1;
                utterance.rate = 0.85;
                break;
            case 'You are a professional business analyst who focuses on clear, actionable insights.':
                utterance.pitch = 1.0;
                utterance.rate = 0.95;
                break;
            case 'You are a programming mentor who helps guide developers through best practices.':
                utterance.pitch = 1.05;
                utterance.rate = 0.9;
                break;
            default:
                utterance.pitch = 1.0;
                utterance.rate = 1.0;
        }
    }
    
    synthesis.speak(utterance);
}

// Send message to the AI
async function sendMessage(message) {
    const character = document.getElementById('character-select').value;
    
    try {
        const response = await fetch('/chat/ai_chat_api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                prompt: message,
                model: 'X',
                character: character
            })
        });
        
        const data = await response.json();
        if (data.response) {
            displayMessage('user', message);
            displayMessage('assistant', data.response);
            speakResponse(data.response);
        }
    } catch (error) {
        console.error('Error sending message:', error);
        displayMessage('system', 'Error: Could not send message');
    }
}

// Get CSRF token from cookies
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Display message in chat
function displayMessage(role, content) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    if (role === 'assistant') {
        const avatar = document.createElement('img');
        avatar.src = '/static/img/X.jpeg';
        avatar.alt = 'Model Image';
        avatar.className = 'message-avatar';
        messageDiv.appendChild(avatar);
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = marked.parse(content);
    messageDiv.appendChild(contentDiv);
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}