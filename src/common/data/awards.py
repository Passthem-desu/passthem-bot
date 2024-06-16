import os
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.download import download, writeData
from src.models.models import *
from src.common.dataclasses.award_info import AwardInfo


async def getAwardInfo(session: AsyncSession, uid: int, aid: int):
    query = (
        select(
            Award.data_id,
            Award.img_path,
            Award.name,
            Award.description,
            Level.name,
            Level.color_code,
        )
        .filter(Award.data_id == aid)
        .join(Level, Level.data_id == Award.level_id)
    )
    award = (await session.execute(query)).one().tuple()

    skinQuery = (
        select(Skin.name, Skin.extra_description, Skin.image)
        .filter(Skin.applied_award_id == award[0])
        .filter(Skin.used_skins.any(UsedSkin.user_id == uid))
    )
    skin = (await session.execute(skinQuery)).one_or_none()

    info = AwardInfo(
        awardId=award[0],
        awardImg=award[1],
        awardName=award[2],
        awardDescription=award[3],
        levelName=award[4],
        color=award[5],
        skinName=None,
    )

    if skin:
        skin = skin.tuple()
        info.skinName = skin[0]
        info.awardDescription = (
            skin[1] if len(skin[1].strip()) > 0 else info.awardDescription
        )
        info.awardImg = skin[2]

    return info


async def getStorage(session: AsyncSession, uid: int, aid: int):
    query = select(StorageStats.count).filter(
        StorageStats.target_user_id == uid, StorageStats.target_award_id == aid
    )

    return (await session.execute(query)).scalar_one_or_none()


async def addStorage(session: AsyncSession, uid: int, aid: int, count: int):
    res = await getStorage(session, uid, aid)

    if res is None:
        newStorage = StorageStats(target_user_id=uid, target_award_id=aid, count=count)
        session.add(newStorage)
        return 0

    query = (
        update(StorageStats)
        .where(
            StorageStats.target_user_id == uid,
            StorageStats.target_award_id == aid,
        )
        .values(count=res + count)
    )
    await session.execute(query)
    return res


async def getAidByName(session: AsyncSession, name: str):
    query = select(Award.data_id).filter(Award.name == name)
    res = (await session.execute(query)).scalar_one_or_none()

    if res is None:
        query = select(Award.data_id).filter(Award.alt_names.any(
            AwardAltName.name == name
        ))
        res = (await session.execute(query)).scalar_one_or_none()
    
    return res


async def downloadAwardImage(aid: int, url: str):
    uIndex: int = 0

    def _path():
        return os.path.join(".", "data", "awards", f"{aid}_{uIndex}.png")

    while os.path.exists(_path()):
        uIndex += 1

    await writeData(await download(url), _path())

    return _path()