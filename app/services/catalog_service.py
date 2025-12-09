"""Service responsible for loading and querying the car catalog."""
from __future__ import annotations

from collections.abc import Iterable

from app.domain.models import Car


class CatalogService:
    """Handle catalog data sourced from a CSV file."""

    def __init__(self) -> None:
        self._catalog: list[Car] = []

    def load_catalog(self, path: str) -> None:
        """Load catalog data from the provided CSV path."""
        # TODO: Implement CSV parsing and bootstrap the in-memory catalog cache.
        _ = path

    def search_cars(self, preferences: dict) -> Iterable[Car]:
        """Return cars that match user preferences."""
        # TODO: Add filtering/scoring strategy aligned with the final preference model.
        _ = preferences
        return []
