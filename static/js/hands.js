import { ScoringSystem } from './scoring.js';

const videoElement = document.getElementById('webcam');
const canvasElement = document.getElementById('output_canvas');
const canvasCtx = canvasElement.getContext('2d');
const accuracyDisplay = document.getElementById('accuracy-display');
const feedbackToast = document.getElementById('feedback');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const timerDisplay = document.getElementById('timer');

const sessionId = document.getElementById('session_id').value;
const threshold = parseFloat(document.getElementById('accuracy_threshold').value);
const duration = parseInt(document.getElementById('duration').value);

const scorer = new ScoringSystem(threshold);
let isRunning = false;
let frameCount = 0;
let startTime;

// Audio feedback
const perfectSound = new Howl({
    src: ['https://actions.google.com/sounds/v1/cartoon/clime_up_the_ladder.ogg']
});

function onResults(results) {
    if (!isRunning) return;

    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        for (const landmarks of results.multiHandLandmarks) {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, { color: '#00FF00', lineWidth: 5 });
            drawLandmarks(canvasCtx, landmarks, { color: '#FF0000', lineWidth: 2 });

            // Scoring
            const accuracy = scorer.calculateAccuracy(landmarks);
            frameCount++;
            updateUI(accuracy);

            // Send periodic updates to backend
            if (frameCount % 30 === 0) {
                updateBackend(accuracy, landmarks, frameCount);
            }
        }
    }
    canvasCtx.restore();
}

function updateUI(accuracy) {
    accuracyDisplay.innerText = `Acc: ${accuracy.toFixed(1)}%`;

    if (accuracy >= threshold) {
        accuracyDisplay.className = "accuracy-indicator text-success";
        feedbackToast.style.display = 'block';
        feedbackToast.innerText = "Perfect!";
        feedbackToast.style.color = "#22c55e";
        if (frameCount % 60 === 0) perfectSound.play();
    } else {
        accuracyDisplay.className = "accuracy-indicator text-danger";
        feedbackToast.style.display = 'block';
        feedbackToast.innerText = "Faster fingers!";
        feedbackToast.style.color = "#ef4444";
    }
}

async function updateBackend(accuracy, landmarks, frameNum) {
    await fetch('/api/session/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            accuracy: accuracy,
            landmarks: landmarks,
            frame_number: frameNum
        })
    });
}

const hands = new Hands({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
});

hands.setOptions({
    maxNumHands: 2,
    modelComplexity: 1,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});

hands.onResults(onResults);

const camera = new Camera(videoElement, {
    onFrame: async () => {
        if (isRunning) {
            await hands.send({ image: videoElement });
        }
    },
    width: 640,
    height: 480
});

startBtn.onclick = () => {
    isRunning = true;
    startBtn.style.display = 'none';
    stopBtn.style.display = 'inline-block';
    startTime = Date.now();

    // Start Timer
    let timeLeft = duration;
    const interval = setInterval(() => {
        if (!isRunning) {
            clearInterval(interval);
            return;
        }
        timeLeft--;
        const mins = Math.floor(timeLeft / 60);
        const secs = timeLeft % 60;
        timerDisplay.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

        if (timeLeft <= 0) {
            clearInterval(interval);
            finishSession();
        }
    }, 1000);
};

stopBtn.onclick = finishSession;

async function finishSession() {
    isRunning = false;
    const finalAccuracy = scorer.getAverageAccuracy();
    const finalScore = scorer.getTotalScore();

    const response = await fetch('/api/session/complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: sessionId,
            avg_accuracy: finalAccuracy,
            total_score: finalScore
        })
    });

    const result = await response.json();
    if (result.redirect) {
        window.location.href = result.redirect;
    }
}

camera.start();

// Initialize Split.js
Split(['#left-view', '#right-view'], {
    sizes: [50, 50],
    minSize: 200
});
