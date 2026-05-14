"""LLM access layer for Groq.

Why this exists:
    The rest of the app should ask for business analysis, not care about the
    exact API client. This makes it easier to swap models or providers later.
"""

from groq import Groq

from src.utils.config import get_settings


class LLMService:
    """Small wrapper around the Groq chat completion API."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = Groq(api_key=self.settings.groq_api_key) if self.settings.groq_api_key else None

    def is_configured(self) -> bool:
        """Return whether a Groq API key is available."""

        return self.client is not None

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a text response from the configured Groq model."""

        if not self.client:
            return "Groq API key is not configured yet. Add GROQ_API_KEY to your .env file."

        response = self.client.chat.completions.create(
            model=self.settings.groq_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""
