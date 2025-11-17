# Changelog

All notable changes to Dreame X40 AI Assistant will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-17

### Added
- Initial release of Dreame X40 AI Assistant
- Integration with Valetudo for local robot control
- AI-powered natural language interface (Polish and English)
- Support for local AI models via LM Studio
- Support for online AI models (OpenAI GPT, Anthropic Claude, Google Gemini)
- Automatic model switching and fallback
- Web-based user interface with real-time chat
- REST API for programmatic control
- WebSocket support for real-time communication
- Robot control commands (start, stop, pause, home, locate)
- Room-based cleaning with natural language
- Battery status and robot state monitoring
- Conversation history management
- Comprehensive documentation

### Features
- **Valetudo Integration:**
  - Full REST API client for Valetudo
  - MQTT support for real-time updates
  - Command mapper for natural language to Valetudo commands

- **AI Models:**
  - Local model support (LM Studio compatible)
  - OpenAI GPT-3.5/GPT-4 integration
  - Anthropic Claude integration
  - Google Gemini integration
  - Automatic fallback between models
  - Configurable temperature and max_tokens

- **Web Interface:**
  - Modern React-based UI
  - Real-time chat interface
  - Robot status dashboard
  - Manual control buttons
  - Model switcher
  - Dark theme

- **Natural Language Understanding:**
  - Polish language support
  - English language support
  - Automatic language detection
  - Room name recognition
  - Intent extraction

### Documentation
- Comprehensive README with quick start guide
- Detailed Valetudo installation guide
- AI configuration and setup guide
- Complete commands reference
- API documentation
- Troubleshooting guide

### Security
- API keys stored in environment variables
- .gitignore for sensitive files
- CORS configuration
- Request timeouts

## [Unreleased]

### Planned Features
- Voice input support (speech-to-text)
- Voice output support (text-to-speech)
- Home Assistant integration
- Multi-language support (German, French, Spanish)
- Advanced scheduling via natural language
- Map visualization in web interface
- Cleaning statistics and history
- Docker deployment option
- Mobile-responsive improvements
- Authentication for web interface
