import core.types
import core.shutdown
from tests import (
    init,
    coins,
    timer,
)

async def main():
    to_run_list: list[core.types.cor_str] = [
        init.create_user,
        coins.get_coins,
        coins.add_coins,
        coins.start_autoclick,
    ]
    for to_run in to_run_list:
        await timer.timer(
            to_run=to_run
        )
    await core.shutdown.shutdown()

