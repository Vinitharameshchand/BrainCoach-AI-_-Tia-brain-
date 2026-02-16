import { ScoringSystem } from './scoring.js';

const videoElement = document.getElementById('webcam');
const canvasElement = document.getElementById('output_canvas');
const canvasCtx = canvasElement.getContext('2d');
const accuracyVal = document.getElementById('acc-val');
const accRing = document.getElementById('acc-ring');
const accCircle = document.querySelector('.progress-ring__circle');
const feedbackEmoji = document.getElementById('feedback-emoji');
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

// Accuracy Circle Settings
const radius = accCircle.r.baseVal.value;
const circumference = radius * 2 * Math.PI;
accCircle.style.strokeDasharray = `${circumference} ${circumference}`;

function setProgress(percent) {
    const offset = circumference - (percent / 100 * circumference);
    accCircle.style.strokeDashoffset = offset;
}

// Audio feedback
const perfectSound = new Howl({
    src: ['https://actions.google.com/sounds/v1/cartoon/clime_up_the_ladder.ogg']
});

const failureSound = new Howl({
    src: ['https://actions.google.com/sounds/v1/cartoon/spring_boing.ogg'],
    volume: 0.2
});

function onResults(results) {
    if (!isRunning) return;

    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

    // Smooth drawing
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        for (const landmarks of results.multiHandLandmarks) {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, { color: '#3b82f6', lineWidth: 4 });
            drawLandmarks(canvasCtx, landmarks, { color: '#10b981', lineWidth: 1, radius: 2 });

            const accuracy = scorer.calculateAccuracy(landmarks);
            frameCount++;
            updateUI(accuracy);

            if (frameCount % 60 === 0) {
                updateBackend(accuracy, landmarks, frameCount);
            }
        }
    }
    canvasCtx.restore();
}

function updateUI(accuracy) {
    accuracyVal.innerText = `${Math.round(accuracy)}%`;
    setProgress(accuracy);

    if (accuracy >= threshold) {
        accRing.className = "accuracy-ring-container glow-success";
        accCircle.style.stroke = "#10b981";

        if (accuracy > 90 && frameCount % 120 === 0) {
            showEmoji('🌟');
            perfectSound.play();
        }
    } else {
        accRing.className = "accuracy-ring-container glow-danger";
        accCircle.style.stroke = "#ef4444";

        if (frameCount % 180 === 0) {
            showEmoji('☝️');
            failureSound.play();
        }
    }
}

function showEmoji(emoji) {
    feedbackEmoji.innerText = emoji;
    feedbackEmoji.classList.add('show');
    setTimeout(() => feedbackEmoji.classList.remove('show'), 1000);
}

async function updateBackend(accuracy, landmarks, frameNum) {
    try {
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
    } catch (e) {
        console.error("Backend update failed", e);
    }
}

const hands = new Hands({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
});

hands.setOptions({
    maxNumHands: 1,
    modelComplexity: 1,
    minDetectionConfidence: 0.7,
    minTrackingConfidence: 0.7
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

Split(['#left-view', '#right-view'], {
    sizes: [50, 50],
    minSize: 200,
    gutterSize: 10,
    snapOffset: 0
});
