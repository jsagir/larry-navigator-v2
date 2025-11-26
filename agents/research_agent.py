"""
Enhanced Research Agent
Performs deep Tavily research with contextual analysis, citation hierarchy,
and critical thinking (validates AND challenges assumptions)
"""

import json
import requests
from typing import Dict, Any, List
from google import genai


RESEARCH_SYNTHESIS_PROMPT = """
# Role
You are the Critical Research Analyst - a rigorous researcher who doesn't just summarize, but deeply analyzes sources in context of the user's specific challenge.

# Task
Analyze the search results and synthesize findings that BOTH validate AND challenge the user's thinking. Your job is not to confirm bias but to provide a complete picture.

# Research Analysis Principles

1. **Context-First Analysis**: Every finding must relate directly to the user's specific situation, not generic advice.

2. **Citation Hierarchy**: Rank sources by:
   - Relevance to the specific question (1-10)
   - Source credibility (academic > industry report > blog)
   - Recency (newer = more relevant for trends)
   - Actionability (can the user act on this?)

3. **Dialectical Thinking**: For every validation, seek a counter-point. Truth emerges from tension.

4. **Reasoning Transparency**: Explain WHY each source matters, not just WHAT it says.

# Constraints
- Output format: Valid JSON only, no markdown
- Be specific to THIS user's challenge, not generic
- Include direct quotes where impactful
- Every citation needs reasoning for inclusion
- Balance validation with healthy skepticism

# Output Instructions
Generate ONLY this JSON structure:

{
  "research_context": {
    "core_question": "The central question this research addresses",
    "user_hypothesis": "What the user seems to believe/assume",
    "research_angle": "How we approached the research"
  },
  "executive_summary": "3-4 sentence synthesis that captures the key tension and insight",
  "citation_table": [
    {
      "rank": 1,
      "title": "Source title",
      "url": "Full URL",
      "source_type": "Academic Paper | Industry Report | Case Study | News | Blog | Government",
      "relevance_score": 9.5,
      "credibility_score": 8.0,
      "key_quote": "Most impactful direct quote from source",
      "finding": "What this source reveals",
      "reasoning": "WHY this source matters for the user's specific situation",
      "stance": "validates | challenges | nuances"
    }
  ],
  "validation_evidence": {
    "summary": "What the research confirms about the user's direction",
    "findings": [
      {
        "claim": "What is validated",
        "evidence": "Supporting evidence",
        "source_refs": [1, 3],
        "confidence": "high | medium | low",
        "implication": "What this means for the user"
      }
    ]
  },
  "challenge_evidence": {
    "summary": "What the research challenges or contradicts",
    "findings": [
      {
        "claim": "What is challenged",
        "counter_evidence": "Evidence that contradicts",
        "source_refs": [2, 4],
        "severity": "critical | significant | minor",
        "how_to_address": "How the user should respond to this challenge"
      }
    ]
  },
  "alternative_perspectives": [
    {
      "perspective": "A different way of thinking about this",
      "source_refs": [2],
      "value": "Why this perspective is worth considering",
      "application": "How to apply this thinking"
    }
  ],
  "blind_spots_identified": [
    {
      "blind_spot": "Something the user may not be considering",
      "why_it_matters": "Potential impact",
      "suggested_action": "What to do about it"
    }
  ],
  "synthesis_insights": [
    {
      "insight": "A non-obvious insight from connecting multiple sources",
      "sources_combined": [1, 2, 3],
      "reasoning": "How these sources together reveal this insight"
    }
  ],
  "research_quality": {
    "coverage": "How well the research covers the question",
    "gaps": ["What we couldn't find", "Areas needing more research"],
    "confidence_level": "high | medium | low",
    "recommended_follow_up": ["Specific follow-up research queries"]
  },
  "actionable_recommendations": [
    {
      "recommendation": "Specific action to take",
      "based_on": "Which findings support this",
      "priority": "immediate | short-term | long-term",
      "expected_outcome": "What this action should achieve"
    }
  ]
}
"""


class ResearchAgent:
    """Enhanced agent that performs deep contextual research using Tavily."""

    def __init__(self, gemini_client: genai.Client, tavily_api_key: str = None):
        self.client = gemini_client
        self.model_name = "gemini-2.5-pro"  # Pro model for deep analysis
        self.tavily_api_key = tavily_api_key

    def research(
        self,
        conversation: List[Dict[str, str]],
        diagnosis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform deep research based on conversation and diagnosis.

        Args:
            conversation: Chat history
            diagnosis: Current problem diagnosis

        Returns:
            Research findings with citation hierarchy and critical analysis
        """
        # Step 1: Analyze context and generate targeted queries
        context_analysis = self._analyze_context(conversation, diagnosis)
        queries = self._generate_queries(context_analysis)

        # Step 2: Execute Tavily searches with more results
        search_results = self._execute_searches(queries)

        # Step 3: Deep synthesis with citation hierarchy
        synthesis = self._synthesize_findings(
            context_analysis,
            search_results
        )

        return synthesis

    def _analyze_context(
        self,
        conversation: List[Dict[str, str]],
        diagnosis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deeply analyze conversation context before research."""
        conv_text = "\n".join([
            f"{m['role'].upper()}: {m['content']}"
            for m in conversation[-8:]
        ])

        profile = diagnosis.get('profile', {})

        prompt = f"""
Analyze this conversation to understand what research would be most valuable.

CONVERSATION:
{conv_text}

DIAGNOSIS:
- Problem Name: {profile.get('name', 'Unknown')}
- Definition Level: {diagnosis.get('definition', 'undefined')}
- Complexity: {diagnosis.get('complexity', 'complex')}
- Wickedness: {diagnosis.get('wickedness', 'messy')}

Identify:
1. The core question/challenge the user is facing
2. What the user seems to believe or assume
3. What aspects need validation
4. What aspects should be challenged
5. What blind spots might exist

Respond with JSON only:
{{
  "core_question": "The central question",
  "user_hypothesis": "What user believes/assumes",
  "needs_validation": ["aspect 1", "aspect 2"],
  "needs_challenging": ["assumption 1", "assumption 2"],
  "potential_blind_spots": ["blind spot 1"],
  "industry_context": "Relevant industry/domain",
  "user_stage": "exploring | defining | validating | implementing"
}}
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
            return json.loads(text.strip())
        except:
            return {
                "core_question": "Understanding the problem space",
                "user_hypothesis": "Initial exploration",
                "needs_validation": ["Market demand", "Solution feasibility"],
                "needs_challenging": ["Assumptions about users"],
                "potential_blind_spots": ["Competition", "Alternative solutions"],
                "industry_context": "General",
                "user_stage": "exploring"
            }

    def _generate_queries(self, context: Dict[str, Any]) -> List[str]:
        """Generate targeted search queries from context analysis."""
        core_q = context.get("core_question", "")
        hypothesis = context.get("user_hypothesis", "")
        validations = context.get("needs_validation", [])
        challenges = context.get("needs_challenging", [])
        blind_spots = context.get("potential_blind_spots", [])
        industry = context.get("industry_context", "")

        prompt = f"""
Generate 5-7 highly specific search queries to research this challenge.

CORE QUESTION: {core_q}
USER'S HYPOTHESIS: {hypothesis}
INDUSTRY: {industry}

NEEDS VALIDATION: {', '.join(validations)}
NEEDS CHALLENGING: {', '.join(challenges)}
POTENTIAL BLIND SPOTS: {', '.join(blind_spots)}

Create queries that:
1. Validate the user's direction (2 queries)
2. Challenge assumptions with counter-evidence (2 queries)
3. Explore blind spots and alternatives (2-3 queries)

Be SPECIFIC - include industry terms, specific metrics, case studies.
Avoid generic queries like "how to validate ideas".

Respond with JSON array only: ["query 1", "query 2", ...]
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
            queries = json.loads(text.strip())
            return queries[:7]
        except:
            return [
                f"{core_q} market research",
                f"{core_q} case studies",
                f"{core_q} challenges failures",
                f"{hypothesis} validation data",
                f"{industry} trends 2024 2025"
            ]

    def _execute_searches(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Execute Tavily searches with enhanced parameters - focusing on recent research (2021+)."""
        all_results = []

        if not self.tavily_api_key:
            return [{
                "query": q,
                "results": [],
                "error": "Tavily API key not configured"
            } for q in queries]

        for query in queries:
            # Add year filter to query for recent research
            enhanced_query = f"{query} 2023 OR 2024 OR 2025"

            try:
                response = requests.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.tavily_api_key,
                        "query": enhanced_query,
                        "search_depth": "advanced",
                        "include_answer": True,
                        "include_raw_content": True,
                        "max_results": 5,
                        "days": 1095  # Last 3 years (2022-2025)
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    all_results.append({
                        "query": query,
                        "answer": data.get("answer", ""),
                        "results": data.get("results", [])
                    })
                else:
                    all_results.append({
                        "query": query,
                        "results": [],
                        "error": f"API error: {response.status_code}"
                    })
            except Exception as e:
                all_results.append({
                    "query": query,
                    "results": [],
                    "error": str(e)
                })

        return all_results

    def _synthesize_findings(
        self,
        context: Dict[str, Any],
        search_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Synthesize search results with deep contextual analysis."""

        # Format search results with full content
        results_text = ""
        source_index = 1
        all_sources = []

        for sr in search_results:
            results_text += f"\n\n=== QUERY: {sr['query']} ===\n"
            if sr.get('answer'):
                results_text += f"TAVILY ANSWER: {sr['answer']}\n"

            for result in sr.get("results", []):
                content = result.get('raw_content', result.get('content', ''))[:800]
                results_text += f"""
[SOURCE {source_index}]
TITLE: {result.get('title', 'N/A')}
URL: {result.get('url', 'N/A')}
CONTENT: {content}
---
"""
                all_sources.append({
                    "index": source_index,
                    "title": result.get("title", "Source"),
                    "url": result.get("url", ""),
                    "content": content,
                    "query": sr['query']
                })
                source_index += 1

        prompt = f"""
{RESEARCH_SYNTHESIS_PROMPT}

# User Context
CORE QUESTION: {context.get('core_question', 'Unknown')}
USER HYPOTHESIS: {context.get('user_hypothesis', 'Unknown')}
NEEDS VALIDATION: {context.get('needs_validation', [])}
NEEDS CHALLENGING: {context.get('needs_challenging', [])}
BLIND SPOTS: {context.get('potential_blind_spots', [])}
USER STAGE: {context.get('user_stage', 'exploring')}

# Search Results ({len(all_sources)} sources)
{results_text}

Analyze these sources and create a comprehensive research synthesis.
Focus on THIS user's specific situation - not generic advice.
Respond with ONLY the JSON object, no markdown.
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
            synthesis = json.loads(text.strip())
            synthesis["raw_sources"] = all_sources
            synthesis["context_analysis"] = context
            return synthesis
        except Exception as e:
            return self._fallback_synthesis(context, all_sources, str(e))

    def _fallback_synthesis(
        self,
        context: Dict[str, Any],
        sources: List[Dict[str, Any]],
        error: str
    ) -> Dict[str, Any]:
        """Fallback when synthesis fails."""
        return {
            "research_context": {
                "core_question": context.get("core_question", "Research question"),
                "user_hypothesis": context.get("user_hypothesis", "Unknown"),
                "research_angle": "General exploration"
            },
            "executive_summary": f"Found {len(sources)} relevant sources. Review the citation table for detailed findings.",
            "citation_table": [
                {
                    "rank": i + 1,
                    "title": s["title"],
                    "url": s["url"],
                    "source_type": "Web Source",
                    "relevance_score": 7.0,
                    "credibility_score": 6.0,
                    "key_quote": s["content"][:150] + "...",
                    "finding": f"Information related to: {s['query']}",
                    "reasoning": "Source found during research",
                    "stance": "nuances"
                }
                for i, s in enumerate(sources[:8])
            ],
            "validation_evidence": {
                "summary": "Review sources for validation evidence",
                "findings": []
            },
            "challenge_evidence": {
                "summary": "Review sources for challenging perspectives",
                "findings": []
            },
            "alternative_perspectives": [],
            "blind_spots_identified": context.get("potential_blind_spots", []),
            "synthesis_insights": [],
            "research_quality": {
                "coverage": "Partial",
                "gaps": ["Full synthesis unavailable"],
                "confidence_level": "medium",
                "recommended_follow_up": []
            },
            "actionable_recommendations": [
                {
                    "recommendation": "Review the sources in the citation table",
                    "based_on": "Research results",
                    "priority": "immediate",
                    "expected_outcome": "Better understanding of the problem space"
                }
            ],
            "raw_sources": sources,
            "context_analysis": context,
            "_error": error
        }
