from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
from .models.product import Product

logger = logging.getLogger(__name__)
class DBManager:

    def __init__(self, db_url: str):

        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind = self.engine)

    def log_product_reseach(self, product_data):

        with self.Session() as session:

            product = Product(
                name = product_data["supplier"],
                supplier = product_data["supplier"],
                cost = product_data["supplier"],
                potential_price = product_data["price"]
            )

            session.add(product)
            session.commit()

    def save_product(self, product_data: dict) -> bool:
        """
        Saves product data with transaction handling
        """

        session = self.Session()

        try:

            product = Product(
                name = product_data.get("name"),
                price = float(product_data["price"].replace('$', '')),
                link = product_data["link"],
                category = product_data.get("category", "unknown"),
                supplier = "aliexpress"
            )

            session.add(product)
            session.commit()

            return True

        except (KeyError, ValueError) as e:

            logger.error(f"Invalid product data: {str(e)}")
            session.rollback()

            return False

        except SQLAlchemyError as e:

            logger.error(f"Database error: {str(e)}")
            session.rollback()

            return False

        finally:

            session.close()


