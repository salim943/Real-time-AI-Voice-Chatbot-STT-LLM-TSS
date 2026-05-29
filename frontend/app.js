const ws = new WebSocket("ws://localhost:8000/ws");

const startBtn = document.getElementById("startBtn");
const messages = document.getElementById("messages");

let mediaRecorder;

function log(msg) {
  messages.textContent += msg + "\n";
  messages.scrollTop = messages.scrollHeight;
}

ws.onopen = () => log("Connected to backend.");
ws.onerror = () => log("WebSocket error.");

ws.onmessage = async (event) => {

  // Text messages
  if (typeof event.data === "string") {

    if (event.data.startsWith("AI_TOKEN:")) {
      const token = event.data.replace("AI_TOKEN:", "");
      messages.textContent += token;
    } else {
      log(event.data);
    }

  } else {

    // Audio response from backend
    const audioBlob = new Blob([event.data], {
      type: "audio/wav"
    });

    const url = URL.createObjectURL(audioBlob);

    const audio = new Audio(url);

    await audio.play();
  }
};

startBtn.onclick = async () => {

  const stream = await navigator.mediaDevices.getUserMedia({
    audio: true
  });

  mediaRecorder = new MediaRecorder(stream, {
    mimeType: "audio/webm;codecs=opus"
  });

  let chunks = [];

  mediaRecorder.ondataavailable = (e) => {
    chunks.push(e.data);
  };

  mediaRecorder.onstop = async () => {

    const blob = new Blob(chunks, {
      type: "audio/webm;codecs=opus"
    });

    chunks = [];

    const buffer = await blob.arrayBuffer();

    ws.send(buffer);

    log("\nListening complete. Processing...\n");
  };

  mediaRecorder.start();

  log("Recording for 4 seconds...");

  setTimeout(() => {
    mediaRecorder.stop();
    stream.getTracks().forEach(track => track.stop());
  }, 4000);
};