import core.config
import tortoise


async def init_db():
    await tortoise.Tortoise.init(
        db_url=core.config.db.url,
        modules={'models': ['main']}
    )
    await tortoise.Tortoise.generate_schemas()
    yield
    await tortoise.Tortoise.close_connections()

