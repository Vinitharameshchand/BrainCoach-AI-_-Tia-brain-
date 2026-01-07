import React, { useState } from 'react';
import { Container, Row, Col, Alert } from 'react-bootstrap';
import Header from '../components/Header';
import TrackingView from '../components/TrackingView';
import ExerciseView from '../components/ExerciseView';
import { Info } from 'lucide-react';

const Dashboard = () => {
    const [aiUpdate, setAiUpdate] = useState({ score: 0, feedback: "Starting..." });

    return (
        <div className="min-vh-100 d-flex flex-column">
            <Header />

            <Container fluid className="flex-grow-1 px-lg-5 py-4">
                <Row className="h-100 g-4">
                    <Col lg={8} className="h-100">
                        <ExerciseView />
                    </Col>

                    <Col lg={4} className="h-100">
                        <div className="d-flex flex-column h-100 gap-4">
                            <TrackingView onScoreUpdate={setAiUpdate} />

                            <Alert variant="info" className="bg-primary bg-opacity-10 border-primary border-opacity-25 text-light mb-0 p-4 rounded-4">
                                <div className="d-flex gap-3">
                                    <div className="bg-primary p-2 rounded-3 h-100">
                                        <Info size={20} color="white" />
                                    </div>
                                    <div>
                                        <h6 className="fw-bold mb-1">Coach Insight</h6>
                                        <p className="small mb-0 text-secondary">
                                            {aiUpdate.feedback === "Great focus!"
                                                ? "You are doing amazing! Keep your fingers moving at this pace."
                                                : "Try to keep your hands more visible in the center of the frame."}
                                        </p>
                                    </div>
                                </div>
                            </Alert>
                        </div>
                    </Col>
                </Row>
            </Container>
        </div>
    );
};

export default Dashboard;
