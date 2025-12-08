"""Main entry point for Xyber Chatbot.

Provides a minimal CLI using argparse to run core actions without extra deps.
"""

import argparse
import asyncio
from pathlib import Path

from src.config import settings
from src.ingestion.crawler import crawl_xyber_docs
from src.ingestion.store import DocumentStore


def init_cmd() -> None:
    paths = [Path("data"), Path("logs"), settings.chroma_db_path]
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)
    print("Initialization complete. Created data and logs directories.")


def ingest_cmd(depth: int = None) -> None:
    depth = depth or settings.max_crawl_depth
    print(f"Crawling {settings.xyber_docs_url} (depth={depth})...")
    docs = asyncio.run(crawl_xyber_docs(url=settings.xyber_docs_url, max_depth=depth))
    store = DocumentStore()
    chunks = store.ingest_documents(docs)
    print(f"Ingested {chunks} chunks.")


def web_cmd(host: str = None, port: int = None) -> None:
    host = host or settings.host
    port = port or settings.port
    import uvicorn

    print(f"Starting web server at http://{host}:{port}")
    uvicorn.run("src.api.server:app", host=host, port=port, reload=settings.debug)


def telegram_cmd() -> None:
    from src.telegram_bot.bot import run_telegram_bot_sync

    print("Starting Telegram bot...")
    run_telegram_bot_sync()


def stats_cmd() -> None:
    store = DocumentStore()
    stats = store.get_stats()
    print("Database stats:")
    print(f"  collection: {stats.get('collection_name')}")
    print(f"  total_chunks: {stats.get('total_chunks')}")


def main():
    parser = argparse.ArgumentParser(prog="xyber-chatbot")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init")
    ingest_p = sub.add_parser("ingest")
    ingest_p.add_argument("--depth", type=int, default=None)
    web_p = sub.add_parser("web")
    web_p.add_argument("--host", default=None)
    web_p.add_argument("--port", type=int, default=None)
    sub.add_parser("telegram")
    sub.add_parser("stats")

    args = parser.parse_args()

    if args.cmd == "init":
        init_cmd()
    elif args.cmd == "ingest":
        ingest_cmd(depth=getattr(args, "depth", None))
    elif args.cmd == "web":
        web_cmd(host=getattr(args, "host", None), port=getattr(args, "port", None))
    elif args.cmd == "telegram":
        telegram_cmd()
    elif args.cmd == "stats":
        stats_cmd()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
