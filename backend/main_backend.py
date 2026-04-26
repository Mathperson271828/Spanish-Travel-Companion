import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import AsyncOpenAI
from fastapi import UploadFile, File
from elevenlabs.client import ElevenLabs
from fastapi.responses import StreamingResponse
from fastapi.responses import Response 
from fastapi import HTTPException
from typing import List, Dict
import io


## The code below was generated mostly by Gemini
# 1. ENVIRONMENT LOADING
# This function looks for your .env file and reads the API keys into memory.
# It allows us to use os.getenv() later without hardcoding secrets in the code.
load_dotenv()

# 2. APP INITIALIZATION
# Here we create the "app" object, which is the heart of your server.
app = FastAPI(title="Spanish Travel Companion API")

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 3. CORS (CROSS-ORIGIN RESOURCE SHARING) CONFIGURATION
# By default, browsers block websites from talking to different servers.
# This block tells the browser: "It is safe for my Next.js frontend (on port 3000)
# to send requests to this FastAPI backend (on port 8000)."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://spanish-travel-companion-rnu2.vercel.app"], # Permits requests from your frontend
    allow_credentials=True,                  # Allows cookies/auth headers if needed
    allow_methods=["*"],                     # Permits all actions (GET, POST, etc.)
    allow_headers=["*"],                     # Permits all metadata headers
)

# 4. DATA MODELING
# We use Pydantic to define exactly what the incoming data should look like.
# This tells FastAPI: "If someone sends a POST request to /chat, it MUST 
# contain a JSON object with a string field named 'message'."
class ChatRequest(BaseModel):
    message: List[Dict[str, str]]
    difficulty: str #New field beginner or intermediate

class TTSRequest(BaseModel):
    text: str
    speed: float = 0.5

# 5. HEALTH CHECK ENDPOINT (GET)
# This is a simple diagnostic tool. You can visit http://localhost:8000/health
# in your browser to verify the server is actually running.
@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "message": "¡Hola Leo! The backend server is up and running."
    }

# 6. CHAT ENDPOINT (POST)
# This is where the main interaction happens. We use 'POST' because the 
# frontend is "posting" new data (the user's message) to the server.
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):        
    #Define out the teaching styles
    user_text = request.message

    if request.difficulty == "Beginner":
        level_instruction = """ 
            RULES:
            1. Tense: Only use present tense.
            2. Vocabulary: Limit to only A1-level Spanish. Focus on nouns and simple verbs.
            3. Sentence Structure: Subject + Verb + Object. No compound sentences. Keep sentences under 8 words and avoid slang.
            """
    else:
        level_instruction = """
            RULES:
            1. Tense: Use present, past, and future tenses
            2. Vocabulary: Incorporate A1, A2, and B1 level Spanish. Use slightly more complex travel vocabulary.
            3. Sentence Structure: Use slightly longer sentences than simple sentences.
            """

    try:
        system_prompt = {
            "role": "system",
            "content": f"You are a helpful Spanish Travel Companion. Speak exclusively in Spanish at a {request.difficulty} level."
        }
        full_conversation = [system_prompt] + user_text

        response = await client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = full_conversation, temperature = 0.1
        )
    
        ai_reply = response.choices[0].message.content

        if request.difficulty == "Beginner":
            bot_difficulty = "Beginner"
        else:
            bot_difficulty = "Intermediate"            

        return {
            "user_sent": user_text,
            "reply": ai_reply,
            "difficulty" : bot_difficulty
        }

    except Exception as e:
        print(f"Error: {e}")
        return{
            "reply": "Lo siento, I had trouble thinking. Check your API key!", 
            "status": "error"
        }

@app.post("/speech-to-text")
async def transcribe_speech(file : UploadFile = File(...)):
    #Save open file temporarily
    content = await file.read()
    if (len(content) == 0):
        return {"text": "", "error": "No audio detected"}

    #Open file and send it to Whisper
    try:
        transcript = await client.audio.transcriptions.create(
            model = "whisper-1",
            file = ("audio.webm", io.BytesIO(content)),
            language="es"
        )
        return {"text": transcript.text}

    except Exception as e:
        print(f"Whisper API Error: {e}")
        return {"error": "Failed to transcribe audio"}
    
# Elevenlabs text to speech
@app.post("/text-to-speech")
async def generate_speech(request: TTSRequest):
    try:
        # We use your existing 'client' (OpenAI) instead of ElevenLabs!
        # "nova" is a great, energetic female voice. "alloy" is a good neutral voice.
        response = await client.audio.speech.create(
            model="tts-1",
            voice="nova", 
            input=request.text,
            speed=request.speed # 2. Pass the speed directly to OpenAI!
        )
        
        # Read the raw audio bytes
        audio_bytes = response.read()

        # Return the audio as a playable MP3 stream
        return Response(content=audio_bytes, media_type="audio/mpeg")

    except Exception as e:
        print(f"OpenAI TTS Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))