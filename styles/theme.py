"""
Larry Navigator Design System - Warm Educational Theme
"""

COLORS = {
    # Backgrounds
    "bg_primary": "#FCFCF9",      # Warm white - main background
    "bg_secondary": "#F7F6F3",    # Soft cream - cards
    "bg_tertiary": "#EFEEEB",     # Light warm gray
    "bg_chat_user": "#E8F4F3",    # Soft teal tint
    "bg_chat_larry": "#FFFFFF",   # Pure white

    # Borders
    "border_light": "#E5E4E1",
    "border_medium": "#D4D3D0",
    "border_focus": "#2A9D8F",

    # Primary Teal
    "primary_900": "#134E4A",
    "primary_700": "#1B6B64",
    "primary_600": "#21808D",
    "primary_500": "#2A9D8F",
    "primary_400": "#32B8C6",
    "primary_300": "#5DD3D9",
    "primary_100": "#D1F2F0",
    "primary_50": "#EFFAF9",

    # PWS Triad
    "pws_real": "#E76F51",
    "pws_real_light": "#FCEAE6",
    "pws_winnable": "#2A9D8F",
    "pws_winnable_light": "#E6F5F3",
    "pws_worth": "#E9C46A",
    "pws_worth_light": "#FDF8E8",

    # Problem Definition
    "undefined": "#9B7ED9",
    "undefined_light": "#F3EFFA",
    "ill_defined": "#5B8DEF",
    "ill_defined_light": "#EBF1FD",
    "well_defined": "#4CAF7D",
    "well_defined_light": "#E8F5ED",

    # Complexity (Cynefin)
    "simple": "#66BB6A",
    "simple_light": "#E8F5E9",
    "complicated": "#2A9D8F",
    "complicated_light": "#E6F5F3",
    "complex": "#FFB74D",
    "complex_light": "#FFF3E0",
    "chaotic": "#E57373",
    "chaotic_light": "#FFEBEE",

    # Wickedness
    "tame": "#A5D6A7",
    "tame_light": "#E8F5E9",
    "messy": "#FFD54F",
    "messy_light": "#FFFDE7",
    "wicked_complex": "#FFB74D",
    "wicked_complex_light": "#FFF3E0",
    "wicked": "#E57373",
    "wicked_light": "#FFEBEE",

    # Text
    "text_primary": "#1A1A1A",
    "text_secondary": "#4A4A4A",
    "text_muted": "#7A7A7A",
    "text_hint": "#9A9A9A",
    "text_link": "#21808D",
}

FONTS = {
    "display": "'DM Sans', sans-serif",
    "body": "'Inter', sans-serif",
    "accent": "'Libre Baskerville', serif",
    "mono": "'JetBrains Mono', monospace",
}

SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "2xl": "3rem",
}

RADIUS = {
    "sm": "8px",
    "md": "12px",
    "lg": "16px",
    "xl": "24px",
    "full": "9999px",
}

SHADOWS = {
    "sm": "0 1px 2px rgba(0,0,0,0.04)",
    "md": "0 2px 8px rgba(0,0,0,0.06)",
    "lg": "0 4px 16px rgba(0,0,0,0.08)",
    "xl": "0 8px 32px rgba(0,0,0,0.12)",
}


def get_css_variables() -> str:
    """Generate CSS custom properties from theme."""
    css = ":root {\n"

    for name, value in COLORS.items():
        css_name = name.replace("_", "-")
        css += f"    --{css_name}: {value};\n"

    css += "}\n"
    return css
