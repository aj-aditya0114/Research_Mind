# ResearchMind — Multi-Agent AI Research System

A multi-agent AI pipeline that researches any topic, writes a structured report, generates relevant illustrations, and critiques the output — all from a single text input.

---

## How It Works

Five specialized components run in sequence:

```
Topic Input
    │
    ▼
① Search Agent      →  Searches the web via Tavily, summarises findings
    │
    ▼
② Reader Agent      →  Scrapes the most relevant URL, extracts deep content
    │
    ▼
③ Writer Chain      →  Drafts a structured research report (LLM)
    │
    ▼
④ Image Generator   →  Analyses the report, generates section illustrations via Pollinations AI
    │
    ▼
⑤ Critic Chain      →  Reviews and scores the report (LLM)
```

The final output is a markdown report with a score, improvement suggestions, and locally saved images.

---

## Stack

| Layer | Technology |
|---|---|
| LLM | Groq (`openai/gpt-oss-120b`) |
| Agent orchestration | LangChain + LangGraph |
| Web search | Tavily API |
| Web scraping | `requests` + `BeautifulSoup4` |
| Image generation | Pollinations AI (`flux.1-schnell`) |
| UI | Streamlit |

---

## Project Structure

```
├── app.py                   # Streamlit web UI
├── pipeline.py              # Sequential 5-step pipeline orchestrator
├── agents.py                # Search agent, Reader agent, Writer chain, Critic chain
├── tools.py                 # web_search and scrape_url tool definitions
├── image_generator_agent.py # LLM-driven image planning + Pollinations AI generation
├── requirements.txt
├── .env                     # API keys (not committed)
└── generated_images/        # Auto-created folder for saved images
```

---

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd "Report Writing System(Multi-Agent)"
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
POLLINATIONS_API_KEY=your_pollinations_api_key
```

| Key | Where to get it |
|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `TAVILY_API_KEY` | [app.tavily.com](https://app.tavily.com) |
| `POLLINATIONS_API_KEY` | [pollinations.ai](https://pollinations.ai) |

---

## Running

### Streamlit UI

```bash
streamlit run app.py
```

Enter a research topic in the input field and click **Run Research Pipeline**. Results appear below once all steps complete. The final report can be downloaded as a `.md` file.

### CLI (pipeline only, no UI)

```bash
python pipeline.py
```

You will be prompted to enter a topic. Output is printed to the terminal.

---

## Output

For each run the pipeline returns:

| Key | Content |
|---|---|
| `search_results` | Summarised web search findings |
| `scraped_content` | Extracted content from the top URL |
| `report` | Full markdown report (Introduction, Key Findings, Conclusion, Sources) |
| `generated_images` | List of image metadata dicts with paths and captions |
| `feedback` | Critic score (X/10), areas to improve, one-line verdict |

Generated images are saved to `generated_images/` with filenames derived from the report section headings.

---

## Testing

Individual components can be tested in isolation:

```bash
# Test web search tool
python test_tool.py

# Test search schema / run_search helper
python test_schema.py

# Test Groq LLM + tool binding
python test_groq.py

# Test full search agent
python agent_test.py
```

---

## Notes

- The Qwen/GPT-OSS models on Groq do not support structured function-calling reliably. The search and reader agents call tools directly (no agent loop) and pass results to the LLM for summarisation.
- Image generation is best-effort — if Pollinations AI fails for a section, that section is skipped and the pipeline continues.
- The `.env` file is excluded from version control via `.gitignore`.
