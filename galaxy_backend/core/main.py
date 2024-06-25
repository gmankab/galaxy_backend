# ruff: noqa: F401
import tg.hello as __hello__
import tg.clans as __clans__
import tg.bonuses as __bonuses__
import api.autoclick
import api.app
import api.coins
import api.clans
import api.planets
import api.routers
import api.ref

app = api.app.app
app.include_router(api.routers.coin)
app.include_router(api.routers.clan)
app.include_router(api.routers.clan_member)
app.include_router(api.routers.sector)
app.include_router(api.routers.planet)
app.include_router(api.routers.ref)

