# 🧠 BrainCoach AI - Kids Concentration Training

![Project Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

**BrainCoach AI** is an interactive, AI-powered web application designed to train kids' concentration using cognitive exercises. Inspired by the **TIA Brain** methodology, it features a split-screen interface where users engage with brain training tasks while their engagement and hand movements are tracked in real-time using **MediaPipe Hands**.


## 🌟 Key Features

*   **Split-Screen Interface**: Seamlessly integrates the game/activity area with the AI monitoring feed.
*   **AI Hand Tracking**: Uses **Google MediaPipe** to interpret hand gestures and track concentration levels in real-time.
*   **Cognitive Exercises**: Fun and engaging tasks designed to boost focus and mental agility.
*   **Real-time Feedback**: Instant visual cues based on user performance and hand positioning.
*   **Secure Backend**: Robust data handling with a Flask REST API.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript | Core structure and logic |
| **UI Framework** | Bootstrap 5 | Responsive, modern styling |
| **AI/ML** | MediaPipe Hands | Real-time hand tracking and gesture recognition |
| **Backend** | Python, Flask | REST API and server-side logic |
| **Database** | MySQL (Railway) | User data and session storage |
| **Hosting** | Netlify (Frontend), Render (Backend) | Cloud deployment |

---

## 📂 Project Structure

```bash
BrainCoach-AI/
├── frontend/                  # Frontend source code
│   ├── index.html             # Main entry point
│   ├── assets/                # Images, icons, and static files
│   ├── css/                   # Custom styles
│   └── js/                    # Game logic and MediaPipe integration
│
├── backend/                   # Backend API source code
│   ├── app.py                 # Flask application entry point
│   ├── models.py              # Database models
│   ├── routes/                # API route definitions
│   └── requirements.txt       # Python dependencies
│
└── README.md                  # Project documentation
```

---

## 🔧 Installation & Setup

Follow these steps to set up the project locally.

### Prerequisites

*   Python 3.8+
*   Node.js (optional, for package management if needed)
*   MySQL Database

### 1. Clone the Repository

```bash
git clone https://github.com/Vinitharameshchand/BrainCoach-AI-_-Tia-brain-.git
cd BrainCoach-AI-_-Tia-brain-
```

### 2. Backend Setup

Navigate to the `backend` directory and install dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set up your environment variables (create a `.env` file):

```env
DATABASE_URL=mysql://user:password@host:port/dbname
SECRET_KEY=your_secret_key
```

Run the server:

```bash
flask run
```

### 3. Frontend Setup

Navigate to the `frontend` directory. Since it uses vanilla JS and Bootstrap via CDN (or local), you can simply open `index.html` in your browser or use a live server:

```bash
# If using Live Server extension or similar
live-server .
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Commit your changes (`git commit -m 'Add some feature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
---

## 🚀 Live Demo

Check out the live application: sooonnn 

---

<div align="center">

**Built with ❤️ for better concentration.**

</div>
# BrainCoach-AI-_-Tia-brain-
