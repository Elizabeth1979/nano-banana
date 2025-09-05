import base64
import concurrent.futures
from datetime import datetime
from api_client import OpenRouterClient
from config import NANO_BANANA_MODEL
from prompt_generator import generate_prompt_variations
from PIL import Image
import io

def generate_single_image(prompt, image_index, input_image_base64=None):
    client = OpenRouterClient()
    action = "Editing" if input_image_base64 else "Generating"
    print(f"{action} image {image_index} with prompt: '{prompt[:50]}...'")
    
    try:
        # Build message content
        if input_image_base64:
            # Image editing mode
            message_content = [
                {
                    "type": "text", 
                    "text": f"Edit this image according to the instruction: {prompt}"
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{input_image_base64}"}
                }
            ]
        else:
            # Text-to-image generation mode
            message_content = f"Generate an image of: {prompt}"
        
        result = client.make_request(
            NANO_BANANA_MODEL,
            [{"role": "user", "content": message_content}],
            modalities=["image", "text"]
        )
        
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']
            
            if 'images' in message and message['images']:
                image_data_obj = message['images'][0]
                image_url = image_data_obj['image_url']['url']
                
                if image_url.startswith('data:image/'):
                    base64_data = image_url.split('base64,')[1]
                    image_data = base64.b64decode(base64_data)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    prefix = "edited" if input_image_base64 else "image"
                    filename = f"outputs/{prefix}_{image_index}_{timestamp}.png"
                    
                    with open(filename, 'wb') as f:
                        f.write(image_data)
                    
                    print(f"✅ Image {image_index} saved: {filename}")
                    return {
                        "success": True,
                        "filename": filename,
                        "prompt": prompt,
                        "index": image_index
                    }
        
        return {
            "success": False,
            "error": "No image data in response",
            "prompt": prompt,
            "index": image_index
        }
    except Exception as e:
        print(f"❌ Error generating image {image_index}: {e}")
        return {
            "success": False,
            "error": str(e),
            "prompt": prompt,
            "index": image_index
        }

def process_uploaded_image(image_file):
    """Process uploaded image for API consumption"""
    try:
        # Open and resize image if needed
        img = Image.open(image_file)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large (max 1024x1024)
        max_size = 1024
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        img_base64 = base64.b64encode(img_data).decode('utf-8')
        
        return img_base64
    except Exception as e:
        print(f"Error processing uploaded image: {e}")
        return None

def generate_multiple_images(base_prompt, num_images=4, input_image_base64=None):
    mode = "editing" if input_image_base64 else "generation"
    print(f"🍌 Starting multi-image {mode}: {num_images} variations")
    
    prompt_variations = generate_prompt_variations(base_prompt, num_images)
    print(f"Generated {len(prompt_variations)} prompt variations")
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_index = {
            executor.submit(generate_single_image, prompt, i, input_image_base64): i 
            for i, prompt in enumerate(prompt_variations)
        }
        
        for future in concurrent.futures.as_completed(future_to_index):
            result = future.result()
            results.append(result)
    
    results.sort(key=lambda x: x['index'])
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    action = "edited" if input_image_base64 else "generated"
    print(f"✅ {len(successful)} images {action} successfully")
    if failed:
        print(f"❌ {len(failed)} images failed to {action.rstrip('ed')}")
    
    return results