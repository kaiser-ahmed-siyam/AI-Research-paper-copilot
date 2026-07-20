from research_copilot.arxiv_client import _year_from_published


def test_year_from_published():
    assert _year_from_published("2024-01-15T12:00:00Z") == 2024


def test_year_from_invalid_published():
    assert _year_from_published("") is None

