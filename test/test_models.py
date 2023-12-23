import factory
import pytest
from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.orm import Session
from engine import base_engine as engine
from .settings import DEFAULT_PRICE
from api.models import Product

session = Session(engine)


class ModelFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = Session()


class FactoryProduct(ModelFactory):
    sku = factory.sequence(lambda x: f'ABC{x+1}')
    brand = factory.Faker('name')
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    price = factory.sequence(lambda x: (x + 1) * DEFAULT_PRICE)
    non_discountable = factory.Faker('boolean')

    class Meta:
        model = Product


def create_factory():
    for idx in range(5):
        id = idx + 1
        product = FactoryProduct(id=id)
        data = Product(
            sku=product.sku,
            brand=product.brand,
            name=product.name,
            description=product.description,
            price=product.price,
            non_discountable=product.non_discountable)
        session.add(data)
    session.commit()


def test_product():
    product = FactoryProduct(id=2)
    assert product.price is not None


def test_create_factory():
    create_factory()

    products = session.query(Product).all()
    assert len(products) == 10

    for product in products:
        assert product.price is not None


def cleanup_after_tests(request):
    def finalizer():
        # Membersihkan data setelah semua tes selesai
        session.query(Product).delete()
        session.commit()

    request.addfinalizer(finalizer)