#!/usr/bin/env python3
"""
DeepSeek Client via OpenRouter
================================
Provides uncensored AI generation through OpenRouter's DeepSeek endpoint.
"""

import requests
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DeepSeekClient:
    """DeepSeek client using OpenRouter API"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable required!")
        
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = model or os.getenv('DEEPSEEK_MODEL', 'deepseek/deepseek-chat')
        
    def generate(self, prompt: str, max_tokens: int = 4000, temperature: float = 0.3) -> Dict:
        """
        Generate code or text using DeepSeek via OpenRouter
        
        Args:
            prompt: The user prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 - 1.0)
            
        Returns:
            Dict with 'content', 'usage', and 'model' keys
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/deepseek-validation",
            "X-Title": "DeepSeek Validation Tool"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'content': result['choices'][0]['message']['content'],
                    'usage': result.get('usage', {}),
                    'model': result.get('model', self.model)
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timed out'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Test function
def test_client():
    """Test the DeepSeek client"""
    try:
        client = DeepSeekClient()
        result = client.generate("Write a hello world function in Python")
        
        if result['success']:
            print("✅ DeepSeek Client Test Successful!")
            print(f"Model: {result['model']}")
            print(f"Response: {result['content'][:200]}...")
        else:
            print(f"❌ Test Failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")


if __name__ == "__main__":
    test_client()
