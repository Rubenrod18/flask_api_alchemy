from flask import Blueprint

from app.blueprints.base import BaseResource
from app.blueprints.currency.serializers import currencies_serializer
from app.blueprints.currency.serializers import currency_serializer
from app.blueprints.currency.service import CurrencyService
from app.blueprints.currency.swagger import currency_search_output_sw_model
from app.blueprints.currency.swagger import currency_sw_model
from app.decorators import token_required
from app.extensions import api as root_api

blueprint = Blueprint('currencies', __name__)
api = root_api.namespace('currencies')


class _CurrencyBaseResource(BaseResource):
    currency_service = CurrencyService()


@api.route('')
class NewCurrencyResource(_CurrencyBaseResource):
    @api.doc(
        responses={
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.expect(currency_sw_model)
    @api.marshal_with(currency_sw_model, envelope='data', code=201)
    @token_required
    def post(self) -> tuple:
        currency = self.currency_service.create(**self.request_payload())
        return currency_serializer.dump(currency), 201


@api.route('/<int:currency_id>')
class CurrencyResource(_CurrencyBaseResource):
    @api.doc(
        responses={
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.marshal_with(currency_sw_model, envelope='data')
    @token_required
    def get(self, currency_id: int) -> tuple:
        currency = self.currency_service.find(currency_id)
        return currency_serializer.dump(currency), 200

    @api.doc(
        responses={
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.expect(currency_sw_model)
    @api.marshal_with(currency_sw_model, envelope='data')
    @token_required
    def put(self, currency_id: int) -> tuple:
        currency = self.currency_service.save(
            currency_id, **self.request_payload()
        )
        return currency_serializer.dump(currency), 200

    @api.doc(
        responses={
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.marshal_with(currency_sw_model, envelope='data')
    @token_required
    def delete(self, currency_id: int) -> tuple:
        currency = self.currency_service.delete(currency_id)
        return currency_serializer.dump(currency), 200


@api.route('/search')
class CurrencysSearchResource(_CurrencyBaseResource):
    @api.doc(
        responses={
            200: 'Success',
            401: 'Unauthorized',
            403: 'Forbidden',
            422: 'Unprocessable Entity',
        },
        security='auth_token',
    )
    @api.marshal_with(currency_search_output_sw_model)
    @token_required
    def post(self) -> tuple:
        currency_data = self.currency_service.get(**self.request_payload())
        currency_data_lst = list(currency_data['query'].items)
        return {
            'data': currencies_serializer.dump(currency_data_lst),
            'records_total': currency_data['records_total'],
            'records_filtered': currency_data['records_filtered'],
        }, 200
