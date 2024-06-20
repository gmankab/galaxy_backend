from models.db import User, Clan
import api.clans as clans


async def check_basic() -> str:
    user1 = await User.create(tg_id = 1)
    user2 = await User.create(tg_id = 2)
    user3 = await User.create(tg_id = 3)
    user4 = await User.create(tg_id = 4)
    clanA = await clans.create_clan("ClanA", user1.tg_id)
    try:
        assert isinstance(clanA, Clan)
    except AssertionError:
        raise AssertionError("create_clan() did not return a Clan object")
    await clanA.save()
    await clans.add_user(clanA.id, user2.tg_id)
    await clans.add_user(clanA.id, user3.tg_id)
    await clans.add_user(clanA.id, user4.tg_id)
    clanA_members = await clans.get_members(clanA.id)
    expected_members = [2, 3, 4] # user1 shouldn't be in the list as it is the owner
    members_id = []
    for member in clanA_members:
        members_id.append(member.tg_id)
    members_id.sort()
    try:
        assert members_id == expected_members
    except AssertionError:
        raise AssertionError("get_members() did not work correctly")
    await clans.remove_user(user2.tg_id)
    clanA_members = await clans.get_members(clanA.id)
    expected_members = [3, 4] # we expect user2 to be removed from the clan
    members_id = []
    for member in clanA_members:
        members_id.append(member.tg_id)
    members_id.sort()
    try:
        assert expected_members == expected_members
    except AssertionError:
        raise AssertionError("remove_user() did not work correctly")
    return "check basic functionality of clans"

