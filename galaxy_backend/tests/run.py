import core.types
import core.shutdown
import asyncio
from tests import (
    pyright,
    coins,
    timer,
    ruff,
    init,
)


async def thread1():
    to_run_list: list[core.types.cor_str] = [
        init.create_user,
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
            timeout=60,
        )
    except asyncio.TimeoutError:
        print('timed out')
    await tasks
    await core.shutdown.shutdown()

