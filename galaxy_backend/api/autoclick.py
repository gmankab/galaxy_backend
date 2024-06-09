import core.config
import models.other
import models.coins
import models.db
import asyncio


async def click(
    user: models.db.User,
):
    user.coins += 1
    user.autoclicks_remain -= 1
    await user.save()


async def background_clicker():
    '''
    background task for adding coins to the user with a specified interval and duration.
    '''
    while True:
        await asyncio.sleep(core.config.env.clicks_interval)
        users = await models.db.User.filter(autoclicks_remain__gt=0)
        for user in users:
            await click(user)

