import tortoise.exceptions
import api.routers
import models.other
import models.coins
import models.db
import fastapi


@api.routers.coin.post('/add')
async def set_coins(
    request: models.coins.AddRequest,
) -> models.other.Success:
    '''
    add coins to balance
    '''
    try:
        user = await models.db.User.get(tg_id=request.tg_id)
    except tortoise.exceptions.DoesNotExist:
        raise fastapi.HTTPException(
            status_code=404,
            detail='unknown user id, you should dm tg bot first',
        )
    user.coins += request.amount
    await user.save()
    return models.other.Success()


@api.routers.coin.get(
    '/get',
)
async def get_coins(
    tg_id: int,
) -> models.coins.GetResponse:
    '''
    get balance
    '''
    try:
        user = await models.db.User.get(tg_id=tg_id)
    except tortoise.exceptions.DoesNotExist:
        raise fastapi.HTTPException(
            status_code=404,
            detail='unknown user id, you should dm tg bot first',
        )
    return models.coins.GetResponse(
        coins=user.coins,
    )

