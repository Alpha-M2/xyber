# Xyber Documentation Chatbot (Telegram-only)

A lightweight RAG chatbot for Xyber documentation with Telegram bot integration.

## 📋 Requirements

- Python 3.9+
- GROQ API Key ([Get one here](https://console.groq.com))
- Telegram Bot Token ([Create with @BotFather](https://t.me/BotFather))
- Internet connection for document crawling

## 🛠️ Installation

### 1. Clone and Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Configure Secrets

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
# - GROQ_API_KEY: Your GROQ API key
# - TELEGRAM_BOT_TOKEN: Your Telegram bot token
```

### 3. Initialize Project

```bash
python main.py init
```

## 💻 Usage

### Telegram Bot

Start the bot locally (blocking):

```bash
python main.py telegram
```

Then send messages to your bot on Telegram. Available commands:
- `/start` - Welcome message
- `/help` - Show help
- `/stats` - Database statistics
- `/clear` - Clear context
- Any question - Get a RAG response

### Ingest Documentation

```bash
# Download and index Xyber docs
python main.py ingest --depth 5

# Or clear and re-ingest
python main.py ingest --clear

# View stats
python main.py stats
```

### Development Mode

```bash
# Run the bot in development mode if available
python main.py dev
```

## 📂 Project Structure

```
xyber-chatbot/
├── src/
│   ├── core/             # RAG pipeline
│   │   └── rag.py        # RAG implementation
│   ├── ingestion/        # Document processing
│   │   ├── crawler.py    # Web crawler
│   │   └── store.py      # ChromaDB vector store
│   ├── telegram_bot/     # Telegram integration
│   │   └── bot.py        # Telegram bot handler
│   ├── utils/            # Utilities
│   │   ├── cli.py        # CLI commands
│   │   ├── logger.py     # Logging setup
│   │   ├── exceptions.py # Custom exceptions
│   │   └── text_processor.py # Text utilities
│   └── config.py         # Configuration management
├── data/                 # Data storage (ChromaDB)
├── logs/                 # Application logs
├── main.py               # Entry point
├── pyproject.toml        # Dependencies
├── .env.example          # Configuration template
└── README.md             # This file
```

### Statistics
```
GET /stats
```


## 🔄 Architecture

```
┌─────────────────────────────────────────┐
│         Web UI / Telegram Bot           │
├─────────────────────────────────────────┤
│          FastAPI Backend                │
├──────────────┬──────────────────────────┤
│  RAG Pipeline│   Document Store        │
│  (GROQ Llama)│  (ChromaDB Vector DB)   │
├──────────────┴──────────────────────────┤
│     Vector Embeddings                   │
└─────────────────────────────────────────┘
         ↓              ↓
    Xyber Docs      Semantic Search
```

### Connection & Logs
```bash
# View logs
tail -f logs/*.log

# Search for errors
grep "ERROR" logs/*.log
```

## 📝 Logging

Logs are saved to `logs/` directory with rotating file handlers:
- `xyber_chatbot.root.log` - Main application log
- `src.ingestion.crawler.log` - Crawler operations
- `src.core.rag.log` - RAG pipeline
- `src.api.server.log` - API server

View logs:
```bash
# Watch logs in real-time
tail -f logs/*.log

# Search for errors
grep "ERROR" logs/*.log
```

## 🙏 Acknowledgments

- GROQ for Llama 3 API
- LangChain for RAG framework
- ChromaDB for vector storage
- python-telegram-bot for Telegram integration

**Made by Alpha-M2 for Xyber Documentation**