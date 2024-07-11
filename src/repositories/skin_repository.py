from pathlib import Path

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..base.repository import BaseRepository
from ..models import Skin


class SkinRepository(BaseRepository[Skin]):
    """
    皮肤的仓库
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Skin)

    async def get_all_images(self) -> dict[int, str]:
        qa = select(Skin.data_id, Skin.image)
        return {row[0]: row[1] for row in (await self.session.execute(qa)).tuples()}

    async def update_image(self, data_id: int, image: str | Path) -> None:
        u = update(Skin).where(Skin.data_id == data_id).values(image=str(image))
        await self.session.execute(u)