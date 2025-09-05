import base64
import concurrent.futures
from datetime import datetime
from api_client import OpenRouterClient
from config import NANO_BANANA_MODEL
from prompt_generator import generate_prompt_variations

def generate_single_image(prompt, image_index):
    client = OpenRouterClient()
    print(f"Generating image {image_index} with prompt: '{prompt[:50]}...'")
    
    try:
        result = client.make_request(
            NANO_BANANA_MODEL,
            [{"role": "user", "content": f"Generate an image of: {prompt}"}],
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
                    filename = f"outputs/image_{image_index}_{timestamp}.png"
                    
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

def generate_multiple_images(base_prompt, num_images=4):
    print(f"🍌 Starting multi-image generation: {num_images} variations")
    
    prompt_variations = generate_prompt_variations(base_prompt, num_images)
    print(f"Generated {len(prompt_variations)} prompt variations")
    
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_index = {
            executor.submit(generate_single_image, prompt, i): i 
            for i, prompt in enumerate(prompt_variations)
        }
        
        for future in concurrent.futures.as_completed(future_to_index):
            result = future.result()
            results.append(result)
    
    results.sort(key=lambda x: x['index'])
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ {len(successful)} images generated successfully")
    if failed:
        print(f"❌ {len(failed)} images failed to generate")
    
    return results