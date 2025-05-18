from .ali_scraper import AliScraper
from .perplexity_llm import PerplexityLLM
from typing import List, Dict
import logging
from agents.database.postgres_manager import DBManager

logger = logging.getLogger(__name__)

class ProductResearchOrchestrator:
    """
    Combines LLM and scraping to produce a list of trending products with details.
    """

    def __init__(self, db_url: str):

        self.llm = PerplexityLLM()
        self.scraper = AliScraper()
        self.db = DBManager(db_url)

    def run_pipeline(self) -> List[Dict]:
        """
        Full pipeline with error handling and database logging
        """

        try:

            products = self.get_trending_products()
            success_count = 0

            for product in products:

                if self.db.save_product(product):
                    success_count += 1

            logger.info(f"Saved {success_count}/{len(products)} products to DB")

            return products

        except Exception as e:

            logger.error(f"Pipeline failed: {str(e)}")

            return []

    def get_trending_products(self, top_n = 5):

        keywords = self.llm.get_trending_keywords(top_n=top_n)
        all_products = []

        for keyword in keywords:

            print(f"Searching AliExpress for: {keyword}")

            products = self.scraper.search_products(keyword)
            for product in products:

                product["category"] = keyword

            all_products.extend(products)

        return all_products

