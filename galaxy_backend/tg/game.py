import json
import os
from core.common import all
import core.config
import models.db
import aiogram.exceptions
import aiogram.types
import aiogram.utils
import aiogram

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_translations(language_code):
    lang_file = os.path.join(BASE_DIR, "langs", f"{language_code}.json")
    if not os.path.exists(lang_file):
        lang_file = os.path.join(BASE_DIR, "langs", "en.json")
    with open(lang_file, "r", encoding="utf-8") as f:
        return json.load(f)

def get_translation(translations, key):
    return translations.get(key, key)

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
            inline_keyboard=[[join_channel_button], [main_back_button]]
        )

def is_bonus_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'bonus'

def is_main_back_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'main_back'

def is_join_channel_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'join_channel'

def is_check_subscription_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'check_subscription'

@all.dp.message()
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
        coins=0,
        autoclicks_remain=0,
    )
    await msg.answer(
        text=get_translation(translations, "hello"),
        reply_markup=kb.markup,
    )

@all.dp.callback_query(is_bonus_callback)
async def on_bonus_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    user_language_code = callback_query.from_user.language_code
    if user_language_code == 'ua':
        user_language_code = 'uk'
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
    if user_language_code == 'ua':
        user_language_code = 'uk'
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
    if user_language_code == 'ua':
        user_language_code = 'uk'
    translations = load_translations(user_language_code)
    kb = InlineKeyboard(translations)

    current_text = callback_query.message.text

    if current_text == get_translation(translations, "click_to_join"):
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
