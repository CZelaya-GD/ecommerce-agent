from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Product(base):

    __tablename__ = "products"

    id = Column(Integer, primary_key = True)
    name = Column(String(255))
    price = Column(Float)
    link = Column(String(512))
    category = Column(String(255))
    supplier = Column(String(50))

    def __repr__(self):

        return f"<Product(name = '{self.name}', price = {self.price})>"