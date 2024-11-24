from models import UserModel
from repositories.repository import ManagerRepository


class UserRepository(ManagerRepository):
    model = UserModel
