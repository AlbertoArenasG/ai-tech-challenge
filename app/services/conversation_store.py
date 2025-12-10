"""Redis-backed storage for conversation context."""
from __future__ import annotations

import json
from datetime import datetime, timedelta

import redis


class ConversationStore:
    """Persist lightweight conversation state keyed by user id."""

    def __init__(self, redis_url: str, ttl_minutes: int = 30) -> None:
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)
        self.ttl = ttl_minutes * 60

    def save_turn(self, user_id: str, payload: dict) -> None:
        key = self._key(user_id)
        existing = self.get_state(user_id)
        history = existing.get("history", []) if existing else []
        history.append({"ts": datetime.utcnow().isoformat(), "payload": payload})
        state = {"history": history[-5:]}
        self.client.set(key, json.dumps(state), ex=self.ttl)

    def get_state(self, user_id: str) -> dict:
        raw = self.client.get(self._key(user_id))
        return json.loads(raw) if raw else {}

    def store_preferences(self, user_id: str, preferences: dict) -> None:
        state = self.get_state(user_id)
        stored = state.get("preferences", {})
        stored.update(preferences)
        state["preferences"] = stored
        self.client.set(self._key(user_id), json.dumps(state), ex=self.ttl)

    def get_preferences(self, user_id: str) -> dict:
        state = self.get_state(user_id)
        return state.get("preferences", {})

    def set_expected_slot(self, user_id: str, slot: str | None) -> None:
        state = self.get_state(user_id)
        state["expected_slot"] = slot
        self.client.set(self._key(user_id), json.dumps(state), ex=self.ttl)

    def get_expected_slot(self, user_id: str) -> str | None:
        state = self.get_state(user_id)
        return state.get("expected_slot")

    def set_question(self, user_id: str, slot: str, options: list[str], metadata: dict | None = None) -> None:
        state = self.get_state(user_id)
        state["question"] = {"slot": slot, "options": options, "metadata": metadata or {}}
        self.client.set(self._key(user_id), json.dumps(state), ex=self.ttl)

    def get_question(self, user_id: str) -> dict | None:
        state = self.get_state(user_id)
        return state.get("question")

    def clear_question(self, user_id: str) -> None:
        state = self.get_state(user_id)
        if "question" in state:
            state.pop("question")
            self.client.set(self._key(user_id), json.dumps(state), ex=self.ttl)

    def _key(self, user_id: str) -> str:
        return f"conversation:{user_id}"
