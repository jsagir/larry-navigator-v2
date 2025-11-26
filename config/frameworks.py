"""
Framework Library for Larry Navigator
Phase 1 (Discovery) and Phase 2 (Solution/Validation) frameworks
"""

from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class FrameworkTemplate:
    """Template for storing framework metadata."""
    title: str
    definition: str
    framework_type: str  # "undefined", "ill-defined", "well-defined", "wicked"
    complexity_fit: List[str]  # ["simple", "complicated", "complex", "chaotic"]
    phase: str  # "discovery" or "solution"
    required_concepts: List[str]
    when_to_use: str
    key_questions: List[str]
    output_structure: Dict[str, str]


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: PROBLEM & OPPORTUNITY DISCOVERY FRAMEWORKS
# ═══════════════════════════════════════════════════════════════════════════════

PHASE_1_FRAMEWORKS: Dict[str, FrameworkTemplate] = {
    "jobs_to_be_done": FrameworkTemplate(
        title="Jobs-To-Be-Done (JTBD)",
        definition="Focus on the underlying job customers are trying to accomplish, not the product they're using.",
        framework_type="ill-defined",
        complexity_fit=["complicated", "complex"],
        phase="discovery",
        required_concepts=["functional job", "emotional job", "social job", "job executor", "circumstance"],
        when_to_use="When you need to understand WHY customers behave the way they do, not just WHAT they do.",
        key_questions=[
            "What job is the customer trying to get done?",
            "What are the functional, emotional, and social dimensions?",
            "What circumstances trigger the need for this job?",
            "What alternatives do they currently use?",
            "What pain points exist in current solutions?"
        ],
        output_structure={
            "job_statement": "When [situation], I want to [motivation], so I can [outcome]",
            "job_dimensions": "Functional / Emotional / Social analysis",
            "pain_points": "Current solution gaps",
            "opportunities": "Unmet needs to address"
        }
    ),

    "reverse_salience": FrameworkTemplate(
        title="Reverse Salience",
        definition="Identify what's NOT being said, what's missing, what's being avoided in the problem space.",
        framework_type="undefined",
        complexity_fit=["complex", "chaotic"],
        phase="discovery",
        required_concepts=["absence", "blind spots", "assumptions", "taboos", "unspoken constraints"],
        when_to_use="When the problem feels stuck or when obvious solutions have failed.",
        key_questions=[
            "What's NOT being discussed in this space?",
            "What assumptions are everyone making?",
            "What questions are considered 'off limits'?",
            "What would a naive outsider ask?",
            "What's the elephant in the room?"
        ],
        output_structure={
            "hidden_assumptions": "Assumptions being made",
            "blind_spots": "What's being overlooked",
            "taboo_questions": "Questions not being asked",
            "reframe": "New perspective on the problem"
        }
    ),

    "trending_to_absurd": FrameworkTemplate(
        title="Trending to the Absurd",
        definition="Extrapolate current trends to extreme conclusions to reveal hidden implications.",
        framework_type="undefined",
        complexity_fit=["complex", "chaotic"],
        phase="discovery",
        required_concepts=["trend", "extrapolation", "limiting factor", "inflection point", "absurdity"],
        when_to_use="When exploring long-term implications or challenging conventional wisdom.",
        key_questions=[
            "If this trend continues, what happens in 10 years?",
            "What would stop this trend?",
            "What's the logical extreme?",
            "At what point does it become absurd?",
            "What does the absurdity reveal?"
        ],
        output_structure={
            "current_trend": "Observable pattern",
            "extrapolation": "Where it leads",
            "absurd_endpoint": "Logical extreme",
            "insight": "What this reveals"
        }
    ),

    "scenario_planning": FrameworkTemplate(
        title="Scenario Planning",
        definition="Develop multiple plausible futures to prepare for uncertainty.",
        framework_type="undefined",
        complexity_fit=["complex", "chaotic"],
        phase="discovery",
        required_concepts=["drivers of change", "critical uncertainties", "scenario matrix", "implications", "signposts"],
        when_to_use="When facing high uncertainty and need to prepare for multiple futures.",
        key_questions=[
            "What are the key drivers of change?",
            "What are the critical uncertainties?",
            "What are 2-4 plausible future scenarios?",
            "What are the implications of each?",
            "What would signal each scenario is unfolding?"
        ],
        output_structure={
            "drivers": "Forces shaping the future",
            "uncertainties": "Key unknowns",
            "scenarios": "2-4 distinct futures",
            "implications": "What each means for you"
        }
    ),

    "process_mapping": FrameworkTemplate(
        title="Process Mapping",
        definition="Visualize the current state of a process to identify pain points and opportunities.",
        framework_type="ill-defined",
        complexity_fit=["simple", "complicated"],
        phase="discovery",
        required_concepts=["steps", "actors", "inputs/outputs", "pain points", "decision points"],
        when_to_use="When the problem involves an existing process with friction or inefficiency.",
        key_questions=[
            "What are all the steps in the current process?",
            "Who is involved at each step?",
            "Where does friction occur?",
            "What causes delays or errors?",
            "Which steps add value vs. waste?"
        ],
        output_structure={
            "process_steps": "Sequential flow",
            "actors": "Who does what",
            "pain_points": "Where friction occurs",
            "waste": "Non-value-adding activities"
        }
    ),

    "six_thinking_hats": FrameworkTemplate(
        title="Six Thinking Hats",
        definition="Structured parallel thinking using six distinct perspectives.",
        framework_type="ill-defined",
        complexity_fit=["complicated", "complex"],
        phase="discovery",
        required_concepts=["white (facts)", "red (emotions)", "black (caution)", "yellow (optimism)", "green (creativity)", "blue (process)"],
        when_to_use="When group thinking is stuck or dominated by one perspective.",
        key_questions=[
            "White: What are the facts and data?",
            "Red: What's your gut feeling?",
            "Black: What could go wrong?",
            "Yellow: What are the benefits?",
            "Green: What alternatives exist?",
            "Blue: What's the process forward?"
        ],
        output_structure={
            "facts": "Objective information",
            "feelings": "Emotional reactions",
            "risks": "Potential problems",
            "benefits": "Potential gains",
            "alternatives": "Creative options",
            "next_steps": "Process forward"
        }
    ),

    "root_cause_analysis": FrameworkTemplate(
        title="Root Cause Analysis (5 Whys)",
        definition="Drill down through symptoms to find underlying causes.",
        framework_type="ill-defined",
        complexity_fit=["simple", "complicated"],
        phase="discovery",
        required_concepts=["symptom", "cause chain", "root cause", "systemic factors"],
        when_to_use="When facing a recurring problem or when symptoms are clear but causes are not.",
        key_questions=[
            "What is the observable problem?",
            "Why does that happen? (x5)",
            "Is this the root cause or another symptom?",
            "What systemic factors enable this?",
            "How do we know we've found the root?"
        ],
        output_structure={
            "symptom": "Observable problem",
            "cause_chain": "5 Why analysis",
            "root_cause": "Fundamental cause",
            "systemic_factors": "Enabling conditions"
        }
    ),

    "macro_trends": FrameworkTemplate(
        title="Macro Trends Analysis",
        definition="Analyze large-scale forces shaping your problem space (PESTLE).",
        framework_type="undefined",
        complexity_fit=["complex", "chaotic"],
        phase="discovery",
        required_concepts=["political", "economic", "social", "technological", "legal", "environmental"],
        when_to_use="When you need to understand the external forces affecting your problem.",
        key_questions=[
            "What political factors are relevant?",
            "What economic forces are at play?",
            "What social/cultural shifts matter?",
            "What technological changes are coming?",
            "What legal/regulatory factors apply?",
            "What environmental factors are relevant?"
        ],
        output_structure={
            "political": "Government, policy factors",
            "economic": "Market, financial forces",
            "social": "Cultural, demographic shifts",
            "technological": "Tech trends, disruptions",
            "legal": "Regulatory environment",
            "environmental": "Sustainability factors"
        }
    ),

    "systems_thinking": FrameworkTemplate(
        title="Systems Thinking",
        definition="Understand the problem as part of an interconnected system with feedback loops.",
        framework_type="wicked",
        complexity_fit=["complex", "chaotic"],
        phase="discovery",
        required_concepts=["system boundaries", "feedback loops", "stocks and flows", "leverage points", "emergence"],
        when_to_use="When the problem involves multiple interdependent parts or unintended consequences.",
        key_questions=[
            "What are the boundaries of the system?",
            "What are the key elements and their relationships?",
            "Where are the feedback loops (reinforcing/balancing)?",
            "What are the leverage points?",
            "What emergent behaviors exist?"
        ],
        output_structure={
            "boundaries": "System scope",
            "elements": "Key components",
            "relationships": "Connections and dependencies",
            "feedback_loops": "Reinforcing and balancing",
            "leverage_points": "Where intervention is effective"
        }
    ),

    "value_migration": FrameworkTemplate(
        title="Value Migration",
        definition="Track where value is moving in your industry to find opportunities.",
        framework_type="ill-defined",
        complexity_fit=["complicated", "complex"],
        phase="discovery",
        required_concepts=["value chain", "profit pools", "migration patterns", "value capture", "disruption"],
        when_to_use="When exploring where competitive advantage is shifting in an industry.",
        key_questions=[
            "Where is value being created today?",
            "Where is value migrating to?",
            "What's driving the migration?",
            "Who is capturing the new value?",
            "Where are the profit pools drying up?"
        ],
        output_structure={
            "current_value": "Where value exists today",
            "migration_direction": "Where it's moving",
            "drivers": "Forces causing migration",
            "opportunities": "Where to position"
        }
    ),
}

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2: SOLUTION & BUSINESS CASE FRAMEWORKS
# ═══════════════════════════════════════════════════════════════════════════════

PHASE_2_FRAMEWORKS: Dict[str, FrameworkTemplate] = {
    "pws_triple_validation": FrameworkTemplate(
        title="PWS Triple Validation Compass",
        definition="Validate that a problem is REAL, WINNABLE, and WORTH IT.",
        framework_type="well-defined",
        complexity_fit=["complicated", "complex"],
        phase="solution",
        required_concepts=["real (pain exists)", "winnable (solution feasible)", "worth it (value > cost)"],
        when_to_use="When you have a problem hypothesis and need to validate it's worth solving.",
        key_questions=[
            "REAL: Do people actually experience this pain? Evidence?",
            "WINNABLE: Can a solution be built within constraints?",
            "WORTH IT: Does the value justify the effort?",
            "What's the evidence for each?",
            "What gaps remain?"
        ],
        output_structure={
            "real_score": "Evidence of pain (1-10)",
            "winnable_score": "Feasibility assessment (1-10)",
            "worth_it_score": "Value vs cost (1-10)",
            "evidence": "Supporting data",
            "gaps": "What needs validation"
        }
    ),

    "heart_framework": FrameworkTemplate(
        title="HEART Framework (Pitching)",
        definition="Structure a compelling pitch: Hook, Evidence, Action, Reason, Timeline.",
        framework_type="well-defined",
        complexity_fit=["simple", "complicated"],
        phase="solution",
        required_concepts=["hook", "evidence", "action", "reason", "timeline"],
        when_to_use="When you need to pitch or communicate your solution compellingly.",
        key_questions=[
            "What's the hook that grabs attention?",
            "What evidence supports your claim?",
            "What action do you want them to take?",
            "Why should they care (what's in it for them)?",
            "What's the timeline/urgency?"
        ],
        output_structure={
            "hook": "Attention grabber",
            "evidence": "Supporting proof",
            "action": "Clear ask",
            "reason": "Why it matters to them",
            "timeline": "Urgency/next steps"
        }
    ),

    "mullins_model": FrameworkTemplate(
        title="Mullins 7 Domains Model",
        definition="Assess opportunity attractiveness across market, industry, and team dimensions.",
        framework_type="well-defined",
        complexity_fit=["complicated"],
        phase="solution",
        required_concepts=["market attractiveness", "industry attractiveness", "team capability", "macro/micro"],
        when_to_use="When evaluating whether to pursue a business opportunity.",
        key_questions=[
            "Is the market large and growing?",
            "Is the industry structurally attractive?",
            "Do you have sustainable advantage?",
            "Can you serve the target segment?",
            "Does the team have the right capabilities?"
        ],
        output_structure={
            "market_macro": "Overall market size and growth",
            "market_micro": "Target segment attractiveness",
            "industry_macro": "Industry structure (Porter's)",
            "industry_micro": "Competitive advantage",
            "team_fit": "Team capability match"
        }
    ),

    "business_model_canvas": FrameworkTemplate(
        title="Business Model Canvas",
        definition="Map the 9 building blocks of a business model.",
        framework_type="well-defined",
        complexity_fit=["complicated"],
        phase="solution",
        required_concepts=["value proposition", "customer segments", "channels", "relationships", "revenue", "resources", "activities", "partners", "costs"],
        when_to_use="When designing or evaluating a business model.",
        key_questions=[
            "What value do you deliver?",
            "Who are your customers?",
            "How do you reach them?",
            "What relationships do you build?",
            "How do you make money?",
            "What resources do you need?",
            "What activities are key?",
            "Who are your partners?",
            "What are your costs?"
        ],
        output_structure={
            "value_proposition": "What you offer",
            "customer_segments": "Who you serve",
            "channels": "How you reach them",
            "relationships": "How you engage",
            "revenue_streams": "How you earn",
            "key_resources": "What you need",
            "key_activities": "What you do",
            "key_partners": "Who helps you",
            "cost_structure": "What it costs"
        }
    ),

    "lean_startup_mvp": FrameworkTemplate(
        title="Lean Startup / MVP",
        definition="Build-Measure-Learn cycle with minimum viable product.",
        framework_type="well-defined",
        complexity_fit=["complex"],
        phase="solution",
        required_concepts=["hypothesis", "MVP", "metrics", "pivot/persevere", "validated learning"],
        when_to_use="When you need to test assumptions quickly with minimal investment.",
        key_questions=[
            "What's the riskiest assumption?",
            "What's the smallest test to validate it?",
            "What metric will indicate success?",
            "What will you learn?",
            "Will you pivot or persevere?"
        ],
        output_structure={
            "hypothesis": "Testable assumption",
            "mvp": "Minimum viable product/test",
            "success_metric": "How to measure",
            "learning": "What you discovered",
            "decision": "Pivot or persevere"
        }
    ),

    "stakeholder_mapping": FrameworkTemplate(
        title="Stakeholder Mapping",
        definition="Identify and analyze all parties affected by or affecting the problem/solution.",
        framework_type="wicked",
        complexity_fit=["complicated", "complex"],
        phase="solution",
        required_concepts=["stakeholders", "power", "interest", "influence", "relationships"],
        when_to_use="When multiple parties are involved with different interests.",
        key_questions=[
            "Who are all the stakeholders?",
            "What are their interests?",
            "What power do they have?",
            "How do they influence each other?",
            "Who are allies vs. blockers?"
        ],
        output_structure={
            "stakeholders": "All parties identified",
            "power_interest": "2x2 mapping",
            "interests": "What each wants",
            "strategy": "How to engage each"
        }
    ),
}

# ═══════════════════════════════════════════════════════════════════════════════
# COMBINED LIBRARY ACCESS
# ═══════════════════════════════════════════════════════════════════════════════

ALL_FRAMEWORKS = {**PHASE_1_FRAMEWORKS, **PHASE_2_FRAMEWORKS}


def get_framework(framework_id: str) -> FrameworkTemplate:
    """Get a framework by ID."""
    return ALL_FRAMEWORKS.get(framework_id)


def get_frameworks_for_type(problem_type: str) -> List[FrameworkTemplate]:
    """Get frameworks suitable for a problem type."""
    return [f for f in ALL_FRAMEWORKS.values() if f.framework_type == problem_type]


def get_frameworks_for_complexity(complexity: str) -> List[FrameworkTemplate]:
    """Get frameworks suitable for a complexity level."""
    return [f for f in ALL_FRAMEWORKS.values() if complexity in f.complexity_fit]


def get_discovery_frameworks() -> List[FrameworkTemplate]:
    """Get Phase 1 discovery frameworks."""
    return list(PHASE_1_FRAMEWORKS.values())


def get_solution_frameworks() -> List[FrameworkTemplate]:
    """Get Phase 2 solution frameworks."""
    return list(PHASE_2_FRAMEWORKS.values())


def get_framework_ids() -> List[str]:
    """Get all framework IDs."""
    return list(ALL_FRAMEWORKS.keys())
