"""
Framework Executor Agent
Executes individual framework analysis on conversation context
Designed to run in parallel when multiple frameworks are selected
"""

import json
from typing import Dict, Any, List
from google import genai
from google.genai import types
from config.frameworks import ALL_FRAMEWORKS, FrameworkTemplate


class FrameworkExecutor:
    """Agent that executes a specific framework analysis."""

    def __init__(self, client: genai.Client, file_search_store: str = None):
        self.client = client
        self.model_name = "gemini-2.5-pro"  # Pro model for deep framework analysis
        self.file_search_store = file_search_store or "fileSearchStores/larry-navigator-neo4j-knowl-30cntohiwvs4"

    def execute(
        self,
        framework_id: str,
        pyramid_analysis: Dict[str, Any],
        conversation: List[Dict[str, str]],
        diagnosis: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Execute a specific framework analysis.

        Args:
            framework_id: ID of the framework to execute
            pyramid_analysis: Minto Pyramid context analysis
            conversation: Full chat history
            diagnosis: Current diagnostic state

        Returns:
            Structured framework analysis with citations
        """
        # Get framework definition
        framework = ALL_FRAMEWORKS.get(framework_id)
        if not framework:
            return self._error_response(f"Framework '{framework_id}' not found")

        # Build the execution prompt
        prompt = self._build_execution_prompt(
            framework, pyramid_analysis, conversation, diagnosis
        )

        try:
            # Execute with File Search for citations
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

            # Extract citations from grounding metadata
            citations = self._extract_citations(response)
            result["citations"] = citations
            result["framework_id"] = framework_id
            result["framework_title"] = framework.title

            return result

        except Exception as e:
            return self._fallback_execution(framework, pyramid_analysis, str(e))

    def _build_execution_prompt(
        self,
        framework: FrameworkTemplate,
        pyramid: Dict[str, Any],
        conversation: List[Dict[str, str]],
        diagnosis: Dict[str, Any]
    ) -> str:
        """Build the framework execution prompt."""

        # Format conversation
        conv_text = "\n".join([
            f"{m['role'].upper()}: {m['content'][:400]}"
            for m in conversation[-8:]
        ])

        # Format SCQA
        scqa = pyramid.get("scqa", {})
        scqa_text = f"""
Situation: {scqa.get('situation', 'N/A')}
Complication: {scqa.get('complication', 'N/A')}
Question: {scqa.get('question', 'N/A')}
Direction: {scqa.get('answer_direction', 'N/A')}
"""

        # Format diagnosis
        diag_text = ""
        if diagnosis:
            diag_text = f"""
Definition Level: {diagnosis.get('definition', 'undefined')}
Complexity: {diagnosis.get('complexity', 'complex')}
Wickedness: {diagnosis.get('wickedness', 'messy')}
"""

        # Build output structure instruction
        output_fields = framework.output_structure
        output_instruction = "{\n"
        for key, desc in output_fields.items():
            output_instruction += f'  "{key}": "...",  // {desc}\n'
        output_instruction += "}"

        return f"""
# Role
You are a Framework Analyst applying the **{framework.title}** framework to analyze a problem.

# Task
Apply the {framework.title} framework to the user's current context and produce a structured analysis.

# Framework: {framework.title}

**Definition:** {framework.definition}

**When to use:** {framework.when_to_use}

**Key Questions to Answer:**
{chr(10).join(f'- {q}' for q in framework.key_questions)}

**Required Concepts:**
{', '.join(framework.required_concepts)}

# Constraints
- Output format: Valid JSON only, no markdown
- Answer ALL key questions from the framework
- Ground analysis in the conversation context
- Include specific evidence from the conversation
- Provide actionable insights, not just observations
- Search the knowledge base for relevant PWS methodology citations

# Context (SCQA from Minto Pyramid):
{scqa_text}

# Diagnostic State:
{diag_text}

# Conversation:
{conv_text}

# Output Instructions
Apply the {framework.title} framework step-by-step, then generate this JSON structure:
{{
  "framework_analysis": {{
    "summary": "2-3 sentence executive summary of the analysis",
    "key_questions_answered": [
      {{
        "question": "The framework question",
        "answer": "Your analysis",
        "evidence": "Supporting evidence from conversation"
      }}
    ],
    "framework_output": {output_instruction},
    "insights": ["Key insight 1", "Key insight 2", "Key insight 3"],
    "opportunities": ["Opportunity 1", "Opportunity 2"],
    "risks_or_gaps": ["Risk or gap 1", "Risk or gap 2"],
    "recommended_next_steps": ["Action 1", "Action 2"]
  }},
  "methodology_notes": "How the PWS methodology informs this analysis",
  "confidence_level": 0.0-1.0,
  "needs_more_info": ["What additional information would strengthen this analysis"]
}}
"""

    def _extract_citations(self, response) -> List[Dict[str, str]]:
        """Extract citations from Gemini response."""
        citations = []
        try:
            if response.candidates and response.candidates[0].grounding_metadata:
                metadata = response.candidates[0].grounding_metadata
                if hasattr(metadata, 'grounding_chunks') and metadata.grounding_chunks:
                    seen_titles = set()
                    for chunk in metadata.grounding_chunks:
                        if hasattr(chunk, 'retrieved_context') and chunk.retrieved_context:
                            ctx = chunk.retrieved_context
                            title = ctx.title if hasattr(ctx, 'title') else "Document"
                            if title not in seen_titles:
                                seen_titles.add(title)
                                citations.append({
                                    "title": title,
                                    "text": ctx.text[:300] + "..." if hasattr(ctx, 'text') and ctx.text and len(ctx.text) > 300 else (ctx.text if hasattr(ctx, 'text') else ""),
                                    "source": "PWS Knowledge Base"
                                })
        except:
            pass
        return citations

    def _error_response(self, error: str) -> Dict[str, Any]:
        """Return error response."""
        return {
            "framework_id": "error",
            "framework_title": "Error",
            "error": error,
            "framework_analysis": None,
            "citations": []
        }

    def _fallback_execution(
        self,
        framework: FrameworkTemplate,
        pyramid: Dict[str, Any],
        error: str
    ) -> Dict[str, Any]:
        """Fallback when execution fails."""
        scqa = pyramid.get("scqa", {})

        return {
            "framework_id": framework.title.lower().replace(" ", "_").replace("-", "_"),
            "framework_title": framework.title,
            "framework_analysis": {
                "summary": f"Applying {framework.title} to analyze the problem context.",
                "key_questions_answered": [
                    {
                        "question": q,
                        "answer": "Analysis pending - requires deeper exploration",
                        "evidence": "Based on conversation context"
                    }
                    for q in framework.key_questions[:3]
                ],
                "framework_output": {k: "To be determined" for k in framework.output_structure.keys()},
                "insights": [
                    f"The {framework.title} framework suggests examining: {framework.when_to_use}"
                ],
                "opportunities": ["Further analysis recommended"],
                "risks_or_gaps": ["Incomplete information for full analysis"],
                "recommended_next_steps": framework.key_questions[:2]
            },
            "methodology_notes": "Analysis based on PWS methodology principles",
            "confidence_level": 0.4,
            "needs_more_info": framework.required_concepts[:3],
            "citations": [],
            "_error": error
        }


async def execute_frameworks_parallel(
    executor: FrameworkExecutor,
    framework_ids: List[str],
    pyramid_analysis: Dict[str, Any],
    conversation: List[Dict[str, str]],
    diagnosis: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """
    Execute multiple frameworks in parallel.

    Note: For true async, use asyncio. This is a synchronous version
    that can be wrapped in ThreadPoolExecutor for parallel execution.
    """
    import concurrent.futures

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures = {
            pool.submit(
                executor.execute,
                fid,
                pyramid_analysis,
                conversation,
                diagnosis
            ): fid
            for fid in framework_ids
        }

        for future in concurrent.futures.as_completed(futures):
            framework_id = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append({
                    "framework_id": framework_id,
                    "error": str(e),
                    "framework_analysis": None
                })

    return results
