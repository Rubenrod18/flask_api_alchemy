import factory
from sqlalchemy import func

from app.blueprints.book import Book
from app.blueprints.book import BookStock
from app.blueprints.country import Country
from app.extensions import db


class BookStockFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = BookStock
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    quantity = factory.Faker('pyint', min_value=1, max_value=9999)

    @factory.lazy_attribute
    def country_id(self):
        total_books = Book.query.count()

        country = (
            Country.query.with_entities(Country.id)
            .outerjoin(BookStock)
            .filter_by(deleted_at=None)
            .group_by(Country.id)
            .having(func.count(Country.id) < total_books)
            .order_by(db.func.random())
            .first()
        )

        return country.id

    @factory.lazy_attribute
    def book_id(self):
        subquery = (
            Book.query.with_entities(Book.id)
            .outerjoin(BookStock)
            .filter(BookStock.country_id == self.country_id)
        )

        if subquery.count():
            book = (
                Book.query.outerjoin(BookStock)
                .outerjoin(Country)
                .filter(Book.deleted_at.is_(None), ~Book.id.in_(subquery))
                .first()
            )
        else:
            book = (
                Book.query.with_entities(Book.id)
                .order_by(db.func.random())
                .first()
            )

        return book.id
