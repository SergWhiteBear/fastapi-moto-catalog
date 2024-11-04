from src.dao.base import BaseDAO
from src.user.models import User, Role


class UserDAO(BaseDAO):
    model = User

class RoleDAO(BaseDAO):
    model = Role