import React from 'react';
import { Navbar, Container, Nav, Badge } from 'react-bootstrap';
import { Brain, User } from 'lucide-react';

const Header = () => {
    return (
        <Navbar expand="lg" variant="dark" className="py-3">
            <Container>
                <Navbar.Brand href="/" className="fw-bold fs-4 d-flex align-items-center gap-2">
                    <div className="bg-primary p-2 rounded-3 d-flex align-items-center justify-content-center">
                        <Brain size={24} color="white" />
                    </div>
                    <span>BrainCoach <span className="text-primary">AI</span></span>
                </Navbar.Brand>
                <Nav className="ms-auto align-items-center gap-3">
                    <Badge bg="success" className="px-3 py-2 rounded-pill d-none d-md-block">Imagine Cup 2026</Badge>
                    <div className="d-flex align-items-center gap-2 bg-white bg-opacity-10 p-2 px-3 rounded-pill border border-white border-opacity-10">
                        <User size={18} />
                        <span className="small fw-medium">Vinitha</span>
                    </div>
                </Nav>
            </Container>
        </Navbar>
    );
};

export default Header;
