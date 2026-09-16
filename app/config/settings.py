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
        self.llm_timeout = self._get_int(
            "LLM_TIMEOUT",
            10
        )

        self.retry_count = self._get_int(
            "RETRY_COUNT",
            3
        )


        # Runtime
        self.worker_count = self._get_int(
            "WORKER_COUNT",
            3
        )

        self.environment = os.getenv(
            "ENVIRONMENT",
            "development"
        )


        self._validate()


    def _get_int(
        self,
        name: str,
        default: int
    ) -> int:

        value = os.getenv(
            name,
            str(default)
        )

        try:
            return int(value)

        except ValueError as exc:
            raise ConfigurationError(
                f"{name} must be an integer"
            ) from exc


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

        if self.llm_timeout <= 0:
            raise ConfigurationError(
                "LLM_TIMEOUT must be greater than 0"
            )

        if self.retry_count < 0:
            raise ConfigurationError(
                "RETRY_COUNT must be greater than or equal to 0"
            )

        if self.worker_count <= 0:
            raise ConfigurationError(
                "WORKER_COUNT must be greater than 0"
            )


# Singleton configuration instance
settings = Settings()
