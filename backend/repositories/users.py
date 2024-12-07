from sqlalchemy import select, null
from sqlalchemy.ext.asyncio import AsyncSession

from models import UserModel, HabitModel
from repositories.repository import ManagerRepository


class UserRepository(ManagerRepository):
    model = UserModel

    @classmethod
    async def get_users_habits_by_hour(cls, session: AsyncSession, hour: int):
        query = (
            select(cls.model.telegram_id, HabitModel.id, HabitModel.name)
            .join(HabitModel)
            .filter(
                HabitModel.notification_hour == hour,
                cls.model.is_active == True,
                HabitModel.is_frozen == False,
                HabitModel.completed_at == null(),
            )
            .order_by(cls.model.telegram_id)
        )
        print(query)
        result = await session.execute(query)
        return result.all()
