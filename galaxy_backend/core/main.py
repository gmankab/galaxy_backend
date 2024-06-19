# ruff: noqa: F401
import tg.game as __game__
import api.autoclick
import api.app
import api.coins
import api.clans
import api.routers

app = api.app.app
app.include_router(api.routers.coin)
app.include_router(api.routers.clan)

