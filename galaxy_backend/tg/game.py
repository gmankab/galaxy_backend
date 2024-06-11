from core.common import all
import core.config
import models.db
import aiogram.exceptions
import aiogram.types
import aiogram.utils
import aiogram

class inline_keyboard:
    start_button = aiogram.types.InlineKeyboardButton(
        text='Start the game',
        web_app=aiogram.types.WebAppInfo(
            url=core.config.env.game_url,
        ),
    )
    bonus_button = aiogram.types.InlineKeyboardButton(
        text='Bonuses',
        callback_data='bonus'
    )
    main_back_button = aiogram.types.InlineKeyboardButton(
        text='Back',
        callback_data='main_back'
    )

    channel_link = f"https://t.me/{core.config.env.channel_username.lstrip('@')}"
    join_button = aiogram.types.InlineKeyboardButton(
        text='Join',
        url=channel_link
    )
    channel_check_button = aiogram.types.InlineKeyboardButton(
        text='Check',
        callback_data='check_subscription'
    )
    join_channel_button = aiogram.types.InlineKeyboardButton(
        text='Join our channel',
        callback_data='join_channel'
    )

    markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[start_button], [bonus_button]]
    )

    join_markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[join_button], [channel_check_button], [main_back_button]]
    )

    check_markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[main_back_button]]
    )

    task_markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[join_channel_button], [main_back_button]]
    )

def is_bonus_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'bonus'

def is_main_back_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'main_back'

def is_join_channel_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'join_channel'

def is_join_back_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'join_back'

def is_check_subscription_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'check_subscription'

@all.dp.message()
async def on_message(
    msg: aiogram.types.Message,
) -> None:
    assert msg.bot
    assert msg.from_user
    await models.db.User.get_or_create(
        tg_id=msg.from_user.id,
        coins=0,
        autoclicks_remain=0,
    )
    await msg.answer(
        text='hello',
        reply_markup=inline_keyboard.markup,
    )

@all.dp.callback_query(is_bonus_callback)
async def on_bonus_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    await callback_query.message.edit_text(
        text='You get coins for completed tasks. Select the task you want to complete below',
        reply_markup=inline_keyboard.task_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_join_channel_callback)
async def on_join_channel_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    await callback_query.message.edit_text(
        text='Click the button below to join the channel',
        reply_markup=inline_keyboard.join_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_main_back_callback)
async def on_back_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    await callback_query.message.edit_text(
        text='hello',
        reply_markup=inline_keyboard.markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_join_back_callback)
async def on_join_back_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    await callback_query.message.edit_text(
        text='You get coins for completed tasks. Select the task you want to complete below',
        reply_markup=inline_keyboard.task_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_check_subscription_callback)
async def on_check_subscription(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    user_id = callback_query.from_user.id
    channel_username = core.config.env.channel_username.lstrip('@')
    bot = callback_query.bot
    assert bot is not None, "Bot instance is None"

    try:
        member = await bot.get_chat_member(chat_id=f"@{channel_username}", user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            await callback_query.message.edit_text(
                text='Thanks for joining our channel, take your 1000 coins!',
                reply_markup=inline_keyboard.check_markup
            )
        else:
            await callback_query.message.edit_text(
                text='You did not join our channel. Please join our channel first.',
                reply_markup=inline_keyboard.check_markup
            )
    except aiogram.exceptions.TelegramAPIError:
        await callback_query.message.edit_text(
            text='You did not join our channel. Please join our channel first.',
            reply_markup=inline_keyboard.check_markup
        )

    await callback_query.answer()
