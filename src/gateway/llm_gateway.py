"""LLM Gateway - Provider-agnostic interface for LLM calls."""
import time
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from src.core.models import LLMRequest, LLMResponse


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def calculate_cost(self, tokens: int, model: str) -> float:
        """Calculate cost for token usage."""
        pass


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing and demonstration."""
    
    COST_PER_1K_TOKENS = {
        "gpt-4": 0.03,
        "gpt-3.5-turbo": 0.002,
        "claude-3": 0.015,
    }
    
    async def generate(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        """Generate a mock response."""
        # Simulate processing time
        await self._simulate_latency(model)
        
        # Generate mock response
        response_text = f"Mock response to: {prompt[:50]}..."
        tokens = len(prompt.split()) + len(response_text.split())
        
        return {
            "response": response_text,
            "tokens": tokens,
            "model": model
        }
    
    async def _simulate_latency(self, model: str):
        """Simulate realistic latency."""
        import asyncio
        latency_map = {
            "gpt-4": 0.8,
            "gpt-3.5-turbo": 0.3,
            "claude-3": 0.5,
        }
        await asyncio.sleep(latency_map.get(model, 0.5))
    
    def calculate_cost(self, tokens: int, model: str) -> float:
        """Calculate cost based on token usage."""
        cost_per_1k = self.COST_PER_1K_TOKENS.get(model, 0.01)
        return (tokens / 1000) * cost_per_1k


class LLMGateway:
    """Central gateway for all LLM interactions."""
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        self.request_log = []
    
    async def process_request(self, request: LLMRequest) -> LLMResponse:
        """Process an LLM request through the gateway."""
        start_time = time.time()
        
        # Call the LLM provider
        result = await self.provider.generate(
            prompt=request.prompt,
            model=request.model,
            **request.metadata
        )
        
        # Calculate metrics
        latency_ms = (time.time() - start_time) * 1000
        cost = self.provider.calculate_cost(result["tokens"], request.model)
        
        # Create response object
        response = LLMResponse(
            trace_id=request.trace_id,
            response=result["response"],
            model=request.model,
            latency_ms=latency_ms,
            tokens_used=result["tokens"],
            cost_usd=cost
        )
        
        # Log the request
        self.request_log.append({
            "request": request,
            "response": response
        })
        
        return response
    
    def get_request_history(self) -> list:
        """Get all logged requests."""
        return self.request_log
