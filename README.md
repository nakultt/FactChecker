# 🔍 FactChecker

An intelligent fact-checking application powered by LangChain and Ollama that verifies claims using local news corpus and web search.

## 📋 Overview

FactChecker is an AI-powered agent that helps verify the accuracy of claims and statements. It uses a two-tier approach:

1. **Local Search**: Searches a curated ChromaDB vector database of news articles
2. **Web Search**: Falls back to DuckDuckGo web search if local sources are insufficient

The agent provides clear verdicts: **TRUE**, **PARTIALLY TRUE**, or **FALSE** with supporting evidence and sources.

## 🏗️ Architecture

```
FactChecker/
├── src/
│   ├── app.py                      # Main application entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   └── fact_checker_agent.py  # ReAct agent with reasoning
│   └── tools/
│       ├── __init__.py
│       ├── local_search_tool.py   # ChromaDB search tool
│       └── web_search_tool.py     # DuckDuckGo search tool
├── scripts/
│   ├── build_corpus.py            # Fetch news articles via NewsAPI
│   └── build_chroma_db.py         # Build vector database
├── data/
│   └── corpus/                    # JSONL news corpus files
├── chroma_db/                     # ChromaDB vector store
└── requirements.txt
```

## 🚀 Features

- **Intelligent Agent**: Uses ReAct (Reasoning + Acting) pattern for step-by-step verification
- **Hybrid Search**: Local vector search + web search fallback
- **Structured Output**: Clear TRUE/PARTIALLY TRUE/FALSE verdicts
- **Source Attribution**: Provides URLs and references for claims
- **News Corpus**: Curated database of verified news articles
- **Embeddings**: Uses Ollama's `mxbai-embed-large` for semantic search

## 📦 Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed locally
- NewsAPI key (optional, for building corpus)

### Step 1: Clone the Repository

```bash
git clone https://github.com/nakultt/FactChecker.git
cd FactChecker
```

### Step 2: Create Virtual Environment

```bash
conda create -n rag python=3.10
conda activate rag
```

Or using venv:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Ollama Models

```bash
ollama pull mxbai-embed-large
ollama pull qwen3
```

### Step 5: Set Up Environment Variables

Create a `.env` file in the project root:

```env
NEWSAPI_KEY=your_newsapi_key_here
```

Get your free API key from [NewsAPI.org](https://newsapi.org/)

## 🎯 Usage

### Build News Corpus (Optional)

Fetch latest news articles to populate the database:

```bash
python scripts/build_corpus.py
```

### Build Vector Database

Create the ChromaDB vector store from the corpus:

```bash
python scripts/build_chroma_db.py
```

### Run the Fact Checker

```bash
cd src
python app.py
```

### Example Interaction

```
🔍 Fact Checker Agent initialized!
==================================================

📝 Enter your query (or 'quit' to exit): Is climate change real?

🤖 Agent is working...

> Entering new AgentExecutor chain...
Thought: I need to search for information about climate change
Action: local_search
Action Input: climate change real scientific consensus

Observation: Found in local database:
...

✅ Final Answer:
✅ TRUE

The claim that climate change is real is accurate based on overwhelming scientific evidence:
- 97% of climate scientists agree that climate change is happening and human-caused
- Global temperatures have risen by 1.1°C since pre-industrial times
- Multiple independent datasets confirm warming trends

Sources:
- https://example.com/climate-science-report
- https://example.com/ipcc-findings

==================================================
```

## 🛠️ Technologies Used

| Technology     | Purpose                                |
| -------------- | -------------------------------------- |
| **LangChain**  | Agent framework and tool orchestration |
| **Ollama**     | Local LLM inference (Qwen3)            |
| **ChromaDB**   | Vector database for semantic search    |
| **DuckDuckGo** | Web search fallback                    |
| **NewsAPI**    | News article collection                |
| **Pydantic**   | Data validation and schemas            |

## 📊 How It Works

1. **User submits a claim** for verification
2. **Agent reasons** about the best approach
3. **Local search** queries ChromaDB with semantic similarity
4. **Web search** activates if local results are insufficient
5. **Agent analyzes** evidence from all sources
6. **Verdict generated** with supporting facts and sources

## 🔧 Configuration

### Change LLM Model

Edit `src/agents/fact_checker_agent.py`:

```python
llm = ChatOllama(
    model="llama3.2",  # or "mistral", "gemma2", etc.
    temperature=0
)
```

### Adjust Search Results

Edit `src/tools/local_search_tool.py`:

```python
results = self.vectorstore.similarity_search_with_score(query, k=5)  # Default: k=3
```

### Change Embedding Model

Edit both `src/tools/local_search_tool.py` and `scripts/build_chroma_db.py`:

```python
embeddings = OllamaEmbeddings(model="nomic-embed-text")  # Default: mxbai-embed-large
```

## 📝 Requirements

```txt
langchain==0.3.13
langchain-community==0.3.13
langchain-chroma==0.1.4
langchain-ollama==0.2.3
chromadb==0.5.23
ollama==0.4.4
duckduckgo-search==7.0.0
newsapi-python==0.2.7
python-dotenv==1.0.1
pydantic==2.10.5
requests==2.32.3
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) for the agent framework
- [Ollama](https://ollama.ai/) for local LLM inference
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [NewsAPI](https://newsapi.org/) for news data

## 📧 Contact

Nakul TT - [@nakultt](https://github.com/nakultt)

Project Link: [https://github.com/nakultt/FactChecker](https://github.com/nakultt/FactChecker)

---

⭐ If you find this project helpful, please give it a star!
