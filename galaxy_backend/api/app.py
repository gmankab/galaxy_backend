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


async def init_all():
    await init_db()
    await start_bot()
    await create_planets_and_sectors()
    asyncio.create_task(api.autoclick.background_clicker())


async def create_planets_and_sectors():
    for planet_id in range(core.config.planet.count):
        sector_id = planet_id // core.config.planet.per_sector
        if sector_id == 0:
            available = True
        else:
            available = False
        sector, created = await models.db.Sector.get_or_create(
            id=sector_id,
            defaults={
                'available': available,
            }
        )
        if created:
            await sector.save()
        if not models.db.Planet.filter(id=planet_id).exists():
            planet_resources = planet_id * core.config.planet.resources_step + core.config.planet.initial_resources_count
            await models.db.Planet.create(
                id=planet_id,
                sector=sector,
                resources=planet_resources,
            )


async def start_bot():
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
    await init_all()
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

