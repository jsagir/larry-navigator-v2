"""
Streaming Pyramid Analysis - Low Latency Implementation
Uses gemini-2.5-flash for speed + streaming for responsiveness
"""

import json
from typing import Dict, Any, List, Generator, Optional
from google import genai
from dataclasses import dataclass


@dataclass
class StreamingChunk:
    """Represents a chunk of streaming output."""
    type: str  # "thinking", "signal", "scqa", "framework", "complete"
    content: str
    data: Optional[Dict] = None


# Compact prompt optimized for speed (fewer tokens = faster)
FAST_PYRAMID_PROMPT = """Analyze this conversation using Minto Pyramid (SCQA).

CONVERSATION:
{conversation}

DIAGNOSIS STATE:
{diagnosis}

OUTPUT JSON ONLY:
{{
  "scqa": {{
    "situation": "1-2 sentences",
    "complication": "1-2 sentences",
    "question": "The core question",
    "answer_direction": "Where solution lies"
  }},
  "signals": ["signal1", "signal2"],
  "primary_signal": "main_signal",
  "stage": "exploring|defining|validating|solving"
}}

SIGNAL OPTIONS: causal_ambiguity, system_bottleneck, stakeholder_conflict,
trend_pressure, user_behavior, business_model, validation_gap, execution_focus,
ideation_needed, narrative_focus, strategic_choice, uncertainty_high, time_pressure

Be concise. JSON only, no markdown."""


FAST_FRAMEWORK_PROMPT = """Based on signals, recommend 1 primary + 2 alternative frameworks.

SIGNALS: {signals}
PRIMARY SIGNAL: {primary_signal}
SCQA: {scqa}
STAGE: {stage}

FRAMEWORK OPTIONS BY SIGNAL:
- causal_ambiguity → root_cause_analysis, five_whys, fishbone
- system_bottleneck → reverse_salience, process_mapping, systems_thinking
- stakeholder_conflict → stakeholder_mapping, six_thinking_hats
- trend_pressure → scenario_planning, macro_trends, value_migration
- user_behavior → jobs_to_be_done, empathy_mapping, user_journey
- business_model → business_model_canvas, lean_canvas, mullins_model
- validation_gap → lean_startup_mvp, mom_test, discovery_driven
- execution_focus → process_mapping, agile_sprint, okrs
- ideation_needed → six_thinking_hats, lateral_thinking, scamper
- narrative_focus → heart_framework, golden_circle, storytelling
- strategic_choice → decision_trees, porters_forces, blue_ocean
- uncertainty_high → cynefin, scenario_planning, real_options
- time_pressure → rapid_prototype, pws_triple_validation

OUTPUT JSON ONLY:
{{
  "primary": {{
    "id": "framework_id",
    "name": "Framework Name",
    "why": "1 sentence why this fits"
  }},
  "alternatives": [
    {{"id": "...", "name": "...", "why": "..."}}
  ],
  "reasoning": "Brief selection logic"
}}"""


class StreamingPyramidAnalyzer:
    """
    Fast, streaming pyramid analysis.
    Uses gemini-2.5-flash for ~3x speed improvement.
    """

    def __init__(self, client: genai.Client):
        self.client = client
        self.model = "gemini-2.5-flash"  # Fast model

    def analyze_streaming(
        self,
        conversation: List[Dict[str, str]],
        diagnosis: Dict[str, Any]
    ) -> Generator[StreamingChunk, None, None]:
        """
        Stream pyramid analysis results as they're generated.

        Yields StreamingChunk objects with progressive results.
        """
        # Format conversation compactly
        conv_text = self._format_conversation_compact(conversation)
        diag_text = json.dumps(diagnosis, separators=(',', ':'))

        # Phase 1: SCQA + Signals (streaming)
        yield StreamingChunk("thinking", "Analyzing conversation structure...")

        pyramid_prompt = FAST_PYRAMID_PROMPT.format(
            conversation=conv_text,
            diagnosis=diag_text
        )

        try:
            # Stream the pyramid analysis
            pyramid_result = None
            accumulated = ""

            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=pyramid_prompt
            ):
                if chunk.text:
                    accumulated += chunk.text
                    yield StreamingChunk("thinking", f"Building pyramid... ({len(accumulated)} chars)")

            # Parse result
            pyramid_result = self._parse_json(accumulated)

            if pyramid_result:
                # Yield SCQA
                yield StreamingChunk(
                    "scqa",
                    f"**Situation:** {pyramid_result.get('scqa', {}).get('situation', 'N/A')}",
                    pyramid_result.get("scqa")
                )

                # Yield signals
                signals = pyramid_result.get("signals", [])
                primary = pyramid_result.get("primary_signal", "")
                yield StreamingChunk(
                    "signal",
                    f"Detected: {', '.join(signals)} (primary: {primary})",
                    {"signals": signals, "primary": primary}
                )
            else:
                pyramid_result = self._fallback_pyramid()
                yield StreamingChunk("signal", "Using fallback analysis", pyramid_result)

            # Phase 2: Framework recommendation (streaming)
            yield StreamingChunk("thinking", "Selecting framework...")

            framework_prompt = FAST_FRAMEWORK_PROMPT.format(
                signals=", ".join(pyramid_result.get("signals", [])),
                primary_signal=pyramid_result.get("primary_signal", "causal_ambiguity"),
                scqa=json.dumps(pyramid_result.get("scqa", {}), separators=(',', ':')),
                stage=pyramid_result.get("stage", "exploring")
            )

            accumulated = ""
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=framework_prompt
            ):
                if chunk.text:
                    accumulated += chunk.text

            framework_result = self._parse_json(accumulated)

            if framework_result:
                yield StreamingChunk(
                    "framework",
                    f"**Recommended:** {framework_result.get('primary', {}).get('name', 'Unknown')}",
                    framework_result
                )
            else:
                framework_result = self._fallback_framework(pyramid_result.get("primary_signal", ""))
                yield StreamingChunk("framework", "Using default framework", framework_result)

            # Final complete result
            yield StreamingChunk(
                "complete",
                "Analysis complete",
                {
                    "pyramid": pyramid_result,
                    "frameworks": framework_result
                }
            )

        except Exception as e:
            yield StreamingChunk("error", f"Analysis error: {str(e)[:100]}", None)

    def analyze_fast(
        self,
        conversation: List[Dict[str, str]],
        diagnosis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Non-streaming fast analysis. Returns complete result.
        ~3-5 seconds total instead of 20-35 seconds.
        """
        conv_text = self._format_conversation_compact(conversation)
        diag_text = json.dumps(diagnosis, separators=(',', ':'))

        # Single call for pyramid
        pyramid_prompt = FAST_PYRAMID_PROMPT.format(
            conversation=conv_text,
            diagnosis=diag_text
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=pyramid_prompt
            )
            pyramid_result = self._parse_json(response.text)
        except Exception:
            pyramid_result = self._fallback_pyramid()

        if not pyramid_result:
            pyramid_result = self._fallback_pyramid()

        # Single call for frameworks
        framework_prompt = FAST_FRAMEWORK_PROMPT.format(
            signals=", ".join(pyramid_result.get("signals", [])),
            primary_signal=pyramid_result.get("primary_signal", "causal_ambiguity"),
            scqa=json.dumps(pyramid_result.get("scqa", {}), separators=(',', ':')),
            stage=pyramid_result.get("stage", "exploring")
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=framework_prompt
            )
            framework_result = self._parse_json(response.text)
        except Exception:
            framework_result = self._fallback_framework(pyramid_result.get("primary_signal", ""))

        if not framework_result:
            framework_result = self._fallback_framework(pyramid_result.get("primary_signal", ""))

        return {
            "pyramid": pyramid_result,
            "frameworks": framework_result
        }

    def _format_conversation_compact(self, conversation: List[Dict[str, str]]) -> str:
        """Format conversation compactly to reduce tokens."""
        lines = []
        for msg in conversation[-10:]:  # Last 10 messages max
            role = "U" if msg["role"] == "user" else "A"
            content = msg["content"][:500]  # Truncate long messages
            lines.append(f"{role}: {content}")
        return "\n".join(lines)

    def _parse_json(self, text: str) -> Optional[Dict]:
        """Parse JSON from response, handling markdown blocks."""
        text = text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        try:
            return json.loads(text.strip())
        except:
            return None

    def _fallback_pyramid(self) -> Dict:
        """Fallback pyramid when analysis fails."""
        return {
            "scqa": {
                "situation": "Conversation in progress",
                "complication": "Problem being explored",
                "question": "What's the core issue?",
                "answer_direction": "Needs more exploration"
            },
            "signals": ["causal_ambiguity"],
            "primary_signal": "causal_ambiguity",
            "stage": "exploring"
        }

    def _fallback_framework(self, signal: str) -> Dict:
        """Fallback framework based on signal."""
        mapping = {
            "causal_ambiguity": ("root_cause_analysis", "Root Cause Analysis"),
            "system_bottleneck": ("reverse_salience", "Reverse Salience"),
            "stakeholder_conflict": ("stakeholder_mapping", "Stakeholder Mapping"),
            "user_behavior": ("jobs_to_be_done", "Jobs-To-Be-Done"),
            "validation_gap": ("lean_startup_mvp", "Lean Startup / MVP"),
            "uncertainty_high": ("scenario_planning", "Scenario Planning"),
        }

        fid, fname = mapping.get(signal, ("root_cause_analysis", "Root Cause Analysis"))

        return {
            "primary": {
                "id": fid,
                "name": fname,
                "why": f"Based on {signal} signal"
            },
            "alternatives": [
                {"id": "six_thinking_hats", "name": "Six Thinking Hats", "why": "Multiple perspectives"},
                {"id": "process_mapping", "name": "Process Mapping", "why": "Visualize the flow"}
            ],
            "reasoning": "Signal-driven fallback selection"
        }


def create_streaming_response(
    client: genai.Client,
    conversation: List[Dict[str, str]],
    diagnosis: Dict[str, Any],
    system_prompt: str
) -> Generator[str, None, None]:
    """
    Create a streaming Larry response with integrated pyramid analysis.
    This is the main entry point for the new fast workflow.

    Yields text chunks as they're generated.
    """
    # Fast pyramid analysis first
    analyzer = StreamingPyramidAnalyzer(client)
    result = analyzer.analyze_fast(conversation, diagnosis)

    # Build context for Larry's response
    pyramid = result.get("pyramid", {})
    frameworks = result.get("frameworks", {})

    scqa = pyramid.get("scqa", {})
    signals = pyramid.get("signals", [])
    primary_signal = pyramid.get("primary_signal", "")
    primary_framework = frameworks.get("primary", {})

    # Construct enhanced prompt with analysis context
    context_injection = f"""
[INTERNAL ANALYSIS - Use to inform response, don't repeat verbatim]
SCQA: Situation: {scqa.get('situation')} | Complication: {scqa.get('complication')} | Question: {scqa.get('question')}
Signals detected: {', '.join(signals)} (Primary: {primary_signal})
Recommended framework: {primary_framework.get('name')} - {primary_framework.get('why')}
Stage: {pyramid.get('stage', 'exploring')}
[END INTERNAL ANALYSIS]

Now respond to the user naturally, weaving in the SCQA understanding and gently introducing the framework when appropriate.
"""

    # Format conversation for Gemini
    formatted_messages = []
    for msg in conversation:
        role = "user" if msg["role"] == "user" else "model"
        formatted_messages.append({"role": role, "parts": [{"text": msg["content"]}]})

    # Add context to last user message
    if formatted_messages and formatted_messages[-1]["role"] == "user":
        formatted_messages[-1]["parts"][0]["text"] += f"\n\n{context_injection}"

    # Stream Larry's response
    try:
        for chunk in client.models.generate_content_stream(
            model="gemini-2.5-flash",  # Fast model for response too
            contents=formatted_messages,
            config={"system_instruction": system_prompt}
        ):
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\n*[Response interrupted: {str(e)[:50]}]*"


# Export for use in app.py
__all__ = ['StreamingPyramidAnalyzer', 'StreamingChunk', 'create_streaming_response']
