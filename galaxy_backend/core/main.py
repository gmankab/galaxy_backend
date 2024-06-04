# ruff: noqa: F401
import tg.game as __game__
import api.coins
import api.app
import api.routers

app = api.app.app
app.include_router(api.routers.coin)

