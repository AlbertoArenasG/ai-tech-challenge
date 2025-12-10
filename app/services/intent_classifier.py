"""LLM-powered intent classifier to guide conversational flow."""
from __future__ import annotations

from typing import Literal

import logging

from openai import OpenAI

Intent = Literal["greeting", "small_talk", "recommendation", "financing", "faq", "off_topic", "ambiguous"]

PROMPT = (
    "Clasifica el siguiente mensaje de cliente en una de las categorías: "
    "greeting (saludo), small_talk (charla casual), recommendation (solicita recomendaciones de autos), "
    "financing (pregunta por financiamiento), faq (propuesta de valor o garantías), off_topic (otros temas), "
    "ambiguous (no queda claro). Responde solo con la etiqueta. Mensaje: {message}"
)


LOGGER = logging.getLogger(__name__)


class IntentClassifier:
    def __init__(self, api_key: str | None, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = model

    def classify(self, message: str) -> Intent:
        if not self.client:
            return "ambiguous"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0,
                messages=[
                    {"role": "system", "content": "Sigue las instrucciones."},
                    {"role": "user", "content": PROMPT.format(message=message)},
                ],
            )
            content = (response.choices[0].message.content or "ambiguous").strip().lower()
        except Exception as exc:  # pragma: no cover - network guard
            LOGGER.warning("Intent classification failed: %s", exc)
            return "ambiguous"
        allowed: set[str] = {"greeting", "small_talk", "recommendation", "financing", "faq", "off_topic", "ambiguous"}
        return content if content in allowed else "ambiguous"
