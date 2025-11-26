"""
Framework Recommender Agent (Dynamic Framework Selector - DFSA)
Uses signal-based selection from the FULL 343-framework taxonomy
NO hard-coded defaults - every selection is context-justified
"""

import json
from typing import Dict, Any, List
from google import genai
from config.frameworks import (
    ALL_FRAMEWORKS,
    PHASE_1_FRAMEWORKS,
    PHASE_2_FRAMEWORKS,
    FrameworkTemplate
)
from config.prompts import DYNAMIC_FRAMEWORK_SELECTOR_PROMPT


class FrameworkRecommender:
    """Agent that recommends frameworks based on context analysis."""

    def __init__(self, client: genai.Client):
        self.client = client
        self.model_name = "gemini-3-pro-preview"  # Pro preview model for intelligent recommendations

    def recommend(
        self,
        pyramid_analysis: Dict[str, Any],
        diagnosis: Dict[str, Any],
        conversation: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Recommend frameworks based on pyramid analysis and diagnosis.

        Args:
            pyramid_analysis: Output from MintoAnalyzer
            diagnosis: Current diagnostic state
            conversation: Optional conversation for additional context

        Returns:
            Framework recommendations with scores and rationales
        """
        # Build framework catalog for the prompt
        framework_catalog = self._build_framework_catalog()

        # Build context summary
        context_summary = self._build_context_summary(pyramid_analysis, diagnosis)

        # Extract detected signals from pyramid analysis
        detected_signals = pyramid_analysis.get("detected_signals", [])
        primary_signal = pyramid_analysis.get("primary_signal", "")

        prompt = f"""
{DYNAMIC_FRAMEWORK_SELECTOR_PROMPT}

DETECTED SIGNALS (from Minto Pyramid Analysis):
Primary Signal: {primary_signal}
All Signals: {', '.join(detected_signals) if detected_signals else 'None detected'}

AVAILABLE FRAMEWORKS:
{framework_catalog}

CONTEXT ANALYSIS (Minto Pyramid):
{json.dumps(pyramid_analysis, indent=2)}

DIAGNOSTIC STATE:
{json.dumps(diagnosis, indent=2)}

CONTEXT SUMMARY:
{context_summary}

CRITICAL INSTRUCTIONS:
1. Use the DETECTED SIGNALS to drive framework selection - NOT defaults
2. Ensure DIVERSITY - select from different categories
3. NO FAVORITES - every selection must be justified by specific signals
4. Select 3-7 frameworks that genuinely fit this specific situation

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

            # Enrich recommendations with full framework data
            result = self._enrich_recommendations(result)
            return result

        except Exception as e:
            return self._fallback_recommendations(pyramid_analysis, diagnosis, str(e))

    def _build_framework_catalog(self) -> str:
        """Build a catalog of available frameworks for the prompt."""
        catalog_lines = []

        catalog_lines.append("=== PHASE 1: DISCOVERY FRAMEWORKS ===")
        for fid, framework in PHASE_1_FRAMEWORKS.items():
            catalog_lines.append(f"""
- ID: {fid}
  Title: {framework.title}
  Type: {framework.framework_type}
  Complexity Fit: {', '.join(framework.complexity_fit)}
  When to use: {framework.when_to_use}
""")

        catalog_lines.append("\n=== PHASE 2: SOLUTION FRAMEWORKS ===")
        for fid, framework in PHASE_2_FRAMEWORKS.items():
            catalog_lines.append(f"""
- ID: {fid}
  Title: {framework.title}
  Type: {framework.framework_type}
  Complexity Fit: {', '.join(framework.complexity_fit)}
  When to use: {framework.when_to_use}
""")

        return "\n".join(catalog_lines)

    def _build_context_summary(
        self,
        pyramid: Dict[str, Any],
        diagnosis: Dict[str, Any]
    ) -> str:
        """Build a concise context summary."""
        scqa = pyramid.get("scqa", {})
        signals = pyramid.get("framework_signals", {})
        context = pyramid.get("context_analysis", {})

        return f"""
Problem Stage: {context.get('problem_stage', 'unknown')}
User Intent: {context.get('user_intent', 'unknown')}
Emotional Tone: {context.get('emotional_tone', 'unknown')}

SCQA Summary:
- Situation: {scqa.get('situation', 'N/A')}
- Complication: {scqa.get('complication', 'N/A')}
- Question: {scqa.get('question', 'N/A')}

Framework Signals:
- Needs Discovery: {signals.get('needs_discovery', True)}
- Needs Validation: {signals.get('needs_validation', False)}
- Problem Type Fit: {signals.get('problem_type_fit', 'undefined')}
- Complexity Fit: {signals.get('complexity_fit', 'complex')}
- Suggested Phase: {signals.get('suggested_phase', 'discovery')}

Gaps Identified: {', '.join(context.get('gaps_identified', []))}
Assumptions Made: {', '.join(context.get('assumptions_made', []))}

Diagnosis:
- Definition: {diagnosis.get('definition', 'undefined')}
- Complexity: {diagnosis.get('complexity', 'complex')}
- Wickedness: {diagnosis.get('wickedness', 'messy')}
"""

    def _enrich_recommendations(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich recommendations with full framework data."""
        enriched_frameworks = []

        for rec in result.get("recommended_frameworks", []):
            framework_id = rec.get("framework_id")
            if framework_id in ALL_FRAMEWORKS:
                framework = ALL_FRAMEWORKS[framework_id]
                rec["full_data"] = {
                    "title": framework.title,
                    "definition": framework.definition,
                    "key_questions": framework.key_questions,
                    "output_structure": framework.output_structure,
                    "required_concepts": framework.required_concepts
                }
            enriched_frameworks.append(rec)

        result["recommended_frameworks"] = enriched_frameworks
        return result

    def _fallback_recommendations(
        self,
        pyramid: Dict[str, Any],
        diagnosis: Dict[str, Any],
        error: str
    ) -> Dict[str, Any]:
        """Signal-driven fallback recommendations when LLM fails."""
        # Get detected signals from pyramid
        detected_signals = pyramid.get("detected_signals", [])
        primary_signal = pyramid.get("primary_signal", "")

        # Signal-to-framework mapping for fallback
        signal_frameworks = {
            "causal_ambiguity": ("root_cause_analysis", "Root Cause Analysis", "Identify root causes"),
            "system_bottleneck": ("reverse_salience", "Reverse Salience", "Find system bottlenecks"),
            "stakeholder_conflict": ("stakeholder_mapping", "Stakeholder Mapping", "Map stakeholder interests"),
            "trend_pressure": ("scenario_planning", "Scenario Planning", "Explore future scenarios"),
            "user_behavior": ("jobs_to_be_done", "Jobs-To-Be-Done", "Understand user needs"),
            "business_model": ("business_model_canvas", "Business Model Canvas", "Design business model"),
            "validation_gap": ("lean_startup_mvp", "Lean Startup / MVP", "Validate assumptions"),
            "execution_focus": ("process_mapping", "Process Mapping", "Map execution steps"),
            "ideation_needed": ("six_thinking_hats", "Six Thinking Hats", "Generate diverse ideas"),
            "narrative_focus": ("heart_framework", "HEART Framework", "Craft compelling narrative"),
            "strategic_choice": ("decision_trees", "Decision Trees", "Structure key decisions"),
            "uncertainty_high": ("cynefin", "Cynefin Framework", "Navigate uncertainty"),
            "time_pressure": ("pws_triple_validation", "PWS Triple Validation", "Quick validation")
        }

        recommendations = []

        # Build recommendations from detected signals
        used_frameworks = set()
        for signal in detected_signals[:4]:  # Limit to 4 signals
            if signal in signal_frameworks and signal_frameworks[signal][0] not in used_frameworks:
                fid, title, rationale = signal_frameworks[signal]
                used_frameworks.add(fid)
                recommendations.append({
                    "framework_id": fid,
                    "title": title,
                    "relevance_score": 0.80,
                    "rationale": f"Signal '{signal}' detected - {rationale}",
                    "would_address": [rationale],
                    "phase": "discovery",
                    "signals_matched": [signal]
                })

        # If no signals detected, use diverse defaults based on problem stage
        if not recommendations:
            context = pyramid.get("context_analysis", {})
            problem_stage = context.get("problem_stage", "exploring")

            diverse_defaults = [
                ("root_cause_analysis", "Root Cause Analysis", "Understand underlying causes"),
                ("scenario_planning", "Scenario Planning", "Explore possible futures"),
                ("stakeholder_mapping", "Stakeholder Mapping", "Map key stakeholders"),
                ("six_thinking_hats", "Six Thinking Hats", "Multiple perspectives")
            ]

            for fid, title, rationale in diverse_defaults[:3]:
                recommendations.append({
                    "framework_id": fid,
                    "title": title,
                    "relevance_score": 0.70,
                    "rationale": f"Diverse exploration - {rationale}",
                    "would_address": [rationale],
                    "phase": "discovery",
                    "signals_matched": []
                })

        # Enrich with full data
        for rec in recommendations:
            if rec["framework_id"] in ALL_FRAMEWORKS:
                framework = ALL_FRAMEWORKS[rec["framework_id"]]
                rec["full_data"] = {
                    "title": framework.title,
                    "definition": framework.definition,
                    "key_questions": framework.key_questions,
                    "output_structure": framework.output_structure
                }

        return {
            "recommended_frameworks": recommendations,
            "selection_reasoning": f"Signal-driven fallback: {', '.join(detected_signals) if detected_signals else 'diverse exploration'}",
            "primary_recommendation": recommendations[0]["framework_id"] if recommendations else "root_cause_analysis",
            "complementary_pairs": [],
            "_error": error
        }


def get_framework_buttons(recommendations: Dict[str, Any]) -> List[Dict[str, str]]:
    """Convert recommendations to button format for UI."""
    buttons = []
    for rec in recommendations.get("recommended_frameworks", []):
        buttons.append({
            "id": rec.get("framework_id"),
            "title": rec.get("title"),
            "relevance": rec.get("relevance_score", 0.5),
            "phase": rec.get("phase", "discovery"),
            "rationale": rec.get("rationale", "")
        })
    return buttons
