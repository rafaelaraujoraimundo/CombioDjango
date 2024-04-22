async function sendMessage() {
    const inputBox = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const userText = inputBox.value;
    chatBox.innerHTML += `<div>Usuário: ${userText}</div>`;

    const response = await fetch('/chatgpt/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: userText })
    });

    const data = await response.json();
    chatBox.innerHTML += `<div>ChatGPT: ${data.response}</div>`;
    inputBox.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;
}