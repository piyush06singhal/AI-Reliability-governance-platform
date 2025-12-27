"""Risk and Safety Detection Engine."""
import re
from typing import List, Tuple
from src.core.models import LLMRequest, LLMResponse, RiskAssessment


class RiskDetectionEngine:
    """Detects risks and safety issues in LLM interactions."""
    
    # Patterns for detecting various risks
    INJECTION_PATTERNS = [
        r"ignore previous instructions",
        r"disregard all",
        r"forget everything",
        r"system prompt",
        r"you are now",
    ]
    
    UNSAFE_PATTERNS = [
        r"how to (hack|exploit|bypass)",
        r"create (malware|virus)",
        r"illegal (activity|substance)",
    ]
    
    DATA_LEAKAGE_PATTERNS = [
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
        r"\b\d{16}\b",  # Credit card
        r"api[_-]?key",
        r"password\s*[:=]",
    ]
    
    def __init__(self):
        self.risk_history = []
    
    def assess_risk(self, request: LLMRequest, response: LLMResponse) -> RiskAssessment:
        """Perform comprehensive risk assessment."""
        risks = []
        risk_scores = []
        
        # Check for prompt injection
        injection_score, injection_evidence = self._detect_injection(request.prompt)
        if injection_score > 0:
            risks.extend(injection_evidence)
            risk_scores.append(injection_score)
        
        # Check for unsafe content
        unsafe_score, unsafe_evidence = self._detect_unsafe_content(
            request.prompt, response.response
        )
        if unsafe_score > 0:
            risks.extend(unsafe_evidence)
            risk_scores.append(unsafe_score)
        
        # Check for data leakage
        leakage_score, leakage_evidence = self._detect_data_leakage(response.response)
        if leakage_score > 0:
            risks.extend(leakage_evidence)
            risk_scores.append(leakage_score)
        
        # Check for hallucination indicators
        hallucination_score, hallucination_evidence = self._detect_hallucination(response)
        if hallucination_score > 0:
            risks.extend(hallucination_evidence)
            risk_scores.append(hallucination_score)
        
        # Calculate overall risk
        overall_risk = max(risk_scores) if risk_scores else 0.0
        risk_category = self._categorize_risk(overall_risk)
        confidence = self._calculate_confidence(len(risks))
        
        assessment = RiskAssessment(
            trace_id=response.trace_id,
            risk_score=overall_risk,
            risk_category=risk_category,
            evidence=risks,
            confidence=confidence
        )
        
        self.risk_history.append(assessment)
        return assessment
    
    def _detect_injection(self, prompt: str) -> Tuple[float, List[str]]:
        """Detect prompt injection attempts."""
        evidence = []
        prompt_lower = prompt.lower()
        
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, prompt_lower):
                evidence.append(f"Injection pattern detected: {pattern}")
        
        score = min(len(evidence) * 0.3, 1.0)
        return score, evidence
    
    def _detect_unsafe_content(self, prompt: str, response: str) -> Tuple[float, List[str]]:
        """Detect unsafe or policy-violating content."""
        evidence = []
        combined = (prompt + " " + response).lower()
        
        for pattern in self.UNSAFE_PATTERNS:
            if re.search(pattern, combined):
                evidence.append(f"Unsafe content pattern: {pattern}")
        
        score = min(len(evidence) * 0.4, 1.0)
        return score, evidence
    
    def _detect_data_leakage(self, response: str) -> Tuple[float, List[str]]:
        """Detect potential data leakage."""
        evidence = []
        
        for pattern in self.DATA_LEAKAGE_PATTERNS:
            matches = re.findall(pattern, response, re.IGNORECASE)
            if matches:
                evidence.append(f"Potential data leakage: {pattern}")
        
        score = min(len(evidence) * 0.5, 1.0)
        return score, evidence
    
    def _detect_hallucination(self, response: LLMResponse) -> Tuple[float, List[str]]:
        """Detect potential hallucination indicators."""
        evidence = []
        
        # Check for uncertainty markers
        uncertainty_markers = [
            "i think", "maybe", "possibly", "might be",
            "not sure", "unclear", "uncertain"
        ]
        
        response_lower = response.response.lower()
        uncertainty_count = sum(
            1 for marker in uncertainty_markers if marker in response_lower
        )
        
        if uncertainty_count > 2:
            evidence.append(f"High uncertainty markers: {uncertainty_count}")
        
        # Check for contradictions (simple heuristic)
        if "however" in response_lower and "but" in response_lower:
            evidence.append("Potential contradiction detected")
        
        score = min(uncertainty_count * 0.15, 0.6)
        return score, evidence
    
    def _categorize_risk(self, score: float) -> str:
        """Categorize risk level."""
        if score >= 0.7:
            return "CRITICAL"
        elif score >= 0.5:
            return "HIGH"
        elif score >= 0.3:
            return "MEDIUM"
        elif score > 0:
            return "LOW"
        return "SAFE"
    
    def _calculate_confidence(self, evidence_count: int) -> float:
        """Calculate confidence in risk assessment."""
        # More evidence = higher confidence
        return min(0.5 + (evidence_count * 0.1), 0.95)
    
    def get_risk_trends(self) -> dict:
        """Get risk trends over time."""
        if not self.risk_history:
            return {"total": 0, "by_category": {}}
        
        by_category = {}
        for assessment in self.risk_history:
            category = assessment.risk_category
            by_category[category] = by_category.get(category, 0) + 1
        
        return {
            "total": len(self.risk_history),
            "by_category": by_category,
            "avg_risk_score": sum(a.risk_score for a in self.risk_history) / len(self.risk_history)
        }
