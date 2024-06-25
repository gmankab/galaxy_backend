from core.common import all, tg
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
    if command.args.startswith('joinclan_'):
        tr = get_tr(msg.from_user.language_code)
        try:
            clan_id = int(command.args.replace('joinclan_', ''))
        except ValueError:
            await msg.reply(tr.clans_invalid_id)
            return
        if not await models.db.Clan.exists(id=clan_id):
            await msg.reply(tr.clans_invalid_id)
        clan = await models.db.Clan.get(id=clan_id)
        user, created = await models.db.User.get_or_create(tg_id=msg.from_user.id)
        if created:
            await user.save()
        if await models.db.User.filter(tg_id=user.tg_id, clan_id=clan.id).exists():
            await msg.reply(tr.clans_already_participate)
            return
        if await models.db.ClanOwner.exists(user_id=user.tg_id):
            await msg.reply(tr.clan_already_owned)
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
    elif command.args.startswith('uid_'):
        tr = get_tr(msg.from_user.language_code)
        user, created = await models.db.User.get_or_create(tg_id=msg.from_user.id)
        if not created:
            await msg.reply(tr.already_have_account)
            return
        try:
            uid = int(command.args.replace('uid_', ''))
        except ValueError:
            await msg.reply(tr.broken_invite)
            await user.delete() # give user a chance to activate a link once again
            return
        if not await models.db.User.filter(tg_id=uid).exists() or uid == msg.from_user.id:
            await msg.reply(tr.broken_invite)
            await user.delete()
            return
        reward = core.config.bonus.bot_invite_reward
        if msg.from_user.is_premium:
            reward = reward * core.config.bonus.prem_user_multiplier
        await msg.answer(tr.ref_receiver_msg.format(coins=reward))
        user.coins += reward
        await user.save()
        sender = await models.db.User.get(tg_id=uid)
        sender.coins += reward
        await sender.save()
        await tg.bot.send_message(uid, tr.ref_sender_msg.format(coins=reward))

