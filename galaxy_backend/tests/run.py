from tests import init, coins
from core.common import all
import core.shutdown


async def main():
    to_run = [
        init.create_user,
        coins.get_coins,
        coins.add_coins,
    ]
    for func in to_run:
        msg = await func()
        all.logger.info(msg)
    await core.shutdown.shutdown()


