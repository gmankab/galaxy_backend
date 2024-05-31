from core.common import all
import tg.game
import asyncio


async def async_main() -> None:
    tg.game.my_pass()
    all.log('[green]started')
    await all.dp.start_polling(all.bot)


def main():
    asyncio.run(async_main())

