from pathlib import Path
import fastapi.testclient
import importlib.metadata
import rich.console
import core.config
import tomllib
import aiogram
import logging
import fastapi
import httpx


def get_toml_data(
    path: Path
) -> dict:
    with path.open('rb') as file:
        return tomllib.load(file)


class path:
    app = Path(__file__).parent.parent.parent.resolve()
    pyproject = app / 'pyproject.toml'


class app:
    if path.pyproject.exists():
        _dict = get_toml_data(path.pyproject)['project']
        version: str = _dict['version']
        name: str = _dict['name']
    else:
        name: str = path.app.name
        version: str = importlib.metadata.version(name)


class tg:
    dp: aiogram.Dispatcher = aiogram.Dispatcher()
    if core.config.env.tg_token:
        bot: aiogram.Bot = aiogram.Bot(
            token=core.config.env.tg_token
        )

class UvicornStyleFormatter(logging.Formatter):
    def format(self, record):
        record.levelprefix = record.levelname  # Align with Uvicorn's format
        return super().format(record)


class logger:
    logger = logging.getLogger(app.name)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    log_formatter = logging.Formatter('%(levelname)s: %(message)s')
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)


class all:
    async_client: httpx.AsyncClient
    fastapi_app: fastapi.FastAPI
    console: rich.console.Console = rich.console.Console()
    dp: aiogram.Dispatcher = tg.dp
    version: str = app.version
    name: str = app.name
    logger: logging.Logger = logger.logger
    exit_code: int = 0

