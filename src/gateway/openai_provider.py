"""OpenAI LLM Provider Implementation."""
import os
from typing import Dict, Any
import httpx
from src.gateway.llm_gateway import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI API provider implementation."""
    
    COST_PER_1K_TOKENS = {
        "gpt-4": 0.03,
        "gpt-4-turbo": 0.01,
        "gpt-3.5-turbo": 0.002,
    }
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.base_url = "https://api.openai.com/v1"
    
    async def generate(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using OpenAI API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 500),
            "temperature": kwargs.get("temperature", 0.7)
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                
                return {
                    "response": data["choices"][0]["message"]["content"],
                    "tokens": data["usage"]["total_tokens"],
                    "model": model
                }
            except httpx.HTTPStatusError as e:
                # Log the error and provide appropriate response
                error_msg = f"OpenAI API returned {e.response.status_code}"
                print(f"[OpenAI Error] {error_msg}: {e.response.text}")
                
                # Check if it's a content policy violation (400 with specific error)
                try:
                    error_data = e.response.json()
                    error_type = error_data.get("error", {}).get("type", "")
                    
                    if e.response.status_code == 400 and "content_policy" in str(error_data).lower():
                        return {
                            "response": "I cannot assist with that request as it may involve harmful or unethical activities. Please ask something else that I can help with constructively.",
                            "tokens": len(prompt.split()) + 30,
                            "model": model,
                            "error": "content_policy_violation"
                        }
                except:
                    pass
                
                # For other errors, return a generic error message
                return {
                    "response": f"I apologize, but I encountered an error processing your request. Please try again or contact support. (Error: {e.response.status_code})",
                    "tokens": len(prompt.split()) + 30,
                    "model": model,
                    "error": error_msg
                }
            except Exception as e:
                # Fallback to mock response on any other error
                print(f"[OpenAI Error] {str(e)}")
                return {
                    "response": f"I'm a mock AI assistant. Your request was: '{prompt[:100]}...' - In production, this would be processed by a real LLM.",
                    "tokens": len(prompt.split()) + 50,
                    "model": model,
                    "error": str(e)
                }
    
    def calculate_cost(self, tokens: int, model: str) -> float:
        """Calculate cost based on token usage."""
        cost_per_1k = self.COST_PER_1K_TOKENS.get(model, 0.01)
        return (tokens / 1000) * cost_per_1k
