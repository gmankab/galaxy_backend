from core.common import all
from tg.parse_langs import get_tr, Lang
import aiogram.filters.command
import aiogram.filters
import aiogram.types
import aiogram
import core.config
import models.db


def get_hello_markup(tr: Lang):
    start_button = aiogram.types.InlineKeyboardButton(
        text=tr.start_game,
        web_app=aiogram.types.WebAppInfo(
            url=core.config.env.game_url,
        ),
    )
    bonus_button = aiogram.types.InlineKeyboardButton(
        text=tr.bonuses,
        callback_data='bonus'
    )
    return aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[start_button], [bonus_button]]
    )


@all.dp.message(aiogram.filters.invert_f(
    aiogram.filters.command.CommandStart(deep_link=True))
)
async def on_message(
    msg: aiogram.types.Message,
) -> None:
    assert msg.bot
    assert msg.from_user
    assert msg.from_user.language_code
    tr = get_tr(msg.from_user.language_code)
    await models.db.User.get_or_create(
        tg_id=msg.from_user.id,
    )
    await msg.answer(
        text=tr.hello,
        reply_markup=get_hello_markup(tr),
    )


@all.dp.message(aiogram.filters.command.CommandStart(deep_link=True))
async def handle_start(
    msg: aiogram.types.Message,
    command: aiogram.filters.command.CommandObject,
):
    assert msg.from_user
    assert msg.from_user.language_code
    assert command.args
    if not command.args.startswith('joinclan_'):
        return
    tr = get_tr(msg.from_user.language_code)
    clan_id = int(command.args.replace('joinclan_', ''))
    if not await models.db.Clan.exists(id=clan_id):
        await msg.reply(tr.clans_invalid_id)
    clan = await models.db.Clan.get(id=clan_id)
    user, created = await models.db.User.get_or_create(tg_id=msg.from_user.id)
    if created:
        await user.save()
    if await models.db.User.filter(tg_id=user.tg_id, clan_id=clan.id).exists():
        await msg.reply(tr.clans_already_participate)
        return
    clan_join_confirm_button = aiogram.types.InlineKeyboardButton(
        text=tr.yes,
        callback_data=f'clan_accept_{clan_id}'
    )
    clan_join_deny_button = aiogram.types.InlineKeyboardButton(
        text=tr.no,
        callback_data=f'clan_deny_{clan_id}'
    )
    markup = aiogram.types.InlineKeyboardMarkup(inline_keyboard=[[clan_join_confirm_button], [clan_join_deny_button]])
    reply_text = tr.clan_join_request
    assert isinstance(reply_text, str)
    reply_text = reply_text.format(clan=clan.name)
    await msg.answer(
        text=reply_text,
        reply_markup=markup,
    )

