import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import { Rocket, BarChart3, ShieldCheck } from 'lucide-react';

const Landing = () => {
    const navigate = useNavigate();

    return (
        <div className="min-vh-100 d-flex flex-column">
            <Header />

            <Container className="flex-grow-1 d-flex align-items-center py-5">
                <Row className="align-items-center g-5">
                    <Col lg={6}>
                        <div className="pe-lg-5">
                            <Badge bg="primary" className="bg-opacity-10 text-primary px-3 py-2 rounded-pill mb-4 border border-primary border-opacity-10">
                                Revolutionizing Concentration
                            </Badge>
                            <h1 className="display-3 fw-bold mb-4">
                                Master Your Focus with <span className="text-primary text-gradient">Azure AI</span>
                            </h1>
                            <p className="lead text-secondary mb-5 fs-4">
                                BrainCoach AI is a gamified concentration trainer for kids. Using advanced hand tracking and computer vision to turn training into play.
                            </p>
                            <div className="d-flex gap-3">
                                <Button variant="primary" className="btn-premium py-3 px-5 shadow-lg" onClick={() => navigate('/dashboard')}>
                                    Get Started <Rocket size={20} className="ms-2" />
                                </Button>
                                <Button variant="outline-light" className="py-3 px-5 border-opacity-10 rounded-3">
                                    Watch Demo
                                </Button>
                            </div>
                        </div>
                    </Col>

                    <Col lg={6}>
                        <div className="position-relative">
                            <div className="glass-card p-2 p-md-4 rotate-3d">
                                <img
                                    src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80"
                                    alt="Dashboard Preview"
                                    className="img-fluid rounded-4 shadow-2xl"
                                />
                            </div>
                            {/* Floating stats card */}
                            <div className="position-absolute bottom-0 start-0 translate-middle-y glass-card p-4 shadow-xl border-primary border-opacity-25 animate-bounce-slow d-none d-md-block" style={{ marginLeft: '-30px' }}>
                                <div className="d-flex align-items-center gap-3">
                                    <div className="p-3 bg-success bg-opacity-10 rounded-3">
                                        <BarChart3 color="#10b981" />
                                    </div>
                                    <div>
                                        <h5 className="mb-0 fw-bold">+18%</h5>
                                        <p className="small text-secondary mb-0">Focus Score</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Col>
                </Row>
            </Container>

            <section className="py-5 bg-white bg-opacity-5 border-top border-white border-opacity-5">
                <Container>
                    <Row className="g-4">
                        {[
                            { icon: <Rocket />, title: "Split-Screen UI", desc: "Interactive exercises paired with real-time AI feedback." },
                            { icon: <ShieldCheck />, title: "Azure AI Core", desc: "Leveraging cloud power for deep behavioral analysis." },
                            { icon: <BarChart3 />, title: "Parent Dashboard", desc: "Detailed insights into progress and improvement." }
                        ].map((f, i) => (
                            <Col md={4} key={i}>
                                <div className="glass-card p-4 h-100 hover-scale">
                                    <div className="p-3 bg-primary bg-opacity-10 rounded-3 d-inline-block mb-4 text-primary">
                                        {f.icon}
                                    </div>
                                    <h4 className="fw-bold mb-3">{f.title}</h4>
                                    <p className="text-secondary mb-0">{f.desc}</p>
                                </div>
                            </Col>
                        ))}
                    </Row>
                </Container>
            </section>

            <footer className="py-5 text-center text-secondary small border-top border-white border-opacity-5">
                <p className="mb-0 text-white text-opacity-25">© 2026 BrainCoach AI. Built for Microsoft Imagine Cup.</p>
            </footer>
        </div>
    );
};

// Add some CSS for the animations and landing effects
const Badge = ({ children, className }) => (
    <span className={className}>{children}</span>
);

export default Landing;
