from sqlalchemy import func

from app.blueprints.base import BaseTest
from app.blueprints.book import BookStock
from app.blueprints.role import Role
from app.blueprints.user import User
from app.blueprints.user import UserRoles
from app.extensions import db


class _BookStockBaseIntegrationTest(BaseTest):
    def setUp(self):
        super(_BookStockBaseIntegrationTest, self).setUp()
        self.base_path = '/api/book_stocks'

    @staticmethod
    def get_rand_admin_user():
        return (
            db.session.query(User)
            .join(UserRoles)
            .join(Role)
            .filter(
                User.deleted_at.is_(None),
                User.active == 1,
                Role.name == 'admin',
            )
            .first()
        )

    @staticmethod
    def get_rand_book_stock():
        return (
            BookStock.query.filter_by(deleted_at=None)
            .order_by(func.rand())
            .first()
        )
