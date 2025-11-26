# Larry Navigator - PWS Innovation Mentor

An AI-powered innovation mentor that helps users discover, diagnose, and develop **Problems Worth Solving (PWS)**.

Larry is not an answer machine - Larry is a **thinking partner**.

## Features

- **Streaming Responses** - Low-latency, real-time response generation
- **Multiple Personas** - Switch between Larry Mentor, Evaluator, and Strategist modes
- **Minto Pyramid Analysis** - SCQA-based conversation structuring
- **Signal Detection** - Automatically detects thinking patterns and recommends frameworks
- **RAG Integration** - Supabase pgvector for semantic search over PWS knowledge base

## Personas

| Icon | Persona | Focus |
|------|---------|-------|
| **Mentor** | Socratic guide for problem discovery |
| **Evaluator** | Framework evaluation & feedback |
| **Strategist** | Strategy & competitive positioning |

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/larry-navigator-v2.git
cd larry-navigator-v2
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up credentials

Copy the secrets template and add your API keys:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` with your credentials:

```toml
GOOGLE_AI_API_KEY = "your-google-ai-api-key"
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
```

### 4. Run locally

```bash
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add secrets in Settings > Secrets:
   - `GOOGLE_AI_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
5. Deploy!

## Project Structure

```
larry-navigator-v2/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── agents/               # AI analysis agents
│   ├── streaming_pyramid.py   # Fast pyramid analyzer
│   ├── minto_analyzer.py      # Minto Pyramid analysis
│   └── ...
├── components/           # UI components
├── config/              # Configuration
│   ├── personas.py          # Larry personas
│   ├── frameworks.py        # Innovation frameworks
│   └── prompts.py           # System prompts
├── styles/              # CSS styling
├── utils/               # Utilities
│   ├── streaming_response.py  # Streaming generator
│   └── supabase_rag.py       # RAG integration
└── .streamlit/
    └── config.toml          # Streamlit config
```

## API Keys

- **Google AI API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Supabase**: Create a project at [supabase.com](https://supabase.com) with pgvector enabled

## License

MIT
