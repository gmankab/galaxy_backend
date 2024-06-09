from core.common import all
import core.types
import datetime

async def timer(
    to_run: core.types.cor_str
):
    start = datetime.datetime.now()
    error: str = ''
    msg: str = ''
    try:
        msg = await to_run()
    except core.types.NotPassed as e:
        all.exit_code = 1
        error = e.msg
    except Exception as e:
        all.exit_code = 1
        raise e
    end = datetime.datetime.now()
    delta = end - start
    ms = int(delta.total_seconds() * 1000)
    if msg:
        all.console.log(
            f'[green]\\[passed] {ms} ms[/] {msg}'
        )
    else:
        all.console.log(
            f'[red]\\[error] {ms} ms[/] {error}'
        )

