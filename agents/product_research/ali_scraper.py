import logging

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)
class AliScraper:
    """
    Scrapes AliExpress for product listings based on a search keyword.

    Returns:
        A list of product dictionaries with name, price and link
    """

    BASE_URL = "https://www.aliexpress.com/wholesale"

    def search_products(self, keyword: str, max_results: int = 5) -> List[Dict]:

        """Scrapes products with comprehensive error handling"""

        try:

            response = requests.get(
                self.BASE_URL,
                params = {'SearchText': keyword, 'page': 1},
                timeout = 15,
                headers = {'User-Agent': 'Mozilla/5.0'}
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            return self._parse_products(soup, max_results)

        except requests.exceptions.RequestException as e:

            logger.error(f"Request failed: {str(e)}")
            return []

        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return []


    def _parse_products(self, soup: BeautifulSoup, max_results: int) -> List[Dict]:
        """Handles parsing errors and selector changes"""

        products = []
        items = soup.select('.manhattan--container--1lP57Ag')[:max_results]

        for item in items:
            try:
                product = {
                    'name': item.select_one('.manhattan--titleText--WccSjUS').get_text(strip=True),
                    'price': item.select_one('.manhattan--price-sale--1CCSZfK').get_text(strip=True),
                    'link': self._clean_link(item.select_one('a')['href'])
                }

                products.append(product)

            except (AttributeError, KeyError) as e:

                logger.warning(f"Failed to parse product: {str(e)}")
                continue

        return products


    def _clean_link(self, link: str) -> str:

        return f"https:{link}" if link.startswith('//') else link

    # Example usage:
if __name__ == "__main__":
    scraper = AliScraper()
    results = scraper.search_products("wireless earbuds")

    for product in results:
        print(product)