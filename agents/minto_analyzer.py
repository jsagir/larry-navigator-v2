"""
Minto Pyramid Context Analyzer Agent
Decomposes conversation context using the Minto Pyramid Principle
With enhanced signal detection for Dynamic Framework Selection
"""

import json
from typing import Dict, Any, List
from google import genai
from config.prompts import MINTO_PYRAMID_PROMPT


# Enhanced prompt that builds on the base prompt with additional analysis
ENHANCED_MINTO_PROMPT = MINTO_PYRAMID_PROMPT + """

# Additional Context Analysis
Also include these fields in your analysis:
{
  "context_analysis": {
    "problem_stage": "exploring | defining | validating | solving",
    "user_intent": "What the user is trying to accomplish",
    "key_entities": ["Companies", "Technologies", "Markets", "People mentioned"],
    "assumptions_made": ["Explicit or implicit assumptions"],
    "gaps_identified": ["Information or clarity gaps"],
    "emotional_tone": "Confident | Uncertain | Frustrated | Curious | etc."
  }
}

IMPORTANT: The "detected_signals" array drives framework selection.
Be thorough in detecting ALL applicable signals from this list:
- causal_ambiguity: User doesn't know WHY something is happening
- system_bottleneck: Progress blocked by constraints, uneven performance
- stakeholder_conflict: Multiple actors with different goals
- trend_pressure: Market/technology changes creating pressure
- user_behavior: Focus on customer needs, jobs, pain points
- business_model: Revenue, pricing, value capture questions
- validation_gap: Untested assumptions, need for evidence
- execution_focus: How to implement, build, deliver
- ideation_needed: Stuck, need new ideas
- narrative_focus: Pitching, storytelling, communication
- strategic_choice: Trade-offs, direction decisions
- uncertainty_high: Unknown unknowns, novel territory
- time_pressure: Urgency, deadlines
"""


class MintoAnalyzer:
    """Agent that analyzes conversation context using Minto Pyramid Principle."""

    def __init__(self, client: genai.Client):
        self.client = client
        self.model_name = "gemini-3-pro-preview"  # Pro preview model for deep analysis

    def analyze(
        self,
        conversation: List[Dict[str, str]],
        diagnosis: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Analyze the full conversation context using Minto Pyramid.

        Args:
            conversation: Full chat history
            diagnosis: Current diagnostic state from 4 agents

        Returns:
            Structured pyramid analysis with framework signals
        """
        if len(conversation) < 1:
            return self._default_pyramid()

        # Build conversation text
        conv_text = self._format_conversation(conversation)

        # Include diagnostic context if available
        diag_text = ""
        if diagnosis:
            diag_text = f"""
CURRENT DIAGNOSIS:
- Definition Level: {diagnosis.get('definition', 'undefined')}
- Complexity: {diagnosis.get('complexity', 'complex')}
- Risk-Uncertainty: {diagnosis.get('risk_uncertainty', 0.5)}
- Wickedness: {diagnosis.get('wickedness', 'messy')}
"""

        prompt = f"""
{ENHANCED_MINTO_PROMPT}

{diag_text}

FULL CONVERSATION TO ANALYZE:
{conv_text}

Analyze this conversation and produce the structured pyramid breakdown with signal detection.
The detected_signals array is CRITICAL - it drives which frameworks will be recommended.
Respond with ONLY the JSON object, no markdown formatting.
"""

        try:
            # Direct API call - Gemini handles its own timeout
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]

            result = json.loads(text.strip())
            return result

        except Exception as e:
            return self._fallback_pyramid(conversation, str(e))

    def _format_conversation(self, conversation: List[Dict[str, str]]) -> str:
        """Format entire conversation for analysis."""
        formatted = []
        for i, msg in enumerate(conversation):
            role = "USER" if msg["role"] == "user" else "LARRY"
            content = msg["content"][:800]  # Limit per message
            formatted.append(f"[{i+1}] {role}: {content}")
        return "\n\n".join(formatted)

    def _default_pyramid(self) -> Dict[str, Any]:
        """Return default pyramid for new conversations."""
        return {
            "pyramid": {
                "governing_thought": "Conversation just started - exploring the problem space",
                "key_arguments": []
            },
            "scqa": {
                "situation": "New conversation initiated",
                "complication": "Problem not yet articulated",
                "question": "What problem is the user trying to solve?",
                "answer_direction": "Need more information"
            },
            "context_analysis": {
                "problem_stage": "exploring",
                "user_intent": "Unknown - conversation just started",
                "key_entities": [],
                "assumptions_made": [],
                "gaps_identified": ["Problem definition", "Context", "Constraints"],
                "emotional_tone": "Neutral"
            },
            "framework_signals": {
                "needs_discovery": True,
                "needs_validation": False,
                "problem_type_fit": "undefined",
                "complexity_fit": "complex",
                "suggested_phase": "discovery"
            }
        }

    def _fallback_pyramid(self, conversation: List[Dict[str, str]], error: str) -> Dict[str, Any]:
        """Fallback pyramid when analysis fails."""
        # Extract basic info from conversation
        user_messages = [m["content"] for m in conversation if m["role"] == "user"]
        latest_user = user_messages[-1] if user_messages else ""

        return {
            "pyramid": {
                "governing_thought": f"User is exploring: {latest_user[:100]}...",
                "key_arguments": [
                    {
                        "argument": "Conversation in progress",
                        "evidence": [f"User messages: {len(user_messages)}"]
                    }
                ]
            },
            "scqa": {
                "situation": "Conversation ongoing",
                "complication": "Analysis needed",
                "question": latest_user[:200] if latest_user else "What's the problem?",
                "answer_direction": "Requires further exploration"
            },
            "context_analysis": {
                "problem_stage": "exploring",
                "user_intent": "Seeking guidance",
                "key_entities": [],
                "assumptions_made": [],
                "gaps_identified": ["Full context analysis"],
                "emotional_tone": "Unknown"
            },
            "framework_signals": {
                "needs_discovery": True,
                "needs_validation": False,
                "problem_type_fit": "undefined",
                "complexity_fit": "complex",
                "suggested_phase": "discovery"
            },
            "_error": error
        }


def get_scqa_summary(pyramid: Dict[str, Any]) -> str:
    """Get a concise SCQA summary from pyramid analysis."""
    scqa = pyramid.get("scqa", {})
    return f"""
**Situation:** {scqa.get('situation', 'N/A')}
**Complication:** {scqa.get('complication', 'N/A')}
**Question:** {scqa.get('question', 'N/A')}
**Direction:** {scqa.get('answer_direction', 'N/A')}
"""
