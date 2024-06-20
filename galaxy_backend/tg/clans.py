from tg.parse_langs import get_tr
from core.common import all
import aiogram.exceptions
import models.db
import aiogram.types
import aiogram.filters


def is_clan_callback(query: aiogram.types.CallbackQuery) -> bool:
    if isinstance(query.data, str):
        if query.data.startswith('clan_'):
            return True
    return False


@all.dp.callback_query(is_clan_callback)
async def on_clan_callbac(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    assert isinstance(callback_query.data, str)
    assert callback_query.from_user
    assert callback_query.from_user.language_code
    _, action, clan_id_str = callback_query.data.split('_')
    user, _ = await models.db.User.get_or_create(tg_id=callback_query.from_user.id)
    clan, _ = await models.db.Clan.get_or_create(id=int(clan_id_str))
    tr = get_tr(callback_query.from_user.language_code)
    match action:
        case 'accept':
            user.clan = clan
            await user.save()
            await callback_query.message.edit_text(
                text=tr.clan_join_confirmed.format(clan=clan.name)
            )
        case 'deny':
            await callback_query.message.edit_text(
                text=tr.clan_join_denied.format(clan=clan.name)
            )
        case _:
            raise AssertionError

