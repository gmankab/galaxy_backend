import tortoise.exceptions
import api.routers
import models.other
import models.coins
import models.db
import fastapi
import asyncio

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

async def autoclick_task(tg_id: int, interval: int, duration: int):
    '''
    Background task for adding coins to the user with a specified interval and duration.
    '''
    start_time = asyncio.get_event_loop().time()
    end_time = start_time + duration
    while asyncio.get_event_loop().time() < end_time:
        try:
            user = await models.db.User.get(tg_id=tg_id)
            user.coins += 1  # Добавляем одну монету за каждый интервал
            await user.save()
        except tortoise.exceptions.DoesNotExist:
            # Если пользователь не найден, прерываем выполнение
            break
        await asyncio.sleep(interval)

@api.routers.coin.post('/autoclick')
async def start_autoclick(
    request: models.coins.autoClickRequest,
    background_tasks: fastapi.BackgroundTasks
) -> models.other.Success:
    '''
    Runs an autoclicker to add coins periodically.
    '''
    background_tasks.add_task(autoclick_task, request.tg_id, request.interval, request.duration)
    return models.other.Success()
