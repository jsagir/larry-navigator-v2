"""
Framework Selector UI Component
Displays framework recommendation buttons above chat input
Supports multi-select for parallel framework execution
"""

import streamlit as st
from typing import Dict, Any, List, Set


def render_framework_selector(
    recommendations: Dict[str, Any],
    pyramid_summary: str = None
) -> List[str]:
    """
    Render framework selection buttons above chat input.

    Args:
        recommendations: Output from FrameworkRecommender
        pyramid_summary: Optional SCQA summary from Minto analysis

    Returns:
        List of selected framework IDs
    """
    # Initialize selected frameworks in session state
    if "selected_frameworks" not in st.session_state:
        st.session_state.selected_frameworks = set()

    frameworks = recommendations.get("recommended_frameworks", [])

    if not frameworks:
        return []

    # Container for framework selector
    st.markdown("""
    <style>
    .framework-selector-container {
        background: linear-gradient(135deg, #F8F9FA 0%, #FFFFFF 100%);
        border: 1px solid #E5E4E1;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .framework-selector-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 0.75rem;
    }
    .framework-selector-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #1A1A1A;
    }
    .framework-selector-subtitle {
        font-size: 0.7rem;
        color: #7A7A7A;
        margin-bottom: 0.5rem;
    }
    .framework-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0.5rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 0.25rem;
        border: 2px solid transparent;
    }
    .framework-chip.discovery {
        background: #E3F2FD;
        color: #1565C0;
    }
    .framework-chip.discovery:hover {
        background: #BBDEFB;
        border-color: #1565C0;
    }
    .framework-chip.solution {
        background: #E8F5E9;
        color: #2E7D32;
    }
    .framework-chip.solution:hover {
        background: #C8E6C9;
        border-color: #2E7D32;
    }
    .framework-chip.selected {
        border-color: #2A9D8F !important;
        box-shadow: 0 0 0 3px rgba(42, 157, 143, 0.2);
    }
    .relevance-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: currentColor;
        opacity: 0.7;
    }
    .framework-rationale {
        font-size: 0.65rem;
        color: #9A9A9A;
        margin-top: 0.5rem;
        padding: 0.5rem;
        background: #FAFAFA;
        border-radius: 8px;
        display: none;
    }
    .selection-count {
        font-size: 0.7rem;
        color: #2A9D8F;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    # Render header
    primary = recommendations.get("primary_recommendation", "")
    reasoning = recommendations.get("selection_reasoning", "")

    st.markdown(f"""
    <div class="framework-selector-container">
        <div class="framework-selector-header">
            <span style="font-size: 1.2rem;">🧩</span>
            <span class="framework-selector-title">Suggested Frameworks</span>
            <span class="selection-count" id="selection-count"></span>
        </div>
        <div class="framework-selector-subtitle">
            Select one or more frameworks to apply. Multiple selections run in parallel.
        </div>
    """, unsafe_allow_html=True)

    # Close the HTML container
    st.markdown("</div>", unsafe_allow_html=True)

    # Render framework buttons using Streamlit
    cols = st.columns(min(len(frameworks), 4))

    selected = []
    for i, fw in enumerate(frameworks):
        col_idx = i % len(cols)
        with cols[col_idx]:
            fw_id = fw.get("framework_id", "")
            fw_title = fw.get("title", "Unknown")
            relevance = fw.get("relevance_score", 0.5)
            phase = fw.get("phase", "discovery")
            rationale = fw.get("rationale", "")

            # Determine if selected
            is_selected = fw_id in st.session_state.selected_frameworks

            # Create button with unique key
            button_label = f"{'✓ ' if is_selected else ''}{fw_title}"
            help_text = f"{rationale}\n\nRelevance: {relevance:.0%}"

            if st.button(
                button_label,
                key=f"fw_btn_{fw_id}",
                use_container_width=True,
                help=help_text,
                type="primary" if is_selected else "secondary"
            ):
                # Toggle selection
                if fw_id in st.session_state.selected_frameworks:
                    st.session_state.selected_frameworks.discard(fw_id)
                else:
                    st.session_state.selected_frameworks.add(fw_id)
                st.rerun()

            # Show phase indicator
            phase_color = "#1565C0" if phase == "discovery" else "#2E7D32"
            phase_label = "Discovery" if phase == "discovery" else "Solution"
            st.markdown(f"""
            <div style="text-align: center; font-size: 0.6rem; color: {phase_color};">
                {phase_label} • {relevance:.0%} match
            </div>
            """, unsafe_allow_html=True)

    # Show selection summary
    selected_count = len(st.session_state.selected_frameworks)
    if selected_count > 0:
        selected_names = [
            fw.get("title", fw.get("framework_id"))
            for fw in frameworks
            if fw.get("framework_id") in st.session_state.selected_frameworks
        ]

        st.markdown(f"""
        <div style="margin-top: 0.5rem; padding: 0.5rem; background: #E6F5F3;
                    border-radius: 8px; font-size: 0.75rem; color: #1B6B64;">
            <strong>Selected ({selected_count}):</strong> {', '.join(selected_names)}
        </div>
        """, unsafe_allow_html=True)

    # Action buttons row
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if selected_count > 0:
            if st.button(
                f"🚀 Apply {selected_count} Framework{'s' if selected_count > 1 else ''}",
                key="apply_frameworks",
                type="primary",
                use_container_width=True
            ):
                return list(st.session_state.selected_frameworks)

    with col2:
        if selected_count > 0:
            if st.button("Clear", key="clear_selection", use_container_width=True):
                st.session_state.selected_frameworks = set()
                st.rerun()

    with col3:
        if st.button("Skip", key="skip_frameworks", use_container_width=True):
            return []

    return None  # No action taken yet


def render_pyramid_summary(pyramid: Dict[str, Any]) -> None:
    """Render the Minto Pyramid SCQA summary."""
    scqa = pyramid.get("scqa", {})
    context = pyramid.get("context_analysis", {})

    st.markdown("""
    <style>
    .pyramid-summary {
        background: linear-gradient(135deg, #FFF8E1 0%, #FFFFFF 100%);
        border: 1px solid #FFE082;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .pyramid-header {
        font-size: 0.8rem;
        font-weight: 600;
        color: #F57C00;
        margin-bottom: 0.5rem;
    }
    .scqa-item {
        font-size: 0.75rem;
        margin: 0.25rem 0;
        padding: 0.25rem 0;
        border-bottom: 1px solid #FFF3E0;
    }
    .scqa-label {
        font-weight: 600;
        color: #E65100;
    }
    .scqa-value {
        color: #5D4037;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="pyramid-summary">
        <div class="pyramid-header">📐 Context Analysis (SCQA)</div>
        <div class="scqa-item">
            <span class="scqa-label">S:</span>
            <span class="scqa-value">{scqa.get('situation', 'N/A')[:100]}...</span>
        </div>
        <div class="scqa-item">
            <span class="scqa-label">C:</span>
            <span class="scqa-value">{scqa.get('complication', 'N/A')[:100]}...</span>
        </div>
        <div class="scqa-item">
            <span class="scqa-label">Q:</span>
            <span class="scqa-value">{scqa.get('question', 'N/A')[:100]}...</span>
        </div>
        <div class="scqa-item" style="border-bottom: none;">
            <span class="scqa-label">→</span>
            <span class="scqa-value">{scqa.get('answer_direction', 'N/A')[:100]}...</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_consolidated_report(report: Dict[str, Any]) -> None:
    """Render the consolidated framework analysis report."""
    consolidated = report.get("consolidated_report", {})

    st.markdown("""
    <style>
    .consolidated-report {
        background: linear-gradient(135deg, #EFFAF9 0%, #FFFFFF 100%);
        border: 1px solid #D1F2F0;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(42, 157, 143, 0.1);
    }
    .report-header {
        font-size: 1rem;
        font-weight: 600;
        color: #1B6B64;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .report-section {
        margin: 1rem 0;
        padding: 0.75rem;
        background: white;
        border-radius: 8px;
        border: 1px solid #E5E4E1;
    }
    .section-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #2A9D8F;
        margin-bottom: 0.5rem;
    }
    .insight-item {
        font-size: 0.8rem;
        color: #333;
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: #FAFAFA;
        border-radius: 6px;
        border-left: 3px solid #2A9D8F;
    }
    .recommendation-box {
        background: #E6F5F3;
        border: 2px solid #2A9D8F;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .recommendation-text {
        font-size: 0.85rem;
        font-weight: 500;
        color: #1B6B64;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    quality = report.get("analysis_quality", {})
    frameworks_used = quality.get("frameworks_used", 0)

    st.markdown(f"""
    <div class="consolidated-report">
        <div class="report-header">
            <span style="font-size: 1.3rem;">📊</span>
            <span>Consolidated Analysis ({frameworks_used} frameworks)</span>
        </div>
    """, unsafe_allow_html=True)

    # Executive Summary
    st.markdown(f"""
        <div class="report-section">
            <div class="section-title">Executive Summary</div>
            <p style="font-size: 0.85rem; color: #333; line-height: 1.6;">
                {consolidated.get('executive_summary', 'Analysis in progress...')}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Top Insights
    insights = consolidated.get("top_insights", [])[:5]
    if insights:
        insights_html = "".join([
            f'<div class="insight-item">💡 {i.get("insight", "")}</div>'
            for i in insights
        ])
        st.markdown(f"""
        <div class="report-section">
            <div class="section-title">Top Insights</div>
            {insights_html}
        </div>
        """, unsafe_allow_html=True)

    # Unified Recommendation
    recommendation = consolidated.get("unified_recommendation", "")
    if recommendation:
        st.markdown(f"""
        <div class="recommendation-box">
            <div style="font-size: 0.75rem; color: #2A9D8F; margin-bottom: 0.5rem;">
                🎯 UNIFIED RECOMMENDATION
            </div>
            <div class="recommendation-text">{recommendation}</div>
        </div>
        """, unsafe_allow_html=True)

    # Next Steps
    next_steps = consolidated.get("next_steps", [])
    if next_steps:
        st.markdown("<div class='section-title' style='margin-top: 1rem;'>Next Steps</div>", unsafe_allow_html=True)
        for i, step in enumerate(next_steps[:3], 1):
            st.markdown(f"""
            <div style="font-size: 0.8rem; color: #333; margin: 0.25rem 0;">
                {i}. {step.get('action', '')}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Citations
    citations = report.get("all_citations", [])
    if citations:
        with st.expander(f"📚 Citations ({len(citations)})"):
            for cite in citations:
                st.markdown(f"""
                <div style="padding: 0.5rem; margin: 0.25rem 0; background: #F7F6F3; border-radius: 6px;">
                    <div style="font-weight: 600; font-size: 0.75rem; color: #1B6B64;">
                        {cite.get('title', 'Source')}
                    </div>
                    <div style="font-size: 0.7rem; color: #666; margin-top: 0.25rem;">
                        {cite.get('text', '')[:200]}...
                    </div>
                </div>
                """, unsafe_allow_html=True)


def clear_framework_selection():
    """Clear all framework selections."""
    if "selected_frameworks" in st.session_state:
        st.session_state.selected_frameworks = set()
