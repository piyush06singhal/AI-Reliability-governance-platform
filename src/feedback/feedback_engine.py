"""Feedback and Continuous Improvement Engine."""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
from src.core.models import LLMResponse, RiskAssessment


class FeedbackEntry:
    """Represents user feedback on an LLM response."""
    
    def __init__(
        self,
        trace_id: str,
        rating: int,  # 1-5 stars
        feedback_type: str,  # "positive", "negative", "neutral"
        comment: Optional[str] = None,
        tags: List[str] = None
    ):
        self.trace_id = trace_id
        self.rating = rating
        self.feedback_type = feedback_type
        self.comment = comment
        self.tags = tags or []
        self.timestamp = datetime.utcnow()


class DriftDetector:
    """Detects behavior drift in LLM responses over time."""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.baseline_metrics = None
        self.drift_alerts = []
    
    def set_baseline(self, metrics: Dict[str, float]):
        """Set baseline metrics for comparison."""
        self.baseline_metrics = metrics
    
    def detect_drift(self, current_metrics: Dict[str, float]) -> Dict:
        """Detect drift from baseline metrics."""
        if not self.baseline_metrics:
            return {"drift_detected": False, "reason": "No baseline set"}
        
        drifts = {}
        drift_detected = False
        
        for metric, current_value in current_metrics.items():
            if metric in self.baseline_metrics:
                baseline_value = self.baseline_metrics[metric]
                
                # Calculate percentage change
                if baseline_value != 0:
                    change_pct = abs((current_value - baseline_value) / baseline_value) * 100
                    
                    # Drift threshold: 20% change
                    if change_pct > 20:
                        drifts[metric] = {
                            "baseline": baseline_value,
                            "current": current_value,
                            "change_pct": change_pct,
                            "drift": True
                        }
                        drift_detected = True
                    else:
                        drifts[metric] = {
                            "baseline": baseline_value,
                            "current": current_value,
                            "change_pct": change_pct,
                            "drift": False
                        }
        
        if drift_detected:
            self.drift_alerts.append({
                "timestamp": datetime.utcnow(),
                "drifts": drifts
            })
        
        return {
            "drift_detected": drift_detected,
            "drifts": drifts,
            "timestamp": datetime.utcnow()
        }


class ThresholdOptimizer:
    """Automatically adjusts risk thresholds based on feedback."""
    
    def __init__(self):
        self.adjustment_history = []
        self.current_thresholds = {
            "critical": 0.7,
            "high": 0.5,
            "medium": 0.3
        }
    
    def optimize_thresholds(
        self,
        feedback_data: List[Dict],
        risk_assessments: List[RiskAssessment]
    ) -> Dict[str, float]:
        """Optimize thresholds based on feedback and outcomes."""
        
        # Analyze false positives and false negatives
        false_positives = 0
        false_negatives = 0
        total_feedback = len(feedback_data)
        
        if total_feedback == 0:
            return self.current_thresholds
        
        for feedback in feedback_data:
            # If user rated highly but we flagged as risky -> false positive
            if feedback.get("rating", 3) >= 4 and feedback.get("risk_score", 0) > 0.5:
                false_positives += 1
            
            # If user rated poorly but we didn't flag -> false negative
            if feedback.get("rating", 3) <= 2 and feedback.get("risk_score", 0) < 0.3:
                false_negatives += 1
        
        # Adjust thresholds
        fp_rate = false_positives / total_feedback if total_feedback > 0 else 0
        fn_rate = false_negatives / total_feedback if total_feedback > 0 else 0
        
        adjustments = {}
        
        # If too many false positives, increase thresholds (be less strict)
        if fp_rate > 0.2:
            adjustments["critical"] = min(self.current_thresholds["critical"] + 0.05, 0.9)
            adjustments["high"] = min(self.current_thresholds["high"] + 0.05, 0.7)
            adjustments["medium"] = min(self.current_thresholds["medium"] + 0.05, 0.5)
        
        # If too many false negatives, decrease thresholds (be more strict)
        elif fn_rate > 0.2:
            adjustments["critical"] = max(self.current_thresholds["critical"] - 0.05, 0.5)
            adjustments["high"] = max(self.current_thresholds["high"] - 0.05, 0.3)
            adjustments["medium"] = max(self.current_thresholds["medium"] - 0.05, 0.1)
        else:
            adjustments = self.current_thresholds.copy()
        
        # Record adjustment
        if adjustments != self.current_thresholds:
            self.adjustment_history.append({
                "timestamp": datetime.utcnow(),
                "old_thresholds": self.current_thresholds.copy(),
                "new_thresholds": adjustments.copy(),
                "fp_rate": fp_rate,
                "fn_rate": fn_rate
            })
            self.current_thresholds = adjustments
        
        return self.current_thresholds


class FeedbackEngine:
    """Main feedback and continuous improvement engine."""
    
    def __init__(self):
        self.feedback_entries = []
        self.drift_detector = DriftDetector()
        self.threshold_optimizer = ThresholdOptimizer()
        self.quality_metrics_history = []
    
    def add_feedback(
        self,
        trace_id: str,
        rating: int,
        feedback_type: str,
        comment: Optional[str] = None,
        tags: List[str] = None
    ):
        """Add user feedback for an interaction."""
        entry = FeedbackEntry(trace_id, rating, feedback_type, comment, tags)
        self.feedback_entries.append(entry)
    
    def calculate_quality_metrics(self) -> Dict[str, float]:
        """Calculate current quality metrics."""
        if not self.feedback_entries:
            return {
                "avg_rating": 0.0,
                "positive_rate": 0.0,
                "negative_rate": 0.0,
                "total_feedback": 0
            }
        
        ratings = [f.rating for f in self.feedback_entries]
        feedback_types = [f.feedback_type for f in self.feedback_entries]
        
        metrics = {
            "avg_rating": np.mean(ratings),
            "positive_rate": feedback_types.count("positive") / len(feedback_types),
            "negative_rate": feedback_types.count("negative") / len(feedback_types),
            "total_feedback": len(self.feedback_entries)
        }
        
        # Store in history
        self.quality_metrics_history.append({
            "timestamp": datetime.utcnow(),
            "metrics": metrics
        })
        
        return metrics
    
    def detect_drift(self) -> Dict:
        """Detect drift in quality metrics."""
        current_metrics = self.calculate_quality_metrics()
        
        # Set baseline if not set (use first 50 entries)
        if not self.drift_detector.baseline_metrics and len(self.feedback_entries) >= 50:
            baseline = self.calculate_baseline_metrics()
            self.drift_detector.set_baseline(baseline)
        
        if self.drift_detector.baseline_metrics:
            return self.drift_detector.detect_drift(current_metrics)
        
        return {"drift_detected": False, "reason": "Insufficient data for baseline"}
    
    def calculate_baseline_metrics(self) -> Dict[str, float]:
        """Calculate baseline metrics from first N entries."""
        if len(self.feedback_entries) < 50:
            return {}
        
        baseline_entries = self.feedback_entries[:50]
        ratings = [f.rating for f in baseline_entries]
        feedback_types = [f.feedback_type for f in baseline_entries]
        
        return {
            "avg_rating": np.mean(ratings),
            "positive_rate": feedback_types.count("positive") / len(feedback_types),
            "negative_rate": feedback_types.count("negative") / len(feedback_types)
        }
    
    def optimize_thresholds(self, risk_assessments: List[RiskAssessment]) -> Dict[str, float]:
        """Optimize risk thresholds based on feedback."""
        # Prepare feedback data with risk scores
        feedback_data = []
        for entry in self.feedback_entries[-100:]:  # Last 100 entries
            # Find corresponding risk assessment
            risk_score = 0.0
            for assessment in risk_assessments:
                if assessment.trace_id == entry.trace_id:
                    risk_score = assessment.risk_score
                    break
            
            feedback_data.append({
                "trace_id": entry.trace_id,
                "rating": entry.rating,
                "risk_score": risk_score
            })
        
        return self.threshold_optimizer.optimize_thresholds(feedback_data, risk_assessments)
    
    def get_feedback_summary(self) -> Dict:
        """Get summary of all feedback."""
        if not self.feedback_entries:
            return {
                "total": 0,
                "by_type": {},
                "avg_rating": 0.0,
                "recent_feedback": []
            }
        
        by_type = defaultdict(int)
        for entry in self.feedback_entries:
            by_type[entry.feedback_type] += 1
        
        ratings = [f.rating for f in self.feedback_entries]
        
        return {
            "total": len(self.feedback_entries),
            "by_type": dict(by_type),
            "avg_rating": np.mean(ratings),
            "recent_feedback": [
                {
                    "trace_id": f.trace_id[:8] + "...",
                    "rating": f.rating,
                    "type": f.feedback_type,
                    "comment": f.comment,
                    "timestamp": f.timestamp
                }
                for f in self.feedback_entries[-10:]
            ]
        }
    
    def get_quality_trends(self, days: int = 7) -> List[Dict]:
        """Get quality trends over time."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        # Group by day
        daily_metrics = defaultdict(list)
        for entry in self.feedback_entries:
            if entry.timestamp >= cutoff:
                day = entry.timestamp.date()
                daily_metrics[day].append(entry)
        
        trends = []
        for day, entries in sorted(daily_metrics.items()):
            ratings = [e.rating for e in entries]
            types = [e.feedback_type for e in entries]
            
            trends.append({
                "date": day,
                "avg_rating": np.mean(ratings),
                "count": len(entries),
                "positive_rate": types.count("positive") / len(types) if types else 0
            })
        
        return trends
    
    def get_drift_alerts(self) -> List[Dict]:
        """Get all drift alerts."""
        return self.drift_detector.drift_alerts
    
    def get_threshold_history(self) -> List[Dict]:
        """Get threshold adjustment history."""
        return self.threshold_optimizer.adjustment_history
