import fastapi
from core.common import tg
from aiogram.utils.deep_linking import create_start_link
import api.routers


@api.routers.ref.get('/get_invite/{uid}')
async def get_invite(uid: int):
    try:
        link = await create_start_link(tg.bot, f'uid_{uid}')
        return {'link': link}
    except Exception as e:
        raise fastapi.HTTPException(status_code=400, detail=str(e))

