import models.db
import api.app


async def create_user():
    await api.app.init_db()
    await models.db.User.get_or_create(
        tg_id=0,
        coins=0,
    )
    return 'passed create user'

