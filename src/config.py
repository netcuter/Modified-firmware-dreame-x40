"""Configuration loader for Dreame X40 AI Assistant"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class ValetudoConfig(BaseModel):
    """Valetudo connection configuration"""
    host: str = "192.168.1.100"
    port: int = 80
    protocol: str = "http"
    api_base: str = "/api/v2"
    timeout: int = 10

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}{self.api_base}"


class ValetudoMQTTConfig(BaseModel):
    """Valetudo MQTT configuration"""
    enabled: bool = True
    broker: str = "192.168.1.100"
    port: int = 1883
    username: str = ""
    password: str = ""
    base_topic: str = "valetudo"


class LocalAIConfig(BaseModel):
    """Local AI (LM Studio) configuration"""
    enabled: bool = True
    type: str = "lmstudio"
    host: str = "192.168.1.50"
    port: int = 1234
    model: str = "local-model"
    timeout: int = 30
    max_tokens: int = 2000
    temperature: float = 0.7

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}/v1"


class OpenAIConfig(BaseModel):
    """OpenAI configuration"""
    enabled: bool = True
    api_key: str = ""
    model: str = "gpt-4"
    base_url: str = "https://api.openai.com/v1"
    max_tokens: int = 2000
    temperature: float = 0.7


class AnthropicConfig(BaseModel):
    """Anthropic Claude configuration"""
    enabled: bool = False
    api_key: str = ""
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 2000
    temperature: float = 0.7


class GoogleConfig(BaseModel):
    """Google Gemini configuration"""
    enabled: bool = False
    api_key: str = ""
    model: str = "gemini-pro"
    max_tokens: int = 2000
    temperature: float = 0.7


class OnlineAIConfig(BaseModel):
    """Online AI providers configuration"""
    default_provider: str = "openai"
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    anthropic: AnthropicConfig = Field(default_factory=AnthropicConfig)
    google: GoogleConfig = Field(default_factory=GoogleConfig)


class AIConfig(BaseModel):
    """AI configuration"""
    default_model: str = "local"  # "local" or "online"
    auto_fallback: bool = True
    language: str = "pl"
    local: LocalAIConfig = Field(default_factory=LocalAIConfig)
    online: OnlineAIConfig = Field(default_factory=OnlineAIConfig)


class VoiceConfig(BaseModel):
    """Voice configuration"""
    enabled: bool = True
    language: str = "pl-PL"


class WebConfig(BaseModel):
    """Web interface configuration"""
    host: str = "0.0.0.0"
    port: int = 3000
    https: bool = False


class APIConfig(BaseModel):
    """API server configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = "INFO"
    file: str = "logs/dreame_x40.log"
    max_size: str = "10MB"
    backup_count: int = 5


class AdvancedConfig(BaseModel):
    """Advanced configuration"""
    reconnect_attempts: int = 5
    reconnect_delay: int = 5
    map_cache_enabled: bool = True
    map_cache_dir: str = "data/maps"
    conversation_history: bool = True
    history_length: int = 50
    history_dir: str = "data/conversations"


class Settings(BaseSettings):
    """Main application settings"""
    valetudo: ValetudoConfig = Field(default_factory=ValetudoConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    voice: VoiceConfig = Field(default_factory=VoiceConfig)
    web: WebConfig = Field(default_factory=WebConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    advanced: AdvancedConfig = Field(default_factory=AdvancedConfig)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_config(config_path: str = "config/settings.yaml") -> Settings:
    """Load configuration from YAML file"""
    config_file = Path(config_path)

    if not config_file.exists():
        print(f"Warning: Config file {config_path} not found. Using defaults.")
        return Settings()

    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    # Create nested structure for Pydantic
    if 'valetudo' in config_data and 'mqtt' in config_data['valetudo']:
        mqtt_config = config_data['valetudo'].pop('mqtt')
        config_data['valetudo']['mqtt'] = mqtt_config

    return Settings(**config_data)


# Global config instance
config: Settings = None


def get_config() -> Settings:
    """Get global config instance"""
    global config
    if config is None:
        config = load_config()
    return config
