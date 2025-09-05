"""
Basic image generation test script using OpenRouter API
Tests connection to Nano Banana (Google Gemini 2.5 Flash Image Preview)
"""
import os
import requests
import base64
import concurrent.futures
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY not found in .env file")
    print("Please copy .env.example to .env and add your API key")
    exit(1)

# OpenRouter API configuration
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
NANO_BANANA_MODEL = "google/gemini-2.5-flash-image-preview"

def generate_image(prompt, image_index=0):
    """Generate a single image using Nano Banana model"""
    print(f"Generating image {image_index + 1} with prompt: '{prompt}'")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": NANO_BANANA_MODEL,
        "messages": [
            {
                "role": "user", 
                "content": f"Generate an image of: {prompt}"
            }
        ],
        "modalities": ["image", "text"],
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        
        # Print detailed error information for debugging
        print(f"Response status code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.text}")
            
        response.raise_for_status()
        
        result = response.json()
        print("API Response received")
        print(f"Response keys: {list(result.keys())}")
        
        # Extract the response content
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']
            content = message.get('content', '')
            print(f"Text response: {content}")
            
            # Check for images in the response
            if 'images' in message and message['images']:
                print(f"Found {len(message['images'])} image(s) in response")
                
                # Process the first image
                image_data_obj = message['images'][0]
                image_url = image_data_obj['image_url']['url']
                
                print(f"Image URL prefix: {image_url[:50]}...")
                
                # Extract base64 data from data URL
                if image_url.startswith('data:image/'):
                    # Format: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
                    base64_data = image_url.split('base64,')[1]
                    
                    # Decode and save the image
                    image_data = base64.b64decode(base64_data)
                    
                    # Save image
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"outputs/image_{image_index}_{timestamp}.png"
                    
                    with open(filename, 'wb') as f:
                        f.write(image_data)
                    
                    print(f"✅ Image saved successfully: {filename}")
                    return filename
                else:
                    print("❌ Unexpected image URL format")
                    return None
            else:
                print("❌ No images found in response")
                print("Available message keys:", list(message.keys()))
                return None
        else:
            print("❌ No valid response from API")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def main():
    """Test multi-image generation"""
    print("🍌 Testing Nano Banana Multi-Image Generation")
    print("-" * 50)
    
    # Test prompt
    test_prompt = "a beautiful sunset over mountains with vibrant colors"
    
    # Generate 4 images in parallel
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(generate_image, test_prompt, i) for i in range(4)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    print(f"\n🎉 Success! Generated {len(results)} images:")
    for result in results:
        print(f"  - {result}")

if __name__ == "__main__":
    main()