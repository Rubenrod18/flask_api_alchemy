import factory

from ...factory import BookFactory
from ._base_integration_test import _BookBaseIntegrationTest
from app.utils import ignore_keys


class TestUpdateBook(_BookBaseIntegrationTest):
    def test_is_book_updated_book_exist_previously_returns_book(
        self,
    ):
        with self.app.app_context():
            book_id = self.get_rand_book().id
            data = ignore_keys(
                factory.build(dict, FACTORY_CLASS=BookFactory),
                exclude=['image'],
            )

            admin_user = self.get_rand_admin_user()
            auth_header = self.build_auth_header(admin_user.email)
            response = self.client.put(
                f'{self.base_path}/{book_id}',
                json=data,
                headers=auth_header,
            )
            json_response = response.get_json()
            json_data = json_response.get('data')

            self.assertEqual(200, response.status_code)
            self.assertEqual(book_id, json_data.get('id'))
            self.assertEqual(data['author'], json_data.get('author'))
            self.assertEqual(data['description'], json_data.get('description'))
            self.assertEqual(data['isbn'], json_data.get('isbn'))
            self.assertEqual(data['total_pages'], json_data.get('total_pages'))
            self.assertEqual(data['publisher'], json_data.get('publisher'))
            self.assertEqual(
                data['published_date'], json_data.get('published_date')
            )
            self.assertEqual(data['language'], json_data.get('language'))
            self.assertEqual(data['dimensions'], json_data.get('dimensions'))
            self.assertTrue(json_data.get('created_at'))
            self.assertGreaterEqual(
                json_data.get('updated_at'), json_data.get('created_at')
            )
            self.assertIsNone(json_data.get('deleted_at'))
