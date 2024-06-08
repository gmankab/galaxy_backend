from tests import init, coins, tg
from core.common import all
import core.shutdown

async def main():
    to_run = [
        init.create_user,
        coins.get_coins,
        coins.add_coins,
        coins.start_autoclick,
        tg.test_on_message_user_not_subscribed,
        tg.test_on_message_user_subscribed,
        tg.test_on_message_no_user
    ]
    for func in to_run:
        msg = await func()
        all.logger.info(msg)
    await core.shutdown.shutdown()


