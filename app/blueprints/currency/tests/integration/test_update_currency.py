import factory

from ..factory import CurrencyFactory
from ._base_integration_test import _CurrencyBaseIntegrationTest


class TestUpdateCurrency(_CurrencyBaseIntegrationTest):
    def test_is_currency_updated_currency_exist_previously_returns_currency(
        self,
    ):
        with self.app.app_context():
            currency_id = self.get_rand_currency().id

            data = factory.build(dict, FACTORY_CLASS=CurrencyFactory)

            admin_user = self.get_rand_admin_user()
            auth_header = self.build_auth_header(admin_user.email)
            response = self.client.put(
                f'{self.base_path}/{currency_id}',
                json=data,
                headers=auth_header,
            )
            json_response = response.get_json()
            json_data = json_response.get('data')

            self.assertEqual(200, response.status_code)
            self.assertEqual(currency_id, json_data.get('id'))
            self.assertEqual(data['code'], json_data.get('code'))
            self.assertEqual(data['decimals'], json_data.get('decimals'))
            self.assertEqual(data['name'], json_data.get('name'))
            self.assertEqual(data['name_plural'], json_data.get('name_plural'))
            self.assertEqual(data['num'], json_data.get('num'))
            self.assertEqual(data['symbol'], json_data.get('symbol'))
            self.assertEqual(
                data['symbol_native'], json_data.get('symbol_native')
            )
            self.assertTrue(json_data.get('created_at'))
            self.assertGreaterEqual(
                json_data.get('updated_at'), json_data.get('created_at')
            )
            self.assertIsNone(json_data.get('deleted_at'))
