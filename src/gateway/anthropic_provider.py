"""Anthropic Claude LLM Provider Implementation."""
import os
from typing import Dict, Any
import httpx
from src.gateway.llm_gateway import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider implementation."""
    
    COST_PER_1K_TOKENS = {
        "claude-3": 0.015,
        "claude-3-opus": 0.015,
        "claude-3-sonnet": 0.003,
        "claude-3-haiku": 0.00025,
    }
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not provided")
        
        self.base_url = "https://api.anthropic.com/v1"
    
    async def generate(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        """Generate a response using Anthropic API."""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        # Map generic model names to Anthropic model names
        model_map = {
            "claude-3": "claude-3-sonnet-20240229",
            "claude-3-opus": "claude-3-opus-20240229",
            "claude-3-sonnet": "claude-3-sonnet-20240229",
            "claude-3-haiku": "claude-3-haiku-20240307"
        }
        
        anthropic_model = model_map.get(model, "claude-3-sonnet-20240229")
        
        payload = {
            "model": anthropic_model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 500)
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/messages",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                
                return {
                    "response": data["content"][0]["text"],
                    "tokens": data["usage"]["input_tokens"] + data["usage"]["output_tokens"],
                    "model": model
                }
            except Exception as e:
                # Fallback to mock response on error
                return {
                    "response": f"[Anthropic API Error: {str(e)}] Mock response to: {prompt[:50]}...",
                    "tokens": len(prompt.split()) + 50,
                    "model": model
                }
    
    def calculate_cost(self, tokens: int, model: str) -> float:
        """Calculate cost based on token usage."""
        cost_per_1k = self.COST_PER_1K_TOKENS.get(model, 0.003)
        return (tokens / 1000) * cost_per_1k
