Project Title: Spanish Travel Companion

Description: This is a Spanish Travel Companion for travelers who have little to no experience speaking Spanish. They can adjust the difficulty of the language of the bot companion and the speed at which the bot companion speaks.

What it Does: The Spanish Travel Companion is an AI-powered conversational tool designed to help language learners bridge the gap between study and real-world speaking through an immersive, hands-free experience. By orchestrating a multi-stage machine learning pipeline—including OpenAI’s Whisper-1 for neural speech-to-text, GPT-4o-mini for conversational reasoning, and TTS-1 for natural speech synthesis—the application allows users to engage in adaptive, multi-turn dialogues. The system utilizes client-side Voice Activity Detection (VAD) via the Web Audio API to detect silence and automatically trigger responses, while simultaneously adjusting linguistic difficulty and playback speed to match the user's CEFR-level proficiency. This infrastructure provides a safe, low-stress environment for ear-training and speaking practice, specifically tailored for travelers navigating real-world scenarios.

Quick Start: Follow these steps to launch the project locally:
1. Clone & Install: Clone the repository and install the Python dependencies in the backend folder via pip install -r requirements.txt, then install the Node.js packages in the frontend folder using npm install.
2. Configure API Keys: Create a .env file in the backend directory and add your OPENAI_API_KEY to enable the transcription, reasoning, and speech synthesis models.
3. Launch Backend: Start the FastAPI server by running uvicorn main_backend:app --reload --port 8000 to handle the ML orchestration and context window management.
4. Launch Frontend: Start the Next.js development server with npm run dev in the frontend directory to access the UI and initialize the silence detection loop at http://localhost:3000.

Video Links: 
Technical Walkthrough: https://youtu.be/Bg_SOecNVDQ
DEMO: https://youtu.be/YFrBAgL9dyU

