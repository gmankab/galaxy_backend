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

