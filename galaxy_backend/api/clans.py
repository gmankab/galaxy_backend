import tortoise.exceptions
from models.db import User, Clan, ClanOwner
import models.other
import asyncio

async def create_clan(clan_name: str, clan_owner_id: int) -> Clan | None:
    clan_owner_user = await User.get(tg_id = clan_owner_id)
    clan = await Clan.create(name = clan_name)
    clan_owner = await ClanOwner.create(user=clan_owner_user, clan=clan)
    await clan.save()
    await clan_owner.save()
    return clan

async def add_user(clan_id: int, user_id: int):
    user = await User.get(tg_id = user_id)
    clan = await Clan.get(id = clan_id)
    user.clan = clan
    await user.save()
    return

async def remove_user(user_id: int):
    user = await User.get(tg_id = user_id)
    user.clan = None
    await user.save()
    return

async def get_owner(clan_id: int):
    req_clan = await Clan.get(id = clan_id)
    clan_owner = await ClanOwner.get(clan = req_clan)
    return clan_owner.user.tg_id

async def get_members(clan_id: int):
    clan = await Clan.get(id = clan_id).prefetch_related("members")
    return clan.members
