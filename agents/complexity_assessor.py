"""
Complexity Assessor Agent
Determines: Simple | Complicated | Complex | Chaotic (Cynefin)
"""

import json
from typing import Dict, Any, List
from google import genai
from config.prompts import COMPLEXITY_ASSESSOR_PROMPT


class ComplexityAssessor:
    """Agent that assesses problem complexity using Cynefin."""

    def __init__(self, client: genai.Client):
        self.client = client
        self.model_name = "gemini-2.5-flash"  # Flash model for fast classification

    def assess(self, conversation: List[Dict[str, str]], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze conversation and assess complexity.

        Args:
            conversation: Chat history
            context: Optional context with citations and summary

        Returns:
            {
                "complexity_level": "simple"|"complicated"|"complex"|"chaotic",
                "confidence": 0.0-1.0,
                "evidence": [...],
                "reasoning": str
            }
        """
        conv_text = self._format_conversation(conversation)

        # Build context section
        context_section = ""
        if context:
            citations = context.get("citations", [])
            if citations:
                context_section = f"\nKNOWLEDGE BASE CONTEXT:\n{json.dumps(citations[:3], indent=2)}\n"

        prompt = f"""
{COMPLEXITY_ASSESSOR_PROMPT}
{context_section}
CONVERSATION TO ANALYZE:
{conv_text}

Respond with ONLY the JSON object, no markdown formatting.
"""

        try:
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
            return {
                "complexity_level": "complex",
                "confidence": 0.3,
                "evidence": [],
                "reasoning": f"Unable to assess: {str(e)}"
            }

    def _format_conversation(self, conversation: List[Dict[str, str]]) -> str:
        formatted = []
        for msg in conversation[-10:]:
            role = "USER" if msg["role"] == "user" else "LARRY"
            formatted.append(f"{role}: {msg['content'][:500]}")
        return "\n\n".join(formatted)
