from api_client import OpenRouterClient
from config import GPT4_MINI_MODEL

def generate_prompt_variations(base_prompt, num_variations=4):
    client = OpenRouterClient()
    
    variation_prompt = f"""Create {num_variations} creative variations of this image prompt: "{base_prompt}"

Keep the core concept but vary:
- Visual style and mood
- Specific details and elements  
- Artistic approach or medium
- Lighting and atmosphere

Return only the {num_variations} variations, one per line, without numbering or extra text."""
    
    try:
        result = client.make_request(
            GPT4_MINI_MODEL,
            [{"role": "user", "content": variation_prompt}],
            max_tokens=300
        )
        
        if 'choices' in result and len(result['choices']) > 0:
            variations_text = result['choices'][0]['message']['content']
            variations = [line.strip() for line in variations_text.strip().split('\n') if line.strip()]
            
            if len(variations) < num_variations:
                variations.extend([base_prompt] * (num_variations - len(variations)))
                
            return variations[:num_variations]
        else:
            return [base_prompt] * num_variations
    except Exception as e:
        print(f"Error generating prompt variations: {e}")
        return [base_prompt] * num_variations