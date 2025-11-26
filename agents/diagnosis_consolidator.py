"""
Diagnosis Consolidator Agent
Combines all diagnostic outputs with File Search context
"""

import json
from typing import Dict, Any, List, Optional
from google import genai
from google.genai import types
from config.prompts import DIAGNOSIS_CONSOLIDATOR_PROMPT

from agents.definition_classifier import DefinitionClassifier
from agents.complexity_assessor import ComplexityAssessor
from agents.risk_uncertainty import RiskUncertaintyEvaluator
from agents.wickedness_classifier import WicknessClassifier


class DiagnosisConsolidator:
    """
    Orchestrates all diagnostic agents and consolidates results.
    Uses File Search to ground diagnosis in PWS frameworks.
    """

    def __init__(self, client: genai.Client, file_search_store: str = None):
        self.client = client
        self.model_name = "gemini-2.5-pro"  # Gemini 2.5 Pro for complex consolidation
        self.file_search_store = file_search_store or "fileSearchStores/larry-navigator-neo4j-knowl-30cntohiwvs4"

        # Initialize sub-agents
        self.definition_agent = DefinitionClassifier(client)
        self.complexity_agent = ComplexityAssessor(client)
        self.risk_agent = RiskUncertaintyEvaluator(client)
        self.wickedness_agent = WicknessClassifier(client)

    def diagnose(
        self,
        conversation: List[Dict[str, str]],
        previous_diagnosis: Dict[str, Any] = None,
        citations: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Run all diagnostic agents with full context and consolidate results.

        Args:
            conversation: Full chat history with messages
            previous_diagnosis: Previous diagnosis for comparison
            citations: Citations from File Search (knowledge base context)

        Returns:
            Consolidated diagnosis with UI updates and research recommendations
        """
        if len(conversation) < 2:
            return self._default_diagnosis()

        # Build rich context from conversation (including any citations stored in messages)
        context = self._build_context(conversation, citations)

        # Run all agents with context
        definition_result = self.definition_agent.classify(conversation, context)
        complexity_result = self.complexity_agent.assess(conversation, context)
        risk_result = self.risk_agent.evaluate(conversation, context)
        wickedness_result = self.wickedness_agent.classify(conversation, context)

        # Consolidate using LLM with File Search for framework matching
        consolidated = self._consolidate_with_file_search(
            definition_result,
            complexity_result,
            risk_result,
            wickedness_result,
            conversation,
            context,
            previous_diagnosis
        )

        return consolidated

    def _build_context(
        self,
        conversation: List[Dict],
        citations: List[Dict] = None
    ) -> Dict[str, Any]:
        """Build rich context from conversation and citations."""

        # Extract all citations from conversation messages
        all_citations = citations or []
        for msg in conversation:
            if msg.get("citations"):
                all_citations.extend(msg["citations"])

        # Build problem summary from conversation
        user_messages = [m["content"] for m in conversation if m["role"] == "user"]
        assistant_messages = [m["content"] for m in conversation if m["role"] == "assistant"]

        # Extract key themes
        context = {
            "message_count": len(conversation),
            "user_statements": user_messages[-3:],  # Last 3 user messages
            "assistant_responses": assistant_messages[-2:],  # Last 2 responses
            "citations": [
                {"title": c.get("title", ""), "text": c.get("text", "")[:200]}
                for c in all_citations[:5]  # Top 5 citations
            ],
            "conversation_summary": self._summarize_conversation(conversation)
        }

        return context

    def _summarize_conversation(self, conversation: List[Dict]) -> str:
        """Create a brief summary of the conversation."""
        if len(conversation) < 2:
            return "Conversation just started."

        # Get first user message (initial problem statement)
        first_user = next((m["content"][:300] for m in conversation if m["role"] == "user"), "")

        # Get latest exchange
        latest_user = ""
        latest_assistant = ""
        for m in reversed(conversation):
            if m["role"] == "user" and not latest_user:
                latest_user = m["content"][:200]
            elif m["role"] == "assistant" and not latest_assistant:
                latest_assistant = m["content"][:200]
            if latest_user and latest_assistant:
                break

        return f"Initial: {first_user}\nLatest exchange - User: {latest_user}\nAssistant: {latest_assistant}"

    def _default_diagnosis(self) -> Dict[str, Any]:
        """Return default diagnosis for new conversations."""
        return {
            "profile": {
                "name": "Just Starting",
                "summary": "Let's explore your challenge together.",
                "diagnosis": {
                    "definition": {"level": "undefined", "confidence": 0.3},
                    "complexity": {"level": "complex", "confidence": 0.3},
                    "knowability": {"position": 0.5, "label": "balanced"},
                    "wickedness": {"level": "messy", "characteristics_count": 0}
                },
                "overall_difficulty": "medium",
                "recommended_approach": "Analysis",
                "framework_matches": ["Problem Discovery", "Design Thinking"]
            },
            "research": {
                "recommended": False,
                "urgency": "low",
                "reason": "Continue the conversation first",
                "suggested_focus": []
            },
            "ui_updates": {
                "definition": "undefined",
                "complexity": "complex",
                "risk_uncertainty": 0.5,
                "wickedness": "messy",
                "show_research_prompt": False,
                "research_prompt_text": ""
            }
        }

    def _consolidate_with_file_search(
        self,
        definition: Dict,
        complexity: Dict,
        risk: Dict,
        wickedness: Dict,
        conversation: List[Dict],
        context: Dict,
        previous: Dict = None
    ) -> Dict[str, Any]:
        """Consolidate using File Search for framework matching."""

        agent_outputs = {
            "definition": definition,
            "complexity": complexity,
            "risk_uncertainty": risk,
            "wickedness": wickedness
        }

        # Build conversation text
        conv_text = "\n".join([
            f"{m['role'].upper()}: {m['content'][:400]}"
            for m in conversation[-6:]
        ])

        # Build context text
        context_text = f"""
CONVERSATION CONTEXT:
- Messages: {context.get('message_count', 0)}
- User focus: {' | '.join(context.get('user_statements', [])[:2])}

KNOWLEDGE BASE CITATIONS:
{json.dumps(context.get('citations', []), indent=2) if context.get('citations') else 'None yet'}

CONVERSATION SUMMARY:
{context.get('conversation_summary', 'N/A')}
"""

        prompt = f"""
{DIAGNOSIS_CONSOLIDATOR_PROMPT}

AGENT DIAGNOSTIC OUTPUTS:
{json.dumps(agent_outputs, indent=2)}

{context_text}

RECENT CONVERSATION:
{conv_text}

{"PREVIOUS DIAGNOSIS (for comparison):" + json.dumps(previous.get('ui_updates', {}), indent=2) if previous else "No previous diagnosis."}

Based on the conversation context, knowledge base citations, and agent outputs:
1. Determine the appropriate problem profile
2. Match relevant PWS frameworks from the knowledge base
3. Recommend the best approach for this type of problem
4. Decide if research would help

Respond with ONLY the JSON object, no markdown formatting.
"""

        try:
            # Use File Search to ground framework recommendations
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[
                        types.Tool(
                            file_search=types.FileSearch(
                                file_search_store_names=[self.file_search_store]
                            )
                        )
                    ]
                )
            )

            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]

            result = json.loads(text.strip())

            # Ensure required fields exist
            if "ui_updates" not in result:
                result["ui_updates"] = {
                    "definition": definition.get("definition_level", "undefined"),
                    "complexity": complexity.get("complexity_level", "complex"),
                    "risk_uncertainty": risk.get("position", 0.5),
                    "wickedness": wickedness.get("wickedness_level", "messy"),
                    "show_research_prompt": True,
                    "research_prompt_text": "🔍 Research this problem"
                }

            return result

        except Exception as e:
            # Fallback consolidation
            return self._fallback_consolidation(definition, complexity, risk, wickedness, str(e))

    def _fallback_consolidation(
        self,
        definition: Dict,
        complexity: Dict,
        risk: Dict,
        wickedness: Dict,
        error: str = ""
    ) -> Dict[str, Any]:
        """Fallback when consolidation fails."""

        def_level = definition.get("definition_level", "undefined")
        comp_level = complexity.get("complexity_level", "complex")
        risk_pos = risk.get("position", 0.5)
        wick_level = wickedness.get("wickedness_level", "messy")

        # Determine profile name based on dimensions
        if def_level == "undefined" and comp_level in ["complex", "chaotic"]:
            profile_name = "Early Exploration"
            approach = "Sense-making"
            frameworks = ["Beautiful Questions", "Problem Discovery"]
        elif def_level == "well-defined" and comp_level == "simple":
            profile_name = "Ready to Execute"
            approach = "Execution"
            frameworks = ["Solution Validation", "MVP Testing"]
        elif def_level == "ill-defined" and comp_level == "complicated":
            profile_name = "Needs Analysis"
            approach = "Analysis"
            frameworks = ["Root Cause Analysis", "Hypothesis Testing"]
        elif wick_level in ["complex", "wicked"]:
            profile_name = "Systemic Challenge"
            approach = "Experimentation"
            frameworks = ["Systems Thinking", "Stakeholder Mapping"]
        else:
            profile_name = "Innovation Challenge"
            approach = "Analysis"
            frameworks = ["Design Thinking", "Jobs to Be Done"]

        return {
            "profile": {
                "name": profile_name,
                "summary": f"Based on current analysis of your challenge.",
                "diagnosis": {
                    "definition": {"level": def_level, "confidence": definition.get("confidence", 0.5)},
                    "complexity": {"level": comp_level, "confidence": complexity.get("confidence", 0.5)},
                    "knowability": {"position": risk_pos, "label": risk.get("label", "balanced")},
                    "wickedness": {"level": wick_level, "characteristics_count": len(wickedness.get("wicked_characteristics", []))}
                },
                "overall_difficulty": "medium",
                "recommended_approach": approach,
                "framework_matches": frameworks
            },
            "research": {
                "recommended": def_level == "undefined" or wick_level in ["complex", "wicked"],
                "urgency": "medium" if def_level == "undefined" else "low",
                "reason": "Additional context would help clarify the problem",
                "suggested_focus": ["Market validation", "Similar cases"]
            },
            "ui_updates": {
                "definition": def_level,
                "complexity": comp_level,
                "risk_uncertainty": risk_pos,
                "wickedness": wick_level,
                "show_research_prompt": def_level == "undefined",
                "research_prompt_text": "🔍 Research this problem"
            }
        }
