from models.db import User, Clan
import api.clans as clans

async def check_basic():
    #user0 = await User.create(tg_id = 0, coins = 0, autoclicks_remain = 0)
    user1 = await User.create(tg_id = 1)
    user2 = await User.create(tg_id = 2)
    user3 = await User.create(tg_id = 3)
    user4 = await User.create(tg_id = 4)
    #await user0.save()
    #await user1.save()
    #await user2.save()
    #await user3.save()
    clanA = await clans.create_clan("ClanA", user1.tg_id)
    if isinstance(clanA, Clan):
        await clanA.save()
    else:
        print("failed to create clan")
        return
    await clans.add_user(clanA.id, user2.tg_id)
    await clans.add_user(clanA.id, user3.tg_id)
    await clans.add_user(clanA.id, user4.tg_id)
    clanA_members = await clans.get_members(clanA.id)
    expected_members = [2, 3, 4] # user1 shouldn't be in the list as it is the owner
    members_id = []
    for member in clanA_members:
        members_id.append(member.tg_id)
    members_id.sort()
    if members_id != expected_members:
        print("lists of members are not identical")
        return
    await clans.remove_user(user2.tg_id)
    clanA_members = await clans.get_members(clanA.id)
    expected_members = [3, 4] # we expect user2 to be removed from the clan
    members_id = []
    for member in clanA_members:
        members_id.append(member.tg_id)
    members_id.sort()
    if expected_members != expected_members:
        print("error in remove_user()")
        return
    return "check basic functionality of clans"
