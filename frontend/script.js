// BrainCoach AI - Core Frontend Logic
const videoElement = document.getElementById('webcam-feed');
const canvasElement = document.getElementById('output-canvas');
const canvasCtx = canvasElement.getContext('2d');
const feedbackEl = document.getElementById('ai-feedback');
const scoreEl = document.getElementById('concentration-score');

// Config
const API_URL = "http://127.0.0.1:5000"; // Update for production
let lastAnalysisTime = 0;
const ANALYSIS_INTERVAL = 3000; // Analyze every 3 seconds

function onResults(results) {
    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    
    // Draw landmarks (Local Feedback)
    if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 5});
            drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2});
        }
        
        // Trigger Cloud Analysis
        const now = Date.now();
        if (now - lastAnalysisTime > ANALYSIS_INTERVAL) {
            performCloudAnalysis();
            lastAnalysisTime = now;
        }
    } else {
        feedbackEl.innerText = "No hand detected";
        feedbackEl.style.color = "orange";
    }
    canvasCtx.restore();
}

const hands = new Hands({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
    }
});

hands.setOptions({
    maxNumHands: 2,
    modelComplexity: 1,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});

hands.onResults(onResults);

async function startCamera() {
    const camera = new Camera(videoElement, {
        onFrame: async () => {
            await hands.send({image: videoElement});
        },
        width: 1280,
        height: 720
    });
    camera.start();
}

async function performCloudAnalysis() {
    // Capture high-res snapshot
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = videoElement.videoWidth;
    tempCanvas.height = videoElement.videoHeight;
    tempCanvas.getContext('2d').drawImage(videoElement, 0, 0);
    const base64Image = tempCanvas.toDataURL('image/jpeg');

    try {
        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                image: base64Image, 
                exercise: document.getElementById('exercise-title')?.innerText || 'demo' 
            })
        });
        
        const data = await response.json();
        if (data.score) {
            scoreEl.innerText = `${data.score}%`;
            feedbackEl.innerText = data.feedback;
            feedbackEl.style.color = "white";
        }
    } catch (err) {
        console.error("Cloud analysis failed", err);
        feedbackEl.innerText = "Offline Mode";
    }
}

// Initialize
window.onload = () => {
    if (videoElement) {
        startCamera();
    }
};
