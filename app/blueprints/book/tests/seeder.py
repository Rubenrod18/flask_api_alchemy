from typing import Type

from app.blueprints.book import Book
from app.blueprints.book import BookPrice
from app.blueprints.book.tests.factory import BookFactory
from app.blueprints.book.tests.factory import BookPriceFactory
from app.blueprints.book.tests.factory import HarryPotterPartFiveBookFactory
from app.blueprints.book.tests.factory import HarryPotterPartFourBookFactory
from app.blueprints.book.tests.factory import HarryPotterPartOneBookFactory
from app.blueprints.book.tests.factory import HarryPotterPartThreeBookFactory
from app.blueprints.book.tests.factory import HarryPotterPartTwoBookFactory
from app.blueprints.country import Country
from app.decorators import seed_actions


class Seeder:
    name = 'BookSeeder'

    @seed_actions
    def __init__(self):
        self.__create_books()
        self.__create_book_prices()

    @staticmethod
    def __create_book(book_factory: Type[BookFactory], **kwargs) -> None:
        if Book.query.filter_by(**kwargs).first() is None:
            book_factory.create()

    @staticmethod
    def __create_book_prices():
        total_books = Book.query.count()
        total_countries = Country.query.count()
        total_book_prices = total_books * total_countries

        if BookPrice.query.count() < total_book_prices:
            BookPriceFactory.create_batch(total_book_prices)

    def __create_books(self) -> None:
        self.__create_book(
            HarryPotterPartOneBookFactory,
            **{'isbn': HarryPotterPartOneBookFactory.isbn}
        )
        self.__create_book(
            HarryPotterPartTwoBookFactory,
            **{'isbn': HarryPotterPartTwoBookFactory.isbn}
        )
        self.__create_book(
            HarryPotterPartThreeBookFactory,
            **{'isbn': HarryPotterPartThreeBookFactory.isbn}
        )
        self.__create_book(
            HarryPotterPartFourBookFactory,
            **{'isbn': HarryPotterPartFourBookFactory.isbn}
        )
        self.__create_book(
            HarryPotterPartFiveBookFactory,
            **{'isbn': HarryPotterPartFiveBookFactory.isbn}
        )
