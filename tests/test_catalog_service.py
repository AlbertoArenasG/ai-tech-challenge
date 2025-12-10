"""Unit tests for CatalogService."""
from pathlib import Path

from app.services.catalog_service import CatalogService

_SAMPLE_CSV = """stock_id,km,price,make,model,year,version,bluetooth,largo,ancho,altura,car_play
123,10000,250000.0,Toyota,Corolla,2019,XLE,Sí,4630,1780,1435,Sí
456,45000,180000.0,Nissan,Sentra,2017,Advance,,4615,1760,1500,
"""


def _write_csv(tmp_path: Path) -> str:
    csv_path = tmp_path / "catalog.csv"
    csv_path.write_text(_SAMPLE_CSV, encoding="utf-8")
    return str(csv_path)


def test_load_catalog_parses_rows(tmp_path: Path) -> None:
    service = CatalogService()
    service.load_catalog(_write_csv(tmp_path))

    results = service.search_cars()
    assert len(results) == 2
    assert results[0].make == "Toyota"
    assert results[0].bluetooth is True
    assert results[1].car_play is None


def test_search_cars_filters_by_preferences(tmp_path: Path) -> None:
    service = CatalogService()
    service.load_catalog(_write_csv(tmp_path))

    filtered = service.search_cars({"make": "toyota", "max_price": 260000})
    assert len(filtered) == 1
    assert filtered[0].model == "Corolla"

    none_match = service.search_cars({"min_year": 2021})
    assert none_match == []
