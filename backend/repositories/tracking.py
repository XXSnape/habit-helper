from models import UserModel, TrackingModel
from repositories.repository import ManagerRepository


class TrackingRepository(ManagerRepository):
    model = TrackingModel
