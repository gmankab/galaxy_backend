import models.other
import models.db
import api.routers


@api.routers.sector.get('/list')
async def sector_list() -> list[dict]:
    '''
    list sectors
    '''
    sectors_list: list[dict] = []
    sectors_models = await models.db.Sector.all()
    for sector in sectors_models:
        sectors_list.append({
            'id': sector.id,
            'available': sector.available,
        })
    return sectors_list


@api.routers.planet.get('/list')
async def planet_list() -> list[dict]:
    '''
    list planets
    '''
    planets_list: list[dict] = []
    planets_models = await models.db.Planet.all().prefetch_related('sector')
    for planet in planets_models:
        planets_list.append({
            'id': planet.id,
            'sector': planet.sector.id,
            'total_resources': planet.total_resources,
            'mined_resources': planet.mined_resources,
            'available': planet.available,
        })
    return planets_list


@api.routers.sector.get('/get')
async def sector_get(
    sector_id: int
) -> list[dict]:
    '''
    get planets from sector
    '''
    planets_list: list[dict] = []
    planets_models = await models.db.Planet.filter(sector_id=sector_id).prefetch_related('sector')
    for planet in planets_models:
        planets_list.append({
            'id': planet.id,
            'sector': planet.sector.id,
            'total_resources': planet.total_resources,
            'mined_resources': planet.mined_resources,
            'available': planet.available,
        })
    return planets_list

