import core.shutdown
import core.common
import core.types
import asyncio
from tests import (
    pyright,
    coins,
    timer,
    ruff,
    clans,
    init,
    clans_fastapi,
)


async def thread1():
    to_run_list: list[core.types.cor_str] = [
        init.create_user,
        clans.check_basic,
        clans_fastapi.run_tests,
        coins.get_coins,
        coins.add_coins,
        coins.start_autoclick,
        ruff.ruff,
    ]
    for to_run in to_run_list:
        await timer.timer(
            to_run=to_run
        )


async def thread2():
    '''
    here is pyright test which is very slow, so it ran as separate thread
    '''
    await timer.timer(
        to_run=pyright.pyright,
    )


async def main():
    tasks = asyncio.gather(
        thread1(),
        thread2(),
    )
    try:
        await asyncio.wait_for(
            tasks,
            timeout=360,
        )
    except asyncio.TimeoutError:
        print('timed out')
    try:
        await tasks
    except asyncio.exceptions.CancelledError as e:
        print(e)
        core.common.all.exit_code = 1
    await core.shutdown.shutdown()

