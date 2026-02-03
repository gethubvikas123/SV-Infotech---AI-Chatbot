function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const loading = document.getElementById("loading");

    const message = input.value.trim();
    if (!message) return;

    chatBox.innerHTML += `
        <div class="message user">${message}</div>
    `;

    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

     // ✅ SHOW GIF
    loading.style.display = "block";
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {

    // ✅ HIDE GIF FIRST (IMPORTANT)
    loading.style.display = "none";

    let formattedReply = data.reply
        .replace(/#/g, "")
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>")
        .replace(/\n/g, "<br>");

    chatBox.innerHTML += `
        <div class="message bot">${formattedReply}</div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
});

}
