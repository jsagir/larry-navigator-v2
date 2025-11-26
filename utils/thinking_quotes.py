"""
Larry's Thinking Quotes - Innovation wisdom shown while processing
Quotes organized by problem type/stage for contextual relevance
"""

import random
from typing import List, Dict, Any

# Innovation quotes organized by context
THINKING_QUOTES = {
    "discovery": [
        "\"The formulation of a problem is often more essential than its solution.\" — Albert Einstein",
        "\"If I had an hour to solve a problem, I'd spend 55 minutes thinking about the problem and 5 minutes thinking about solutions.\" — Einstein",
        "\"The best way to have a good idea is to have lots of ideas.\" — Linus Pauling",
        "\"Problems are not stop signs, they are guidelines.\" — Robert H. Schuller",
        "\"Every problem is a gift—without problems we would not grow.\" — Anthony Robbins",
    ],
    "definition": [
        "\"A problem well stated is a problem half solved.\" — Charles Kettering",
        "\"The ability to simplify means to eliminate the unnecessary so that the necessary may speak.\" — Hans Hofmann",
        "\"If you can't explain it simply, you don't understand it well enough.\" — Einstein",
        "\"Clarity precedes success.\" — Robin Sharma",
        "\"The most serious mistakes are not being made as a result of wrong answers. The truly dangerous thing is asking the wrong question.\" — Peter Drucker",
    ],
    "complexity": [
        "\"For every complex problem there is an answer that is clear, simple, and wrong.\" — H.L. Mencken",
        "\"Simplicity is the ultimate sophistication.\" — Leonardo da Vinci",
        "\"In the middle of difficulty lies opportunity.\" — Einstein",
        "\"The art of being wise is the art of knowing what to overlook.\" — William James",
        "\"Complex problems have simple, easy-to-understand wrong answers.\" — Grossman's Law",
    ],
    "uncertainty": [
        "\"The only way to discover the limits of the possible is to go beyond them into the impossible.\" — Arthur C. Clarke",
        "\"I have not failed. I've just found 10,000 ways that won't work.\" — Thomas Edison",
        "\"In preparing for battle I have always found that plans are useless, but planning is indispensable.\" — Eisenhower",
        "\"The future cannot be predicted, but futures can be invented.\" — Dennis Gabor",
        "\"Uncertainty is the only certainty there is.\" — John Allen Paulos",
    ],
    "validation": [
        "\"Get out of the building.\" — Steve Blank",
        "\"Your most unhappy customers are your greatest source of learning.\" — Bill Gates",
        "\"Fall in love with the problem, not the solution.\" — Uri Levine",
        "\"The goal is not to build a product. The goal is to learn.\" — Eric Ries",
        "\"Evidence beats opinion. Every time.\" — Marty Cagan",
    ],
    "innovation": [
        "\"Innovation distinguishes between a leader and a follower.\" — Steve Jobs",
        "\"The best time to plant a tree was 20 years ago. The second best time is now.\" — Chinese Proverb",
        "\"Don't find customers for your products, find products for your customers.\" — Seth Godin",
        "\"The secret of change is to focus all of your energy not on fighting the old, but on building the new.\" — Socrates",
        "\"Creativity is thinking up new things. Innovation is doing new things.\" — Theodore Levitt",
    ],
    "strategy": [
        "\"Strategy is about making choices, trade-offs; it's about deliberately choosing to be different.\" — Michael Porter",
        "\"The essence of strategy is choosing what not to do.\" — Michael Porter",
        "\"Vision without execution is hallucination.\" — Thomas Edison",
        "\"Good strategy works by focusing energy and resources on one, or a very few, pivotal objectives.\" — Richard Rumelt",
        "\"If you don't know where you're going, any road will get you there.\" — Lewis Carroll",
    ],
    "wicked": [
        "\"Wicked problems are not solved, they are re-solved—over and over again.\" — Rittel & Webber",
        "\"There's no such thing as a failed experiment, only experiments with unexpected outcomes.\" — Buckminster Fuller",
        "\"In wicked problems, every solution creates new problems.\" — Horst Rittel",
        "\"The significant problems we face cannot be solved at the same level of thinking we were at when we created them.\" — Einstein",
        "\"Progress is impossible without change, and those who cannot change their minds cannot change anything.\" — George Bernard Shaw",
    ],
    "pws": [
        "\"A problem worth solving is Real, Winnable, and Worth it.\" — PWS Framework",
        "\"Before solving, ask: Is this problem REAL? Evidence must exist.\" — PWS Methodology",
        "\"Winnable problems have a plausible path to success.\" — PWS Framework",
        "\"Worth it means the value justifies the effort and risk.\" — PWS Methodology",
        "\"The best problems to solve are at the intersection of Real, Winnable, and Worth It.\" — PWS Framework",
    ],
}

# General quotes for any context
GENERAL_QUOTES = [
    "\"The measure of intelligence is the ability to change.\" — Einstein",
    "\"It is not the strongest of the species that survives, nor the most intelligent. It is the one that is most adaptable to change.\" — Darwin",
    "\"What gets measured gets managed.\" — Peter Drucker",
    "\"Think like a wise man but communicate in the language of the people.\" — W.B. Yeats",
    "\"The only thing worse than starting something and failing... is not starting something.\" — Seth Godin",
    "\"Ideas are easy. Execution is everything.\" — John Doerr",
    "\"Move fast and break things. Unless you are breaking stuff, you are not moving fast enough.\" — Mark Zuckerberg",
    "\"Stay hungry, stay foolish.\" — Steve Jobs",
    "\"The way to get started is to quit talking and begin doing.\" — Walt Disney",
    "\"Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work.\" — Steve Jobs",
]


def get_thinking_quote(diagnosis: Dict[str, Any] = None, used_quotes: List[str] = None) -> str:
    """
    Get a contextually relevant thinking quote based on current diagnosis.

    Args:
        diagnosis: Current problem diagnosis dict
        used_quotes: List of already used quotes to avoid repetition

    Returns:
        A relevant quote string
    """
    if used_quotes is None:
        used_quotes = []

    # Determine relevant categories based on diagnosis
    categories = ["innovation", "pws"]  # Always include these

    if diagnosis:
        definition = diagnosis.get("definition", "undefined")
        complexity = diagnosis.get("complexity", "complex")
        wickedness = diagnosis.get("wickedness", "messy")
        risk_uncertainty = diagnosis.get("risk_uncertainty", 0.5)

        # Add categories based on diagnosis
        if definition in ["undefined", "ill-defined"]:
            categories.extend(["discovery", "definition"])
        elif definition == "well-defined":
            categories.append("validation")

        if complexity in ["complex", "chaotic"]:
            categories.append("complexity")

        if wickedness in ["wicked", "complex"]:
            categories.append("wicked")

        if risk_uncertainty > 0.6:
            categories.append("uncertainty")

        if risk_uncertainty < 0.4:
            categories.append("strategy")

    # Collect quotes from relevant categories
    available_quotes = []
    for cat in set(categories):
        if cat in THINKING_QUOTES:
            available_quotes.extend(THINKING_QUOTES[cat])

    # Add some general quotes
    available_quotes.extend(GENERAL_QUOTES)

    # Filter out used quotes
    fresh_quotes = [q for q in available_quotes if q not in used_quotes]

    # If all quotes used, reset
    if not fresh_quotes:
        fresh_quotes = available_quotes

    return random.choice(fresh_quotes)


def get_thinking_insight(step: int) -> str:
    """Get a thinking insight message for each step."""
    insights = {
        1: "Decomposing your conversation into logical structure...",
        2: "Identifying key signals and patterns in your problem...",
        3: "Matching your situation to proven frameworks...",
    }
    return insights.get(step, "Processing...")


class ThinkingQuoteRotator:
    """Rotates through quotes, avoiding repetition."""

    def __init__(self, diagnosis: Dict[str, Any] = None):
        self.diagnosis = diagnosis
        self.used_quotes = []

    def next_quote(self) -> str:
        """Get the next quote."""
        quote = get_thinking_quote(self.diagnosis, self.used_quotes)
        self.used_quotes.append(quote)
        return quote

    def reset(self):
        """Reset used quotes."""
        self.used_quotes = []
