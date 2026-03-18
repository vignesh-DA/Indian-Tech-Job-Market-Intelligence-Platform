"""
Chatbot engine for career assistant responses.
This module intentionally keeps dependencies minimal so it works in serverless deploys.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class ChatbotEngine:
    """Lightweight intent-based chatbot engine used by /api/chat."""

    def __init__(self) -> None:
        self.intent_keywords = {
            "salary_info": ["salary", "pay", "compensation", "ctc", "package"],
            "skill_trends": ["skills", "skill", "trending", "in-demand", "learn"],
            "company_info": ["company", "companies", "hiring", "employer"],
            "role_info": ["role", "job", "position", "career", "transition"],
            "location_info": ["location", "city", "bangalore", "hyderabad", "mumbai", "delhi", "pune"],
            "greeting": ["hello", "hi", "hey"],
        }

    def detect_intent(self, user_message: str) -> str:
        """Detect a basic intent from keyword matching."""
        msg = (user_message or "").lower()

        for intent, keywords in self.intent_keywords.items():
            if any(k in msg for k in keywords):
                return intent

        return "general"

    def generate_response(
        self,
        user_message: str,
        user_profile: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        recommendations: Optional[List[Dict[str, Any]]] = None,
        use_gemini: bool = True,
        user_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate chatbot response in the shape expected by server.py.
        """
        try:
            profile = user_profile or {}
            role = str(profile.get("role", "job seeker"))
            experience = str(profile.get("experience", "mid-level"))
            location = str(profile.get("location", "India"))
            name = (user_name or profile.get("name") or "there").strip()

            intent = self.detect_intent(user_message)
            category = "career_assistant"
            confidence = 0.86

            if intent == "greeting":
                message = (
                    f"Hi {name}. I can help with salaries, skills, companies, role planning, and location trends "
                    f"for the Indian tech market."
                )

            elif intent == "salary_info":
                message = (
                    f"For a {experience} {role} in {location}, salary typically depends on skills, company tier, and interview performance. "
                    "Ask for a specific role and city, and I will give a tighter range with next-step advice."
                )

            elif intent == "skill_trends":
                message = (
                    "High-demand areas include cloud, backend engineering, AI/ML, and data engineering. "
                    "Share your target role and I will provide a focused learning roadmap."
                )

            elif intent == "company_info":
                top_hint = ""
                if recommendations:
                    first_company = recommendations[0].get("company") if isinstance(recommendations[0], dict) else None
                    if first_company:
                        top_hint = f" You already have matches that include {first_company}."

                message = (
                    "You should target a mix of product companies, strong startups, and MNCs to balance growth and stability."
                    + top_hint
                )

            elif intent == "role_info":
                message = (
                    f"Given your profile ({experience}, {location}), we can map a role transition path with skills, projects, and application targets. "
                    "Tell me your current role and your target role."
                )

            elif intent == "location_info":
                message = (
                    "Top hiring hubs remain Bangalore, Hyderabad, Pune, Mumbai, and Delhi NCR. "
                    "If you share one city, I can give role and salary focus areas for that location."
                )

            else:
                message = (
                    "I can help with salary benchmarks, skill roadmaps, company targeting, and job-market insights. "
                    "Try asking: 'skills for backend developer', 'salary for data scientist in Bangalore', or 'top companies hiring now'."
                )

            return {
                "success": True,
                "message": message,
                "intent": intent,
                "category": category,
                "confidence": confidence,
            }

        except Exception as exc:
            return {
                "success": False,
                "message": "I ran into an issue generating a response. Please try again.",
                "error": str(exc),
                "intent": "error",
                "category": "system",
                "confidence": 0.0,
            }
