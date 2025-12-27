"""Guardrails and Policy Enforcement Layer."""
from typing import Optional
from src.core.models import LLMRequest, LLMResponse, RiskAssessment, PolicyDecision


class Policy:
    """Represents a governance policy."""
    
    def __init__(self, policy_id: str, name: str, risk_threshold: float, action: str):
        self.policy_id = policy_id
        self.name = name
        self.risk_threshold = risk_threshold
        self.action = action  # "allow", "block", "rewrite", "fallback"
        self.enabled = True
    
    def should_enforce(self, risk_assessment: RiskAssessment) -> bool:
        """Check if policy should be enforced."""
        return self.enabled and risk_assessment.risk_score >= self.risk_threshold


class GuardrailsEngine:
    """Enforces policies and guardrails on LLM interactions."""
    
    def __init__(self):
        self.policies = self._initialize_default_policies()
        self.enforcement_history = []
    
    def _initialize_default_policies(self) -> dict:
        """Initialize default policies."""
        return {
            "critical_risk_block": Policy(
                policy_id="critical_risk_block",
                name="Block Critical Risk Responses",
                risk_threshold=0.7,
                action="block"
            ),
            "high_risk_fallback": Policy(
                policy_id="high_risk_fallback",
                name="Fallback for High Risk",
                risk_threshold=0.6,  # Increased from 0.5 to reduce false positives
                action="fallback"
            ),
            "medium_risk_rewrite": Policy(
                policy_id="medium_risk_rewrite",
                name="Rewrite Medium Risk Prompts",
                risk_threshold=0.3,
                action="rewrite"
            ),
        }
    
    def enforce(
        self,
        request: LLMRequest,
        response: LLMResponse,
        risk_assessment: RiskAssessment
    ) -> PolicyDecision:
        """Enforce policies based on risk assessment."""
        
        # Check policies in order of severity
        for policy in sorted(
            self.policies.values(),
            key=lambda p: p.risk_threshold,
            reverse=True
        ):
            if policy.should_enforce(risk_assessment):
                decision = self._apply_policy(policy, request, response, risk_assessment)
                self.enforcement_history.append(decision)
                return decision
        
        # No policy triggered - allow
        decision = PolicyDecision(
            trace_id=response.trace_id,
            action="allow",
            policy_id="default_allow",
            reason="No policy violations detected"
        )
        self.enforcement_history.append(decision)
        return decision
    
    def _apply_policy(
        self,
        policy: Policy,
        request: LLMRequest,
        response: LLMResponse,
        risk_assessment: RiskAssessment
    ) -> PolicyDecision:
        """Apply a specific policy."""
        
        if policy.action == "block":
            return PolicyDecision(
                trace_id=response.trace_id,
                action="block",
                policy_id=policy.policy_id,
                reason=f"Blocked due to {risk_assessment.risk_category} risk",
                modified_response="[Response blocked by safety policy]"
            )
        
        elif policy.action == "fallback":
            return PolicyDecision(
                trace_id=response.trace_id,
                action="fallback",
                policy_id=policy.policy_id,
                reason=f"Fallback triggered for {risk_assessment.risk_category} risk",
                modified_response="I cannot assist with that request as it may involve harmful or unethical activities. Please ask something else that I can help with constructively."
            )
        
        elif policy.action == "rewrite":
            # In production, this would use a safer model or prompt rewriting
            return PolicyDecision(
                trace_id=response.trace_id,
                action="rewrite",
                policy_id=policy.policy_id,
                reason=f"Prompt rewritten due to {risk_assessment.risk_category} risk",
                modified_response=response.response  # Placeholder
            )
        
        return PolicyDecision(
            trace_id=response.trace_id,
            action="allow",
            policy_id=policy.policy_id,
            reason="Policy check passed"
        )
    
    def add_policy(self, policy: Policy):
        """Add a new policy."""
        self.policies[policy.policy_id] = policy
    
    def remove_policy(self, policy_id: str):
        """Remove a policy."""
        if policy_id in self.policies:
            del self.policies[policy_id]
    
    def toggle_policy(self, policy_id: str):
        """Enable/disable a policy."""
        if policy_id in self.policies:
            self.policies[policy_id].enabled = not self.policies[policy_id].enabled
    
    def get_enforcement_stats(self) -> dict:
        """Get enforcement statistics."""
        if not self.enforcement_history:
            return {"total": 0, "by_action": {}}
        
        by_action = {}
        for decision in self.enforcement_history:
            action = decision.action
            by_action[action] = by_action.get(action, 0) + 1
        
        return {
            "total": len(self.enforcement_history),
            "by_action": by_action
        }
