from core.common import all
import tortoise
import os


async def shutdown() -> None:
    all.logger.info('exiting')
    await tortoise.Tortoise.close_connections()
    os._exit(0)


@all.dp.shutdown()
async def dp_shutdown():
    await shutdown()

