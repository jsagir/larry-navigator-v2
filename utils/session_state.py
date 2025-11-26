"""
Session State Management for Larry Navigator v2.0
With Framework System Support
"""

import streamlit as st
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ConversationState:
    """Tracks conversation state."""
    messages: List[Dict[str, str]] = field(default_factory=list)
    message_count: int = 0
    started_at: datetime = field(default_factory=datetime.now)


@dataclass
class DiagnosisState:
    """Tracks problem diagnosis state."""
    definition: str = "undefined"
    complexity: str = "complex"
    risk_uncertainty: float = 0.5
    wickedness: str = "messy"
    profile: Dict[str, Any] = field(default_factory=dict)
    confidence: Dict[str, float] = field(default_factory=lambda: {
        "definition": 0.3,
        "complexity": 0.3,
        "risk_uncertainty": 0.3,
        "wickedness": 0.3
    })
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class ResearchState:
    """Tracks research state."""
    has_researched: bool = False
    last_research: Optional[Dict[str, Any]] = None
    research_count: int = 0
    show_research_prompt: bool = False
    research_prompt_text: str = ""


@dataclass
class FrameworkState:
    """Tracks framework analysis state."""
    pyramid_analysis: Optional[Dict[str, Any]] = None
    framework_recommendations: Optional[Dict[str, Any]] = None
    selected_frameworks: Set[str] = field(default_factory=set)
    framework_results: List[Dict[str, Any]] = field(default_factory=list)
    consolidated_report: Optional[Dict[str, Any]] = None
    last_updated: datetime = field(default_factory=datetime.now)


def init_session_state() -> None:
    """Initialize all session state variables."""

    if "conversation" not in st.session_state:
        st.session_state.conversation = ConversationState()

    if "diagnosis" not in st.session_state:
        st.session_state.diagnosis = DiagnosisState()

    if "research" not in st.session_state:
        st.session_state.research = ResearchState()

    if "framework_state" not in st.session_state:
        st.session_state.framework_state = FrameworkState()

    if "diagnosing" not in st.session_state:
        st.session_state.diagnosing = False

    if "researching" not in st.session_state:
        st.session_state.researching = False

    if "analyzing_frameworks" not in st.session_state:
        st.session_state.analyzing_frameworks = False

    if "pyramid_analyzing" not in st.session_state:
        st.session_state.pyramid_analyzing = False

    if "full_diagnosis" not in st.session_state:
        st.session_state.full_diagnosis = None

    if "expanded_dimension" not in st.session_state:
        st.session_state.expanded_dimension = None

    if "selected_frameworks" not in st.session_state:
        st.session_state.selected_frameworks = set()


def add_message(role: str, content: str, citations: List = None) -> None:
    """Add a message to conversation history."""
    st.session_state.conversation.messages.append({
        "role": role,
        "content": content,
        "citations": citations or [],
        "timestamp": datetime.now().isoformat()
    })
    st.session_state.conversation.message_count += 1


def update_diagnosis(diagnosis: Dict[str, Any]) -> None:
    """Update diagnosis state from consolidator output."""
    ui_updates = diagnosis.get("ui_updates", {})
    profile = diagnosis.get("profile", {})
    research = diagnosis.get("research", {})

    st.session_state.diagnosis.definition = ui_updates.get("definition", "undefined")
    st.session_state.diagnosis.complexity = ui_updates.get("complexity", "complex")
    st.session_state.diagnosis.risk_uncertainty = ui_updates.get("risk_uncertainty", 0.5)
    st.session_state.diagnosis.wickedness = ui_updates.get("wickedness", "messy")
    st.session_state.diagnosis.profile = profile
    st.session_state.diagnosis.last_updated = datetime.now()

    # Update research state
    st.session_state.research.show_research_prompt = ui_updates.get("show_research_prompt", False)
    st.session_state.research.research_prompt_text = ui_updates.get("research_prompt_text", "")

    # Store full diagnosis
    st.session_state.full_diagnosis = diagnosis


def get_diagnosis_dict() -> Dict[str, Any]:
    """Get diagnosis as dictionary for components."""
    d = st.session_state.diagnosis
    return {
        "definition": d.definition,
        "complexity": d.complexity,
        "risk_uncertainty": d.risk_uncertainty,
        "wickedness": d.wickedness
    }


def get_messages() -> List[Dict[str, str]]:
    """Get conversation messages."""
    return st.session_state.conversation.messages


def clear_session() -> None:
    """Clear all session state."""
    st.session_state.conversation = ConversationState()
    st.session_state.diagnosis = DiagnosisState()
    st.session_state.research = ResearchState()
    st.session_state.framework_state = FrameworkState()
    st.session_state.full_diagnosis = None
    st.session_state.diagnosing = False
    st.session_state.researching = False
    st.session_state.analyzing_frameworks = False
    st.session_state.pyramid_analyzing = False
    st.session_state.expanded_dimension = None
    st.session_state.selected_frameworks = set()
