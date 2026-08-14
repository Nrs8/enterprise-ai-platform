from pathlib import Path
import os

from dotenv import load_dotenv

from .exceptions import ConfigurationError


# Load environment variables once during application startup.
BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(
    BASE_DIR / ".env"
)


class Settings:

    def __init__(self):

        # LLM
        self.api_key = os.getenv(
            "DASHSCOPE_API_KEY"
        )

        self.base_url = os.getenv(
            "QWEN_BASE_URL"
        )

        self.model = os.getenv(
            "QWEN_MODEL"
        )


        # Reliability
        self.llm_timeout = int(
            os.getenv(
                "LLM_TIMEOUT",
                "10"
            )
        )

        self.retry_count = int(
            os.getenv(
                "RETRY_COUNT",
                "3"
            )
        )


        # Runtime
        self.worker_count = int(
            os.getenv(
                "WORKER_COUNT",
                "3"
            )
        )

        self.environment = os.getenv(
            "ENVIRONMENT",
            "development"
        )


        self._validate()


    def _validate(self):

        if not self.api_key:
            raise ConfigurationError(
                "DASHSCOPE_API_KEY is missing"
            )

        if not self.base_url:
            raise ConfigurationError(
                "QWEN_BASE_URL is missing"
            )

        if not self.model:
            raise ConfigurationError(
                "QWEN_MODEL is missing"
            )


# Singleton configuration instance
settings = Settings()