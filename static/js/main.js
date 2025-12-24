// Initialize Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (!SpeechRecognition) {
    alert("Your browser does not support Speech Recognition. Please use Chrome.");
}

const recognition = new SpeechRecognition();
recognition.lang = 'en-US';
recognition.interimResults = false;

const micBtn = document.getElementById('micBtn');
const usernameInput = document.getElementById('username');
const statusText = document.getElementById('status');
const resultArea = document.getElementById('resultArea');

// 1. Handle Microphone Click
micBtn.onclick = () => {
    const name = usernameInput.value.trim();
    
    if (!name) {
        alert("Please enter your name first!");
        usernameInput.focus();
        return;
    }

    recognition.start();
    micBtn.classList.add('mic-active');
    statusText.innerText = "Listening... speak now!";
};

// 2. Process Voice Result
recognition.onresult = async (event) => {
    micBtn.classList.remove('mic-active');
    const transcript = event.results[0][0].transcript;
    statusText.innerText = "Analyzing your review...";

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: usernameInput.value,
                text: transcript
            })
        });

        const data = await response.json();
        displayResult(transcript, data);
        statusText.innerText = "Feedback saved!";
        
    } catch (error) {
        console.error("Error:", error);
        statusText.innerText = "Error analyzing voice.";
    }
};

// 3. Update UI with Results
function displayResult(text, data) {
    resultArea.classList.remove('d-none');
    document.getElementById('transcript').innerText = `"${text}"`;
    document.getElementById('scoreVal').innerText = data.score;

    const label = document.getElementById('sentimentLabel');
    label.innerText = data.label;
    
    // Dynamic coloring based on label
    label.className = "badge rounded-pill px-3 py-2 ";
    if (data.label === 'Positive') label.classList.add('bg-success');
    else if (data.label === 'Negative') label.classList.add('bg-danger');
    else label.classList.add('bg-warning', 'text-dark');
}

recognition.onerror = (event) => {
    micBtn.classList.remove('mic-active');
    statusText.innerText = "Microphone error: " + event.error;
};