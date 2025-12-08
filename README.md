# Xyber Documentation RAG Chatbot

A production-ready Retrieval-Augmented Generation (RAG) chatbot for Xyber documentation with a modern web interface and Telegram bot integration.

## 🚀 Features

- **Intelligent Document Search**: Uses ChromaDB vector store with semantic search
- **RAG Pipeline**: Powered by GROQ's Llama 3 8B for accurate answers based on documentation
- **Web UI**: Modern, responsive HTML/CSS/JS interface
- **Telegram Bot**: Full integration for on-the-go access
- **Environment Configuration**: Secure secrets management via `.env`
- **Production Ready**: Clean architecture supporting scaling and future expansion
- **Streaming Ready**: Built for easy streaming response integration
- **Citation Tracking**: Maintains source references for all answers
- **Comprehensive Logging**: Debug and monitor all operations

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

### Web Interface (Recommended for Development)

```bash
# Start the web server
python main.py web

# Visit http://localhost:8000
```

The web UI includes:
- Real-time chat interface
- Document ingestion trigger
- Statistics dashboard
- Source attribution
- Health status monitor

### Telegram Bot

```bash
# Start the bot
python main.py telegram

# Send messages to your bot on Telegram
```

Bot commands:
- `/start` - Welcome message
- `/help` - Show help
- `/stats` - Database statistics
- `/clear` - Clear context
- Any question - Get RAG response

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
# Run everything with hot-reload
python main.py dev
```

## 📂 Project Structure

```
xyber-chatbot/
├── src/
│   ├── api/              # FastAPI backend
│   │   ├── models.py     # Pydantic request/response models
│   │   └── server.py     # FastAPI application
│   ├── core/             # RAG pipeline
│   │   └── rag.py        # RAG implementation
│   ├── ingestion/        # Document processing
│   │   ├── crawler.py    # Web crawler
│   │   └── store.py      # ChromaDB vector store
│   ├── telegram_bot/     # Telegram integration
│   │   └── bot.py        # Telegram bot handler
│   ├── web/              # Web UI
│   │   ├── index.html    # Frontend
│   │   ├── styles.css    # Styling
│   │   └── script.js     # JavaScript logic
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

## 🔧 Configuration

All configuration is managed via `.env` file. Key settings:

```env
# API Keys (Required)
GROQ_API_KEY=your_key_here
TELEGRAM_BOT_TOKEN=your_token_here

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Document Processing
XYBER_DOCS_URL=https://docs.xyber.inc/
MAX_CRAWL_DEPTH=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# RAG Settings
RETRIEVE_K=5
TEMPERATURE=0.3
MAX_TOKENS=2048

# Features
ENABLE_CITATIONS=true
ENABLE_STREAMING=false
```

## 🚀 Deployment

### Docker (Coming Soon)

```bash
docker build -t xyber-chatbot .
docker run -p 8000:8000 --env-file .env xyber-chatbot
```

### Cloud Deployment

The application is designed for easy deployment to:
- **Heroku**: Use Procfile (to be created)
- **AWS**: Lambda + API Gateway compatible
- **Google Cloud**: Cloud Run support
- **Azure**: App Service compatible
- **Self-Hosted**: Docker or systemd

## 📚 API Reference

### Health Check
```
GET /health
```

### Query
```
POST /query
Content-Type: application/json

{
  "question": "How do I install Xyber?",
  "k": 5
}
```

### Statistics
```
GET /stats
```

### Ingest Documents
```
POST /ingest
Content-Type: application/json

{
  "clear_first": true
}
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

## 🎯 Features Roadmap

- [ ] Streaming responses
- [ ] Response citations with links
- [ ] User authentication
- [ ] Conversation history
- [ ] Advanced filters and search
- [ ] Multi-language support
- [ ] Rate limiting
- [ ] Analytics dashboard
- [ ] Document upload UI
- [ ] Custom document collections

## 🐛 Troubleshooting

### API Key Issues
```bash
# Check if .env exists
ls -la .env

# Verify keys are not empty
grep "GROQ_API_KEY" .env
grep "TELEGRAM_BOT_TOKEN" .env
```

### No Documents Found
```bash
# Re-ingest documentation
python main.py ingest --clear --depth 5

# Check status
python main.py stats
```

### Connection Issues
```bash
# Check health
curl http://localhost:8000/health

# View logs
tail -f logs/*.log
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

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional document source formats
- Performance optimization
- New interface implementations
- Deployment templates
- Testing coverage

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- GROQ for Llama 3 API
- LangChain for RAG framework
- ChromaDB for vector storage
- FastAPI for web framework
- python-telegram-bot for Telegram integration

## 📧 Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Review the troubleshooting section
3. Check logs in `logs/` directory
4. Create a new GitHub issue with details

---

**Made by Alpha-M2 for Xyber Documentation**