"""
Framework Consolidator Agent
Merges parallel framework outputs into a unified analysis report
"""

import json
from typing import Dict, Any, List
from google import genai
from google.genai import types


FRAMEWORK_CONSOLIDATOR_PROMPT = """
# Role
You are a Framework Consolidator that synthesizes multiple framework analyses into a unified, coherent report.

# Task
Given outputs from multiple framework analyses (run in parallel), produce a consolidated report that:
1. Synthesizes key findings across all frameworks
2. Identifies overlapping insights (convergence)
3. Highlights contradictions or tensions (divergence)
4. Distills a top-line recommendation
5. Provides a clear narrative for the user

# Consolidation Principles

1. **Convergence is Signal**: When multiple frameworks point to the same insight, that's strong signal.
2. **Divergence is Opportunity**: Contradictions reveal where deeper thinking is needed.
3. **Synthesis over Summary**: Don't just list findings - weave them into a narrative.
4. **Actionable Output**: End with clear next steps, not just observations.

# Constraints
- Output format: Valid JSON only, no markdown
- Maintain citations from all source analyses
- Preserve the strongest insights from each framework
- Identify the 3-5 most important takeaways overall
- Provide a unified recommendation

# Output Instructions
Think step-by-step, then generate ONLY this JSON structure:
{
  "consolidated_report": {
    "executive_summary": "2-3 paragraph synthesis of all framework analyses",
    "top_insights": [
      {
        "insight": "Key finding",
        "source_frameworks": ["framework_1", "framework_2"],
        "confidence": 0.0-1.0,
        "evidence": "Supporting evidence"
      }
    ],
    "convergence_points": [
      {
        "point": "What multiple frameworks agree on",
        "frameworks_aligned": ["framework_1", "framework_2"],
        "implication": "What this means"
      }
    ],
    "divergence_points": [
      {
        "point": "Where frameworks disagree or reveal tension",
        "framework_a": {"name": "framework_1", "view": "Its perspective"},
        "framework_b": {"name": "framework_2", "view": "Its perspective"},
        "resolution": "How to reconcile or use this tension"
      }
    ],
    "opportunities": [
      {
        "opportunity": "Identified opportunity",
        "from_framework": "Which framework surfaced it",
        "priority": "high | medium | low"
      }
    ],
    "risks_and_gaps": [
      {
        "risk_or_gap": "Identified risk or information gap",
        "from_framework": "Which framework surfaced it",
        "mitigation": "How to address"
      }
    ],
    "unified_recommendation": "Clear, actionable recommendation synthesizing all analyses",
    "next_steps": [
      {
        "action": "Specific action to take",
        "rationale": "Why this action",
        "framework_basis": "Which framework(s) support this"
      }
    ]
  },
  "framework_contributions": [
    {
      "framework_id": "framework_1",
      "framework_title": "Framework Name",
      "key_contribution": "What this framework uniquely added",
      "best_insight": "Its strongest insight"
    }
  ],
  "all_citations": [
    {
      "title": "Source title",
      "text": "Relevant excerpt",
      "source": "Origin",
      "used_by_frameworks": ["framework_1"]
    }
  ],
  "overall_confidence": 0.0-1.0,
  "analysis_quality": {
    "frameworks_used": 3,
    "total_insights": 10,
    "convergence_strength": "high | medium | low",
    "gaps_remaining": ["Gap 1", "Gap 2"]
  }
}
"""


class FrameworkConsolidator:
    """Agent that consolidates multiple framework analyses into one report."""

    def __init__(self, client: genai.Client, file_search_store: str = None):
        self.client = client
        self.model_name = "gemini-2.5-pro"  # Pro model for complex synthesis
        self.file_search_store = file_search_store or "fileSearchStores/larry-navigator-neo4j-knowl-30cntohiwvs4"

    def consolidate(
        self,
        framework_results: List[Dict[str, Any]],
        pyramid_analysis: Dict[str, Any],
        conversation: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Consolidate multiple framework analyses into one report.

        Args:
            framework_results: List of outputs from FrameworkExecutor
            pyramid_analysis: Minto Pyramid context analysis
            conversation: Optional conversation for context

        Returns:
            Consolidated analysis report
        """
        if not framework_results:
            return self._empty_consolidation()

        if len(framework_results) == 1:
            # Single framework - minimal consolidation needed
            return self._single_framework_report(framework_results[0])

        # Build the consolidation prompt
        prompt = self._build_consolidation_prompt(
            framework_results, pyramid_analysis, conversation
        )

        try:
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

            # Merge all citations
            result["all_citations"] = self._merge_citations(framework_results)

            return result

        except Exception as e:
            return self._fallback_consolidation(framework_results, str(e))

    def _build_consolidation_prompt(
        self,
        framework_results: List[Dict[str, Any]],
        pyramid: Dict[str, Any],
        conversation: List[Dict[str, str]]
    ) -> str:
        """Build the consolidation prompt."""

        # Format framework results
        frameworks_text = ""
        for result in framework_results:
            if result.get("framework_analysis"):
                analysis = result["framework_analysis"]
                frameworks_text += f"""
=== {result.get('framework_title', 'Unknown')} ===
Summary: {analysis.get('summary', 'N/A')}

Insights:
{json.dumps(analysis.get('insights', []), indent=2)}

Opportunities:
{json.dumps(analysis.get('opportunities', []), indent=2)}

Risks/Gaps:
{json.dumps(analysis.get('risks_or_gaps', []), indent=2)}

Next Steps:
{json.dumps(analysis.get('recommended_next_steps', []), indent=2)}

Confidence: {result.get('confidence_level', 'N/A')}
---
"""

        # Format SCQA context
        scqa = pyramid.get("scqa", {})
        context_text = f"""
CONTEXT (SCQA):
- Situation: {scqa.get('situation', 'N/A')}
- Complication: {scqa.get('complication', 'N/A')}
- Question: {scqa.get('question', 'N/A')}
- Direction: {scqa.get('answer_direction', 'N/A')}
"""

        return f"""
{FRAMEWORK_CONSOLIDATOR_PROMPT}

{context_text}

FRAMEWORK ANALYSES TO CONSOLIDATE:
{frameworks_text}

Number of frameworks: {len(framework_results)}
Framework names: {', '.join(r.get('framework_title', 'Unknown') for r in framework_results)}

Consolidate these analyses into a unified report.
Respond with ONLY the JSON object, no markdown formatting.
"""

    def _merge_citations(self, framework_results: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Merge citations from all framework results."""
        all_citations = []
        seen_titles = set()

        for result in framework_results:
            for citation in result.get("citations", []):
                title = citation.get("title", "")
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    citation["used_by_frameworks"] = [result.get("framework_id", "unknown")]
                    all_citations.append(citation)
                elif title in seen_titles:
                    # Add framework to existing citation
                    for existing in all_citations:
                        if existing.get("title") == title:
                            existing.setdefault("used_by_frameworks", []).append(
                                result.get("framework_id", "unknown")
                            )
                            break

        return all_citations

    def _empty_consolidation(self) -> Dict[str, Any]:
        """Return empty consolidation when no frameworks provided."""
        return {
            "consolidated_report": {
                "executive_summary": "No frameworks were selected for analysis.",
                "top_insights": [],
                "convergence_points": [],
                "divergence_points": [],
                "opportunities": [],
                "risks_and_gaps": [],
                "unified_recommendation": "Select one or more frameworks to analyze your problem.",
                "next_steps": []
            },
            "framework_contributions": [],
            "all_citations": [],
            "overall_confidence": 0.0,
            "analysis_quality": {
                "frameworks_used": 0,
                "total_insights": 0,
                "convergence_strength": "low",
                "gaps_remaining": ["No analysis performed"]
            }
        }

    def _single_framework_report(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create consolidation from single framework."""
        analysis = result.get("framework_analysis", {})

        return {
            "consolidated_report": {
                "executive_summary": analysis.get("summary", "Single framework analysis completed."),
                "top_insights": [
                    {
                        "insight": insight,
                        "source_frameworks": [result.get("framework_id")],
                        "confidence": result.get("confidence_level", 0.7),
                        "evidence": "From framework analysis"
                    }
                    for insight in analysis.get("insights", [])[:5]
                ],
                "convergence_points": [],
                "divergence_points": [],
                "opportunities": [
                    {
                        "opportunity": opp,
                        "from_framework": result.get("framework_title"),
                        "priority": "medium"
                    }
                    for opp in analysis.get("opportunities", [])
                ],
                "risks_and_gaps": [
                    {
                        "risk_or_gap": risk,
                        "from_framework": result.get("framework_title"),
                        "mitigation": "Further analysis needed"
                    }
                    for risk in analysis.get("risks_or_gaps", [])
                ],
                "unified_recommendation": f"Based on {result.get('framework_title')} analysis: " +
                    (analysis.get("recommended_next_steps", ["Continue analysis"])[0] if analysis.get("recommended_next_steps") else "Continue analysis"),
                "next_steps": [
                    {
                        "action": step,
                        "rationale": "From framework analysis",
                        "framework_basis": result.get("framework_title")
                    }
                    for step in analysis.get("recommended_next_steps", [])
                ]
            },
            "framework_contributions": [
                {
                    "framework_id": result.get("framework_id"),
                    "framework_title": result.get("framework_title"),
                    "key_contribution": analysis.get("summary", "Framework analysis"),
                    "best_insight": analysis.get("insights", ["N/A"])[0] if analysis.get("insights") else "N/A"
                }
            ],
            "all_citations": result.get("citations", []),
            "overall_confidence": result.get("confidence_level", 0.7),
            "analysis_quality": {
                "frameworks_used": 1,
                "total_insights": len(analysis.get("insights", [])),
                "convergence_strength": "low",
                "gaps_remaining": result.get("needs_more_info", [])
            }
        }

    def _fallback_consolidation(
        self,
        framework_results: List[Dict[str, Any]],
        error: str
    ) -> Dict[str, Any]:
        """Fallback when consolidation fails."""
        # Extract basic info from each framework
        all_insights = []
        all_opportunities = []
        all_risks = []

        for result in framework_results:
            analysis = result.get("framework_analysis", {})
            all_insights.extend(analysis.get("insights", []))
            all_opportunities.extend(analysis.get("opportunities", []))
            all_risks.extend(analysis.get("risks_or_gaps", []))

        return {
            "consolidated_report": {
                "executive_summary": f"Consolidated analysis from {len(framework_results)} frameworks. " +
                    f"Key themes: {', '.join(all_insights[:3]) if all_insights else 'Analysis in progress'}",
                "top_insights": [
                    {
                        "insight": insight,
                        "source_frameworks": ["multiple"],
                        "confidence": 0.6,
                        "evidence": "From framework analyses"
                    }
                    for insight in all_insights[:5]
                ],
                "convergence_points": [],
                "divergence_points": [],
                "opportunities": [
                    {"opportunity": opp, "from_framework": "Multiple", "priority": "medium"}
                    for opp in all_opportunities[:3]
                ],
                "risks_and_gaps": [
                    {"risk_or_gap": risk, "from_framework": "Multiple", "mitigation": "TBD"}
                    for risk in all_risks[:3]
                ],
                "unified_recommendation": "Review the individual framework analyses for detailed insights.",
                "next_steps": [
                    {"action": "Review framework outputs", "rationale": "Consolidation incomplete", "framework_basis": "All"}
                ]
            },
            "framework_contributions": [
                {
                    "framework_id": r.get("framework_id", "unknown"),
                    "framework_title": r.get("framework_title", "Unknown"),
                    "key_contribution": r.get("framework_analysis", {}).get("summary", "Analysis provided"),
                    "best_insight": r.get("framework_analysis", {}).get("insights", ["N/A"])[0] if r.get("framework_analysis", {}).get("insights") else "N/A"
                }
                for r in framework_results
            ],
            "all_citations": self._merge_citations(framework_results),
            "overall_confidence": 0.5,
            "analysis_quality": {
                "frameworks_used": len(framework_results),
                "total_insights": len(all_insights),
                "convergence_strength": "unknown",
                "gaps_remaining": ["Full consolidation incomplete"]
            },
            "_error": error
        }
