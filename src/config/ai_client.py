import os
import requests
import json
import logging
from typing import List, Dict, Any, Optional

class GitHubModelsClient:
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.endpoint = "https://models.inference.ai.azure.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        if not self.token:
            logging.error("GITHUB_TOKEN environment variable not set")
            print("⚠️ GITHUB_TOKEN not found - AI features will be disabled")
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to GitHub Models
        
        Args:
            messages: List of message objects with 'role' and 'content'
            model: Model name to use
            temperature: Randomness of the response (0-1)
            max_tokens: Maximum tokens in response
            system_prompt: Optional system prompt to prepend
        
        Returns:
            API response containing the generated text
        """
        if not self.token:
            return {"error": "GitHub token not configured"}
            
        try:
            # Prepare messages with optional system prompt
            formatted_messages = []
            
            if system_prompt:
                formatted_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            formatted_messages.extend(messages)
            
            payload = {
                "messages": formatted_messages,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": 1.0
            }
            
            response = requests.post(
                f"{self.endpoint}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"GitHub Models API error: {response.status_code} - {response.text}")
                return {
                    "error": f"API request failed with status {response.status_code}",
                    "details": response.text
                }
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            logging.error(f"Unexpected error in chat_completion: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    def extract_content(self, response: Dict[str, Any]) -> str:
        """
        Extract the content from API response
        
        Args:
            response: API response from chat_completion
            
        Returns:
            Generated text content or error message
        """
        try:
            if "error" in response:
                return f"Error: {response['error']}"
            
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            
            return "No response generated"
            
        except Exception as e:
            return f"Error extracting content: {str(e)}"

# Global AI client instance
try:
    ai_client = GitHubModelsClient()
except Exception as e:
    print(f"⚠️ AI client initialization failed: {e}")
    ai_client = None