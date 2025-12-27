"""Main Governance Platform Orchestrator."""
import os
from src.core.models import LLMRequest, LLMResponse
from src.gateway.llm_gateway import LLMGateway, MockLLMProvider
from src.gateway.openai_provider import OpenAIProvider
from src.gateway.anthropic_provider import AnthropicProvider
from src.detection.risk_engine import RiskDetectionEngine
from src.policy.guardrails import GuardrailsEngine
from src.monitoring.cost_monitor import CostMonitor
from src.audit.audit_logger import AuditLogger
from src.feedback.feedback_engine import FeedbackEngine


class GovernancePlatform:
    """Central orchestrator for the AI Governance Platform."""
    
    def __init__(self, use_real_llm: bool = True):
        # Initialize all components
        # Try to use real LLM providers if API keys are available
        if use_real_llm:
            try:
                # Try OpenAI first
                if os.getenv("OPENAI_API_KEY"):
                    provider = OpenAIProvider()
                    print("✅ Using OpenAI provider")
                elif os.getenv("ANTHROPIC_API_KEY"):
                    provider = AnthropicProvider()
                    print("✅ Using Anthropic provider")
                else:
                    provider = MockLLMProvider()
                    print("⚠️ No API keys found, using Mock provider")
            except Exception as e:
                provider = MockLLMProvider()
                print(f"⚠️ Error initializing real provider: {e}, using Mock provider")
        else:
            provider = MockLLMProvider()
            print("ℹ️ Using Mock provider (use_real_llm=False)")
        
        self.gateway = LLMGateway(provider)
        self.risk_engine = RiskDetectionEngine()
        self.guardrails = GuardrailsEngine()
        self.cost_monitor = CostMonitor()
        self.audit_logger = AuditLogger()
        self.feedback_engine = FeedbackEngine()
    
    async def process_llm_request(self, request: LLMRequest) -> dict:
        """
        Process an LLM request through the complete governance pipeline.
        
        Returns a dict with:
        - response: The final response (potentially modified)
        - risk_assessment: Risk analysis
        - policy_decision: Policy enforcement decision
        - allowed: Whether the response was allowed
        """
        # Step 1: Route through LLM Gateway
        llm_response = await self.gateway.process_request(request)
        
        # Step 2: Assess Risk
        risk_assessment = self.risk_engine.assess_risk(request, llm_response)
        
        # Step 3: Enforce Policies
        policy_decision = self.guardrails.enforce(request, llm_response, risk_assessment)
        
        # Step 4: Monitor Cost & Performance
        self.cost_monitor.record_metrics(llm_response)
        
        # Step 5: Audit Log
        self.audit_logger.log_interaction(
            request=request,
            response=llm_response,
            risk_assessment=risk_assessment,
            policy_decision=policy_decision
        )
        
        # Step 6: Determine final response
        final_response = llm_response.response
        allowed = True
        
        if policy_decision.action in ["block", "fallback", "rewrite"]:
            final_response = policy_decision.modified_response or llm_response.response
            allowed = policy_decision.action != "block"
        
        return {
            "trace_id": llm_response.trace_id,
            "response": final_response,
            "original_response": llm_response.response,
            "risk_assessment": risk_assessment,
            "policy_decision": policy_decision,
            "allowed": allowed,
            "cost_usd": llm_response.cost_usd,
            "latency_ms": llm_response.latency_ms,
            "tokens_used": llm_response.tokens_used
        }
    
    def get_system_health(self) -> dict:
        """Get overall system health metrics."""
        return {
            "risk_trends": self.risk_engine.get_risk_trends(),
            "enforcement_stats": self.guardrails.get_enforcement_stats(),
            "performance": self.cost_monitor.get_performance_summary(),
            "audit_summary": self.audit_logger.get_audit_summary(),
            "feedback_summary": self.feedback_engine.get_feedback_summary()
        }
    
    def get_all_interactions(self) -> list:
        """Get all logged interactions."""
        return self.gateway.get_request_history()
