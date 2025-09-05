# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a Python Flask web application for AI-powered image generation and editing using Google's Gemini 2.5 Flash Image Preview (nicknamed "Nano Banana") via OpenRouter API. The app features multi-agent architecture with GPT-4 mini for conversations and parallel image generation capabilities.

## Development Environment Setup
1. **Virtual Environment**: The project uses a Python virtual environment located in `nano-banana/`
   - Activate: `source nano-banana/bin/activate` (macOS/Linux) 
   - Deactivate: `deactivate`
2. **Dependencies**: Install with `pip install -r requirements.txt`
3. **Environment Variables**: Copy `.env.example` to `.env` and add your OpenRouter API key

## Running the Application
- **Main Flask App**: `python app.py` (starts web server)
- **Basic Test Script**: `python basic_image_gen.py` (tests API connection)

## Architecture
- **Backend**: Flask application in `app.py` with multi-threaded image generation
- **Frontend**: HTML templates in `templates/`, static assets would go in `static/` (currently empty)
- **API Integration**: Uses OpenRouter API with two models:
  - `google/gemini-2.5-flash-image-preview` (Nano Banana) for image generation
  - `openai/gpt-4o-mini` for prompt variations and conversations
- **Outputs**: Generated images saved to `outputs/` directory

## Key Components
- **Multi-Agent System**: `generate_prompt_variations()` creates 4 prompt variations, then parallel generation with `concurrent.futures`
- **Image Processing**: Base64 encoding/decoding for API communication, PIL for image handling
- **Error Handling**: Comprehensive error handling for API failures and invalid responses

## API Configuration
- Primary endpoint: `https://openrouter.ai/api/v1/chat/completions`
- Authentication via `OPENROUTER_API_KEY` environment variable
- Cost: ~$0.03 per generated image, free tier available for testing