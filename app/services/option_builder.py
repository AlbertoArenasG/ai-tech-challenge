"""Build predefined option lists from the catalog."""
from __future__ import annotations

from app.services.catalog_service import CatalogService


class OptionBuilder:
    def __init__(self, catalog: CatalogService) -> None:
        self.catalog = catalog

    def make_options(self, limit: int = 5) -> list[str]:
        makes = sorted(self.catalog.list_makes())
        return makes[:limit] if limit else makes

    def model_options(self, make: str, limit: int = 5) -> list[str]:
        models = sorted(self.catalog.list_models(make))
        return models[:limit] if limit else models
