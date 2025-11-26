"""
Streaming Response Generator for Larry Navigator
Low-latency, streaming responses with integrated pyramid analysis
"""

import json
from typing import Dict, Any, List, Generator, Optional
from google import genai
from google.genai import types


class StreamingResponseGenerator:
    """
    Generates streaming Larry responses with integrated context analysis.

    Key improvements:
    - Uses gemini-2.5-flash for ~3x speed
    - Streams response chunks in real-time
    - Integrates pyramid analysis seamlessly
    - Reduces perceived latency significantly
    """

    def __init__(
        self,
        client: genai.Client,
        system_prompt: str,
        knowledge_base=None  # SupabaseKnowledgeBase instance
    ):
        self.client = client
        self.system_prompt = system_prompt
        self.kb = knowledge_base
        self.fast_model = "gemini-2.5-flash"
        # Store metadata for retrieval after streaming
        self.last_citations = []
        self.last_signals = {}

    def generate_streaming(
        self,
        query: str,
        chat_history: List[Dict[str, str]],
        diagnosis: Dict[str, Any] = None
    ) -> Generator[str, None, None]:
        """
        Generate a streaming response with integrated analysis.

        Yields:
            String chunks as they're generated

        After streaming, access metadata via:
            generator.last_citations
            generator.last_signals
        """
        # Step 1: Fast RAG retrieval (parallel-ready)
        context_text, citations = self._get_rag_context(query)
        self.last_citations = citations  # Store for later access

        # Step 2: Fast signal detection (compact prompt, fast model)
        signals_data = self._detect_signals_fast(query, chat_history, diagnosis)
        self.last_signals = signals_data  # Store for later access

        # Step 3: Build enhanced prompt with analysis context
        enhanced_prompt = self._build_enhanced_prompt(
            query=query,
            chat_history=chat_history,
            context_text=context_text,
            signals_data=signals_data,
            diagnosis=diagnosis
        )

        # Step 4: Stream the response
        full_response = ""

        try:
            stream = self.client.models.generate_content_stream(
                model=self.fast_model,
                contents=enhanced_prompt
            )

            for chunk in stream:
                if chunk.text:
                    full_response += chunk.text
                    yield chunk.text

        except Exception as e:
            error_msg = f"\n\n*[Response interrupted: {str(e)[:100]}]*"
            yield error_msg

    def _get_rag_context(self, query: str) -> tuple:
        """Retrieve RAG context from Supabase."""
        context_text = ""
        citations = []

        if self.kb:
            try:
                results = self.kb.retrieve_context(query, top_k=5, threshold=0.5)
                if results:
                    context_text = self.kb.format_context_for_llm(results)
                    citations = [
                        {
                            "title": r.get("title", "Document"),
                            "text": r.get("content", "")[:200] + "..." if len(r.get("content", "")) > 200 else r.get("content", "")
                        }
                        for r in results
                    ]
            except Exception:
                pass  # Continue without RAG if retrieval fails

        return context_text, citations

    def _detect_signals_fast(
        self,
        query: str,
        chat_history: List[Dict[str, str]],
        diagnosis: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Fast signal detection using compact prompt.
        ~1-2 seconds with gemini-2.5-flash.
        """
        # Compact conversation summary
        recent_messages = chat_history[-6:] if chat_history else []
        conv_summary = "\n".join([
            f"{'U' if m['role'] == 'user' else 'A'}: {m['content'][:300]}"
            for m in recent_messages
        ])

        compact_prompt = f"""Analyze this conversation for thinking signals.

CONVERSATION:
{conv_summary}

CURRENT MESSAGE: {query[:500]}

DIAGNOSIS: {json.dumps(diagnosis or {}, separators=(',', ':'))}

Return JSON only:
{{"signals": ["signal1", "signal2"], "primary": "main_signal", "stage": "exploring|defining|validating|solving", "scqa_hint": "one sentence situation-complication summary"}}

SIGNAL OPTIONS: causal_ambiguity, system_bottleneck, stakeholder_conflict, trend_pressure, user_behavior, business_model, validation_gap, execution_focus, ideation_needed, narrative_focus, strategic_choice, uncertainty_high, time_pressure

JSON only:"""

        try:
            response = self.client.models.generate_content(
                model=self.fast_model,
                contents=compact_prompt
            )

            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]

            return json.loads(text.strip())
        except Exception:
            return {
                "signals": ["causal_ambiguity"],
                "primary": "causal_ambiguity",
                "stage": "exploring",
                "scqa_hint": "User exploring a problem"
            }

    def _build_enhanced_prompt(
        self,
        query: str,
        chat_history: List[Dict[str, str]],
        context_text: str,
        signals_data: Dict[str, Any],
        diagnosis: Dict[str, Any] = None
    ) -> str:
        """Build the enhanced prompt with all context."""

        # Format history
        history_text = ""
        if chat_history:
            history_parts = []
            for msg in chat_history[-6:]:
                role = "User" if msg["role"] == "user" else "Larry"
                history_parts.append(f"{role}: {msg['content'][:500]}")
            history_text = "\n".join(history_parts)

        # Get signal info
        signals = signals_data.get("signals", [])
        primary_signal = signals_data.get("primary", "")
        stage = signals_data.get("stage", "exploring")
        scqa_hint = signals_data.get("scqa_hint", "")

        # Framework suggestion based on primary signal
        framework_map = {
            "causal_ambiguity": ("Root Cause Analysis / 5 Whys", "understand WHY something is happening"),
            "system_bottleneck": ("Reverse Salience / Process Mapping", "find what's blocking progress"),
            "stakeholder_conflict": ("Stakeholder Mapping", "understand different perspectives"),
            "trend_pressure": ("Scenario Planning", "prepare for multiple futures"),
            "user_behavior": ("Jobs-To-Be-Done", "understand what the customer really wants"),
            "business_model": ("Business Model Canvas", "design how value is created"),
            "validation_gap": ("Lean Startup / MVP", "test assumptions quickly"),
            "execution_focus": ("Process Mapping", "clarify how to implement"),
            "ideation_needed": ("Six Thinking Hats", "generate new perspectives"),
            "narrative_focus": ("HEART Framework", "craft a compelling story"),
            "strategic_choice": ("Decision Trees", "structure the key choices"),
            "uncertainty_high": ("Cynefin Framework", "navigate the unknown"),
            "time_pressure": ("PWS Triple Validation", "validate quickly")
        }

        framework_name, framework_purpose = framework_map.get(
            primary_signal,
            ("Exploratory Questions", "clarify the situation")
        )

        # Build the full prompt
        prompt = f"""{self.system_prompt}

## Knowledge Base Context:
{context_text if context_text else "No specific context retrieved. Use your general knowledge of PWS methodology."}

## Previous Conversation:
{history_text if history_text else "This is the start of a new conversation."}

## Internal Analysis (use to inform response, don't repeat verbatim):
- Detected signals: {', '.join(signals)}
- Primary signal: {primary_signal}
- Conversation stage: {stage}
- SCQA hint: {scqa_hint}
- Suggested framework: {framework_name} (to {framework_purpose})

## Current Diagnosis State:
- Definition: {diagnosis.get('definition', 'undefined') if diagnosis else 'undefined'}
- Complexity: {diagnosis.get('complexity', 'complex') if diagnosis else 'complex'}
- Wickedness: {diagnosis.get('wickedness', 'messy') if diagnosis else 'messy'}

## User's Current Message:
{query}

## Response Guidelines:
1. Start with a hook or reframe that shows you understand their situation
2. If you sense {primary_signal}, naturally weave in why {framework_name} could help
3. Don't overwhelm - introduce ONE framework naturally if appropriate
4. Ask 2-3 powerful questions to deepen their thinking
5. End with a clear next step or "homework"

Respond as Larry, the warm but rigorous PWS Innovation Mentor:"""

        return prompt


def create_streaming_generator(
    client: genai.Client,
    system_prompt: str,
    knowledge_base=None
) -> StreamingResponseGenerator:
    """Factory function to create a streaming generator."""
    return StreamingResponseGenerator(client, system_prompt, knowledge_base)


class StreamingResponse:
    """
    Wrapper that provides both streaming and metadata access.
    """

    def __init__(
        self,
        client: genai.Client,
        query: str,
        chat_history: List[Dict[str, str]],
        system_prompt: str,
        diagnosis: Dict[str, Any] = None,
        knowledge_base=None
    ):
        self.generator = StreamingResponseGenerator(client, system_prompt, knowledge_base)
        self.query = query
        self.chat_history = chat_history
        self.diagnosis = diagnosis
        self._stream = None

    def __iter__(self):
        """Iterate over streaming chunks."""
        self._stream = self.generator.generate_streaming(
            self.query,
            self.chat_history,
            self.diagnosis
        )
        return self

    def __next__(self):
        """Get next chunk."""
        if self._stream is None:
            self._stream = self.generator.generate_streaming(
                self.query,
                self.chat_history,
                self.diagnosis
            )
        return next(self._stream)

    @property
    def citations(self) -> List[Dict]:
        """Get citations after streaming completes."""
        return self.generator.last_citations

    @property
    def signals(self) -> Dict:
        """Get detected signals after streaming completes."""
        return self.generator.last_signals


def stream_larry_response(
    client: genai.Client,
    query: str,
    chat_history: List[Dict[str, str]],
    system_prompt: str,
    diagnosis: Dict[str, Any] = None,
    knowledge_base=None
) -> StreamingResponse:
    """
    Stream a Larry response with integrated analysis.

    Usage in Streamlit:
        response_placeholder = st.empty()
        full_response = ""

        stream = stream_larry_response(client, query, history, prompt, diagnosis, kb)
        for chunk in stream:
            full_response += chunk
            response_placeholder.markdown(full_response + "▌")

        response_placeholder.markdown(full_response)

        # Get metadata after streaming
        citations = stream.citations
        signals = stream.signals
    """
    return StreamingResponse(
        client=client,
        query=query,
        chat_history=chat_history,
        system_prompt=system_prompt,
        diagnosis=diagnosis,
        knowledge_base=knowledge_base
    )


__all__ = [
    'StreamingResponseGenerator',
    'StreamingResponse',
    'create_streaming_generator',
    'stream_larry_response'
]
