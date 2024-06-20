import api.routers
import core.config
import models.other
import models.coins
import models.db


@api.routers.coin.post('/add')
async def coin_add(
    request: models.coins.AddRequest,
) -> models.other.Success:
    '''
    add coins to balance
    '''
    user, _ = await models.db.User.get_or_create(tg_id=request.tg_id)
    user.coins += request.amount
    await user.save()
    return models.other.Success()


@api.routers.coin.get(
    '/get',
)
async def coin_get(
    tg_id: int,
) -> models.coins.GetResponse:
    '''
    get balance
    '''
    user, _ = await models.db.User.get_or_create(tg_id=tg_id)
    return models.coins.GetResponse(
        coins=user.coins,
    )


@api.routers.coin.get(
    '/autoclick',
)
async def coin_autoclick(
    tg_id: int,
) -> models.other.Success:
    '''
    runs an autoclicker to add coins in background
    '''
    user, _ = await models.db.User.get_or_create(tg_id=tg_id)
    user.autoclicks_remain = core.config.env.max_autoclicks
    await user.save()
    return models.other.Success()

