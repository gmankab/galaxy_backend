from core.common import all, tg
import fastapi.middleware
import fastapi.middleware.cors
import fastapi.testclient
import fastapi
import models.db
import api.autoclick
import core.shutdown
import core.config
import contextlib
import tortoise
import asyncio
import httpx


async def init_db():
    await tortoise.Tortoise.init(
        db_url=core.config.env.db_url,
        modules={'models': ['models.db']}
    )
    await tortoise.Tortoise.generate_schemas()


@contextlib.asynccontextmanager
async def lifespan(
    __fastapi_app__,
):
    await init_db()
    if core.config.env.tg_token:
        asyncio.create_task(
            all.dp.start_polling(tg.bot)
        )
        all.logger.info('started tg bot')
    else:
        all.logger.warn('tg_token is not in env, skipping tg bot start')
        await models.db.User.get_or_create(
            tg_id=12345,
            coins=0,
            autoclicks_remain=0,
        )
    asyncio.create_task(api.autoclick.background_clicker())
    yield
    await core.shutdown.shutdown()


app = fastapi.FastAPI(
    title=all.name,
    version=all.version,
    lifespan=lifespan,
)
all.fastapi_app = app
transport = httpx.ASGITransport(app) # type: ignore
all.async_client = httpx.AsyncClient(
    transport=transport,
    base_url='http://test',
)

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['*']
)

