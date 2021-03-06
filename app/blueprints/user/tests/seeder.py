import os

from .factory import Role
from .factory import User
from .factory import UserFactory
from app.decorators import seed_actions


class Seeder:
    name = 'UserSeeder'
    priority = 1

    @staticmethod
    def __create_admin_user():
        test_user_email = os.getenv('TEST_USER_EMAIL')
        test_user = User.query.filter_by(email=test_user_email).first()

        if test_user is None:
            admin_role = Role.query.filter_by(name='admin').first()

            params = {
                'email': test_user_email,
                'deleted_at': None,
                'active': True,
                'created_by': None,
                'roles': [admin_role],
            }
            UserFactory.create(**params)

    @seed_actions
    def __init__(self, rows: int = 10):
        self.__create_admin_user()
        UserFactory.create_batch(rows)
