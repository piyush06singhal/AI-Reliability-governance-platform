"""Cost and Performance Monitoring."""
from typing import List, Dict
from datetime import datetime, timedelta
from src.core.models import LLMResponse


class CostMonitor:
    """Monitors cost and performance metrics."""
    
    def __init__(self):
        self.metrics_history = []
        self.cost_alerts = []
    
    def record_metrics(self, response: LLMResponse):
        """Record metrics for a response."""
        self.metrics_history.append({
            "trace_id": response.trace_id,
            "model": response.model,
            "tokens": response.tokens_used,
            "cost": response.cost_usd,
            "latency": response.latency_ms,
            "timestamp": response.timestamp
        })
        
        # Check for anomalies
        self._check_cost_anomaly(response)
    
    def _check_cost_anomaly(self, response: LLMResponse):
        """Check for cost anomalies."""
        # Simple threshold-based detection
        if response.cost_usd > 0.5:  # $0.50 per request
            self.cost_alerts.append({
                "trace_id": response.trace_id,
                "cost": response.cost_usd,
                "reason": "High cost per request",
                "timestamp": response.timestamp
            })
    
    def get_total_cost(self, hours: int = 24) -> float:
        """Get total cost for the last N hours."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent = [m for m in self.metrics_history if m["timestamp"] >= cutoff]
        return sum(m["cost"] for m in recent)
    
    def get_cost_by_model(self) -> Dict[str, float]:
        """Get cost breakdown by model."""
        by_model = {}
        for metric in self.metrics_history:
            model = metric["model"]
            by_model[model] = by_model.get(model, 0.0) + metric["cost"]
        return by_model
    
    def get_avg_latency(self) -> float:
        """Get average latency."""
        if not self.metrics_history:
            return 0.0
        return sum(m["latency"] for m in self.metrics_history) / len(self.metrics_history)
    
    def get_token_usage(self) -> Dict[str, int]:
        """Get token usage by model."""
        by_model = {}
        for metric in self.metrics_history:
            model = metric["model"]
            by_model[model] = by_model.get(model, 0) + metric["tokens"]
        return by_model
    
    def get_cost_trends(self, hours: int = 24) -> List[Dict]:
        """Get cost trends over time."""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        recent = [m for m in self.metrics_history if m["timestamp"] >= cutoff]
        
        # Group by hour
        hourly = {}
        for metric in recent:
            hour = metric["timestamp"].replace(minute=0, second=0, microsecond=0)
            if hour not in hourly:
                hourly[hour] = {"cost": 0.0, "requests": 0}
            hourly[hour]["cost"] += metric["cost"]
            hourly[hour]["requests"] += 1
        
        return [
            {"timestamp": k, "cost": v["cost"], "requests": v["requests"]}
            for k, v in sorted(hourly.items())
        ]
    
    def get_high_cost_prompts(self, top_n: int = 10) -> List[Dict]:
        """Get the most expensive prompts."""
        sorted_metrics = sorted(
            self.metrics_history,
            key=lambda m: m["cost"],
            reverse=True
        )
        return sorted_metrics[:top_n]
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance summary."""
        if not self.metrics_history:
            return {
                "total_requests": 0,
                "total_cost": 0.0,
                "avg_latency": 0.0,
                "total_tokens": 0
            }
        
        return {
            "total_requests": len(self.metrics_history),
            "total_cost": sum(m["cost"] for m in self.metrics_history),
            "avg_latency": self.get_avg_latency(),
            "total_tokens": sum(m["tokens"] for m in self.metrics_history),
            "cost_by_model": self.get_cost_by_model(),
            "alerts": len(self.cost_alerts)
        }
