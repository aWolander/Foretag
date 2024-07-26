from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    # jag vet inte varför man gör såhär
    pass


class Review(Base):
    __tablename__ = "review"
    id: Mapped[int] = mapped_column(primary_key=True)

    text: Mapped[Optional[str]] = mapped_column(String)
    rating: Mapped[str] = mapped_column(String)
    # datetime bättre
    date: Mapped[str] = mapped_column(String)

    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id", ondelete="CASCADE"))
    product: Mapped["Product"] = relationship("Product", back_populates="reviews")


class Product(Base):
    # var visst fel sätt...
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String)

    category: Mapped["Category"] = relationship(back_populates="products")
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"))

    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="product", cascade="all, delete", passive_deletes=True) # cascade?


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String)

    source_id: Mapped[int] = mapped_column(ForeignKey("source.id", ondelete="CASCADE"))
    source:  Mapped["Source"] = relationship(back_populates="categories")

    products: Mapped[List["Product"]] = relationship(back_populates="category", cascade="all, delete")


class Source(Base):
    __tablename__ = "source"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    name: Mapped[int] = mapped_column(String)

    categories: Mapped[List["Category"]] = relationship(back_populates="source", cascade="all, delete")


