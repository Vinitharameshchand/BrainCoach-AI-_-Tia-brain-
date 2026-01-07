import React, { useEffect, useRef, useState } from 'react';
import { Hands, HAND_CONNECTIONS } from '@mediapipe/hands';
import { Camera } from '@mediapipe/camera_utils';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils';
import axios from 'axios';

const TrackingView = ({ onScoreUpdate }) => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [feedback, setFeedback] = useState("Initializing AI...");
    const [score, setScore] = useState(0);
    const lastAnalysisTime = useRef(0);
    const API_URL = "http://127.0.0.1:5000";

    useEffect(() => {
        const hands = new Hands({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
        });

        hands.setOptions({
            maxNumHands: 2,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5,
        });

        hands.onResults((results) => {
            const canvasCtx = canvasRef.current.getContext('2d');
            canvasCtx.save();
            canvasCtx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);

            if (results.multiHandLandmarks) {
                for (const landmarks of results.multiHandLandmarks) {
                    drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, { color: '#6366f1', lineWidth: 5 });
                    drawLandmarks(canvasCtx, landmarks, { color: '#ffffff', lineWidth: 2, radius: 3 });
                }

                const now = Date.now();
                if (now - lastAnalysisTime.current > 3000) {
                    performCloudAnalysis();
                    lastAnalysisTime.current = now;
                }
            } else {
                setFeedback("No hand detected");
            }
            canvasCtx.restore();
        });

        const camera = new Camera(videoRef.current, {
            onFrame: async () => {
                await hands.send({ image: videoRef.current });
            },
            width: 640,
            height: 480,
        });
        camera.start();

        return () => camera.stop();
    }, []);

    const performCloudAnalysis = async () => {
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = videoRef.current.videoWidth;
        tempCanvas.height = videoRef.current.videoHeight;
        tempCanvas.getContext('2d').drawImage(videoRef.current, 0, 0);
        const base64Image = tempCanvas.toDataURL('image/jpeg');

        try {
            const response = await axios.post(`${API_URL}/analyze`, {
                image: base64Image,
                exercise: 'finger-yoga'
            });

            const { score, feedback } = response.data;
            setScore(score);
            setFeedback(feedback);
            onScoreUpdate({ score, feedback });
        } catch (err) {
            console.error("Analysis error:", err);
            setFeedback("Offline Mode");
        }
    };

    return (
        <div className="glass-card p-4 h-100 d-flex flex-column">
            <h5 className="mb-4 d-flex align-items-center gap-2">
                <span className="p-1 bg-success rounded-circle animate-pulse-slow"></span>
                AI Concentration Feed
            </h5>

            <div className="position-relative bg-dark rounded-4 overflow-hidden mb-4 shadow-lg border border-white border-opacity-10" style={{ aspectRatio: '4/3' }}>
                <video ref={videoRef} className="w-100 h-100 object-fit-cover" muted playsInline />
                <canvas ref={canvasRef} className="position-absolute top-0 left-0 w-100 h-100" />
                <div className="position-absolute top-3 start-3 px-3 py-1 bg-dark bg-opacity-75 rounded-pill small border border-white border-opacity-10">
                    {feedback}
                </div>
            </div>

            <div className="mt-auto">
                <div className="d-flex justify-content-between mb-2">
                    <span className="text-secondary small">Real-time Focus</span>
                    <span className="fw-bold text-primary">{score}%</span>
                </div>
                <div className="progress bg-white bg-opacity-10" style={{ height: '8px', borderRadius: '4px' }}>
                    <div
                        className="progress-bar bg-primary transition-all duration-500"
                        style={{ width: `${score}%`, borderRadius: '4px' }}
                    />
                </div>
            </div>
        </div>
    );
};

export default TrackingView;
