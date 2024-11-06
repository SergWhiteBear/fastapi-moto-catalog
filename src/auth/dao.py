from src.dao.base import BaseDAO
from src.auth.models import User, Role


class UsersDAO(BaseDAO):
    model = User

class RoleDAO(BaseDAO):
    model = Role