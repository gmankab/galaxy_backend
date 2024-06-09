from core.common import all
import core.types
import datetime

async def timer(
    to_run: core.types.cor_str
):
    start = datetime.datetime.now()
    msg = await to_run()
    end = datetime.datetime.now()
    delta = end - start
    ms = int(delta.total_seconds() * 1000)
    all.logger.info(
        f'[passed] {ms} ms {msg}'
    )

