"""
Rapid Response Agent System - Main Implementation
Multi-agent system for crisis management in mission-driven organizations

Built for the Kaggle Agents Intensive Capstone Project - Agents for Good Track
"""

import google.generativeai as genai
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import asyncio
from typing import List, Dict, Any
import logging

class Issue:
    """Represents a detected issue requiring potential rapid response"""
    
    def __init__(self, title: str, content: str, source: str, urgency: str = "medium"):
        self.id = f"issue_{int(time.time())}"
        self.title = title
        self.content = content
        self.source = source
        self.urgency = urgency
        self.timestamp = datetime.now()
        self.mai_score = None
        self.status = "detected"
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'urgency': self.urgency,
            'timestamp': self.timestamp.isoformat(),
            'mai_score': self.mai_score,
            'status': self.status
        }

class MAIScore:
    """Mission Alignment Intelligence Score"""
    
    def __init__(self, mission_alignment: int, impact_growth: int, risk_evaluation: int):
        self.mission_alignment = mission_alignment  # 0-15 points
        self.impact_growth = impact_growth          # 0-15 points  
        self.risk_evaluation = risk_evaluation      # 0-15 points
        self.total_score = mission_alignment + impact_growth + risk_evaluation
        
    def get_recommendation(self):
        if self.total_score >= 30:
            return "TIER_2_HUMAN_REVIEW"
        elif self.total_score >= 15:
            return "ENHANCED_MONITORING" 
        else:
            return "DOCUMENTATION_ONLY"

class MAIScoringAgent:
    """Agent that applies Mission Alignment Intelligence scoring using Gemini"""
    
    def __init__(self, manifesto: dict, api_key: str = None):
        self.manifesto = manifesto
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.decision_history = []
        
    def calculate_full_mai_score(self, issue: Issue) -> MAIScore:
        """Calculate complete MAI score for an issue"""
        print(f"🔍 Analyzing issue: {issue.title}")
        
        mission_score = self.score_mission_alignment(issue)
        impact_score = self.score_impact_growth(issue)
        risk_score = self.score_risk_evaluation(issue)
        
        mai_score = MAIScore(mission_score, impact_score, risk_score)
        
        # Store in memory for pattern learning
        self.decision_history.append({
            'issue_id': issue.id,
            'timestamp': datetime.now(),
            'mai_score': mai_score.total_score,
            'breakdown': {
                'mission': mission_score,
                'impact': impact_score, 
                'risk': risk_score
            }
        })
        
        print(f"📊 MAI Score: {mai_score.total_score}/45")
        print(f"   Mission: {mission_score}/15, Impact: {impact_score}/15, Risk: {risk_score}/15")
        print(f"   Recommendation: {mai_score.get_recommendation()}")
        
        return mai_score
    
    def score_mission_alignment(self, issue: Issue) -> int:
        """Score 0-15 based on alignment with organizational mission"""
        prompt = f"""
        Analyze this issue for mission alignment:
        
        Issue: {issue.title}
        Content: {issue.content}
        
        Our Core Principles: {', '.join(self.manifesto['core_principles'])}
        Strategic Priorities: {', '.join(self.manifesto['strategic_priorities'])}
        
        Score 0-15 points for mission alignment where:
        - 0-5: Low alignment, tangentially related 
        - 6-10: Moderate alignment, clearly relevant
        - 11-15: High alignment, directly impacts core mission
        
        Respond with just the number (0-15).
        """
        
        try:
            response = self.model.generate_content(prompt)
            score = int(response.text.strip().split()[0])
            return min(max(score, 0), 15)
        except:
            return self._fallback_mission_score(issue)
    
    def score_impact_growth(self, issue: Issue) -> int:
        """Score 0-15 based on potential impact and community growth"""
        prompt = f"""
        Score this issue 0-15 points for impact potential:
        
        Issue: {issue.title}
        Content: {issue.content}
        
        Consider community growth, reach, and engagement sustainability.
        Respond with just the number (0-15).
        """
        
        try:
            response = self.model.generate_content(prompt)
            score = int(response.text.strip().split()[0])
            return min(max(score, 0), 15)
        except:
            return self._fallback_impact_score(issue)
    
    def score_risk_evaluation(self, issue: Issue) -> int:
        """Score 0-15 based on risk factors (higher score = lower risk)"""
        prompt = f"""
        Score this issue 0-15 points for risk (higher = lower risk):
        
        Issue: {issue.title}
        Content: {issue.content}
        
        Consider stakeholder perception and reputational risks.
        Respond with just the number (0-15).
        """
        
        try:
            response = self.model.generate_content(prompt)
            score = int(response.text.strip().split()[0])
            return min(max(score, 0), 15)
        except:
            return self._fallback_risk_score(issue)
    
    def _fallback_mission_score(self, issue: Issue) -> int:
        """Fallback scoring if API fails"""
        keywords = ['privacy', 'security', 'rights', 'accessibility', 'ethics']
        content_lower = (issue.title + " " + issue.content).lower()
        matches = sum(1 for keyword in keywords if keyword in content_lower)
        return min(matches * 3, 15)
    
    def _fallback_impact_score(self, issue: Issue) -> int:
        urgency_scores = {'low': 5, 'medium': 10, 'high': 15}
        return urgency_scores.get(issue.urgency, 10)
    
    def _fallback_risk_score(self, issue: Issue) -> int:
        return 8  # Default medium-low risk


class MonitorAgent:
    """Agent that monitors for emerging issues requiring rapid response"""
    
    def __init__(self):
        self.keywords = [
            'privacy breach', 'security vulnerability', 'data leak', 
            'ai ethics', 'platform accountability', 'digital rights',
            'accessibility', 'open source', 'regulation'
        ]
    
    def simulate_web_monitoring(self) -> List[Issue]:
        """Simulate real-time web monitoring"""
        print("🔍 Monitoring web sources for emerging issues...")
        
        sample_issues = [
            {
                "title": "Major social media platform changes privacy policy without user notice",
                "content": "Platform updated terms to allow broader data sharing with third parties, affecting 2 billion users globally.",
                "source": "Privacy Watch Blog",
                "urgency": "high"
            },
            {
                "title": "New AI model shows concerning bias in hiring recommendations", 
                "content": "Research reveals AI hiring tool consistently recommends male candidates over equally qualified female candidates.",
                "source": "AI Ethics Journal",
                "urgency": "medium"
            },
            {
                "title": "Government proposes new internet regulation framework",
                "content": "Proposed legislation would require platforms to implement content filtering, raising free expression concerns.",
                "source": "Tech Policy News",
                "urgency": "medium"
            }
        ]
        
        detected_issues = []
        for issue_data in sample_issues:
            if self._is_relevant_issue(issue_data):
                issue = Issue(**issue_data)
                detected_issues.append(issue)
                print(f"   📥 Detected: {issue.title[:50]}...")
        
        return detected_issues
    
    def _is_relevant_issue(self, issue_data: dict) -> bool:
        """Check if issue matches monitoring criteria"""
        content = (issue_data["title"] + " " + issue_data["content"]).lower()
        keyword_matches = sum(1 for keyword in self.keywords if keyword in content)
        is_urgent = issue_data["urgency"] in ["medium", "high"]
        return keyword_matches > 0 or is_urgent


class ConflictResolutionAgent:
    """Agent implementing Lightning Conflict Resolution Protocol"""
    
    def __init__(self):
        self.resolution_timeout = 900  # 15 minutes max
    
    def detect_channel_conflict(self, new_issue: Issue) -> dict:
        """Detect competing priorities requiring resolution"""
        # Simulate scheduled content
        scheduled_content = {
            'type': 'fundraising_email',
            'title': 'Year-end Giving Campaign',
            'scheduled_time': datetime.now() + timedelta(hours=2),
            'priority': 'high'
        }
        
        time_diff = abs((scheduled_content['scheduled_time'] - datetime.now()).total_seconds() / 3600)
        
        if time_diff < 6:  # Conflict within 6 hours
            conflict = {
                'conflict_id': f"conflict_{int(time.time())}",
                'new_issue': new_issue,
                'conflicting_content': scheduled_content,
                'severity': self._assess_conflict_severity(new_issue, scheduled_content),
                'detected_at': datetime.now()
            }
            print(f"⚠️  Channel conflict detected")
            return conflict
        return None
    
    def execute_lightning_protocol(self, conflict: dict) -> dict:
        """Execute 4-minute Lightning Protocol"""
        print(f"\n🚨 LIGHTNING PROTOCOL ACTIVATED")
        print(f"   Conflict ID: {conflict['conflict_id']}")
        print(f"   Severity: {conflict['severity']}")
        
        # Rapid decision based on severity and urgency
        if conflict['severity'] == 'CRITICAL':
            decision = {
                'action': 'SEGMENT_AND_STAGGER',
                'rationale': 'High-priority issue requires immediate response with audience segmentation.'
            }
        else:
            decision = {
                'action': 'DELAY_SECONDARY',
                'rationale': 'Delay scheduled content to avoid message collision.'
            }
        
        print(f"✅ Conflict resolved! Decision: {decision['action']}")
        
        return {
            'conflict_id': conflict['conflict_id'],
            'resolution_time': datetime.now(),
            'decision': decision
        }
    
    def _assess_conflict_severity(self, issue: Issue, content: dict) -> str:
        """Assess conflict severity"""
        severity_score = 0
        if content.get('priority') == 'high':
            severity_score += 2
        if issue.urgency == 'high':
            severity_score += 3
        
        return 'CRITICAL' if severity_score >= 4 else 'MODERATE'


class DecisionSupportAgent:
    """Agent providing decision support and routing"""
    
    def route_issue(self, issue: Issue, mai_score: MAIScore) -> dict:
        """Route issue based on MAI score"""
        print(f"🎯 Routing decision for: {issue.title[:50]}...")
        
        recommendation = mai_score.get_recommendation()
        routing_decision = {
            'issue_id': issue.id,
            'mai_score': mai_score.total_score,
            'routing': recommendation,
            'priority_level': self._determine_priority(mai_score, issue),
            'estimated_response_time': self._estimate_response_time(recommendation, issue.urgency),
            'decision_timestamp': datetime.now()
        }
        
        print(f"   📊 MAI Score: {mai_score.total_score}/45")
        print(f"   🎯 Routing: {recommendation}")
        print(f"   ⏰ Est. response time: {routing_decision['estimated_response_time']}")
        
        return routing_decision
    
    def _determine_priority(self, mai_score: MAIScore, issue: Issue) -> str:
        """Determine priority level"""
        if mai_score.total_score >= 35 and issue.urgency == 'high':
            return 'P0 - CRITICAL'
        elif mai_score.total_score >= 25 or issue.urgency == 'high':
            return 'P1 - HIGH'
        elif mai_score.total_score >= 15:
            return 'P2 - MEDIUM'
        else:
            return 'P3 - LOW'
    
    def _estimate_response_time(self, routing: str, urgency: str) -> str:
        """Estimate response time"""
        if routing == 'TIER_2_HUMAN_REVIEW':
            return '2-4 hours' if urgency == 'high' else '4-8 hours'
        elif routing == 'ENHANCED_MONITORING':
            return '8-24 hours'
        else:
            return '24-48 hours'


class RapidResponseSystem:
    """Main orchestrator for the multi-agent rapid response system"""
    
    def __init__(self, manifesto: dict, api_key: str = None):
        self.monitor = MonitorAgent()
        self.scorer = MAIScoringAgent(manifesto, api_key)
        self.conflict_resolver = ConflictResolutionAgent()
        self.decision_support = DecisionSupportAgent()
        self.system_metrics = {'issues_processed': 0, 'conflicts_resolved': 0}
    
    def run_full_cycle(self) -> dict:
        """Execute complete rapid response cycle"""
        print("🚀 RAPID RESPONSE SYSTEM - FULL CYCLE EXECUTION")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # Monitor for issues
        detected_issues = self.monitor.simulate_web_monitoring()
        
        cycle_results = {
            'timestamp': start_time,
            'issues_detected': len(detected_issues),
            'issues_processed': [],
            'conflicts_resolved': []
        }
        
        # Process each issue
        for issue in detected_issues[:3]:  # Process first 3 for demo
            print(f"\n{'='*40}")
            
            # Score the issue
            mai_score = self.scorer.calculate_full_mai_score(issue)
            
            # Check for conflicts
            conflict = self.conflict_resolver.detect_channel_conflict(issue)
            if conflict:
                resolution = self.conflict_resolver.execute_lightning_protocol(conflict)
                cycle_results['conflicts_resolved'].append(resolution)
            
            # Route the issue
            routing_decision = self.decision_support.route_issue(issue, mai_score)
            
            cycle_results['issues_processed'].append({
                'issue': issue,
                'mai_score': mai_score.total_score,
                'routing': routing_decision
            })
        
        end_time = datetime.now()
        cycle_time = (end_time - start_time).total_seconds()
        cycle_results['total_cycle_time'] = f"{cycle_time:.1f} seconds"
        
        print(f"\n🏁 CYCLE COMPLETE - Total time: {cycle_results['total_cycle_time']}")
        return cycle_results


# Example usage
if __name__ == "__main__":
    # Sample manifesto for demonstration
    SAMPLE_MANIFESTO = {
        "core_principles": [
            "Digital privacy and security",
            "Open and accessible technology", 
            "User empowerment and education",
            "Inclusive digital rights"
        ],
        "strategic_priorities": [
            "Privacy protection",
            "Platform accountability",
            "Digital literacy", 
            "Ethical AI development"
        ]
    }
    
    # Initialize and run system
    system = RapidResponseSystem(SAMPLE_MANIFESTO)
    results = system.run_full_cycle()
