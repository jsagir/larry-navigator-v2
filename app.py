#!/usr/bin/env python3
"""
Larry Navigator v2.0 - Dynamic Problem Diagnosis System
Streamlit chatbot with diagnostic agents, warm UI, and research capabilities
"""

import os
import sys
import time
import streamlit as st
from google import genai
from google.genai import types

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from styles.components import get_main_css
from components.header import render_larry_header
from components.problem_dashboard import (
    render_problem_dashboard_horizontal,
    render_dimension_detail,
    render_profile_card
)
from components.research_panel import render_research_panel, render_web_sources
from components.framework_selector import (
    render_framework_selector,
    render_pyramid_summary,
    render_consolidated_report,
    clear_framework_selection
)
from utils.session_state import (
    init_session_state, add_message, update_diagnosis,
    get_diagnosis_dict, get_messages, clear_session
)
from agents.diagnosis_consolidator import DiagnosisConsolidator
from agents.research_agent import ResearchAgent
from agents.minto_analyzer import MintoAnalyzer, get_scqa_summary
from agents.framework_recommender import FrameworkRecommender, get_framework_buttons
from agents.framework_executor import FrameworkExecutor, execute_frameworks_parallel
from agents.framework_consolidator import FrameworkConsolidator
from config.prompts import LARRY_SYSTEM_PROMPT
from config.personas import get_all_personas, get_persona, get_default_persona
from utils.thinking_quotes import ThinkingQuoteRotator, get_thinking_insight
from utils.supabase_rag import SupabaseKnowledgeBase
from utils.streaming_response import stream_larry_response


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

def get_config(key, default=None):
    """Get config from Streamlit secrets or environment variables."""
    try:
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)


GOOGLE_AI_API_KEY = get_config("GOOGLE_AI_API_KEY")
TAVILY_API_KEY = get_config("TAVILY_API_KEY")

# Supabase Configuration (new RAG backend)
SUPABASE_URL = get_config("SUPABASE_URL", "https://ulmymxxmvsehjiyymqoi.supabase.co")
SUPABASE_KEY = get_config("SUPABASE_KEY")

# Legacy: File Search (fallback if Supabase not configured)
FILE_SEARCH_STORE_NAME = get_config(
    "FILE_SEARCH_STORE_NAME",
    "fileSearchStores/larrypwsnavigatorv2-7pkxk5lhy0xc"
)

# Gemini Model Configuration (Tiered by Task)
# Flash for fluent conversation, Pro for deep framework analysis
MODELS = {
    "flash": "gemini-2.5-flash",          # Main conversation - fast, fluent responses
    "pro": "gemini-3-pro-preview",        # Framework analysis - deep thinking
}
MODEL_NAME = MODELS["flash"]  # Fast model for fluent conversation


# ═══════════════════════════════════════════════════════════════════════════════
# QUICK ACTIONS
# ═══════════════════════════════════════════════════════════════════════════════

QUICK_ACTIONS = [
    {"label": "Help me find a problem worth solving", "icon": "🎯"},
    {"label": "I have an idea - challenge it", "icon": "💡"},
    {"label": "I'm stuck and need direction", "icon": "🧭"},
    {"label": "Explain the PWS framework", "icon": "📚"},
    {"label": "Show me a case study", "icon": "📖"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# CLIENT INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def init_gemini_client():
    """Initialize Gemini client."""
    if not GOOGLE_AI_API_KEY:
        return None
    return genai.Client(api_key=GOOGLE_AI_API_KEY)


def get_consolidator(client):
    """Get or create diagnosis consolidator."""
    if "consolidator" not in st.session_state and client:
        st.session_state.consolidator = DiagnosisConsolidator(client, FILE_SEARCH_STORE_NAME)
    return st.session_state.get("consolidator")


def get_research_agent(client):
    """Get or create research agent."""
    if "research_agent" not in st.session_state and client:
        st.session_state.research_agent = ResearchAgent(client, TAVILY_API_KEY)
    return st.session_state.get("research_agent")


def get_minto_analyzer(client):
    """Get or create Minto Pyramid analyzer."""
    if "minto_analyzer" not in st.session_state and client:
        st.session_state.minto_analyzer = MintoAnalyzer(client)
    return st.session_state.get("minto_analyzer")


def get_framework_recommender(client):
    """Get or create framework recommender."""
    if "framework_recommender" not in st.session_state and client:
        st.session_state.framework_recommender = FrameworkRecommender(client)
    return st.session_state.get("framework_recommender")


def get_framework_executor(client):
    """Get or create framework executor."""
    if "framework_executor" not in st.session_state and client:
        st.session_state.framework_executor = FrameworkExecutor(client, FILE_SEARCH_STORE_NAME)
    return st.session_state.get("framework_executor")


def get_framework_consolidator(client):
    """Get or create framework consolidator."""
    if "framework_consolidator" not in st.session_state and client:
        st.session_state.framework_consolidator = FrameworkConsolidator(client, FILE_SEARCH_STORE_NAME)
    return st.session_state.get("framework_consolidator")


# ═══════════════════════════════════════════════════════════════════════════════
# SUPABASE KNOWLEDGE BASE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def init_supabase_kb():
    """Initialize Supabase Knowledge Base for RAG."""
    if not SUPABASE_KEY or not GOOGLE_AI_API_KEY:
        return None
    try:
        return SupabaseKnowledgeBase(
            supabase_url=SUPABASE_URL,
            supabase_key=SUPABASE_KEY,
            google_ai_key=GOOGLE_AI_API_KEY
        )
    except Exception as e:
        st.warning(f"⚠️ Knowledge base initialization failed: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE GENERATION (Supabase RAG)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_response_with_rag(client, query: str, chat_history: list, kb: SupabaseKnowledgeBase = None) -> dict:
    """Generate response using Gemini with Supabase RAG."""

    history_text = ""
    if chat_history:
        history_parts = []
        for msg in chat_history[-6:]:
            role = "User" if msg["role"] == "user" else "Larry"
            history_parts.append(f"{role}: {msg['content'][:500]}")
        history_text = "\n".join(history_parts)

    # Retrieve relevant context from Supabase
    context_text = ""
    citations = []

    if kb:
        try:
            # Semantic search in knowledge base
            results = kb.retrieve_context(query, top_k=5, threshold=0.5)

            if results:
                context_text = kb.format_context_for_llm(results)
                citations = [
                    {
                        "title": r.get("title", "Document"),
                        "text": r.get("content", "")[:200] + "..." if len(r.get("content", "")) > 200 else r.get("content", "")
                    }
                    for r in results
                ]
        except Exception as e:
            # Continue without RAG if retrieval fails
            context_text = ""
            citations = []

    full_prompt = f"""{LARRY_SYSTEM_PROMPT}

## Knowledge Base Context:
{context_text if context_text else "No specific context retrieved. Use your general knowledge of PWS methodology."}

## Previous Conversation:
{history_text if history_text else "This is the start of a new conversation."}

## User's Current Message:
{query}

Respond as Larry, the PWS Innovation Mentor. Use the retrieved context from the knowledge base to ground your response in specific frameworks, concepts, and examples from the course materials.

Remember to:
1. Start with a hook or reframe
2. Challenge assumptions
3. Provide a relevant framework
4. End with actionable next steps or homework
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt
        )

        response_text = response.text if response.text else "No response generated."

        return {
            "text": response_text,
            "citations": citations,
            "success": True
        }

    except Exception as e:
        return {
            "text": f"Error generating response: {str(e)}",
            "citations": [],
            "success": False
        }


# Alias for backwards compatibility
def generate_response_with_file_search(client, query: str, chat_history: list) -> dict:
    """Legacy wrapper - redirects to Supabase RAG."""
    kb = init_supabase_kb()
    return generate_response_with_rag(client, query, chat_history, kb)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main Streamlit application."""

    st.set_page_config(
        page_title="Larry Navigator - PWS Mentor",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    init_session_state()

    # Apply custom CSS
    st.markdown(get_main_css(), unsafe_allow_html=True)

    # Initialize client
    client = init_gemini_client()
    consolidator = get_consolidator(client)
    research_agent = get_research_agent(client)

    # Framework system agents
    minto_analyzer = get_minto_analyzer(client)
    framework_recommender = get_framework_recommender(client)
    framework_executor = get_framework_executor(client)
    framework_consolidator = get_framework_consolidator(client)

    # ═══════════════════════════════════════════════════════════════════════════
    # SIDEBAR
    # ═══════════════════════════════════════════════════════════════════════════

    with st.sidebar:
        st.markdown("### 🧠 Larry Navigator")
        st.markdown("*Dynamic Problem Diagnosis*")

        # ═══════════════════════════════════════════════════════════════════════
        # PERSONA SELECTOR
        # ═══════════════════════════════════════════════════════════════════════
        st.markdown('<div class="sidebar-section">Larry Mode</div>', unsafe_allow_html=True)

        # Initialize persona in session state
        if "selected_persona" not in st.session_state:
            st.session_state.selected_persona = get_default_persona().id

        # Get all personas
        personas = get_all_personas()
        current_persona = get_persona(st.session_state.selected_persona)

        # Create persona buttons
        persona_cols = st.columns(len(personas))
        for i, (pid, persona) in enumerate(personas.items()):
            with persona_cols[i]:
                is_selected = st.session_state.selected_persona == pid
                btn_type = "primary" if is_selected else "secondary"
                if st.button(
                    f"{persona.icon}",
                    key=f"persona_{pid}",
                    help=f"{persona.name}: {persona.short_description}",
                    use_container_width=True,
                    type=btn_type
                ):
                    if st.session_state.selected_persona != pid:
                        st.session_state.selected_persona = pid
                        st.toast(f"Switched to {persona.name}", icon=persona.icon)
                        st.rerun()

        # Show current persona name
        st.caption(f"**{current_persona.name}**: {current_persona.short_description}")

        st.divider()

        # Show knowledge base status
        kb = init_supabase_kb()
        if kb:
            try:
                stats = kb.get_stats()
                total_chunks = stats.get('total_chunks', 0)
                if total_chunks > 0:
                    st.success(f"✅ Knowledge Base: {total_chunks:,} chunks")
                else:
                    st.warning("⚠️ Knowledge base empty")
            except:
                st.warning("⚠️ Knowledge base unavailable")
        else:
            st.warning("⚠️ Knowledge base not configured")

        st.divider()

        # Compact Diagnosis Status (dashboard moved to main area)
        st.markdown('<div class="sidebar-section">📊 Problem Status</div>', unsafe_allow_html=True)

        if st.session_state.full_diagnosis:
            profile = st.session_state.full_diagnosis.get("profile", {})
            if profile.get("name"):
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #EFFAF9 0%, #fff 100%);
                            padding: 0.75rem; border-radius: 10px; margin-bottom: 0.5rem;
                            border-left: 3px solid #2A9D8F; box-shadow: 0 2px 8px rgba(42, 157, 143, 0.1);">
                    <div style="font-size: 0.8rem; font-weight: 600; color: #1B6B64;">
                        {profile.get('name', 'Analyzing...')}
                    </div>
                    <div style="font-size: 0.7rem; color: #7A7A7A; margin-top: 0.25rem;">
                        {profile.get('recommended_approach', 'Analysis')} approach
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Show framework matches
                frameworks = profile.get("framework_matches", [])
                if frameworks:
                    pills_html = "".join([
                        f'<span style="display: inline-block; background: #D1F2F0; color: #1B6B64; '
                        f'padding: 0.2rem 0.5rem; border-radius: 10px; font-size: 0.65rem; '
                        f'font-weight: 500; margin: 0.1rem;">{f}</span>'
                        for f in frameworks[:3]
                    ])
                    st.markdown(f'<div style="margin-bottom: 0.5rem;">{pills_html}</div>', unsafe_allow_html=True)
        else:
            st.caption("💬 Start a conversation to see diagnosis")

        st.divider()

        # Research Section
        st.markdown('<div class="sidebar-section">Research</div>', unsafe_allow_html=True)

        research_disabled = (
            len(get_messages()) < 2 or
            not TAVILY_API_KEY or
            st.session_state.researching
        )

        research_text = st.session_state.research.research_prompt_text or "🔍 Research This Problem"

        if st.button(
            research_text,
            disabled=research_disabled,
            use_container_width=True,
            key="research_btn"
        ):
            st.session_state.researching = True
            st.rerun()

        if not TAVILY_API_KEY:
            st.caption("⚠️ Tavily API not configured")
        elif len(get_messages()) < 2:
            st.caption("💬 Have a conversation first")
        elif st.session_state.research.show_research_prompt:
            st.caption("💡 Research recommended!")

        st.divider()

        # Pyramid Analysis Section
        st.markdown('<div class="sidebar-section">Framework Analysis</div>', unsafe_allow_html=True)

        pyramid_disabled = (
            len(get_messages()) < 2 or
            st.session_state.get("pyramid_analyzing", False)
        )

        if st.button(
            "📐 Pyramid Analysis",
            disabled=pyramid_disabled,
            use_container_width=True,
            key="pyramid_btn",
            help="Analyze conversation context with Minto Pyramid (SCQA) and get framework recommendations"
        ):
            st.session_state.pyramid_analyzing = True
            st.rerun()

        if len(get_messages()) < 2:
            st.caption("💬 Have a conversation first")
        elif st.session_state.framework_state.framework_recommendations:
            st.caption("✅ Frameworks ready - see above chat")

        st.divider()

        # Status
        st.markdown('<div class="sidebar-section">Status</div>', unsafe_allow_html=True)

        if client:
            st.success("✅ Gemini Connected")
        else:
            st.error("❌ Gemini not configured")

        if TAVILY_API_KEY:
            st.success("✅ Tavily Ready")
        else:
            st.warning("⚠️ Tavily not configured")

        st.caption(f"Model: {MODEL_NAME}")
        st.caption(f"Messages: {len(get_messages())}")

        # Framework status
        if st.session_state.framework_state.framework_recommendations:
            rec_count = len(st.session_state.framework_state.framework_recommendations.get("recommended_frameworks", []))
            st.success(f"🧩 {rec_count} frameworks ready")
        elif st.session_state.framework_state.pyramid_analysis:
            st.info("📐 Pyramid done, no frameworks")

        st.divider()

        # Clear Button with confirmation
        if st.session_state.get("confirm_clear_pending"):
            st.warning("⚠️ This will clear all conversation history and diagnosis data.")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("✓ Yes, Clear", key="confirm_clear_yes", type="primary", use_container_width=True):
                    st.session_state.confirm_clear_pending = False
                    clear_session()
                    st.rerun()
            with col_no:
                if st.button("✗ Cancel", key="confirm_clear_no", use_container_width=True):
                    st.session_state.confirm_clear_pending = False
                    st.rerun()
        else:
            if st.button("🗑️ New Conversation", use_container_width=True):
                # Only show confirmation if there's actual conversation to clear
                if get_messages():
                    st.session_state.confirm_clear_pending = True
                    st.rerun()
                else:
                    clear_session()
                    st.rerun()

        st.divider()
        st.caption("Built by Jonathan Sagir")

    # ═══════════════════════════════════════════════════════════════════════════
    # MAIN CONTENT
    # ═══════════════════════════════════════════════════════════════════════════

    # Header
    render_larry_header()

    # ═══════════════════════════════════════════════════════════════════════════
    # LIVE STATUS CARD (Always Visible Above Chat)
    # ═══════════════════════════════════════════════════════════════════════════

    # Profile card is ALWAYS visible - shows current diagnosis status
    profile = st.session_state.diagnosis.profile if st.session_state.diagnosis.profile else None
    diagnosis_dict = get_diagnosis_dict() if get_messages() else None
    render_profile_card(profile=profile, diagnosis=diagnosis_dict)

    # ═══════════════════════════════════════════════════════════════════════════
    # PROBLEM DIAGNOSIS DASHBOARD (Above Chat - only when conversation exists)
    # ═══════════════════════════════════════════════════════════════════════════

    # Only show full dashboard if there's conversation history
    if get_messages():
        # Render clickable dashboard
        clicked_dimension = render_problem_dashboard_horizontal(get_diagnosis_dict())

        # Handle dimension click - show detail expansion
        if clicked_dimension:
            st.session_state.expanded_dimension = clicked_dimension

        # Show expanded dimension detail if one was clicked
        if st.session_state.get("expanded_dimension"):
            render_dimension_detail(
                st.session_state.expanded_dimension,
                get_diagnosis_dict()
            )
            # Add close button
            if st.button("✕ Close", key="close_detail"):
                st.session_state.expanded_dimension = None
                st.rerun()

    # Handle research mode
    if st.session_state.researching and client and research_agent:
        with st.chat_message("assistant", avatar="🧠"):
            st.markdown("**🔍 Researching your challenge...**")

            # Progress feedback for long-running research
            progress_bar = st.progress(0, text="Initializing research...")
            status_text = st.empty()

            status_text.markdown("*Step 1/3: Analyzing conversation context...*")
            progress_bar.progress(15, text="Analyzing context...")

            status_text.markdown("*Step 2/3: Generating search queries and fetching sources...*")
            progress_bar.progress(30, text="Searching web sources...")

            full_diagnosis = st.session_state.full_diagnosis or {}
            research_results = research_agent.research(
                get_messages(),
                full_diagnosis
            )

            status_text.markdown("*Step 3/3: Synthesizing findings...*")
            progress_bar.progress(90, text="Synthesizing findings...")

            # Clear progress indicators
            progress_bar.progress(100, text="Research complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()

            render_research_panel(research_results)

            # Store research
            st.session_state.research.last_research = research_results
            st.session_state.research.has_researched = True
            st.session_state.research.research_count += 1

            # Add to messages
            research_summary = research_results.get("research_summary", "Research completed.")
            add_message("assistant", f"**Research Findings:**\n\n{research_summary}", [])

        st.session_state.researching = False
        st.rerun()

    # Handle Pyramid Analysis mode (user clicked button) - STICKY PROGRESS WITH QUOTES
    if st.session_state.get("pyramid_analyzing") and client and minto_analyzer:
        # Initialize quote rotator with current diagnosis for relevant quotes
        quote_rotator = ThinkingQuoteRotator(get_diagnosis_dict())

        # Sticky progress indicator near chat input
        progress_col, cancel_col = st.columns([5, 1])

        with cancel_col:
            if st.button("❌ Cancel", key="cancel_minto_analysis", help="Cancel analysis"):
                st.session_state.pyramid_analyzing = False
                st.toast("Analysis cancelled", icon="⚠️")
                st.rerun()

        progress_placeholder = progress_col.empty()

        def render_sticky_progress_with_quote(step: int, status: str, progress_pct: int, quote: str = ""):
            """Render sticky progress indicator with Larry-style quote."""
            quote_html = f'<div style="font-style: italic; color: #595959; font-size: 0.85rem; margin-top: 0.75rem; padding: 0.5rem; background: rgba(42, 157, 143, 0.08); border-radius: 8px; border-left: 3px solid #2A9D8F;">{quote}</div>' if quote else ""

            progress_placeholder.markdown(f"""
            <div class="sticky-progress-container">
                <div class="sticky-progress-header">
                    <span class="icon">📐</span>
                    <span>Minto Pyramid Analysis</span>
                </div>
                <div style="background: #E5E4E1; border-radius: 4px; height: 8px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #2A9D8F, #32B8C6); height: 100%; width: {progress_pct}%; transition: width 0.3s ease;"></div>
                </div>
                <div class="sticky-progress-status">Step {step}/3: {status}</div>
                {quote_html}
            </div>
            """, unsafe_allow_html=True)

        # Step 1: Minto Pyramid Analysis with thinking quote
        current_quote = quote_rotator.next_quote()
        render_sticky_progress_with_quote(1, "Building Minto Pyramid (SCQA framework)...", 20, current_quote)

        # Run analysis directly (no threading - Streamlit doesn't support it well)
        pyramid = None
        analysis_error = None

        try:
            pyramid = minto_analyzer.analyze(get_messages(), get_diagnosis_dict())
        except Exception as e:
            analysis_error = str(e)

        if analysis_error or not pyramid:
            progress_placeholder.empty()
            st.toast(f"⚠️ Analysis issue: {analysis_error or 'Unknown error'}...", icon="⚠️")
            st.session_state.pyramid_analyzing = False
            st.rerun()

        st.session_state.framework_state.pyramid_analysis = pyramid

        # Check for timeout/error in result
        if pyramid.get("_error"):
            st.toast(f"⚠️ {pyramid.get('_error', 'Analysis issue')[:50]}...", icon="⚠️")

        # Step 2: Signal Detection
        current_quote = quote_rotator.next_quote()
        render_sticky_progress_with_quote(2, "Detecting signals for framework selection...", 50, current_quote)
        time.sleep(0.5)

        # Step 3: Framework Recommendations
        current_quote = quote_rotator.next_quote()
        render_sticky_progress_with_quote(3, "Selecting best frameworks from 343-framework taxonomy...", 70, current_quote)

        if framework_recommender:
            recommendations = framework_recommender.recommend(
                pyramid,
                get_diagnosis_dict(),
                get_messages()
            )
            st.session_state.framework_state.framework_recommendations = recommendations

            current_quote = quote_rotator.next_quote()
            render_sticky_progress_with_quote(3, "Framework selection complete!", 100, current_quote)
            time.sleep(0.8)

        # Clear progress and show result in chat
        progress_placeholder.empty()

        # Add result as assistant message
        scqa = pyramid.get("scqa", {})
        framework_names = []
        if framework_recommender and st.session_state.framework_state.framework_recommendations:
            framework_names = [
                f.get("title", "Unknown")
                for f in st.session_state.framework_state.framework_recommendations.get("recommended_frameworks", [])
            ]

        # Check for errors in analysis
        pyramid_error = pyramid.get("_error", "")
        rec_error = ""
        if st.session_state.framework_state.framework_recommendations:
            rec_error = st.session_state.framework_state.framework_recommendations.get("_error", "")

        error_note = ""
        if pyramid_error or rec_error:
            error_note = f"\n\n⚠️ *Analysis used fallback: {pyramid_error or rec_error}*"

        result_msg = f"""**📐 Minto Pyramid Analysis Complete**

**Context Analysis (SCQA):**
- **Situation:** {scqa.get('situation', 'N/A')}
- **Complication:** {scqa.get('complication', 'N/A')}
- **Question:** {scqa.get('question', 'N/A')}
- **Direction:** {scqa.get('answer_direction', 'N/A')}

**Recommended Frameworks ({len(framework_names)}):** {', '.join(framework_names) if framework_names else 'None - check sidebar status'}

👆 **Scroll up** to see framework selection buttons, or click them in the panel above the chat.{error_note}"""

        add_message("assistant", result_msg)

        st.session_state.pyramid_analyzing = False
        st.rerun()

    # Welcome message
    if not get_messages():
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-icon">🧠</div>
            <div class="welcome-title">Welcome! I'm Larry, your innovation mentor.</div>
            <div class="welcome-text">
                I'm here to help you discover and refine <strong>problems worth solving</strong>.
                Rather than giving easy answers, I'll challenge your thinking,
                ask better questions, and help you see challenges from new angles.
                <br><br>
                As we talk, I'll diagnose your problem across four dimensions to recommend
                the best frameworks and approaches.
            </div>
            <div class="welcome-question">
                "What problem are you really trying to solve?"
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick Actions
        st.markdown("### 💡 Quick Start")
        cols = st.columns(3)
        for i, action in enumerate(QUICK_ACTIONS[:3]):
            with cols[i]:
                if st.button(f"{action['icon']} {action['label']}", key=f"quick_{i}", use_container_width=True):
                    st.session_state.quick_action = action['label']
                    st.rerun()

        cols2 = st.columns(3)
        for i, action in enumerate(QUICK_ACTIONS[3:]):
            with cols2[i]:
                if st.button(f"{action['icon']} {action['label']}", key=f"quick_{i+3}", use_container_width=True):
                    st.session_state.quick_action = action['label']
                    st.rerun()

    # Handle quick action
    if st.session_state.get("quick_action") and not get_messages():
        prompt = st.session_state.quick_action
        st.session_state.quick_action = None

        add_message("user", prompt)
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🧠"):
            if client:
                # Get knowledge base for RAG
                kb = init_supabase_kb()

                # Streaming response
                response_placeholder = st.empty()
                full_response = ""
                citations = []

                try:
                    # Get selected persona's system prompt
                    active_persona = get_persona(st.session_state.get("selected_persona", "mentor"))

                    stream = stream_larry_response(
                        client=client,
                        query=prompt,
                        chat_history=[],
                        system_prompt=active_persona.system_prompt,
                        diagnosis=get_diagnosis_dict(),
                        knowledge_base=kb
                    )

                    for chunk in stream:
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")

                    response_placeholder.markdown(full_response)
                    citations = stream.citations

                except Exception as e:
                    full_response = f"Let me try a different approach. What's the core challenge you're facing?"
                    response_placeholder.markdown(full_response)

                if citations:
                    with st.expander("📚 Knowledge Sources", expanded=False):
                        for cite in citations:
                            st.markdown(f"""
                            <div class="citation-card">
                                <div class="citation-title">📘 {cite.get('title', 'Document')}</div>
                                <div class="citation-excerpt">{cite.get('text', '')}</div>
                            </div>
                            """, unsafe_allow_html=True)

                add_message("assistant", full_response, citations)

                # Run diagnosis for quick action (fast, automatic) with loading indicator
                if consolidator and len(get_messages()) >= 2:
                    with st.status("📊 Updating diagnosis...", expanded=False) as diagnosis_status:
                        try:
                            st.write("Analyzing conversation patterns...")
                            diagnosis = consolidator.diagnose(
                                get_messages(),
                                st.session_state.full_diagnosis,
                                result.get("citations", [])
                            )
                            update_diagnosis(diagnosis)
                            st.session_state.diagnosis_error = None  # Clear error on success
                            diagnosis_status.update(label="✅ Diagnosis updated", state="complete", expanded=False)
                        except Exception as e:
                            st.session_state.diagnosis_error = str(e)
                            diagnosis_status.update(label="⚠️ Diagnosis failed", state="error", expanded=False)
                            # Show non-blocking warning
                            st.toast(f"⚠️ Diagnosis update failed: {str(e)[:50]}...", icon="⚠️")

                st.rerun()

    # Display chat messages
    for message in get_messages():
        avatar = "🧑‍🎓" if message["role"] == "user" else "🧠"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

            # Show citations
            if message.get("citations"):
                with st.expander("📚 Knowledge Sources", expanded=False):
                    for cite in message["citations"]:
                        st.markdown(f"""
                        <div class="citation-card">
                            <div class="citation-title">📘 {cite.get('title', 'Document')}</div>
                            <div class="citation-excerpt">{cite.get('text', '')}</div>
                        </div>
                        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # FRAMEWORK SYSTEM (Above Chat Input)
    # ═══════════════════════════════════════════════════════════════════════════

    # Show consolidated report if available
    if st.session_state.framework_state.consolidated_report:
        render_consolidated_report(st.session_state.framework_state.consolidated_report)
        # Button to clear and continue
        if st.button("✓ Continue Conversation", key="clear_framework_report"):
            st.session_state.framework_state.consolidated_report = None
            st.session_state.framework_state.framework_results = []
            clear_framework_selection()
            st.rerun()

    # Show framework selector if recommendations are available and no report showing
    elif (st.session_state.framework_state.framework_recommendations and
          get_messages() and
          not st.session_state.get("analyzing_frameworks")):

        # Show SCQA summary from Minto analysis
        if st.session_state.framework_state.pyramid_analysis:
            render_pyramid_summary(st.session_state.framework_state.pyramid_analysis)

        # Render framework selector
        selected_frameworks = render_framework_selector(
            st.session_state.framework_state.framework_recommendations
        )

        # Handle framework selection (user clicked Apply)
        if selected_frameworks:
            st.session_state.analyzing_frameworks = True
            st.session_state.selected_frameworks = set(selected_frameworks)
            st.rerun()

    # Handle framework execution with cancel support
    if st.session_state.get("analyzing_frameworks") and client and framework_executor:
        selected_ids = list(st.session_state.selected_frameworks)

        with st.chat_message("assistant", avatar="🧠"):
            # Progress and cancel UI
            progress_col, cancel_col = st.columns([4, 1])
            with progress_col:
                st.markdown(f"**🧩 Applying {len(selected_ids)} framework{'s' if len(selected_ids) > 1 else ''}...**")
                progress_bar = st.progress(0)
            with cancel_col:
                if st.button("❌ Cancel", key="cancel_framework_analysis", help="Stop framework analysis"):
                    st.session_state.cancel_framework_analysis = True
                    st.session_state.analyzing_frameworks = False
                    st.warning("⚠️ Analysis cancelled by user.")
                    clear_framework_selection()
                    st.rerun()

            # Execute frameworks in parallel
            import concurrent.futures
            results = []

            pyramid = st.session_state.framework_state.pyramid_analysis or {}
            diagnosis = get_diagnosis_dict()
            cancelled = False

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
                futures = {
                    pool.submit(
                        framework_executor.execute,
                        fid,
                        pyramid,
                        get_messages(),
                        diagnosis
                    ): fid for fid in selected_ids
                }

                completed = 0
                for future in concurrent.futures.as_completed(futures):
                    # Check for cancellation
                    if st.session_state.get("cancel_framework_analysis"):
                        cancelled = True
                        # Cancel remaining futures
                        for f in futures:
                            f.cancel()
                        break

                    try:
                        result = future.result()
                        results.append(result)
                        completed += 1
                        progress_bar.progress(completed / len(selected_ids))
                        st.write(f"✓ {result.get('framework_title', 'Framework')} complete")
                    except Exception as e:
                        completed += 1
                        progress_bar.progress(completed / len(selected_ids))
                        st.write(f"⚠️ Framework error: {str(e)[:50]}")

            # Clear cancellation flag
            st.session_state.cancel_framework_analysis = False

            if cancelled:
                st.warning("⚠️ Analysis was cancelled. Partial results may be available.")
            else:
                progress_bar.progress(1.0)

            # Store results (even partial ones)
            st.session_state.framework_state.framework_results = results

            # Consolidate if multiple frameworks and not cancelled
            if len(results) > 0 and framework_consolidator and not cancelled:
                with st.spinner("Consolidating insights..."):
                    consolidated = framework_consolidator.consolidate(
                        results,
                        pyramid,
                        get_messages()
                    )
                    st.session_state.framework_state.consolidated_report = consolidated

                    # Add summary to chat
                    summary = consolidated.get("consolidated_report", {}).get("executive_summary", "")
                    if summary:
                        add_message("assistant", f"**📊 Framework Analysis:**\n\n{summary}",
                                   consolidated.get("all_citations", []))

        st.session_state.analyzing_frameworks = False
        clear_framework_selection()
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Share your challenge, idea, or question..."):
        add_message("user", prompt)
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🧠"):
            if client:
                # Get knowledge base for RAG
                kb = init_supabase_kb()

                # Streaming response with integrated analysis
                response_placeholder = st.empty()
                full_response = ""
                citations = []

                try:
                    # Get selected persona's system prompt
                    active_persona = get_persona(st.session_state.get("selected_persona", "mentor"))

                    # Create streaming response
                    stream = stream_larry_response(
                        client=client,
                        query=prompt,
                        chat_history=get_messages()[:-1],
                        system_prompt=active_persona.system_prompt,
                        diagnosis=get_diagnosis_dict(),
                        knowledge_base=kb
                    )

                    # Stream the response with cursor
                    for chunk in stream:
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")

                    # Final render without cursor
                    response_placeholder.markdown(full_response)

                    # Get citations from stream metadata
                    citations = stream.citations

                except Exception as e:
                    full_response = f"I apologize, but I encountered an issue: {str(e)[:100]}. Let me try again."
                    response_placeholder.markdown(full_response)

                # Show citations if available
                if citations:
                    with st.expander("📚 Knowledge Sources", expanded=False):
                        for cite in citations:
                            st.markdown(f"""
                            <div class="citation-card">
                                <div class="citation-title">📘 {cite.get('title', 'Document')}</div>
                                <div class="citation-excerpt">{cite.get('text', '')}</div>
                            </div>
                            """, unsafe_allow_html=True)

                add_message("assistant", full_response, citations)

                # Run background diagnosis (fast, non-blocking) with loading indicator
                if consolidator and len(get_messages()) >= 2:
                    with st.status("📊 Updating diagnosis...", expanded=False) as diagnosis_status:
                        try:
                            st.write("Analyzing conversation patterns...")
                            diagnosis = consolidator.diagnose(
                                get_messages(),
                                st.session_state.full_diagnosis,
                                result.get("citations", [])
                            )
                            update_diagnosis(diagnosis)
                            st.session_state.diagnosis_error = None  # Clear error on success
                            diagnosis_status.update(label="✅ Diagnosis updated", state="complete", expanded=False)
                            st.rerun()
                        except Exception as e:
                            st.session_state.diagnosis_error = str(e)
                            diagnosis_status.update(label="⚠️ Diagnosis failed", state="error", expanded=False)
                            st.toast(f"⚠️ Diagnosis update failed: {str(e)[:50]}...", icon="⚠️")
                            st.rerun()  # Still rerun to show chat response

            else:
                error_msg = "⚠️ Gemini not configured. Please set GOOGLE_AI_API_KEY."
                st.error(error_msg)
                add_message("assistant", error_msg)


if __name__ == "__main__":
    main()
