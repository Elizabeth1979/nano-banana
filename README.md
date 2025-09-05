# Nano Banana 🍌

AI-powered image generation and editing web application using Google's Gemini 2.5 Flash Image Preview (nicknamed "Nano Banana") via OpenRouter API. Features a multi-agent architecture with gamified progression system.

## ✨ Features

- **Multi-Image Generation**: Generate 4 image variations simultaneously using parallel processing
- **Image Upload & Editing**: Upload and edit existing images with AI-powered modifications
- **Gamified Progression**: Unlock themed stages (Neon Nights, Urban Exploration, Mystical Forest, Ancient Ruins) as you create more images
- **Multi-Agent Architecture**: GPT-4 mini for conversations and prompt variations, Nano Banana for image operations
- **Web Interface**: Clean Flask-based web application with responsive design
- **Concurrent Processing**: Parallel API calls for faster image generation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenRouter API key ([Get one here](https://openrouter.ai/))

### Installation

1. **Clone and navigate to the project**
   ```bash
   cd nano-banana
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv nano-banana
   source nano-banana/bin/activate  # On Windows: nano-banana\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Visit `http://localhost:5000`

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **AI Models**: 
  - Google Gemini 2.5 Flash Image Preview (Nano Banana) - Image generation/editing
  - OpenAI GPT-4 mini - Prompt variations and conversations
- **API**: OpenRouter integration
- **Image Processing**: PIL (Python Imaging Library)
- **Frontend**: HTML/CSS/JavaScript
- **Concurrency**: Python concurrent.futures

## 📁 Project Structure

```
nano-banana/
├── app.py                 # Main Flask application with game progression
├── image_generator.py     # Multi-threaded image generation logic
├── api_client.py          # OpenRouter API client
├── config.py              # Configuration and model settings
├── prompt_generator.py    # AI-powered prompt variation generator
├── basic_image_gen.py     # Simple test script for API validation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── templates/
│   └── index.html        # Web interface template
├── static/               # CSS/JS files (if any)
└── outputs/              # Generated images directory
```

## 🎮 Game Progression System

The app features a gamified experience with unlockable themes:

| Stage | Theme | Unlock Requirement | Description |
|-------|-------|-------------------|-------------|
| 🌆 Neon Nights | Cyberpunk neon-lit cityscapes | Start (0 images) | Vibrant cyberpunk scenes |
| 🏚️ Urban Exploration | Dark urban environments | 3 images | Gritty city streets and alleyways |
| 🍄 Mystical Forest | Fantasy forest with magical elements | 6 images | Enchanted forests and magic |
| 🏛️ Ancient Ruins | Historical architecture | 9 images | Lost civilizations and archaeology |

## 🔑 API Configuration

### Models Used
- **Primary**: `google/gemini-2.5-flash-image-preview` (Nano Banana)
- **Chat**: `openai/gpt-4o-mini` for prompt enhancement

### Costs
- ~$0.03 per generated image
- Free tier available for testing
- Charges through OpenRouter billing

### Environment Variables
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## 🖼️ Usage Examples

### Text-to-Image Generation
1. Enter a prompt in the web interface
2. Select a theme stage (if unlocked)
3. Click "Generate Images"
4. View 4 AI-generated variations

### Image Editing
1. Upload an image using the file picker
2. Enter editing instructions
3. Apply theme styling (optional)
4. Generate edited variations

### API Testing
```bash
python basic_image_gen.py  # Test basic API connectivity
```

## 🧪 Testing

### Basic API Test
```bash
python basic_image_gen.py
```

### Web Interface Test
1. Start the application: `python app.py`
2. Visit: `http://localhost:5000/test`
3. Check console output for generation results

## 🔧 Development

### Key Components

- **Multi-Agent System**: `generate_prompt_variations()` creates diverse prompts using GPT-4 mini
- **Parallel Processing**: `concurrent.futures` for simultaneous image generation
- **Image Processing**: Base64 encoding/decoding, PIL for image manipulation
- **Session Management**: Flask sessions track user progress and unlocks
- **Error Handling**: Comprehensive error handling for API failures

### Adding New Themes
Edit the `GAME_STAGES` dictionary in `app.py` to add new unlockable themes and requirements.

## 📝 License

This project is for educational and experimental purposes. Please respect OpenRouter's API terms of service.

## 🤝 Contributing

This is an experimental project. Feel free to fork and experiment with different AI models or features!

---

*Built with Claude Code and the OpenRouter API ecosystem* 🍌✨