import json
import os

from core.common import all
import core.config
import models.db
import aiogram.exceptions
import aiogram.types
import aiogram.utils
import aiogram.filters
import aiogram
from aiogram.filters import CommandStart, CommandObject, callback_data
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram import F
import tortoise.exceptions

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_translations(language_code):
    lang_file = os.path.join(BASE_DIR, "langs", f"{language_code}.json")
    if not os.path.exists(lang_file):
        lang_file = os.path.join(BASE_DIR, "langs", "en.json")
    with open(lang_file, "r", encoding="utf-8") as f:
        return json.load(f)

def get_translation(translations, key):
    return translations.get(key, key)

class ClanJoinCallback(callback_data.CallbackData, prefix="cj"):
    clan_id: int
    confirm: bool

class InlineKeyboard:
    def __init__(self, translations):
        self.translations = translations

        start_button = aiogram.types.InlineKeyboardButton(
            text=get_translation(translations, "start_game"),
            web_app=aiogram.types.WebAppInfo(
                url=core.config.env.game_url,
            ),
        )
        bonus_button = aiogram.types.InlineKeyboardButton(
            text=get_translation(translations, "bonuses"),
            callback_data='bonus'
        )
        main_back_button = aiogram.types.InlineKeyboardButton(
            text=get_translation(translations, "back"),
            callback_data='main_back'
        )

        channel_link = f"https://t.me/{core.config.env.channel_username.lstrip('@')}"
        join_button = aiogram.types.InlineKeyboardButton(
            text=get_translation(translations, "join"),
            url=channel_link
        )

        invite_friend_button = aiogram.types.InlineKeyboardButton(
            text=get_translation(translations, "invite_friend_button"),
            callback_data='invite_friend'
        )

        channel_check_button = aiogram.types.InlineKeyboardButton(
            text=get_translation(translations, "check"),
            callback_data='check_subscription'
        )
        join_channel_button = aiogram.types.InlineKeyboardButton(
            text=get_translation(translations, "join_our_channel"),
            callback_data='join_channel'
        )

        self.markup = aiogram.types.InlineKeyboardMarkup(
            inline_keyboard=[[start_button], [bonus_button]]
        )

        self.join_markup = aiogram.types.InlineKeyboardMarkup(
            inline_keyboard=[[join_button], [channel_check_button], [main_back_button]]
        )

        self.check_markup = aiogram.types.InlineKeyboardMarkup(
            inline_keyboard=[[main_back_button]]
        )

        self.task_markup = aiogram.types.InlineKeyboardMarkup(
            inline_keyboard=[[join_channel_button], [invite_friend_button], [main_back_button]]
        )

def is_bonus_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'bonus'

def is_main_back_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'main_back'

def is_join_channel_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'join_channel'

def is_check_subscription_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'check_subscription'

@all.dp.message(aiogram.filters.invert_f(CommandStart(deep_link=True)))
async def on_message(
    msg: aiogram.types.Message,
) -> None:
    assert msg.bot
    assert msg.from_user

    user_language_code = msg.from_user.language_code
    if user_language_code == 'uk':
        user_language_code = 'ua'
    translations = load_translations(user_language_code)
    kb = InlineKeyboard(translations)

    await models.db.User.get_or_create(
        tg_id=msg.from_user.id,
    )
    await msg.answer(
        text=get_translation(translations, "hello"),
        reply_markup=kb.markup,
    )

@all.dp.callback_query(is_bonus_callback)
async def on_bonus_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    user_language_code = callback_query.from_user.language_code
    if user_language_code == 'uk':
        user_language_code = 'ua'
    translations = load_translations(user_language_code)
    kb = InlineKeyboard(translations)

    await callback_query.message.edit_text(
        text=get_translation(translations, "coins_for_tasks"),
        reply_markup=kb.task_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_join_channel_callback)
async def on_join_channel_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    user_language_code = callback_query.from_user.language_code
    if user_language_code == 'uk':
        user_language_code = 'ua'
    translations = load_translations(user_language_code)
    kb = InlineKeyboard(translations)

    await callback_query.message.edit_text(
        text=get_translation(translations, "click_to_join"),
        reply_markup=kb.join_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_main_back_callback)
async def on_back_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    user_language_code = callback_query.from_user.language_code
    if user_language_code == 'uk':
        user_language_code = 'ua'
    translations = load_translations(user_language_code)
    kb = InlineKeyboard(translations)

    current_text = callback_query.message.text

    if current_text == get_translation(translations, "thanks_for_joining"):
        new_text = get_translation(translations, "coins_for_tasks")
        new_markup = kb.task_markup
    elif current_text == get_translation(translations, "click_to_join"):
        new_text = get_translation(translations, "coins_for_tasks")
        new_markup = kb.task_markup
    else:
        new_text = get_translation(translations, "hello")
        new_markup = kb.markup

    await callback_query.message.edit_text(
        text=new_text,
        reply_markup=new_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_check_subscription_callback)
async def on_check_subscription(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    user_language_code = callback_query.from_user.language_code
    if user_language_code == 'uk':
        user_language_code = 'ua'
    translations = load_translations(user_language_code)
    kb = InlineKeyboard(translations)

    user_id = callback_query.from_user.id
    channel_username = core.config.env.channel_username.lstrip('@')

    if callback_query.bot is not None:
        try:
            member = await callback_query.bot.get_chat_member(f"@{channel_username}", user_id)
            if member.status in ['member', 'administrator', 'creator']:
                await callback_query.message.edit_text(
                    text=get_translation(translations, "thanks_for_joining"),
                    reply_markup=kb.check_markup
                )
            else:
                await callback_query.message.edit_text(
                    text=get_translation(translations, "not_subscribed"),
                    reply_markup=kb.join_markup
                )
        except aiogram.exceptions.TelegramAPIError as e:
            print(f"Error checking subscription: {e}")
            await callback_query.message.edit_text(
                text=get_translation(translations, "not_subscribed"),
                reply_markup=kb.join_markup
            )
    else:
        await callback_query.message.edit_text(
            text=get_translation(translations, "bot_error"),
            reply_markup=kb.join_markup
        )
    await callback_query.answer()

@all.dp.message(CommandStart(deep_link=True))
async def handle_start(msg: Message, command: CommandObject):
    assert msg.from_user
    lang_code = msg.from_user.language_code
    translation = load_translations(lang_code)
    args = command.args
    try:
        assert isinstance(args, str)
    except AssertionError:
        return
    if "joinclan_" in args:
        try:
            clan_id = int(args.replace("joinclan_", ""))
            clan = await models.db.Clan.get(id=clan_id)
            user_res = await models.db.User.get_or_create(tg_id=msg.from_user.id)
            if user_res[1]: # True is returned if an object was created (not fetched)
                await on_message(msg)
                await user_res[0].save()
            user = user_res[0]
            if await models.db.User.filter(tg_id=user.tg_id, clan_id=clan.id).exists():
                await msg.reply(get_translation(translation, "clans_already_participate"))
                return

            clan_join_confirm_button = aiogram.types.InlineKeyboardButton(
                text=get_translation(translation, "yes"),
                callback_data=ClanJoinCallback(clan_id=clan.id, confirm=True).pack()
            )

            clan_join_deny_button = aiogram.types.InlineKeyboardButton(
                text=get_translation(translation, "no"),
                callback_data=ClanJoinCallback(clan_id=clan.id, confirm=False).pack()
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[[clan_join_confirm_button], [clan_join_deny_button]])
            reply_text = get_translation(translation, "clan_join_request")
            assert isinstance(reply_text, str)
            reply_text = reply_text.replace("%clan%", clan.name)
            await msg.answer(text=reply_text, reply_markup=kb)
        except (ValueError, tortoise.exceptions.DoesNotExist):
            await msg.reply(get_translation(translation, "clans_invalid_id"))

@all.dp.callback_query(ClanJoinCallback.filter(F.confirm))
async def on_clan_join_confirm_button_press(callback_query: aiogram.types.CallbackQuery, callback_data: ClanJoinCallback):
    assert isinstance(callback_query.message, Message)
    lang_code = callback_query.from_user.language_code
    translation = load_translations(lang_code)
    user_id = callback_query.from_user.id
    clan_id = callback_data.clan_id
    user = (await models.db.User.get_or_create(tg_id=user_id))[0]
    clan = (await models.db.Clan.get_or_create(id=clan_id))[0]
    user.clan = clan
    await user.save()
    new_text = get_translation(translation, "clan_join_confirmed")
    assert isinstance(new_text, str)
    new_text = new_text.replace("%clan%", clan.name)
    await callback_query.message.edit_text(text=new_text)

@all.dp.callback_query(ClanJoinCallback.filter(not F.confirm))
async def on_clan_deny_button_press(callback_query: aiogram.types.CallbackQuery, callback_data: ClanJoinCallback):
    assert isinstance(callback_query.message, Message)
    lang_code = callback_query.from_user.language_code
    translation = load_translations(lang_code)
    clan = await models.db.Clan.get(id=callback_data.clan_id)
    new_text = get_translation(translation, "clan_join_denied")
    assert isinstance(new_text, str)
    new_text = new_text.replace("%clan%", clan.name)
    await callback_query.message.edit_text(text=new_text)

