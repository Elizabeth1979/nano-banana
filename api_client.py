import requests
from config import OPENROUTER_API_KEY, OPENROUTER_URL

class OpenRouterClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def make_request(self, model, messages, max_tokens=1000, modalities=None):
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens
        }
        if modalities:
            data["modalities"] = modalities
            
        response = requests.post(OPENROUTER_URL, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()