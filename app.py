import os
from flask import Flask, request, jsonify, render_template, send_file, session
from image_generator import generate_multiple_images, process_uploaded_image
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'nano-banana-secret-key-2024'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

GAME_STAGES = {
    1: {
        "title": "🌆 Neon Nights",
        "theme": "cyberpunk neon-lit cityscapes",
        "description": "Create vibrant cyberpunk scenes with neon lights and futuristic aesthetics",
        "unlock_requirement": 0,
        "example_prompts": [
            "cyberpunk city with neon cats",
            "retro arcade with glowing signs", 
            "neon-lit alleyway at night"
        ]
    },
    2: {
        "title": "🏚️ Urban Exploration", 
        "theme": "dark urban environments",
        "description": "Explore gritty city streets and shadowy alleyways",
        "unlock_requirement": 3,
        "example_prompts": [
            "dark alley with mysterious shadows",
            "abandoned city street at night",
            "urban cats in a rainy environment"
        ]
    },
    3: {
        "title": "🍄 Mystical Forest",
        "theme": "fantasy forest with magical elements",
        "description": "Journey into enchanted forests filled with wonder",
        "unlock_requirement": 6,
        "example_prompts": [
            "magical forest with glowing mushrooms",
            "wizard cats in an enchanted forest",
            "fairy tale woodland scene"
        ]
    },
    4: {
        "title": "🏛️ Ancient Ruins",
        "theme": "historical architecture and ancient civilizations",
        "description": "Discover the mysteries of lost civilizations",
        "unlock_requirement": 9,
        "example_prompts": [
            "ancient temple with golden light",
            "explorer cats in mysterious ruins",
            "archaeological discovery scene"
        ]
    }
}

def get_user_progress():
    if 'images_generated' not in session:
        session['images_generated'] = 0
    if 'current_stage' not in session:
        session['current_stage'] = 1
    return session['images_generated'], session['current_stage']

def update_progress():
    session['images_generated'] = session.get('images_generated', 0) + 1
    
    # Check for stage unlock
    current_images = session['images_generated']
    for stage_num, stage_data in GAME_STAGES.items():
        if (current_images >= stage_data['unlock_requirement'] and 
            stage_num > session.get('current_stage', 1)):
            session['current_stage'] = stage_num
            return True  # Stage unlocked
    return False  # No new stage unlocked

@app.route('/')
def index():
    images_generated, current_stage = get_user_progress()
    unlocked_stages = [stage for stage, data in GAME_STAGES.items() 
                      if images_generated >= data['unlock_requirement']]
    
    return render_template('index.html', 
                         current_stage=current_stage,
                         images_generated=images_generated,
                         unlocked_stages=unlocked_stages,
                         stages=GAME_STAGES)

@app.route('/api/stages')
def get_stages():
    images_generated, current_stage = get_user_progress()
    unlocked_stages = [stage for stage, data in GAME_STAGES.items() 
                      if images_generated >= data['unlock_requirement']]
    
    return jsonify({
        'current_stage': current_stage,
        'images_generated': images_generated,
        'unlocked_stages': unlocked_stages,
        'stages': GAME_STAGES
    })

@app.route('/generate', methods=['POST'])
def generate_images():
    # Handle both JSON and form data (for file uploads)
    if request.is_json:
        data = request.get_json()
        input_image_base64 = None
    else:
        # Form data with potential file upload
        data = request.form.to_dict()
        uploaded_file = request.files.get('image')
        
        if uploaded_file and allowed_file(uploaded_file.filename):
            input_image_base64 = process_uploaded_image(uploaded_file)
            if not input_image_base64:
                return jsonify({"error": "Failed to process uploaded image"}), 400
        else:
            input_image_base64 = None
    
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400
    
    # Enhance prompt with stage theme if specified
    stage_id = data.get('stage_id')
    enhanced_prompt = data['prompt']
    if stage_id and int(stage_id) in GAME_STAGES:
        stage_theme = GAME_STAGES[int(stage_id)]['theme']
        if input_image_base64:
            enhanced_prompt = f"{data['prompt']} in the style of {stage_theme}"
        else:
            enhanced_prompt = f"{data['prompt']} in the style of {stage_theme}"
    
    # Generate images (either from text or from uploaded image)
    results = generate_multiple_images(
        enhanced_prompt, 
        int(data.get('num_images', 4)), 
        input_image_base64
    )
    
    # Update user progress on successful generation
    successful_images = len([r for r in results if r['success']])
    stage_unlocked = False
    if successful_images > 0:
        for _ in range(successful_images):
            if update_progress():
                stage_unlocked = True
    
    images_generated, current_stage = get_user_progress()
    
    return jsonify({
        "base_prompt": data['prompt'],
        "enhanced_prompt": enhanced_prompt,
        "results": results,
        "successful_count": successful_images,
        "failed_count": len([r for r in results if not r['success']]),
        "stage_unlocked": stage_unlocked,
        "current_stage": current_stage,
        "images_generated": images_generated,
        "mode": "edit" if input_image_base64 else "generate"
    })

@app.route('/outputs/<filename>')
def serve_image(filename):
    return send_file(f'outputs/{filename}')

@app.route('/test')
def test_generation():
    results = generate_multiple_images("a serene lake at sunset", 2)
    return jsonify({"results": results})

if __name__ == '__main__':
    os.makedirs('outputs', exist_ok=True)
    print("🍌 Starting Nano Banana Multi-Agent System")
    print("Visit http://localhost:5000 to use the web interface")
    app.run(debug=True, port=5000)