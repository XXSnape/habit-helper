from sqlalchemy import select, null
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from collections.abc import Sequence
from models import HabitModel, TrackingModel
from repositories.repository import ManagerRepository


class HabitRepository(ManagerRepository):
    model = HabitModel

    @classmethod
    async def get_required_count(cls, session: AsyncSession, data: dict) -> int | None:
        query = select(cls.model.count).filter_by(**data)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_habits(
        cls,
        session: AsyncSession,
        user_id: int,
        # is_frozen: bool,
        is_complete_null: bool,
    ) -> Sequence[HabitModel]:
        query = (
            select(cls.model)
            .options(
                selectinload(HabitModel.tracking).load_only(
                    TrackingModel.date, TrackingModel.is_done, TrackingModel.reason
                )
            )
            .filter_by(user_id=user_id)
            .order_by(cls.model.is_frozen.desc())
        )
        if is_complete_null:
            query = query.filter(cls.model.completed_at == null())
        else:
            query = query.filter(cls.model.completed_at != null())
        result = await session.execute(query)
        return result.scalars().all()
