from models.db import User, Clan, ClanOwner
import fastapi
import api.routers
import models.other
import models.clans
from core.common import tg
from aiogram.utils.deep_linking import create_start_link


@api.routers.clan.post('/create')
async def create_clan_endpoint(request: models.clans.ClanCreateRequest):
    try:
        clan = await create_clan(request.clan_name, request.clan_owner_id)
        return {'clan_id': clan.id, 'clan_name': clan.name}
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))


@api.routers.clan_member.post('/remove')
async def remove_user_endpoint(request: models.clans.UserRequest):
    try:
        await remove_user(request.user_id)
        return {'message': 'User removed from clan'}
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))


@api.routers.clan.get('/get_owner/{clan_id}')
async def get_owner_endpoint(clan_id: int):
    try:
        owner_id = await get_owner(clan_id)
        return {'clan_owner_id': owner_id}
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))


@api.routers.clan_member.get('/list/{clan_id}')
async def get_members_endpoint(clan_id: int):
    try:
        members = await get_members(clan_id)
        return {'members': [member.tg_id for member in members]}
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))


async def create_clan(clan_name: str, clan_owner_id: int) -> Clan:
    clan_owner_user, _ = await User.get_or_create(tg_id = clan_owner_id)
    clan = await Clan.create(name = clan_name)
    clan_owner = await ClanOwner.create(user=clan_owner_user, clan=clan)
    await clan.save()
    await clan_owner.save()
    return clan


async def add_user(clan_id: int, user_id: int) -> None:
    user = await User.get(tg_id = user_id)
    clan = await Clan.get(id = clan_id)
    user.clan = clan
    await user.save()
    return


async def remove_user(user_id: int) -> None:
    user = await User.get(tg_id = user_id)
    user.clan = None
    await user.save()
    return


async def get_owner(clan_id: int) -> int:
    req_clan = await Clan.get(id=clan_id)
    clan_owner = await ClanOwner.get(clan=req_clan)
    clan_owner_user = await clan_owner.user  # Fetch the related user object
    return clan_owner_user.tg_id


async def get_members(clan_id: int) -> list[User]:
    return await User.filter(clan_id=clan_id)


# get an invite link for a clan with id clan_id
@api.routers.clan.get('/get_invite/{clan_id}')
async def get_invite_link(clan_id: int):
    try:
        link = await create_start_link(tg.bot, f'joinclan_{clan_id}')
        return {'link': link}
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))

