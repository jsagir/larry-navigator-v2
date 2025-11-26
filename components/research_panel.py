"""
Enhanced Research Results Panel
Displays deep research with citation hierarchy, validation/challenge analysis,
and alternative perspectives
"""

import streamlit as st
from typing import Dict, Any, List


def render_research_panel(results: Dict[str, Any]) -> None:
    """
    Render comprehensive research results with TABBED interface for better UX.
    Reduces information overload by organizing 10+ sections into 4 tabs.

    Args:
        results: Dict containing enhanced research synthesis
    """

    # Research Context
    context = results.get("research_context", {})
    summary = results.get("executive_summary", "")
    citations = results.get("citation_table", [])
    validation = results.get("validation_evidence", {})
    challenges = results.get("challenge_evidence", {})
    alternatives = results.get("alternative_perspectives", [])
    blind_spots = results.get("blind_spots_identified", [])
    insights = results.get("synthesis_insights", [])
    quality = results.get("research_quality", {})
    recommendations = results.get("actionable_recommendations", [])

    # Header (always visible)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;
                border: 1px solid #0f3460;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="font-size: 2rem;">🔬</span>
            <div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #e94560;">
                    Critical Research Analysis
                </div>
                <div style="font-size: 0.8rem; color: #a0a0a0;">
                    Sources from 2021-2025 | Validates & Challenges Your Thinking
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Research Context Box (always visible - anchor context)
    if context:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;
                    border-left: 4px solid #6c5ce7; margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; color: #6c5ce7; font-weight: 600; margin-bottom: 0.5rem;">
                RESEARCH FOCUS
            </div>
            <div style="font-size: 0.9rem; color: #2d3436; font-weight: 500;">
                {context.get('core_question', 'Exploring the problem space')}
            </div>
            <div style="font-size: 0.8rem; color: #636e72; margin-top: 0.5rem;">
                <strong>Your Hypothesis:</strong> {context.get('user_hypothesis', 'Under investigation')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Executive Summary (always visible - TL;DR)
    if summary:
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px;
                    border: 1px solid #dfe6e9; margin-bottom: 1rem;">
            <div style="font-size: 0.75rem; color: #00b894; font-weight: 600; margin-bottom: 0.5rem;">
                EXECUTIVE SUMMARY
            </div>
            <div style="font-size: 0.95rem; color: #2d3436; line-height: 1.6;">
                {summary}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # TABBED INTERFACE - Reduces information overload
    # ═══════════════════════════════════════════════════════════════════════════
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Sources",
        "⚖️ Evidence",
        "💡 Insights",
        "🎯 Actions"
    ])

    with tab1:
        # Citation Table
        if citations:
            st.markdown("#### Citation Hierarchy")
            render_citation_table(citations)
        else:
            st.info("No citations available for this research.")

    with tab2:
        # Validation vs Challenge - Side by Side
        col1, col2 = st.columns(2)

        with col1:
            if validation:
                render_validation_section(validation)
            else:
                st.success("✅ No validation evidence yet")

        with col2:
            if challenges:
                render_challenge_section(challenges)
            else:
                st.warning("⚠️ No challenges identified yet")

        # Alternative Perspectives
        if alternatives:
            st.divider()
            render_alternatives_section(alternatives)

        # Blind Spots
        if blind_spots:
            st.divider()
            render_blind_spots_section(blind_spots)

    with tab3:
        # Synthesis Insights
        if insights:
            render_insights_section(insights)
        else:
            st.info("💡 Insights will emerge as research deepens.")

    with tab4:
        # Recommendations
        if recommendations:
            render_recommendations_section(recommendations)
        else:
            st.info("🎯 Recommendations will appear after analysis.")

    # Research Quality Footer (always visible)
    if quality:
        st.divider()
        render_quality_footer(quality)


def render_citation_table(citations: List[Dict[str, Any]]) -> None:
    """Render the citation table with relevancy hierarchy using Streamlit components."""
    import pandas as pd

    # Build data for dataframe display
    table_data = []
    for cite in citations[:10]:
        rank = cite.get("rank", 0)
        title = cite.get("title", "Source")[:40]
        relevance = cite.get("relevance_score", 5)
        credibility = cite.get("credibility_score", 5)
        stance = cite.get("stance", "nuances")
        finding = cite.get("finding", "")[:80]

        # Emoji indicators for stance
        stance_emoji = "✅" if stance == "validates" else "⚠️" if stance == "challenges" else "💡"

        table_data.append({
            "#": rank,
            "Source": title,
            "Finding": finding + "..." if finding else "-",
            "Relevance": f"{relevance}/10",
            "Credibility": f"{credibility}/10",
            "Stance": f"{stance_emoji} {stance.title()}"
        })

    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "#": st.column_config.NumberColumn(width="small"),
                "Source": st.column_config.TextColumn(width="medium"),
                "Finding": st.column_config.TextColumn(width="large"),
                "Relevance": st.column_config.TextColumn(width="small"),
                "Credibility": st.column_config.TextColumn(width="small"),
                "Stance": st.column_config.TextColumn(width="small"),
            }
        )

        # Show detailed cards with links below the table
        with st.expander("📎 Source Links & Details", expanded=False):
            for cite in citations[:10]:
                rank = cite.get("rank", 0)
                title = cite.get("title", "Source")
                url = cite.get("url", "#")
                source_type = cite.get("source_type", "Web")
                reasoning = cite.get("reasoning", "")[:100]

                st.markdown(f"""
                **#{rank}** [{title}]({url})
                *{source_type}* | Why ranked: {reasoning}...
                """)
                st.divider()


def render_validation_section(validation: Dict[str, Any]) -> None:
    """Render what the research validates."""
    summary = validation.get("summary", "")
    findings = validation.get("findings", [])

    st.markdown("""
    <div style="background: #d1fae5; padding: 1rem; border-radius: 8px;
                border-left: 4px solid #00b894;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
            <span style="font-size: 1.2rem;">✅</span>
            <span style="font-weight: 700; color: #00b894;">VALIDATES</span>
        </div>
    """, unsafe_allow_html=True)

    if summary:
        st.markdown(f"<div style='font-size: 0.85rem; color: #2d3436; margin-bottom: 0.5rem;'>{summary}</div>", unsafe_allow_html=True)

    for finding in findings[:3]:
        claim = finding.get("claim", "")
        evidence = finding.get("evidence", "")[:100]
        confidence = finding.get("confidence", "medium")
        implication = finding.get("implication", "")[:80]
        sources = finding.get("source_refs", [])

        conf_color = "#00b894" if confidence == "high" else "#fdcb6e" if confidence == "medium" else "#e17055"

        st.markdown(f"""
        <div style="background: white; padding: 0.5rem; border-radius: 6px; margin-top: 0.5rem;">
            <div style="font-size: 0.85rem; font-weight: 500; color: #2d3436;">{claim}</div>
            <div style="font-size: 0.75rem; color: #636e72; margin-top: 4px;">"{evidence}..."</div>
            <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                <span style="font-size: 0.7rem; color: {conf_color};">Confidence: {confidence}</span>
                <span style="font-size: 0.7rem; color: #b2bec3;">Sources: {', '.join(map(str, sources))}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_challenge_section(challenges: Dict[str, Any]) -> None:
    """Render what the research challenges."""
    summary = challenges.get("summary", "")
    findings = challenges.get("findings", [])

    st.markdown("""
    <div style="background: #fee2e2; padding: 1rem; border-radius: 8px;
                border-left: 4px solid #e17055;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
            <span style="font-size: 1.2rem;">⚠️</span>
            <span style="font-weight: 700; color: #e17055;">CHALLENGES</span>
        </div>
    """, unsafe_allow_html=True)

    if summary:
        st.markdown(f"<div style='font-size: 0.85rem; color: #2d3436; margin-bottom: 0.5rem;'>{summary}</div>", unsafe_allow_html=True)

    for finding in findings[:3]:
        claim = finding.get("claim", "")
        evidence = finding.get("counter_evidence", "")[:100]
        severity = finding.get("severity", "significant")
        how_to = finding.get("how_to_address", "")[:80]
        sources = finding.get("source_refs", [])

        sev_color = "#e17055" if severity == "critical" else "#fdcb6e" if severity == "significant" else "#00b894"

        st.markdown(f"""
        <div style="background: white; padding: 0.5rem; border-radius: 6px; margin-top: 0.5rem;">
            <div style="font-size: 0.85rem; font-weight: 500; color: #2d3436;">{claim}</div>
            <div style="font-size: 0.75rem; color: #636e72; margin-top: 4px;">"{evidence}..."</div>
            <div style="font-size: 0.75rem; color: #0984e3; margin-top: 4px;">→ {how_to}...</div>
            <div style="display: flex; justify-content: space-between; margin-top: 4px;">
                <span style="font-size: 0.7rem; color: {sev_color};">Severity: {severity}</span>
                <span style="font-size: 0.7rem; color: #b2bec3;">Sources: {', '.join(map(str, sources))}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_alternatives_section(alternatives: List[Dict[str, Any]]) -> None:
    """Render alternative perspectives."""
    st.markdown("### 💡 Alternative Ways of Thinking")

    for alt in alternatives[:3]:
        perspective = alt.get("perspective", "")
        value = alt.get("value", "")
        application = alt.get("application", "")
        sources = alt.get("source_refs", [])

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e0e7ff 0%, #f3f4f6 100%);
                    padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;
                    border-left: 4px solid #6c5ce7;">
            <div style="font-size: 0.9rem; font-weight: 600; color: #4c1d95;">{perspective}</div>
            <div style="font-size: 0.8rem; color: #636e72; margin-top: 0.5rem;">
                <strong>Why consider:</strong> {value}
            </div>
            <div style="font-size: 0.8rem; color: #0984e3; margin-top: 0.25rem;">
                <strong>Apply by:</strong> {application}
            </div>
            <div style="font-size: 0.7rem; color: #b2bec3; margin-top: 0.25rem;">
                Sources: {', '.join(map(str, sources))}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_blind_spots_section(blind_spots: List[Dict[str, Any]]) -> None:
    """Render identified blind spots."""
    st.markdown("### 🔍 Potential Blind Spots")

    for spot in blind_spots[:3]:
        if isinstance(spot, dict):
            blind_spot = spot.get("blind_spot", "")
            why = spot.get("why_it_matters", "")
            action = spot.get("suggested_action", "")
        else:
            blind_spot = str(spot)
            why = ""
            action = ""

        st.markdown(f"""
        <div style="background: #fef3c7; padding: 0.75rem; border-radius: 8px;
                    margin-bottom: 0.5rem; border-left: 4px solid #f59e0b;">
            <div style="font-size: 0.85rem; font-weight: 500; color: #92400e;">{blind_spot}</div>
            {f'<div style="font-size: 0.75rem; color: #636e72; margin-top: 0.25rem;">{why}</div>' if why else ''}
            {f'<div style="font-size: 0.75rem; color: #0984e3; margin-top: 0.25rem;">→ {action}</div>' if action else ''}
        </div>
        """, unsafe_allow_html=True)


def render_insights_section(insights: List[Dict[str, Any]]) -> None:
    """Render synthesis insights."""
    st.markdown("### ✨ Synthesis Insights")

    for insight in insights[:3]:
        text = insight.get("insight", "")
        reasoning = insight.get("reasoning", "")
        sources = insight.get("sources_combined", [])

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fce7f3 0%, #fff 100%);
                    padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;
                    border: 1px solid #f9a8d4;">
            <div style="font-size: 0.9rem; font-weight: 600; color: #9d174d;">{text}</div>
            <div style="font-size: 0.75rem; color: #636e72; margin-top: 0.5rem;">
                <strong>How we got here:</strong> {reasoning}
            </div>
            <div style="font-size: 0.7rem; color: #b2bec3; margin-top: 0.25rem;">
                Combined sources: {', '.join(map(str, sources))}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_recommendations_section(recommendations: List[Dict[str, Any]]) -> None:
    """Render actionable recommendations."""
    st.markdown("### 🎯 Actionable Recommendations")

    for i, rec in enumerate(recommendations[:5], 1):
        text = rec.get("recommendation", "")
        based_on = rec.get("based_on", "")
        priority = rec.get("priority", "medium")
        outcome = rec.get("expected_outcome", "")

        priority_colors = {
            "immediate": ("#e17055", "#fee2e2"),
            "short-term": ("#fdcb6e", "#fef3c7"),
            "long-term": ("#00b894", "#d1fae5")
        }
        text_color, bg_color = priority_colors.get(priority, ("#6c5ce7", "#e0e7ff"))

        st.markdown(f"""
        <div style="background: {bg_color}; padding: 1rem; border-radius: 8px;
                    margin-bottom: 0.5rem; border-left: 4px solid {text_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="font-size: 0.9rem; font-weight: 600; color: #2d3436;">
                    {i}. {text}
                </div>
                <span style="background: {text_color}; color: white; padding: 2px 8px;
                             border-radius: 4px; font-size: 0.7rem; text-transform: uppercase;">
                    {priority}
                </span>
            </div>
            <div style="font-size: 0.75rem; color: #636e72; margin-top: 0.5rem;">
                <strong>Based on:</strong> {based_on}
            </div>
            <div style="font-size: 0.75rem; color: #0984e3; margin-top: 0.25rem;">
                <strong>Expected outcome:</strong> {outcome}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_quality_footer(quality: Dict[str, Any]) -> None:
    """Render research quality assessment."""
    coverage = quality.get("coverage", "")
    gaps = quality.get("gaps", [])
    confidence = quality.get("confidence_level", "medium")
    follow_up = quality.get("recommended_follow_up", [])

    conf_color = "#00b894" if confidence == "high" else "#fdcb6e" if confidence == "medium" else "#e17055"

    st.markdown(f"""
    <div style="background: #f5f6fa; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <div style="font-size: 0.8rem; font-weight: 600; color: #636e72;">RESEARCH QUALITY</div>
            <div style="background: {conf_color}; color: white; padding: 2px 10px;
                        border-radius: 12px; font-size: 0.75rem;">
                {confidence.upper()} CONFIDENCE
            </div>
        </div>
        <div style="font-size: 0.8rem; color: #2d3436;"><strong>Coverage:</strong> {coverage}</div>
        {f'<div style="font-size: 0.75rem; color: #e17055; margin-top: 0.5rem;"><strong>Gaps:</strong> {", ".join(gaps[:3])}</div>' if gaps else ''}
        {f'<div style="font-size: 0.75rem; color: #0984e3; margin-top: 0.5rem;"><strong>Follow-up queries:</strong> {", ".join(follow_up[:2])}</div>' if follow_up else ''}
    </div>
    """, unsafe_allow_html=True)


def render_web_sources(sources: List[Dict[str, Any]]) -> None:
    """Render web sources in an expander."""
    if not sources:
        return

    with st.expander("🌐 All Raw Sources", expanded=False):
        for source in sources[:10]:
            st.markdown(f"""
            <div style="padding: 0.5rem; margin: 0.25rem 0; background: #f7f6f3; border-radius: 6px;">
                <a href="{source.get('url', '#')}" target="_blank" style="color: #0984e3; font-weight: 500;">
                    🌐 {source.get('title', 'Source')}
                </a>
                <div style="font-size: 0.75rem; color: #636e72; margin-top: 0.25rem;">
                    {source.get('content', source.get('snippet', ''))[:150]}...
                </div>
            </div>
            """, unsafe_allow_html=True)
