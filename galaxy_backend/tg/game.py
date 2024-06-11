from core.common import all
import core.config
import models.db
import aiogram.exceptions
import aiogram.types
import aiogram.utils
import aiogram
from aiogram import Bot, types

bot = Bot(token=core.config.env.tg_token)

class InlineKeyboard:
    start_button = types.InlineKeyboardButton(
        text='Start the game',
        web_app=types.WebAppInfo(
            url=core.config.env.game_url,
        ),
    )
    bonus_button = types.InlineKeyboardButton(
        text='Bonuses',
        callback_data='bonus'
    )
    join_channel_button = types.InlineKeyboardButton(
        text='Join our channel',
        callback_data='join_channel'
    )
    back_button = types.InlineKeyboardButton(
        text='Back',
        callback_data='back'
    )
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[[start_button], [bonus_button]]
    )

    tasks_markup = types.InlineKeyboardMarkup(
        inline_keyboard=[[join_channel_button], [back_button]]
    )

    back_tasks_button = types.InlineKeyboardButton(
        text='Back',
        callback_data='back_tasks'
    )

def is_bonus_callback(query: types.CallbackQuery) -> bool:
    return query.data == 'bonus'

def is_back_callback(query: types.CallbackQuery) -> bool:
    return query.data == 'back'

def is_join_channel_callback(query: types.CallbackQuery) -> bool:
    return query.data == 'join_channel'

def is_check_subscription_callback(query: types.CallbackQuery) -> bool:
    return query.data == 'check_subscription'

def is_back_tasks_callback(query: types.CallbackQuery) -> bool:
    return query.data == 'back_tasks'

def is_nothing_callback(query: types.CallbackQuery) -> bool:
    return query.data == 'nothing'

async def check_subscription(bot: Bot, user_id: int, channel_username: str) -> bool:
    member = await bot.get_chat_member(chat_id=f"@{channel_username}", user_id=user_id)
    return member.status in ('creator', 'administrator', 'member')

@all.dp.message()
async def on_message(msg: types.Message) -> None:
    assert msg.bot
    assert msg.from_user
    await models.db.User.get_or_create(
        tg_id=msg.from_user.id,
        coins=0,
        autoclicks_remain=0,
    )
    await msg.answer(
        text='hello',
        reply_markup=InlineKeyboard.markup,
    )

@all.dp.callback_query(is_bonus_callback)
async def on_bonus_button_press(callback_query: types.CallbackQuery):
    assert isinstance(callback_query.message, types.Message)
    await callback_query.message.edit_text(
        text='You get coins for completed tasks. Select the task you want to complete below',
        reply_markup=InlineKeyboard.tasks_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_back_callback)
async def on_back_button_press(callback_query: types.CallbackQuery):
    assert isinstance(callback_query.message, types.Message)
    await callback_query.message.edit_text(
        text='hello',
        reply_markup=InlineKeyboard.markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_join_channel_callback)
async def on_join_channel_button_press(callback_query: types.CallbackQuery):
    assert isinstance(callback_query.message, types.Message)
    channel_username = core.config.env.channel_username.lstrip('@')
    join_button = types.InlineKeyboardButton(
        text='Join',
        url=f'https://t.me/{channel_username}'
    )
    check_button = types.InlineKeyboardButton(
        text='Check',
        callback_data='check_subscription'
    )
    join_markup = types.InlineKeyboardMarkup(
        inline_keyboard=[[join_button], [check_button], [InlineKeyboard.back_tasks_button]]
    )
    await callback_query.message.edit_text(
        text='Click the link below to join the channel',
        reply_markup=join_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_check_subscription_callback)
async def on_check_subscription_button_press(callback_query: types.CallbackQuery):
    assert isinstance(callback_query.message, types.Message)
    user_id = callback_query.from_user.id
    channel_username = core.config.env.channel_username.lstrip('@')
    if await check_subscription(bot, user_id, channel_username):
        await callback_query.message.answer(
            text='You did join'
        )
    else:
        await callback_query.message.answer(
            text="You didn't join the channel."
        )
    await callback_query.answer()

@all.dp.callback_query(is_back_tasks_callback)
async def on_back_tasks_button_press(callback_query: types.CallbackQuery):
    assert isinstance(callback_query.message, types.Message)
    await callback_query.message.edit_text(
        text='You get coins for completed tasks. Select the task you want to complete below',
        reply_markup=InlineKeyboard.tasks_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_nothing_callback)
async def on_nothing_button_press(callback_query: types.CallbackQuery):
    await callback_query.answer()

