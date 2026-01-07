import React, { useState, useEffect } from 'react';
import { Card, Button } from 'react-bootstrap';
import { Play, RotateCcw, CheckCircle } from 'lucide-react';

const ExerciseView = () => {
    const [step, setStep] = useState(1);
    const totalSteps = 10;

    const handleNext = () => {
        if (step < totalSteps) setStep(step + 1);
    };

    const handleReset = () => setStep(1);

    return (
        <div className="glass-card p-4 h-100 d-flex flex-column text-center justify-content-center">
            <div className="mb-4">
                <h2 className="display-6 fw-bold mb-3">Finger Yoga</h2>
                <p className="text-secondary lead">Touch your thumb to each finger in sequence.</p>
            </div>

            <div className="flex-grow-1 d-flex flex-column justify-content-center py-5">
                <div className="display-1 mb-4">
                    {step % 2 === 0 ? '👋' : '✋'}
                </div>
                <div className="d-flex justify-content-center gap-2 mb-4">
                    {[...Array(totalSteps)].map((_, i) => (
                        <div
                            key={i}
                            className={`rounded-circle ${i + 1 <= step ? 'bg-primary' : 'bg-white bg-opacity-10'}`}
                            style={{ width: '12px', height: '12px', transition: 'all 0.3s ease' }}
                        />
                    ))}
                </div>
                <p className="text-primary fw-bold">Step {step} of {totalSteps}</p>
            </div>

            <div className="d-flex justify-content-center gap-3 mt-auto">
                <Button variant="outline-light" className="px-4 py-2 rounded-3 border-opacity-10" onClick={handleReset}>
                    <RotateCcw size={18} className="me-2" /> Reset
                </Button>
                <Button variant="primary" className="btn-premium px-5" onClick={handleNext}>
                    {step === totalSteps ? (
                        <span className="d-flex align-items-center"><CheckCircle size={18} className="me-2" /> Finish</span>
                    ) : (
                        <span className="d-flex align-items-center"><Play size={18} className="me-2" /> Next Step</span>
                    )}
                </Button>
            </div>
        </div>
    );
};

export default ExerciseView;
