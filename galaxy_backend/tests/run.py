import core.types
import core.shutdown
from tests import (
    init,
    coins,
    tg,
    timer,
)

async def main():
    to_run_list: list[core.types.cor_str] = [
        init.create_user,
        coins.get_coins,
        coins.add_coins,
        coins.start_autoclick,
        tg.test_on_message_user_not_subscribed,
        tg.test_on_message_user_subscribed,
        tg.test_on_message_no_user
    ]
    for to_run in to_run_list:
        await timer.timer(
            to_run=to_run
        )
    await core.shutdown.shutdown()

