"""Main entry point for Dreame X40 AI Assistant"""

import sys
import os
import logging
import uvicorn
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_config
from src.api.server import app


def setup_logging(config):
    """Setup logging configuration"""

    # Create logs directory if it doesn't exist
    log_file = Path(config.logging.file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Configure logging
    log_level = getattr(logging, config.logging.level.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.logging.file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("Logging configured")


def main():
    """Main function"""

    print("=" * 60)
    print("  Dreame X40 AI Assistant - Valetudo + AI Integration")
    print("=" * 60)
    print()

    # Load configuration
    print("Loading configuration...")
    config = load_config()

    # Setup logging
    setup_logging(config)
    logger = logging.getLogger(__name__)

    logger.info("Starting Dreame X40 AI Assistant...")

    # Print configuration summary
    print(f"\n📋 Configuration:")
    print(f"  • Valetudo: {config.valetudo.protocol}://{config.valetudo.host}:{config.valetudo.port}")
    print(f"  • AI Default Model: {config.ai.default_model}")
    print(f"  • Language: {config.ai.language}")

    if config.ai.local.enabled:
        print(f"  • Local AI (LM Studio): {config.ai.local.host}:{config.ai.local.port}")

    if config.ai.online.openai.enabled and config.ai.online.openai.api_key:
        print(f"  • OpenAI: {config.ai.online.openai.model}")

    if config.ai.online.anthropic.enabled and config.ai.online.anthropic.api_key:
        print(f"  • Anthropic: {config.ai.online.anthropic.model}")

    if config.ai.online.google.enabled and config.ai.online.google.api_key:
        print(f"  • Google: {config.ai.online.google.model}")

    print(f"\n🚀 Starting API server...")
    print(f"  • Host: {config.api.host}:{config.api.port}")
    print(f"  • API docs: http://localhost:{config.api.port}/docs")
    print(f"  • WebSocket: ws://localhost:{config.api.port}/ws/chat")
    print()

    # Create data directories
    Path("data/maps").mkdir(parents=True, exist_ok=True)
    Path("data/conversations").mkdir(parents=True, exist_ok=True)

    # Run server
    try:
        uvicorn.run(
            app,
            host=config.api.host,
            port=config.api.port,
            log_level=config.logging.level.lower()
        )
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        print("\n\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
