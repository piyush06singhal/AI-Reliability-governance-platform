"""Audit and Compliance Logger."""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from src.core.models import AuditLog, LLMRequest, LLMResponse, RiskAssessment, PolicyDecision


class AuditLogger:
    """Maintains immutable audit logs for compliance."""
    
    def __init__(self, log_dir: str = "audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.in_memory_logs = []
    
    def log_interaction(
        self,
        request: LLMRequest,
        response: LLMResponse,
        risk_assessment: Optional[RiskAssessment] = None,
        policy_decision: Optional[PolicyDecision] = None
    ):
        """Log a complete LLM interaction."""
        audit_entry = AuditLog(
            trace_id=response.trace_id,
            event_type="llm_interaction",
            user_id=request.user_id,
            prompt=request.prompt,
            response=response.response,
            risk_assessment=risk_assessment,
            policy_decision=policy_decision
        )
        
        # Store in memory
        self.in_memory_logs.append(audit_entry)
        
        # Persist to disk
        self._persist_log(audit_entry)
    
    def _persist_log(self, audit_entry: AuditLog):
        """Persist log entry to disk."""
        # Create daily log file
        date_str = audit_entry.timestamp.strftime("%Y-%m-%d")
        log_file = self.log_dir / f"audit_{date_str}.jsonl"
        
        # Append to JSONL file
        with open(log_file, "a") as f:
            f.write(audit_entry.model_dump_json() + "\n")
    
    def get_logs(
        self,
        trace_id: Optional[str] = None,
        user_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AuditLog]:
        """Query audit logs with filters."""
        filtered = self.in_memory_logs
        
        if trace_id:
            filtered = [log for log in filtered if log.trace_id == trace_id]
        
        if user_id:
            filtered = [log for log in filtered if log.user_id == user_id]
        
        if start_date:
            filtered = [log for log in filtered if log.timestamp >= start_date]
        
        if end_date:
            filtered = [log for log in filtered if log.timestamp <= end_date]
        
        return filtered
    
    def export_compliance_report(self, output_file: str):
        """Export compliance-ready report."""
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "total_interactions": len(self.in_memory_logs),
            "logs": [log.model_dump() for log in self.in_memory_logs]
        }
        
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2, default=str)
    
    def get_audit_summary(self) -> dict:
        """Get summary of audit logs."""
        if not self.in_memory_logs:
            return {
                "total_logs": 0,
                "unique_users": 0,
                "risk_events": 0,
                "policy_enforcements": 0
            }
        
        unique_users = len(set(log.user_id for log in self.in_memory_logs if log.user_id))
        risk_events = sum(1 for log in self.in_memory_logs if log.risk_assessment)
        policy_enforcements = sum(
            1 for log in self.in_memory_logs
            if log.policy_decision and log.policy_decision.action != "allow"
        )
        
        return {
            "total_logs": len(self.in_memory_logs),
            "unique_users": unique_users,
            "risk_events": risk_events,
            "policy_enforcements": policy_enforcements
        }
