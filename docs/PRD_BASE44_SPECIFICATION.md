# Larry Navigator - Product Requirements Document
## Base44 Implementation Specification

**Version**: 2.0
**Date**: November 2024
**Author**: Jonathan Sagir
**Platform**: Base44 Low-Code

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Vision](#2-product-vision)
3. [User Personas](#3-user-personas)
4. [Core Features](#4-core-features)
5. [User Flows](#5-user-flows)
6. [Data Models](#6-data-models)
7. [API Integrations](#7-api-integrations)
8. [UI/UX Specification](#8-uiux-specification)
9. [Business Logic & Workflows](#9-business-logic--workflows)
10. [Persona System](#10-persona-system)
11. [RAG Knowledge Base](#11-rag-knowledge-base)
12. [Analytics & Tracking](#12-analytics--tracking)
13. [Security Requirements](#13-security-requirements)
14. [Implementation Phases](#14-implementation-phases)

---

## 1. Executive Summary

### 1.1 What is Larry Navigator?

Larry Navigator is an AI-powered innovation mentor that helps users discover, diagnose, and develop **Problems Worth Solving (PWS)**. Unlike traditional chatbots that provide answers, Larry is a **thinking partner** that:

- Challenges assumptions through Socratic questioning
- Diagnoses problem types (undefined, ill-defined, well-defined, wicked)
- Recommends and applies innovation frameworks
- Guides users through structured problem-solving methodology

### 1.2 Core Value Proposition

> "Innovation begins with problems, not ideas. The best mentors don't give answers — they give better questions."

Larry transforms passive users into active problem-solvers by providing:
1. **Diagnosis before prescription** - Understanding the problem type before suggesting solutions
2. **Framework-driven thinking** - Systematic approaches over random creativity
3. **Socratic methodology** - Questions that deepen understanding
4. **Actionable outcomes** - Every session ends with concrete next steps

### 1.3 Target Platform

Base44 low-code platform with:
- Custom data collections
- AI integrations (Google Gemini)
- External API connections (Supabase)
- Custom UI components
- Workflow automation

---

## 2. Product Vision

### 2.1 Mission Statement

Democratize access to world-class innovation mentorship by encoding decades of methodology into an intelligent, conversational AI system.

### 2.2 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| User Engagement | >5 messages per session | Average conversation length |
| Problem Clarity | 80% report clearer understanding | Post-session survey |
| Framework Application | 70% successfully apply framework | Completion tracking |
| Return Usage | 40% weekly active users | DAU/WAU ratio |
| Session Completion | 60% reach actionable outcome | Conversation analysis |

### 2.3 Competitive Differentiation

| Feature | ChatGPT | Larry Navigator |
|---------|---------|-----------------|
| Problem Diagnosis | Generic | Structured (4-type taxonomy) |
| Framework Selection | User-driven | AI-recommended based on signals |
| Teaching Methodology | Answer-first | Question-first (Socratic) |
| Session Structure | Unstructured | SCQA + Aronhime Close |
| Domain Expertise | General | PWS/Innovation specialized |

---

## 3. User Personas

### 3.1 Primary Persona: The Aspiring Entrepreneur

**Name**: Sarah, 28
**Role**: MBA Student / Early-stage founder
**Goal**: Validate business idea before investing time/money
**Pain Points**:
- Doesn't know if problem is worth solving
- Overwhelmed by framework options
- Needs structured thinking process
- Wants expert guidance without expensive consultants

**User Story**: *"As an aspiring entrepreneur, I want to validate whether my problem is worth solving so that I don't waste months building something nobody needs."*

### 3.2 Secondary Persona: The Corporate Innovator

**Name**: Michael, 42
**Role**: Innovation Manager at Fortune 500
**Goal**: Systematically evaluate innovation opportunities
**Pain Points**:
- Need to justify innovation investments
- Must present structured analysis to leadership
- Wants consistent methodology across projects

**User Story**: *"As a corporate innovator, I want to apply proven frameworks consistently so that I can build a defensible business case for new initiatives."*

### 3.3 Tertiary Persona: The Graduate Student

**Name**: Alex, 24
**Role**: Innovation/Entrepreneurship student
**Goal**: Learn and apply innovation frameworks
**Pain Points**:
- Theoretical knowledge, limited practical application
- Needs feedback on framework usage
- Wants to improve strategic thinking

**User Story**: *"As a student, I want feedback on my framework application so that I can improve my innovation skills before entering the workforce."*

---

## 4. Core Features

### 4.1 Feature Matrix

| Feature | Priority | Complexity | Description |
|---------|----------|------------|-------------|
| AI Chat Interface | P0 | Medium | Core conversational UI with streaming |
| Persona Switching | P0 | Low | Toggle between Mentor/Evaluator/Strategist |
| Problem Diagnosis | P0 | High | Classify problem type automatically |
| Framework Recommendations | P0 | High | Signal-based framework suggestions |
| RAG Knowledge Base | P1 | Medium | Semantic search over PWS content |
| Session History | P1 | Low | Persist and retrieve past conversations |
| Progress Tracking | P2 | Medium | Track user journey through problem-solving |
| Export/Share | P2 | Low | Export session summaries |
| Multi-language | P3 | Medium | Support for Hebrew, Spanish |

### 4.2 Feature Specifications

#### 4.2.1 AI Chat Interface

**Description**: Real-time conversational interface with Larry

**Requirements**:
- Streaming response display (token-by-token)
- Markdown rendering support
- Code block formatting
- Message history persistence
- Typing indicators
- Error handling with graceful fallbacks

**Acceptance Criteria**:
- [ ] First token appears within 2 seconds
- [ ] Full response streams without buffering
- [ ] Conversation persists across page refreshes
- [ ] Graceful handling of API failures

#### 4.2.2 Persona System

**Description**: Three distinct Larry "modes" with different behaviors

| Persona | Icon | Purpose | Behavior |
|---------|------|---------|----------|
| **Larry Mentor** | 🧠 | Problem discovery | Socratic questioning, gentle guidance |
| **Larry Evaluator** | 📋 | Framework assessment | Structured feedback, scoring |
| **Larry Strategist** | 🎯 | Strategic positioning | SCQA analysis, competitive focus |

**Requirements**:
- Visual persona selector in sidebar
- Distinct system prompts per persona
- Persona-specific UI theming (optional)
- Seamless mid-conversation switching

#### 4.2.3 Problem Diagnosis Engine

**Description**: Automatically classify user's problem into taxonomy

**Problem Types**:

| Type | Characteristics | Approach |
|------|-----------------|----------|
| **Undefined** | Future-focused, high uncertainty | Foresight, scenario planning |
| **Ill-Defined** | Visible problem, ambiguous solution | Exploration, multiple pathways |
| **Well-Defined** | Clear parameters, measurable | Optimization, execution |
| **Wicked** | Multi-layered, systemic | Systems thinking, stakeholder mapping |

**Signal Detection**:
The system detects 13 thinking signals to inform diagnosis:

```
causal_ambiguity      - User unclear on root cause
system_bottleneck     - Process or system constraint
stakeholder_conflict  - Multiple competing interests
trend_pressure        - External market/technology change
user_behavior         - Customer/user understanding needed
business_model        - Value creation/capture question
validation_gap        - Assumptions need testing
execution_focus       - Implementation challenges
ideation_needed       - Generating new options
narrative_focus       - Story/positioning question
strategic_choice      - Decision between alternatives
uncertainty_high      - Unknown unknowns dominate
time_pressure         - Urgency constraints
```

#### 4.2.4 Framework Recommendation Engine

**Description**: Match detected signals to appropriate frameworks

**Framework Mapping**:

| Signal | Primary Framework | Alternatives |
|--------|-------------------|--------------|
| causal_ambiguity | Root Cause Analysis / 5 Whys | Fishbone Diagram |
| system_bottleneck | Reverse Salience | Process Mapping, TOC |
| stakeholder_conflict | Stakeholder Mapping | Six Thinking Hats |
| trend_pressure | Scenario Planning | Macro Trends Analysis |
| user_behavior | Jobs-To-Be-Done | Empathy Mapping |
| business_model | Business Model Canvas | Lean Canvas |
| validation_gap | Lean Startup / MVP | Mom Test |
| execution_focus | Process Mapping | Agile Sprint Planning |
| ideation_needed | Six Thinking Hats | SCAMPER, Lateral Thinking |
| narrative_focus | HEART Framework | Golden Circle |
| strategic_choice | Decision Trees | Porter's Five Forces |
| uncertainty_high | Cynefin Framework | Real Options |
| time_pressure | Rapid Prototype | PWS Triple Validation |

---

## 5. User Flows

### 5.1 New User Onboarding Flow

```
┌─────────────────┐
│   Landing Page  │
│  "Meet Larry"   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Quick Context  │
│  (Optional)     │
│  - Your role    │
│  - Your goal    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Select Persona │
│  🧠 📋 🎯       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Start Chat     │
│  Larry greeting │
└─────────────────┘
```

### 5.2 Core Conversation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER MESSAGE                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              SIGNAL DETECTION (Background)                   │
│  - Analyze message + history                                 │
│  - Detect thinking signals                                   │
│  - Determine conversation stage                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              RAG RETRIEVAL (Background)                      │
│  - Embed query                                               │
│  - Search knowledge base                                     │
│  - Retrieve top 5 relevant chunks                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              RESPONSE GENERATION                             │
│  - Inject context + signals into prompt                      │
│  - Generate streaming response                               │
│  - Apply Aronhime Teaching Structure                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              LARRY RESPONSE                                  │
│  1. Hook / Reframe                                           │
│  2. Explicit Diagnosis                                       │
│  3. Apply ONE Framework                                      │
│  4. Ask 2-5 Powerful Questions                               │
│  5. Aronhime Close (Synthesis + Action + Challenge)          │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 Persona Switch Flow

```
User clicks persona button
         │
         ▼
┌─────────────────┐
│ Update session  │
│ state           │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Show transition │
│ message         │
│ "Switching to   │
│  Larry [Mode]"  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Next response   │
│ uses new        │
│ system prompt   │
└─────────────────┘
```

### 5.4 Framework Application Flow

```
┌─────────────────┐
│ Signal Detected │
│ e.g., "causal   │
│ ambiguity"      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Larry suggests  │
│ "5 Whys" framew │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│ User accepts?   │──No─▶│ Continue        │
│                 │      │ conversation    │
└────────┬────────┘      └─────────────────┘
         │Yes
         ▼
┌─────────────────┐
│ Larry guides    │
│ through framewk │
│ step-by-step    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Synthesis &     │
│ Next Steps      │
└─────────────────┘
```

---

## 6. Data Models

### 6.1 Collections Schema

#### 6.1.1 Users Collection

```javascript
{
  collection: "users",
  fields: {
    id: { type: "uuid", primaryKey: true },
    email: { type: "string", required: true, unique: true },
    name: { type: "string" },
    role: { type: "enum", values: ["student", "entrepreneur", "corporate", "other"] },
    created_at: { type: "datetime", default: "now()" },
    last_active: { type: "datetime" },
    preferences: {
      default_persona: { type: "string", default: "mentor" },
      theme: { type: "string", default: "light" }
    },
    metadata: {
      sessions_count: { type: "number", default: 0 },
      frameworks_used: { type: "array" }
    }
  }
}
```

#### 6.1.2 Sessions Collection

```javascript
{
  collection: "sessions",
  fields: {
    id: { type: "uuid", primaryKey: true },
    user_id: { type: "uuid", foreignKey: "users.id" },
    title: { type: "string" },  // Auto-generated from first message
    persona: { type: "string", default: "mentor" },
    created_at: { type: "datetime", default: "now()" },
    updated_at: { type: "datetime" },
    status: { type: "enum", values: ["active", "completed", "archived"] },
    diagnosis: {
      definition: { type: "enum", values: ["undefined", "ill-defined", "well-defined", "wicked"] },
      complexity: { type: "enum", values: ["simple", "complicated", "complex", "chaotic"] },
      signals: { type: "array" },
      primary_signal: { type: "string" }
    },
    summary: { type: "text" },  // AI-generated session summary
    frameworks_applied: { type: "array" },
    outcome: { type: "text" }  // Final action items
  }
}
```

#### 6.1.3 Messages Collection

```javascript
{
  collection: "messages",
  fields: {
    id: { type: "uuid", primaryKey: true },
    session_id: { type: "uuid", foreignKey: "sessions.id" },
    role: { type: "enum", values: ["user", "assistant"] },
    content: { type: "text", required: true },
    created_at: { type: "datetime", default: "now()" },
    metadata: {
      tokens_used: { type: "number" },
      model: { type: "string" },
      latency_ms: { type: "number" },
      signals_detected: { type: "array" },
      framework_suggested: { type: "string" },
      citations: { type: "array" }  // RAG sources used
    }
  }
}
```

#### 6.1.4 Knowledge Base Collection (if not using Supabase)

```javascript
{
  collection: "knowledge_base",
  fields: {
    id: { type: "uuid", primaryKey: true },
    content: { type: "text", required: true },
    title: { type: "string" },
    source: { type: "string" },
    category: { type: "string" },
    embedding: { type: "vector", dimensions: 768 },
    metadata: {
      framework: { type: "string" },
      concepts: { type: "array" },
      author: { type: "string" }
    },
    created_at: { type: "datetime", default: "now()" }
  }
}
```

#### 6.1.5 Frameworks Collection

```javascript
{
  collection: "frameworks",
  fields: {
    id: { type: "string", primaryKey: true },  // e.g., "five_whys"
    name: { type: "string", required: true },
    description: { type: "text" },
    category: { type: "enum", values: ["diagnosis", "ideation", "validation", "strategy", "execution"] },
    signals: { type: "array" },  // Which signals trigger this framework
    steps: { type: "array" },    // Step-by-step guide
    examples: { type: "array" }, // Case studies
    prerequisites: { type: "array" },  // Other frameworks that should come first
    outcomes: { type: "array" }  // What user should have after applying
  }
}
```

### 6.2 Relationships

```
┌─────────┐       ┌──────────┐       ┌──────────┐
│  Users  │──1:N──│ Sessions │──1:N──│ Messages │
└─────────┘       └──────────┘       └──────────┘
                        │
                        │ N:N
                        ▼
                  ┌────────────┐
                  │ Frameworks │
                  └────────────┘
```

---

## 7. API Integrations

### 7.1 Google Gemini AI

**Purpose**: Core LLM for conversation and analysis

**Endpoints Used**:
- `generateContent` - Standard response generation
- `generateContentStream` - Streaming responses
- `embedContent` - Query embedding for RAG

**Configuration**:
```javascript
{
  provider: "google_gemini",
  model: "gemini-2.5-flash",  // Fast model for low latency
  config: {
    temperature: 0.7,
    maxOutputTokens: 2048,
    topP: 0.9,
    topK: 40
  }
}
```

**Rate Limits**:
- 60 requests/minute (free tier)
- 1500 requests/day (free tier)
- Consider upgrading to paid tier for production

### 7.2 Supabase (RAG)

**Purpose**: Vector database for knowledge base retrieval

**Connection**:
```javascript
{
  provider: "supabase",
  url: "https://[project].supabase.co",
  key: "[anon-key]",
  table: "knowledge_base"
}
```

**RPC Function**: `search_knowledge_base`
```sql
CREATE OR REPLACE FUNCTION search_knowledge_base(
  query_embedding vector(768),
  match_threshold float DEFAULT 0.5,
  match_count int DEFAULT 5
)
RETURNS TABLE (
  id uuid,
  content text,
  title text,
  source text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    kb.id,
    kb.content,
    kb.title,
    kb.source,
    1 - (kb.embedding <=> query_embedding) AS similarity
  FROM knowledge_base kb
  WHERE 1 - (kb.embedding <=> query_embedding) > match_threshold
  ORDER BY similarity DESC
  LIMIT match_count;
END;
$$;
```

### 7.3 Authentication (Optional)

**Options**:
1. **Base44 Built-in Auth** - Simple email/password
2. **Supabase Auth** - If already using Supabase
3. **Auth0** - For enterprise SSO requirements

---

## 8. UI/UX Specification

### 8.1 Layout Structure

```
┌────────────────────────────────────────────────────────────────┐
│                         HEADER                                  │
│  [Logo] Larry Navigator          [User Menu] [Settings]         │
├──────────────┬─────────────────────────────────────────────────┤
│              │                                                  │
│   SIDEBAR    │                 MAIN CHAT AREA                   │
│              │                                                  │
│  ┌────────┐  │  ┌────────────────────────────────────────────┐ │
│  │Personas│  │  │                                            │ │
│  │ 🧠 📋 🎯│  │  │  Message bubbles                          │ │
│  └────────┘  │  │                                            │ │
│              │  │  - User messages (right)                   │ │
│  ┌────────┐  │  │  - Larry messages (left)                   │ │
│  │Session │  │  │                                            │ │
│  │History │  │  │                                            │ │
│  │        │  │  │                                            │ │
│  │ • Sess1│  │  │                                            │ │
│  │ • Sess2│  │  │                                            │ │
│  │ • Sess3│  │  └────────────────────────────────────────────┘ │
│  └────────┘  │                                                  │
│              │  ┌────────────────────────────────────────────┐ │
│  ┌────────┐  │  │  [Message Input]                      [▶]  │ │
│  │Diagnosis│  │  └────────────────────────────────────────────┘ │
│  │Dashboard│  │                                                  │
│  └────────┘  │                                                  │
│              │                                                  │
└──────────────┴─────────────────────────────────────────────────┘
```

### 8.2 Component Specifications

#### 8.2.1 Persona Selector

```
┌─────────────────────────────┐
│ Choose Your Larry           │
├─────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐    │
│ │ 🧠  │ │ 📋  │ │ 🎯  │    │
│ │Mentr│ │Eval │ │Strat│    │
│ └─────┘ └─────┘ └─────┘    │
│   ↑ active                  │
├─────────────────────────────┤
│ Socratic guide for problem  │
│ discovery                   │
└─────────────────────────────┘
```

**States**:
- Default: Mentor selected
- Hover: Show tooltip with description
- Active: Highlighted border, checkmark

#### 8.2.2 Chat Message Bubbles

**User Message**:
```
                    ┌────────────────────────┐
                    │ I'm trying to figure   │
                    │ out if my startup idea │
                    │ is worth pursuing...   │
                    └────────────────────────┘
                                        12:34 PM
```

**Larry Message**:
```
┌─────────────────────────────────────────┐
│ 🧠 Larry Mentor                         │
├─────────────────────────────────────────┤
│ That's a great question to be asking    │
│ early. But here's what everyone misses: │
│ the idea itself matters less than the   │
│ **problem** you're solving.             │
│                                         │
│ Let me challenge you with this:         │
│ - What breakdown are you observing?     │
│ - Who experiences this pain?            │
│ - How are they solving it today?        │
└─────────────────────────────────────────┘
12:35 PM
```

#### 8.2.3 Diagnosis Dashboard (Sidebar)

```
┌─────────────────────────────┐
│ 📊 Problem Diagnosis        │
├─────────────────────────────┤
│ Definition:                 │
│ ▓▓▓▓▓▓░░░░ Ill-Defined     │
│                             │
│ Complexity:                 │
│ ▓▓▓▓▓▓▓░░░ Complex         │
│                             │
│ Signals Detected:           │
│ • causal_ambiguity ●        │
│ • validation_gap ○          │
│                             │
│ Suggested Framework:        │
│ ┌─────────────────────────┐ │
│ │ 🔍 Root Cause Analysis  │ │
│ │ "Understand WHY before  │ │
│ │  solving WHAT"          │ │
│ └─────────────────────────┘ │
└─────────────────────────────┘
```

### 8.3 Color Palette

```
Primary:     #2563EB (Blue - Trust, Intelligence)
Secondary:   #7C3AED (Purple - Innovation, Creativity)
Success:     #10B981 (Green - Progress, Validation)
Warning:     #F59E0B (Amber - Attention, Caution)
Error:       #EF4444 (Red - Issues, Blocks)

Background:  #F9FAFB (Light Gray)
Surface:     #FFFFFF (White)
Text:        #111827 (Near Black)
Text Muted:  #6B7280 (Gray)

Persona Colors:
- Mentor:    #3B82F6 (Blue)
- Evaluator: #8B5CF6 (Purple)
- Strategist:#EF4444 (Red)
```

### 8.4 Typography

```
Font Family: Inter, system-ui, sans-serif

Headings:
- H1: 24px, Bold, #111827
- H2: 20px, SemiBold, #111827
- H3: 16px, SemiBold, #374151

Body:
- Regular: 14px, Normal, #374151
- Small: 12px, Normal, #6B7280

Chat:
- User message: 14px, Normal, #111827
- Larry message: 14px, Normal, #1F2937
- Timestamp: 11px, Normal, #9CA3AF
```

### 8.5 Responsive Breakpoints

```
Mobile:  < 640px   - Single column, collapsible sidebar
Tablet:  640-1024px - Narrow sidebar, full chat
Desktop: > 1024px  - Full layout as specified
```

---

## 9. Business Logic & Workflows

### 9.1 Message Processing Pipeline

```javascript
// Pseudocode for message processing

async function processUserMessage(message, session) {
  // 1. Update session
  await saveMessage(session.id, "user", message);

  // 2. Parallel processing
  const [signals, ragContext] = await Promise.all([
    detectSignals(message, session.history),
    retrieveRAGContext(message)
  ]);

  // 3. Update diagnosis
  const diagnosis = await updateDiagnosis(session.diagnosis, signals);
  await updateSession(session.id, { diagnosis });

  // 4. Build enhanced prompt
  const prompt = buildEnhancedPrompt({
    systemPrompt: getPersonaPrompt(session.persona),
    history: session.history,
    ragContext: ragContext,
    signals: signals,
    diagnosis: diagnosis,
    userMessage: message
  });

  // 5. Generate streaming response
  const stream = await generateStreamingResponse(prompt);

  // 6. Process stream
  let fullResponse = "";
  for await (const chunk of stream) {
    yield chunk;  // Send to UI
    fullResponse += chunk;
  }

  // 7. Save assistant message
  await saveMessage(session.id, "assistant", fullResponse, {
    signals: signals,
    ragSources: ragContext.sources
  });

  return fullResponse;
}
```

### 9.2 Signal Detection Logic

```javascript
const SIGNAL_PATTERNS = {
  causal_ambiguity: [
    /why.*(happening|occurring|problem)/i,
    /don't (understand|know) (why|what's causing)/i,
    /root cause/i,
    /what's (really|actually) going on/i
  ],
  validation_gap: [
    /not sure if.*(right|correct|valid)/i,
    /how (do|can) I (test|validate|verify)/i,
    /assumption/i,
    /might be wrong/i
  ],
  stakeholder_conflict: [
    /different (opinions|views|perspectives)/i,
    /(team|they|management) (wants|thinks|believes)/i,
    /conflicting/i,
    /disagree/i
  ],
  // ... more patterns
};

function detectSignals(message, history) {
  const detectedSignals = [];
  const combinedText = [...history.slice(-5), message].join(" ");

  for (const [signal, patterns] of Object.entries(SIGNAL_PATTERNS)) {
    for (const pattern of patterns) {
      if (pattern.test(combinedText)) {
        detectedSignals.push(signal);
        break;
      }
    }
  }

  // Use LLM for nuanced detection
  const llmSignals = await detectSignalsWithLLM(combinedText);

  return mergeAndRank(detectedSignals, llmSignals);
}
```

### 9.3 Framework Selection Logic

```javascript
const FRAMEWORK_MAPPING = {
  causal_ambiguity: {
    primary: "root_cause_analysis",
    alternatives: ["five_whys", "fishbone_diagram"]
  },
  validation_gap: {
    primary: "lean_startup_mvp",
    alternatives: ["mom_test", "discovery_driven_planning"]
  },
  stakeholder_conflict: {
    primary: "stakeholder_mapping",
    alternatives: ["six_thinking_hats", "empathy_mapping"]
  },
  // ... more mappings
};

function recommendFramework(signals, diagnosis) {
  const primarySignal = signals[0];  // Highest ranked signal
  const mapping = FRAMEWORK_MAPPING[primarySignal];

  // Check prerequisites
  const prereqs = getPrerequisites(mapping.primary);
  const missingPrereqs = prereqs.filter(p => !diagnosis.frameworksApplied.includes(p));

  if (missingPrereqs.length > 0) {
    return {
      recommended: missingPrereqs[0],
      reason: "prerequisite",
      next: mapping.primary
    };
  }

  return {
    recommended: mapping.primary,
    alternatives: mapping.alternatives,
    reason: `Detected ${primarySignal} signal`
  };
}
```

### 9.4 Session Lifecycle

```
                    ┌─────────────┐
                    │   CREATED   │
                    └──────┬──────┘
                           │ First message
                           ▼
                    ┌─────────────┐
                    │   ACTIVE    │◄────────┐
                    └──────┬──────┘         │
                           │                 │
           ┌───────────────┼───────────────┐│
           │               │               ││
           ▼               ▼               ▼│
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  COMPLETED  │ │  ARCHIVED   │ │   RESUMED   │──┘
    │ (User ends) │ │ (30 days)   │ │ (User back) │
    └─────────────┘ └─────────────┘ └─────────────┘
```

---

## 10. Persona System

### 10.1 Persona Configuration

```javascript
const PERSONAS = {
  mentor: {
    id: "mentor",
    name: "Larry Mentor",
    icon: "🧠",
    description: "Socratic guide for problem discovery",
    color: "#3B82F6",
    systemPrompt: LARRY_MENTOR_PROMPT,
    behaviors: {
      questionRatio: 0.7,      // 70% responses include questions
      frameworkIntro: "gentle", // Suggest, don't prescribe
      toneWarmth: 0.8,         // Warm and encouraging
      challengeLevel: 0.5      // Moderate challenge
    }
  },
  evaluator: {
    id: "evaluator",
    name: "Larry Evaluator",
    icon: "📋",
    description: "Framework evaluation & feedback",
    color: "#8B5CF6",
    systemPrompt: LARRY_EVALUATOR_PROMPT,
    behaviors: {
      questionRatio: 0.3,
      frameworkIntro: "structured",
      toneWarmth: 0.5,
      challengeLevel: 0.8
    }
  },
  strategist: {
    id: "strategist",
    name: "Larry Strategist",
    icon: "🎯",
    description: "Strategy & competitive positioning",
    color: "#EF4444",
    systemPrompt: LARRY_STRATEGIST_PROMPT,
    behaviors: {
      questionRatio: 0.5,
      frameworkIntro: "analytical",
      toneWarmth: 0.4,
      challengeLevel: 0.9
    }
  }
};
```

### 10.2 Persona Switching Behavior

When user switches persona mid-conversation:

1. **Preserve Context**: Maintain conversation history and diagnosis
2. **Transition Message**: "Switching to Larry [Mode]. Let me look at this from a different angle..."
3. **Adjust Lens**: Apply new persona's analytical framework to existing context
4. **No Reset**: Don't restart the conversation

---

## 11. RAG Knowledge Base

### 11.1 Content Categories

| Category | Description | Example Sources |
|----------|-------------|-----------------|
| **Frameworks** | Innovation methodology descriptions | PWS Course Materials |
| **Concepts** | Key innovation concepts | Glossary entries |
| **Case Studies** | Real-world examples | Published cases |
| **Exercises** | Framework application guides | Workshop materials |
| **Principles** | Core beliefs and philosophies | Aronhime teachings |

### 11.2 Chunk Structure

```javascript
{
  id: "chunk_001",
  content: "Jobs-To-Be-Done (JTBD) is a framework that focuses on understanding...",
  title: "Jobs-To-Be-Done Framework",
  source: "PWS Course - Module 4",
  category: "frameworks",
  metadata: {
    framework_id: "jobs_to_be_done",
    concepts: ["functional_job", "emotional_job", "social_job"],
    author: "Larry Aronhime",
    difficulty: "intermediate"
  },
  embedding: [0.123, -0.456, ...]  // 768 dimensions
}
```

### 11.3 Retrieval Strategy

1. **Embed Query**: Convert user message to vector using `text-embedding-004`
2. **Semantic Search**: Find top 5 chunks with similarity > 0.5
3. **Re-rank** (optional): Use detected signals to boost relevant categories
4. **Format Context**: Structure for LLM consumption

```javascript
async function retrieveRAGContext(query, signals = []) {
  // 1. Embed query
  const embedding = await embedQuery(query);

  // 2. Search
  let results = await supabase.rpc('search_knowledge_base', {
    query_embedding: embedding,
    match_threshold: 0.5,
    match_count: 10
  });

  // 3. Re-rank based on signals
  if (signals.length > 0) {
    results = reRankBySignals(results, signals);
  }

  // 4. Take top 5
  results = results.slice(0, 5);

  // 5. Format
  return {
    context: formatForLLM(results),
    sources: results.map(r => ({ title: r.title, source: r.source }))
  };
}
```

---

## 12. Analytics & Tracking

### 12.1 Events to Track

| Event | Properties | Purpose |
|-------|------------|---------|
| `session_started` | user_id, persona | Usage patterns |
| `message_sent` | session_id, message_length | Engagement |
| `persona_switched` | from, to | Feature usage |
| `framework_suggested` | framework_id, signal | Recommendation effectiveness |
| `framework_applied` | framework_id, session_id | Learning outcomes |
| `session_completed` | duration, messages_count | Completion rates |
| `feedback_given` | rating, comment | Quality measurement |

### 12.2 Metrics Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│ Larry Navigator Analytics                        [7 days ▼] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────┐│
│  │ 1,234       │ │ 5.7         │ │ 62%         │ │ 4.2/5  ││
│  │ Sessions    │ │ Avg Length  │ │ Completion  │ │ Rating ││
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────┘│
│                                                             │
│  Popular Personas:              Top Frameworks:             │
│  🧠 Mentor    68%              1. Root Cause    23%        │
│  📋 Evaluator 22%              2. JTBD          18%        │
│  🎯 Strategist 10%             3. Stakeholder   15%        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 13. Security Requirements

### 13.1 Data Protection

- **Encryption at Rest**: All stored data encrypted
- **Encryption in Transit**: HTTPS only
- **API Key Security**: Never expose in client code
- **PII Handling**: Minimize collection, allow deletion

### 13.2 Authentication

- **Session Tokens**: JWT with 24h expiration
- **Rate Limiting**: 60 requests/minute per user
- **IP Throttling**: Block after 1000 requests/hour

### 13.3 Content Safety

- **Input Sanitization**: Prevent injection attacks
- **Output Filtering**: Block harmful content generation
- **Audit Logging**: Track all AI interactions

---

## 14. Implementation Phases

### Phase 1: MVP (2 weeks)

**Goal**: Basic working chatbot with one persona

**Deliverables**:
- [ ] Chat interface with streaming
- [ ] Larry Mentor persona
- [ ] Basic message history
- [ ] Gemini API integration
- [ ] Deploy to Base44

**Success Criteria**:
- User can have 5-turn conversation
- Responses stream in real-time
- Session persists across refreshes

### Phase 2: Core Features (2 weeks)

**Goal**: Full persona system and diagnosis

**Deliverables**:
- [ ] All 3 personas
- [ ] Persona switching
- [ ] Signal detection
- [ ] Problem diagnosis dashboard
- [ ] Framework recommendations

**Success Criteria**:
- Persona switch works mid-conversation
- Diagnosis updates based on conversation
- Frameworks suggested appropriately

### Phase 3: RAG Integration (1 week)

**Goal**: Knowledge base retrieval

**Deliverables**:
- [ ] Supabase connection
- [ ] Query embedding
- [ ] Context injection
- [ ] Citation display

**Success Criteria**:
- Relevant knowledge retrieved
- Sources shown to user
- Response quality improves

### Phase 4: Polish & Analytics (1 week)

**Goal**: Production-ready application

**Deliverables**:
- [ ] Session history UI
- [ ] User preferences
- [ ] Analytics tracking
- [ ] Error handling
- [ ] Mobile responsiveness

**Success Criteria**:
- Smooth UX across devices
- Metrics visible in dashboard
- Graceful error handling

---

## Appendix A: System Prompts

### A.1 Larry Mentor System Prompt

[See config/personas.py - LARRY_MENTOR_PROMPT]

### A.2 Larry Evaluator System Prompt

[See config/personas.py - LARRY_EVALUATOR_PROMPT]

### A.3 Larry Strategist System Prompt

[See config/personas.py - LARRY_STRATEGIST_PROMPT]

---

## Appendix B: Framework Library

### B.1 Diagnostic Frameworks

1. **Root Cause Analysis / 5 Whys**
2. **Fishbone Diagram (Ishikawa)**
3. **Cynefin Framework**

### B.2 Discovery Frameworks

1. **Jobs-To-Be-Done**
2. **Empathy Mapping**
3. **Customer Journey Mapping**

### B.3 Ideation Frameworks

1. **Six Thinking Hats**
2. **SCAMPER**
3. **Lateral Thinking**

### B.4 Validation Frameworks

1. **Lean Startup / MVP**
2. **Mom Test**
3. **Discovery-Driven Planning**

### B.5 Strategy Frameworks

1. **SCQA (Minto Pyramid)**
2. **Porter's Five Forces**
3. **Blue Ocean Strategy**

### B.6 Execution Frameworks

1. **Business Model Canvas**
2. **Process Mapping**
3. **OKRs**

---

## Appendix C: Glossary

| Term | Definition |
|------|------------|
| **PWS** | Problems Worth Solving - the core methodology |
| **SCQA** | Situation-Complication-Question-Answer structure |
| **Signal** | Detected pattern indicating thinking mode |
| **Diagnosis** | Classification of problem type and complexity |
| **Framework** | Structured methodology for problem-solving |
| **RAG** | Retrieval-Augmented Generation |
| **Persona** | Distinct Larry "mode" with unique behavior |

---

**Document Version History**:

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Nov 2024 | J. Sagir | Initial draft |
| 2.0 | Nov 2024 | J. Sagir | Base44 specification added |

---

*End of Document*
