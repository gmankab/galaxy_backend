from pathlib import Path
import rich.console
import core.config
import tomllib
import aiogram


def get_toml_data(
    path: Path
) -> dict:
    with path.open('rb') as file:
        return tomllib.load(file)


class path:
    app = Path(__file__).parent.parent.parent.resolve()
    pyproject = app / 'pyproject.toml'


class app:
    _dict = get_toml_data(path.pyproject)['project']
    dependencies: str = _dict['dependencies']
    version: str = _dict['version']
    name: str = _dict['name']


class tg:
    dp: aiogram.Dispatcher = aiogram.Dispatcher()
    bot: aiogram.Bot = aiogram.Bot(
        token=core.config.tg.token
    )

class all:
    console: rich.console.Console = rich.console.Console()
    log = console.log
    dp: aiogram.Dispatcher = tg.dp
    bot: aiogram.Bot = tg.bot

