# Nano Banana Multi-Agent System

## Project Overview
Interactive web application for image generation and editing using Google Gemini 2.5 Flash Image Preview (Nano Banana) through OpenRouter API.

## Core Features
- **Multi-Image Generation**: Generate 4 variations simultaneously using parallel API calls
- **Image Upload & Editing**: Upload images and edit them with consistent modifications
- **Interactive Tree UI**: Visual canvas showing image generation hierarchy with branching
- **Conversational Assistant**: Chat interface for natural language image requests
- **Multi-Agent Architecture**: GPT-4 mini for conversations, Nano Banana for image operations

## Technical Stack
- **Backend**: Python Flask
- **Frontend**: HTML/CSS/JavaScript 
- **AI Models**: OpenRouter API (Gemini 2.5 Flash + GPT-4 mini)
- **Environment**: Python venv
- **Dependencies**: flask, requests, python-dotenv, pillow

## API Integration
- **Primary Model**: Google Gemini 2.5 Flash Image Preview (internal name: Nano Banana)
- **Chat Model**: GPT-4 mini for prompt variations and conversations
- **Cost**: ~$0.03 per generated image
- **Free Tier**: Available for testing

## Project Structure
```
nano-banana/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies  
├── .env               # API keys (create from .env.example)
├── project_details.md # This file
├── outputs/           # Generated images
├── templates/         # HTML templates
└── static/           # CSS/JS files
```

## Development Phases
1. **Foundation**: Basic image generation with OpenRouter
2. **Multi-Agent**: Parallel generation with prompt variations
3. **Web Interface**: Flask app with HTML templates
4. **Image Editing**: Upload and edit functionality
5. **Tree UI**: Interactive canvas with branching
6. **Chat Assistant**: Conversational interface
7. **Polish**: UI/UX improvements and optimization

## Getting Started
1. Create virtual environment: `python3 -m venv nano-banana`
2. Activate: `source nano-banana/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your OpenRouter API key
5. Run: `python app.py`