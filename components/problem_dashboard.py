"""
Problem Diagnosis Dashboard Component
Clickable dashboard with shadows - displays above chat
"""

import streamlit as st
from typing import Dict, Any


def render_problem_dashboard_horizontal(diagnosis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render the 4-dimension problem diagnosis dashboard horizontally above chat.
    Returns clicked dimension info if any.
    """
    definition = diagnosis.get("definition", "undefined")
    complexity = diagnosis.get("complexity", "complex")
    risk_position = diagnosis.get("risk_uncertainty", 0.5)
    wickedness = diagnosis.get("wickedness", "messy")

    # Inject CSS for clickable dashboard
    st.markdown("""
    <style>
    .dashboard-container {
        display: flex;
        gap: 12px;
        padding: 1rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #E5E4E1;
    }
    .dash-card {
        flex: 1;
        background: #FCFCF9;
        border-radius: 12px;
        padding: 1rem;
        border: 2px solid transparent;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .dash-label {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #595959;  /* Darkened from #7A7A7A for WCAG AA compliance */
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .dash-value {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    .dash-indicator {
        display: flex;
        gap: 4px;
        margin-top: 0.5rem;
    }
    .indicator-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #E5E4E1;
    }
    .indicator-dot.active {
        background: #2A9D8F;
        box-shadow: 0 0 0 3px rgba(42, 157, 143, 0.2);
    }
    .indicator-dot.completed {
        background: #4CAF7D;
    }
    .pill-row {
        display: flex;
        gap: 4px;
        margin-top: 0.5rem;
    }
    .mini-pill {
        flex: 1;
        padding: 4px 2px;
        border-radius: 6px;
        text-align: center;
        font-size: 0.75rem;
        font-weight: 600;
        background: #F7F6F3;
        color: #767676;  /* Darkened from #9A9A9A for WCAG AA compliance */
    }
    .mini-pill.active {
        color: white;
    }
    .mini-pill.simple { background: #66BB6A; }
    .mini-pill.complicated { background: #2A9D8F; }
    .mini-pill.complex { background: #E65100; }
    .mini-pill.chaotic { background: #E57373; }
    .mini-pill.tame { background: #2E7D32; }
    .mini-pill.messy { background: #F9A825; }
    .mini-pill.wcomplex { background: #E65100; }
    .mini-pill.wicked { background: #E57373; }
    .slider-mini {
        height: 6px;
        background: linear-gradient(90deg, #5B8DEF 0%, #9B7ED9 100%);
        border-radius: 3px;
        position: relative;
        margin-top: 0.75rem;
    }
    .slider-thumb-mini {
        position: absolute;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 14px;
        height: 14px;
        background: white;
        border: 3px solid #2A9D8F;
        border-radius: 50%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .value-undefined { color: #9B7ED9; }
    .value-ill-defined { color: #5B8DEF; }
    .value-well-defined { color: #4CAF7D; }
    .value-simple { color: #66BB6A; }
    .value-complicated { color: #2A9D8F; }
    .value-complex { color: #E65100; }
    .value-chaotic { color: #E57373; }
    .value-tame { color: #2E7D32; }
    .value-messy { color: #F9A825; }
    .value-wicked { color: #E57373; }
    </style>
    """, unsafe_allow_html=True)

    # Definition card
    levels = ["undefined", "ill-defined", "well-defined"]
    current_idx = levels.index(definition) if definition in levels else 0
    def_dots = ""
    for i in range(3):
        if i == current_idx:
            def_dots += '<div class="indicator-dot active"></div>'
        elif i < current_idx:
            def_dots += '<div class="indicator-dot completed"></div>'
        else:
            def_dots += '<div class="indicator-dot"></div>'

    def_display = definition.replace("-", " ").title()

    # Complexity pills - using inline styles for reliable rendering
    complexity_colors = {
        "simple": "#66BB6A",
        "complicated": "#2A9D8F",
        "complex": "#E65100",
        "chaotic": "#E57373"
    }
    comp_pills = ""
    complexity_labels = {"simple": "Simp", "complicated": "Compd", "complex": "Cplx", "chaotic": "Chao"}
    for level in ["simple", "complicated", "complex", "chaotic"]:
        short = complexity_labels[level]
        if level == complexity:
            bg_color = complexity_colors.get(level, "#2A9D8F")
            comp_pills += f'''<div style="flex: 1; padding: 4px 2px; border-radius: 6px;
                text-align: center; font-size: 0.75rem; font-weight: 600;
                background: {bg_color}; color: white;">{short}</div>'''
        else:
            comp_pills += f'''<div style="flex: 1; padding: 4px 2px; border-radius: 6px;
                text-align: center; font-size: 0.75rem; font-weight: 600;
                background: #F7F6F3; color: #767676;">{short}</div>'''

    # Wickedness pills - using inline styles for reliable rendering
    wickedness_colors = {
        "tame": "#2E7D32",
        "messy": "#F9A825",
        "complex": "#E65100",
        "wicked": "#E57373"
    }
    wick_pills = ""
    for level in ["tame", "messy", "complex", "wicked"]:
        short = level[:4].title()
        if level == wickedness:
            bg_color = wickedness_colors.get(level, "#F9A825")
            wick_pills += f'''<div style="flex: 1; padding: 4px 2px; border-radius: 6px;
                text-align: center; font-size: 0.75rem; font-weight: 600;
                background: {bg_color}; color: white;">{short}</div>'''
        else:
            wick_pills += f'''<div style="flex: 1; padding: 4px 2px; border-radius: 6px;
                text-align: center; font-size: 0.75rem; font-weight: 600;
                background: #F7F6F3; color: #767676;">{short}</div>'''

    dashboard_html = f"""
    <div class="dashboard-container">
        <!-- Definition Card -->
        <div class="dash-card">
            <div class="dash-label">📍 Definition</div>
            <div class="dash-value value-{definition}">{def_display}</div>
            <div class="dash-indicator">{def_dots}</div>
        </div>

        <!-- Complexity Card -->
        <div class="dash-card">
            <div class="dash-label">🔄 Complexity</div>
            <div class="dash-value value-{complexity}">{complexity.title()}</div>
            <div style="display: flex; gap: 4px; margin-top: 0.5rem;">{comp_pills}</div>
        </div>

        <!-- Knowability Card -->
        <div class="dash-card">
            <div class="dash-label">🎯 Knowability</div>
            <div class="dash-value" style="color: {'#5B8DEF' if risk_position < 0.5 else '#9B7ED9'}">
                {"Risk" if risk_position < 0.3 else "Balanced" if risk_position < 0.7 else "Uncertain"}
            </div>
            <div class="slider-mini">
                <div class="slider-thumb-mini" style="left: {risk_position * 100}%;"></div>
            </div>
        </div>

        <!-- Wickedness Card -->
        <div class="dash-card">
            <div class="dash-label">⚡ Problem Type</div>
            <div class="dash-value value-{wickedness}">{wickedness.title()}</div>
            <div style="display: flex; gap: 4px; margin-top: 0.5rem;">{wick_pills}</div>
        </div>
    </div>
    """

    st.markdown(dashboard_html, unsafe_allow_html=True)

    # Clickable buttons below (actual Streamlit buttons for interaction)
    col1, col2, col3, col4 = st.columns(4)

    clicked = None
    with col1:
        if st.button("📍 Definition", key="btn_def", use_container_width=True, help="Click to learn about problem definition"):
            clicked = "definition"
    with col2:
        if st.button("🔄 Complexity", key="btn_comp", use_container_width=True, help="Click to learn about Cynefin framework"):
            clicked = "complexity"
    with col3:
        if st.button("🎯 Knowability", key="btn_know", use_container_width=True, help="Click to learn about risk vs uncertainty"):
            clicked = "knowability"
    with col4:
        if st.button("⚡ Problem Type", key="btn_wick", use_container_width=True, help="Click to learn about wicked problems"):
            clicked = "wickedness"

    return clicked


def render_dimension_detail(dimension: str, diagnosis: Dict[str, Any]) -> None:
    """Render expanded detail for a clicked dimension."""

    details = {
        "definition": {
            "title": "📍 Problem Definition",
            "description": "How clearly the problem is understood and articulated.",
            "levels": [
                ("Un-defined", "The problem hasn't been clearly identified yet. You're still exploring."),
                ("Ill-defined", "You can describe symptoms but haven't identified root causes."),
                ("Well-defined", "Clear problem statement with specific user, pain point, and constraints.")
            ],
            "current": diagnosis.get("definition", "undefined")
        },
        "complexity": {
            "title": "🔄 Complexity (Cynefin)",
            "description": "What domain does your problem belong to?",
            "levels": [
                ("Simple", "Clear cause and effect. Best practices exist. Sense → Categorize → Respond"),
                ("Complicated", "Requires expertise. Multiple right answers. Sense → Analyze → Respond"),
                ("Complex", "Unpredictable outcomes. Probe → Sense → Respond"),
                ("Chaotic", "No patterns. Act → Sense → Respond immediately")
            ],
            "current": diagnosis.get("complexity", "complex")
        },
        "knowability": {
            "title": "🎯 Knowability (Risk vs Uncertainty)",
            "description": "Can outcomes be predicted or estimated?",
            "levels": [
                ("Risk (Known)", "Probabilities can be estimated based on data and experience."),
                ("Uncertainty (Unknown)", "No basis for prediction. Unknown unknowns.")
            ],
            "current": "risk" if diagnosis.get("risk_uncertainty", 0.5) < 0.5 else "uncertainty"
        },
        "wickedness": {
            "title": "⚡ Problem Wickedness",
            "description": "How 'wicked' is this problem? (Rittel & Webber)",
            "levels": [
                ("Tame", "Definite formulation. Clear stopping rule. Right/wrong solutions."),
                ("Messy", "Multiple stakeholders. Coordination challenges. But knowable."),
                ("Complex", "Multiple valid framings. Solutions create sub-problems."),
                ("Wicked", "No definitive formulation. Every solution is one-shot. Unique.")
            ],
            "current": diagnosis.get("wickedness", "messy")
        }
    }

    info = details.get(dimension, details["definition"])

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #EFFAF9 0%, #fff 100%);
                padding: 1.5rem; border-radius: 12px; margin: 1rem 0;
                border: 1px solid #D1F2F0; box-shadow: 0 4px 15px rgba(42, 157, 143, 0.1);">
        <h3 style="color: #1B6B64; margin: 0 0 0.5rem 0;">{info['title']}</h3>
        <p style="color: #7A7A7A; margin-bottom: 1rem;">{info['description']}</p>
        <div style="background: white; border-radius: 8px; padding: 1rem;">
    """, unsafe_allow_html=True)

    for level, desc in info['levels']:
        is_current = level.lower().replace("-", "").replace(" ", "").startswith(info['current'].lower().replace("-", ""))
        bg = "#E6F5F3" if is_current else "#F7F6F3"
        border = "2px solid #2A9D8F" if is_current else "1px solid #E5E4E1"
        icon = "✓" if is_current else "○"

        st.markdown(f"""
        <div style="background: {bg}; border: {border}; border-radius: 8px;
                    padding: 0.75rem; margin: 0.5rem 0; display: flex; gap: 0.75rem;">
            <span style="font-size: 1.2rem;">{icon}</span>
            <div>
                <strong style="color: #1A1A1A;">{level}</strong>
                <p style="color: #7A7A7A; margin: 0.25rem 0 0 0; font-size: 0.85rem;">{desc}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


def render_profile_card(profile: Dict[str, Any] = None, diagnosis: Dict[str, Any] = None) -> None:
    """
    Render the diagnosis profile card - ALWAYS visible above chat.
    Shows current status, updates dynamically with context, and displays timestamp.
    """
    import datetime

    # Helper function to format time ago
    def _time_ago(dt_str: str) -> str:
        """Convert ISO timestamp to human-readable 'X ago' format."""
        if not dt_str:
            return "just now"
        try:
            dt = datetime.datetime.fromisoformat(dt_str)
            delta = datetime.datetime.now() - dt
            if delta.seconds < 60:
                return "just now"
            elif delta.seconds < 3600:
                mins = delta.seconds // 60
                return f"{mins} min{'s' if mins > 1 else ''} ago"
            elif delta.seconds < 86400:
                hrs = delta.seconds // 3600
                return f"{hrs} hr{'s' if hrs > 1 else ''} ago"
            else:
                days = delta.days
                return f"{days} day{'s' if days > 1 else ''} ago"
        except:
            return "recently"

    # Get last update timestamp
    last_updated = diagnosis.get("last_updated", "") if diagnosis else ""
    time_ago_str = _time_ago(last_updated)

    # Determine state based on profile and diagnosis
    if profile and profile.get("name"):
        name = profile.get("name", "Analyzing...")
        summary = profile.get("summary", "")
        frameworks = profile.get("framework_matches", [])
        approach = profile.get("recommended_approach", "")
        status_color = "#1B6B64"  # Teal when analyzing
        border_color = "#2A9D8F"
        pulse_animation = ""
    elif diagnosis:
        # Have diagnosis but no profile name yet
        definition = diagnosis.get("definition", "undefined")
        complexity = diagnosis.get("complexity", "complex")
        wickedness = diagnosis.get("wickedness", "messy")

        def_display = definition.replace("-", " ").title()
        name = f"Sensing: {def_display} → {complexity.title()}"
        summary = f"Problem type appears to be {wickedness}. Continue sharing to refine diagnosis."
        frameworks = []
        approach = "Sense-making"
        status_color = "#F9A825"  # Gold when sensing
        border_color = "#F9A825"
        pulse_animation = "animation: pulse 2s infinite;"
    else:
        # Initial state - listening
        name = "Listening..."
        summary = "Share your challenge, idea, or question. I'll analyze it across four dimensions as we talk."
        frameworks = []
        approach = ""
        status_color = "#9B7ED9"  # Purple when listening
        border_color = "#9B7ED9"
        pulse_animation = "animation: pulse 2s infinite;"
        time_ago_str = ""  # No timestamp for initial state

    # Build framework pills if available
    framework_pills = "".join([
        f'<span style="display: inline-block; background: #D1F2F0; color: #1B6B64; '
        f'padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; '
        f'font-weight: 500; margin: 0.2rem;">{f}</span>'
        for f in frameworks[:3]
    ])

    # Add CSS animation for pulse effect
    st.markdown("""
    <style>
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .profile-card-live {
        transition: all 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="profile-card-live" style="background: linear-gradient(135deg, #EFFAF9 0%, #fff 100%);
                border: 2px solid {border_color}; border-radius: 12px; padding: 1rem;
                margin: 0.5rem 0 1rem 0; box-shadow: 0 3px 15px rgba(42, 157, 143, 0.12);
                {pulse_animation}">
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <div style="width: 10px; height: 10px; border-radius: 50%; background: {status_color}; {pulse_animation}"></div>
            <div style="font-weight: 600; color: {status_color}; font-size: 0.95rem;">
                📊 {name}
            </div>
        </div>
        <div style="font-size: 0.85rem; color: #7A7A7A; line-height: 1.5;">
            {summary}
        </div>
        {"<div style='margin-top: 0.75rem; font-size: 0.85rem;'><strong>Approach:</strong> " + approach + "</div>" if approach else ""}
        {"<div style='margin-top: 0.5rem;'>" + framework_pills + "</div>" if frameworks else ""}
        {"<div style='margin-top: 0.75rem; font-size: 0.7rem; color: #767676; text-align: right;'>Updated " + time_ago_str + "</div>" if time_ago_str else ""}
    </div>
    """, unsafe_allow_html=True)


# Keep the old function for sidebar compatibility
def render_problem_dashboard(diagnosis: Dict[str, Any]) -> None:
    """Render compact dashboard for sidebar."""
    render_problem_dashboard_horizontal(diagnosis)
