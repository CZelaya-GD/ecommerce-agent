import pytest
from unittest.mock import Mock
from agents.product_research.ali_scraper import AliScraper
from agents.product_research.perplexity_llm import PerplexityLLM

@pytest.fixture
def mock_requests(monkeypatch):

    mock_response = Mock()
    mock_response.text = '<html><div class="manhattan--container--1lP57Ag"><a href="//test.com"></a></div></html>'
    mock_response.raise_for_status.return_value = None

    monkeypatch.setattr("requests.get", lambda *args, **kwargs: mock_response)

def test_ali_scraper_success(mock_requests):

    scraper = AliScraper()
    results = scraper.search_products("test")
    assert len(results) > 0
    assert results[0]['link'] == "https://test.com"

def test_ali_scraper_failure(monkeypatch):
    monkeypatch.setattr('requests.get', Mock(side_effect=Exception("Test error")))
    scraper = AliScraper()
    results = scraper.search_products("test")
    assert len(results) == 0

def test_perplexity_integration(monkeypatch):
    mock_llm = Mock(return_value="1. Test Product\n2. Another Product")
    monkeypatch.setattr('langchain_community.chat_models.ChatPerplexity', Mock(return_value=mock_llm))

    llm = PerplexityLLM()
    assert llm.get_trending_keywords() == ["Test Product", "Another Product"]