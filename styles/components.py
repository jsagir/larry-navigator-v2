"""
Component-specific CSS styles for Larry Navigator v2.0
Warm Educational Theme
"""


def get_main_css() -> str:
    return """
<style>
/* ═══════════════════════════════════════════════════════════════════════════
   FONTS
   ═══════════════════════════════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600&family=Libre+Baskerville:ital@0;1&display=swap');

/* ═══════════════════════════════════════════════════════════════════════════
   CSS VARIABLES
   ═══════════════════════════════════════════════════════════════════════════ */
:root {
    /* Backgrounds */
    --bg-primary: #FCFCF9;
    --bg-secondary: #F7F6F3;
    --bg-tertiary: #EFEEEB;
    --bg-chat-user: #E8F4F3;
    --bg-chat-larry: #FFFFFF;

    /* Borders */
    --border-light: #E5E4E1;
    --border-medium: #D4D3D0;
    --border-focus: #2A9D8F;

    /* Primary */
    --primary-900: #134E4A;
    --primary-700: #1B6B64;
    --primary-600: #21808D;
    --primary-500: #2A9D8F;
    --primary-400: #32B8C6;
    --primary-300: #5DD3D9;
    --primary-100: #D1F2F0;
    --primary-50: #EFFAF9;

    /* PWS */
    --pws-real: #E76F51;
    --pws-real-light: #FCEAE6;
    --pws-winnable: #2A9D8F;
    --pws-winnable-light: #E6F5F3;
    --pws-worth: #E9C46A;
    --pws-worth-light: #FDF8E8;

    /* Problem Types */
    --undefined: #9B7ED9;
    --undefined-light: #F3EFFA;
    --ill-defined: #5B8DEF;
    --ill-defined-light: #EBF1FD;
    --well-defined: #4CAF7D;
    --well-defined-light: #E8F5ED;

    /* Complexity */
    --simple: #66BB6A;
    --complicated: #2A9D8F;
    --complex: #FFB74D;
    --chaotic: #E57373;

    /* Wickedness */
    --tame: #A5D6A7;
    --messy: #FFD54F;
    --wicked-complex: #FFB74D;
    --wicked: #E57373;

    /* Text - WCAG AA compliant (4.5:1 minimum contrast ratio) */
    --text-primary: #1A1A1A;
    --text-secondary: #4A4A4A;
    --text-muted: #595959;  /* Darkened from #7A7A7A for 7:1 contrast */
    --text-hint: #767676;   /* Darkened from #9A9A9A for 4.54:1 contrast (WCAG AA minimum) */
}

/* ═══════════════════════════════════════════════════════════════════════════
   HIDE STREAMLIT DEFAULTS (but keep sidebar toggle visible)
   ═══════════════════════════════════════════════════════════════════════════ */
#MainMenu, footer { visibility: hidden; }

/* Sidebar Toggle Button - Always Visible */
button[data-testid="baseButton-headerNoPadding"],
button[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    visibility: visible !important;
    opacity: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Beautiful Sidebar Toggle when Collapsed */
[data-testid="collapsedControl"] {
    position: fixed !important;
    top: 1rem !important;
    left: 1rem !important;
    z-index: 999999 !important;
    background: linear-gradient(135deg, #2A9D8F 0%, #1B6B64 100%) !important;
    border-radius: 12px !important;
    padding: 0.75rem !important;
    box-shadow: 0 4px 15px rgba(42, 157, 143, 0.4), 0 2px 6px rgba(0,0,0,0.1) !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}

[data-testid="collapsedControl"]::before {
    content: '☰' !important;
    font-size: 1.2rem !important;
    color: white !important;
}

[data-testid="collapsedControl"] svg {
    display: none !important;
}

[data-testid="collapsedControl"]:hover {
    background: linear-gradient(135deg, #32B8C6 0%, #2A9D8F 100%) !important;
    transform: scale(1.05) !important;
    box-shadow: 0 6px 20px rgba(42, 157, 143, 0.5), 0 3px 8px rgba(0,0,0,0.15) !important;
}

/* Sidebar Collapse Button (inside sidebar) */
button[data-testid="stSidebarCollapseButton"] {
    background: transparent !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
    transition: all 0.2s ease !important;
}

button[data-testid="stSidebarCollapseButton"]:hover {
    background: var(--primary-50) !important;
    border-color: var(--primary-400) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   GLOBAL
   ═══════════════════════════════════════════════════════════════════════════ */
.stApp {
    background-color: var(--bg-primary) !important;
}

.main .block-container {
    padding: 1rem 1rem 3rem 1rem;
    max-width: 920px;
}

/* ═══════════════════════════════════════════════════════════════════════════
   SIDEBAR
   ═══════════════════════════════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-light);
}

section[data-testid="stSidebar"] > div:first-child {
    background-color: var(--bg-secondary) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   TYPOGRAPHY
   ═══════════════════════════════════════════════════════════════════════════ */
h1, h2, h3, h4 {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
}

p, li, span, label, div {
    font-family: 'Inter', sans-serif !important;
}

.stMarkdown p {
    color: var(--text-secondary);
    line-height: 1.75;
}

.stMarkdown strong {
    color: var(--text-primary);
}

.stMarkdown em {
    font-family: 'Libre Baskerville', serif !important;
    color: #1B6B64;
}

/* ═══════════════════════════════════════════════════════════════════════════
   CHAT MESSAGES
   ═══════════════════════════════════════════════════════════════════════════ */
[data-testid="stChatMessage"] {
    border-radius: 16px !important;
    padding: 1.25rem 1.5rem !important;
    margin: 0.875rem 0 !important;
    animation: messageSlideUp 0.3s ease-out;
}

@keyframes messageSlideUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Larry's Messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: var(--bg-chat-larry) !important;
    border-left: 4px solid var(--primary-500) !important;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06) !important;
    border-radius: 4px 16px 16px 4px !important;
}

/* User Messages */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: var(--bg-chat-user) !important;
    border-radius: 16px 4px 4px 16px !important;
    margin-left: 3rem !important;
    border-right: 4px solid var(--primary-400) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   CHAT INPUT
   ═══════════════════════════════════════════════════════════════════════════ */
[data-testid="stChatInput"] > div {
    background-color: var(--bg-chat-larry) !important;
    border: 2px solid var(--border-light) !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04) !important;
    transition: all 0.2s ease !important;
}

[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--primary-400) !important;
    box-shadow: 0 0 0 4px var(--primary-100), 0 2px 8px rgba(0, 0, 0, 0.04) !important;
}

[data-testid="stChatInput"] textarea {
    background-color: transparent !important;
    color: var(--text-primary) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   BUTTONS
   ═══════════════════════════════════════════════════════════════════════════ */
.stButton > button {
    background-color: var(--bg-chat-larry) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-medium) !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.625rem 1rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
}

.stButton > button:hover {
    background-color: var(--primary-50) !important;
    border-color: var(--primary-400) !important;
    color: #1B6B64 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(42, 157, 143, 0.15) !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   CUSTOM COMPONENTS
   ═══════════════════════════════════════════════════════════════════════════ */

/* Larry Header */
.larry-header {
    text-align: center;
    padding: 1.5rem 0 2rem 0;
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 1.5rem;
    background: linear-gradient(180deg, var(--bg-chat-larry) 0%, var(--bg-primary) 100%);
    border-radius: 16px 16px 0 0;
}

.larry-logo { font-size: 3rem; margin-bottom: 0.25rem; }

.larry-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 2.25rem;
    font-weight: 700;
    color: #1B6B64;
    margin: 0;
}

.larry-subtitle {
    font-family: 'Libre Baskerville', serif;
    color: var(--text-muted);
    font-size: 1rem;
    font-style: italic;
}

/* PWS Badges */
.pws-badges {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    margin-top: 1.25rem;
    flex-wrap: wrap;
}

.pws-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1rem;
    border-radius: 24px;
    font-size: 0.8rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.pws-badge:hover { transform: translateY(-2px); }

.badge-real {
    background-color: var(--pws-real-light);
    color: var(--pws-real);
    border: 1px solid rgba(231, 111, 81, 0.3);
}

.badge-winnable {
    background-color: var(--pws-winnable-light);
    color: var(--pws-winnable);
    border: 1px solid rgba(42, 157, 143, 0.3);
}

.badge-worth {
    background-color: var(--pws-worth-light);
    color: #7A6300;  /* Darkened from #B8860B for WCAG AA compliance */
    border: 1px solid rgba(233, 196, 106, 0.5);
}

/* Problem Dashboard */
.diagnosis-dashboard {
    background: var(--bg-chat-larry);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
}

.diagnosis-section {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-light);
}

.diagnosis-section:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
}

.diagnosis-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}

/* Definition Track */
.definition-track {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    padding: 0.5rem 0;
}

.definition-track::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 15%;
    right: 15%;
    height: 3px;
    background: var(--border-light);
    transform: translateY(-50%);
    z-index: 0;
}

.definition-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 1;
    flex: 1;
}

.definition-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--bg-secondary);
    border: 3px solid var(--border-medium);
    transition: all 0.3s ease;
}

.definition-dot.active {
    border-color: var(--primary-500);
    background: var(--primary-500);
    box-shadow: 0 0 0 4px var(--primary-100);
}

.definition-dot.completed {
    border-color: var(--well-defined);
    background: var(--well-defined);
}

.def-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
    text-align: center;
}

.def-label.active {
    color: var(--primary-500);
    font-weight: 600;
}

/* Complexity Selector */
.complexity-track {
    display: flex;
    gap: 0.5rem;
}

.complexity-item {
    flex: 1;
    padding: 0.5rem;
    border-radius: 8px;
    text-align: center;
    font-size: 0.75rem;
    font-weight: 500;
    background: var(--bg-secondary);
    color: var(--text-muted);
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.complexity-item.active.simple {
    background: #E8F5E9;
    color: var(--simple);
    border-color: var(--simple);
}

.complexity-item.active.complicated {
    background: var(--pws-winnable-light);
    color: var(--complicated);
    border-color: var(--complicated);
}

.complexity-item.active.complex {
    background: #FFF3E0;
    color: #E65100;
    border-color: var(--complex);
}

.complexity-item.active.chaotic {
    background: #FFEBEE;
    color: var(--chaotic);
    border-color: var(--chaotic);
}

/* Risk-Uncertainty Slider */
.risk-uncertainty-container {
    padding: 0.5rem 0;
}

.risk-uncertainty-track {
    position: relative;
    height: 8px;
    background: linear-gradient(90deg, var(--ill-defined) 0%, var(--undefined) 100%);
    border-radius: 4px;
    margin: 0.75rem 0;
}

.risk-uncertainty-thumb {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 20px;
    height: 20px;
    background: var(--bg-chat-larry);
    border: 3px solid var(--primary-500);
    border-radius: 50%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    transition: left 0.3s ease;
}

.risk-uncertainty-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.7rem;
    color: var(--text-muted);
}

/* Wickedness Scale */
.wickedness-track {
    display: flex;
    gap: 0.5rem;
}

.wickedness-item {
    flex: 1;
    padding: 0.5rem;
    border-radius: 8px;
    text-align: center;
    font-size: 0.75rem;
    font-weight: 500;
    background: var(--bg-secondary);
    color: var(--text-muted);
    border: 1px solid transparent;
    transition: all 0.2s ease;
}

.wickedness-item.active.tame {
    background: #E8F5E9;
    color: #2E7D32;
    border-color: var(--tame);
}

.wickedness-item.active.messy {
    background: #FFFDE7;
    color: #8B6914;  /* Darkened from #F9A825 for WCAG AA compliance */
    border-color: var(--messy);
}

.wickedness-item.active.wicked-complex {
    background: #FFF3E0;
    color: #E65100;
    border-color: var(--wicked-complex);
}

.wickedness-item.active.wicked {
    background: #FFEBEE;
    color: var(--wicked);
    border-color: var(--wicked);
}

/* Research Panel */
.research-panel {
    background: var(--bg-chat-larry);
    border: 1px solid var(--primary-400);
    border-radius: 12px;
    padding: 1.25rem;
    margin: 1rem 0;
}

.research-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    color: var(--primary-500);
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border-light);
}

.research-finding {
    background: var(--bg-secondary);
    border-radius: 8px;
    padding: 1rem;
    margin: 0.75rem 0;
}

.finding-title {
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.finding-source {
    font-size: 0.75rem;
    color: var(--primary-600);
    text-decoration: none;
}

.finding-source:hover {
    text-decoration: underline;
}

/* Citation Card */
.citation-card {
    background: var(--bg-secondary);
    border-left: 3px solid var(--primary-400);
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    margin: 0.75rem 0;
    transition: all 0.2s ease;
}

.citation-card:hover {
    background: var(--primary-50);
    transform: translateX(4px);
}

.citation-icon { font-size: 1.25rem; }

.citation-title {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.9rem;
}

.citation-excerpt {
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-style: italic;
    margin: 0.25rem 0;
}

.citation-meta {
    font-size: 0.7rem;
    color: var(--text-muted);
}

/* Typing Indicator */
.typing-container {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    color: var(--text-muted);
    font-style: italic;
    font-family: 'Libre Baskerville', serif;
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: var(--primary-400);
    border-radius: 50%;
    animation: bounce 1.4s ease-in-out infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-8px); }
}

/* Quick Actions */
.quick-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 1rem 0;
}

.quick-action {
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: 20px;
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.quick-action:hover {
    background: var(--primary-50);
    border-color: var(--primary-400);
    color: var(--primary-700);
    transform: translateY(-2px);
}

/* Profile Card */
.profile-card {
    background: linear-gradient(135deg, var(--primary-50) 0%, var(--bg-chat-larry) 100%);
    border: 1px solid var(--primary-100);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
}

.profile-name {
    font-weight: 600;
    color: var(--primary-700);
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.profile-summary {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* Sidebar Sections */
.sidebar-section {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    margin: 1.5rem 0 0.75rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border-light);
}

/* Framework Pills */
.framework-pill {
    display: inline-block;
    background: var(--primary-100);
    color: var(--primary-700);
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.25rem;
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb { background: var(--border-medium); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* Welcome Card */
.welcome-card {
    background: var(--bg-chat-larry);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(42, 157, 143, 0.08);
    border: 1px solid var(--border-light);
    margin: 2rem auto;
    max-width: 600px;
}

.welcome-icon { font-size: 3.5rem; margin-bottom: 1rem; }

.welcome-title {
    font-family: 'DM Sans', sans-serif;
    color: var(--primary-700);
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.welcome-text {
    color: var(--text-secondary);
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.welcome-question {
    font-family: 'Libre Baskerville', serif;
    color: var(--primary-500);
    font-size: 1.1rem;
    font-style: italic;
}

/* ═══════════════════════════════════════════════════════════════════════════
   ACCESSIBILITY - REDUCED MOTION
   ═══════════════════════════════════════════════════════════════════════════ */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }

    .typing-dot {
        animation: none !important;
    }

    .pws-badge:hover,
    .quick-action:hover,
    .stButton > button:hover {
        transform: none !important;
    }

    @keyframes messageSlideUp {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
    }
}

/* ═══════════════════════════════════════════════════════════════════════════
   ACCESSIBILITY - FOCUS VISIBLE
   ═══════════════════════════════════════════════════════════════════════════ */
*:focus-visible {
    outline: 2px solid var(--primary-500) !important;
    outline-offset: 2px !important;
}

.stButton > button:focus-visible {
    outline: 2px solid var(--primary-500) !important;
    outline-offset: 2px !important;
    box-shadow: 0 0 0 4px var(--primary-100) !important;
}

[data-testid="stChatInput"] > div:focus-visible {
    outline: none !important;
    border-color: var(--primary-400) !important;
    box-shadow: 0 0 0 4px var(--primary-100) !important;
}

/* Dashboard cards focus */
.dash-card:focus-visible,
.complexity-item:focus-visible,
.definition-step:focus-visible {
    outline: 2px solid var(--primary-500) !important;
    outline-offset: 2px !important;
}

/* ═══════════════════════════════════════════════════════════════════════════
   STICKY PROGRESS INDICATOR (Above Chat Input)
   ═══════════════════════════════════════════════════════════════════════════ */
.sticky-progress-container {
    position: fixed;
    bottom: 90px;  /* Above chat input */
    left: 50%;
    transform: translateX(-50%);
    width: calc(100% - 2rem);
    max-width: 880px;
    z-index: 999;
    background: linear-gradient(135deg, var(--primary-50) 0%, var(--bg-chat-larry) 100%);
    border: 2px solid var(--primary-400);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    box-shadow: 0 -4px 20px rgba(42, 157, 143, 0.15), 0 4px 15px rgba(0,0,0,0.1);
    animation: slideUpProgress 0.3s ease-out;
}

@keyframes slideUpProgress {
    from {
        opacity: 0;
        transform: translateX(-50%) translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}

.sticky-progress-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    color: var(--primary-700);
    margin-bottom: 0.75rem;
}

.sticky-progress-header .icon {
    font-size: 1.25rem;
}

.sticky-progress-status {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-style: italic;
    margin-top: 0.5rem;
}

/* Cancel button in sticky progress */
.sticky-progress-cancel {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
}

/* ═══════════════════════════════════════════════════════════════════════════
   ACCESSIBILITY - MOBILE TOUCH TARGETS
   ═══════════════════════════════════════════════════════════════════════════ */
@media (max-width: 768px) {
    .stButton > button {
        min-height: 44px !important;
        min-width: 44px !important;
        padding: 0.75rem 1rem !important;
    }

    .quick-action {
        min-height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .pws-badge {
        min-height: 44px;
        padding: 0.75rem 1.25rem;
    }

    .complexity-item {
        min-height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
}
</style>
"""
