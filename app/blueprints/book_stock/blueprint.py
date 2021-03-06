from flask import Blueprint

from .serializers import book_stock_serializer
from .serializers import book_stocks_serializer
from .service import BookStockService
from .swagger import book_stock_search_output_sw_model
from .swagger import book_stock_sw_model
from app.blueprints.base import BaseResource
from app.decorators import token_required
from app.extensions import api as root_api


blueprint = Blueprint('book_stocks', __name__)
api = root_api.namespace('book_stocks', description='Book Stocks endpoints.')


class _BookStockResource(BaseResource):
    book_stock_service = BookStockService()


@api.route('')
class NewBookStockResource(_BookStockResource):
    @api.doc(
        responses={
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.expect(book_stock_sw_model)
    @api.marshal_with(book_stock_sw_model, envelope='data', code=201)
    @token_required
    def post(self) -> tuple:
        book = self.book_stock_service.create(**self.request_payload())
        return book_stock_serializer.dump(book), 201


@api.route('/<int:book_stock_id>')
class BookStockResource(_BookStockResource):
    @api.doc(
        responses={
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.marshal_with(book_stock_sw_model, envelope='data')
    @token_required
    def get(self, book_stock_id: int) -> tuple:
        book_stock = self.book_stock_service.find(book_stock_id)
        return book_stock_serializer.dump(book_stock), 200

    @api.doc(
        responses={
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.expect(book_stock_sw_model)
    @api.marshal_with(book_stock_sw_model, envelope='data')
    @token_required
    def put(self, book_stock_id: int) -> tuple:
        book_stock = self.book_stock_service.save(
            book_stock_id, **self.request_payload()
        )
        return book_stock_serializer.dump(book_stock), 200

    @api.doc(
        responses={
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.marshal_with(book_stock_sw_model, envelope='data')
    @token_required
    def delete(self, book_stock_id: int) -> tuple:
        book = self.book_stock_service.delete(book_stock_id)
        return book_stock_serializer.dump(book), 200


@api.route('/search')
class BookStocksSearchResource(_BookStockResource):
    @api.doc(
        responses={
            200: 'Success',
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.marshal_with(book_stock_search_output_sw_model)
    @token_required
    def post(self) -> tuple:
        book_stock_data = self.book_stock_service.get(**self.request_payload())
        book_stock_data_lst = list(book_stock_data['query'].items)
        return {
            'data': book_stocks_serializer.dump(book_stock_data_lst),
            'records_total': book_stock_data['records_total'],
            'records_filtered': book_stock_data['records_filtered'],
        }, 200
