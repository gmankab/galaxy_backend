from core.common import all
import core.config
import models.db
import aiogram.exceptions
import aiogram.types
import aiogram.utils
import aiogram

class inline_keyboard:
    button1 = aiogram.types.InlineKeyboardButton(
        text='start game',
        web_app=aiogram.types.WebAppInfo(
            url=core.config.env.game_url,
        ),
    )
    button2 = aiogram.types.InlineKeyboardButton(
        text='bonus',
        callback_data='bonus'
    )
    markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[button1], [button2]]
    )

    back_button = aiogram.types.InlineKeyboardButton(
        text='back',
        callback_data='back'
    )
    back_markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[back_button]]
    )

def is_bonus_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'bonus'

def is_back_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'back'

@all.dp.message()
async def on_message(
    msg: aiogram.types.Message,
) -> None:
    assert msg.bot
    assert msg.from_user
    user_status = await msg.bot.get_chat_member(
        chat_id=core.config.env.channel_username,
        user_id=msg.from_user.id
    )
    if user_status.status not in ['member', 'administrator', 'creator']:
        await msg.answer(
            text='You need to subscribe to our channel for the game to work.',
            reply_markup=aiogram.types.InlineKeyboardMarkup(
                inline_keyboard=[[
                    aiogram.types.InlineKeyboardButton(
                        text='Subscribe',
                        url=f'https://t.me/{core.config.env.channel_username.lstrip("@")}'
                    )
                ]]
            )
        )
        return
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
        text='hello buddy',
        reply_markup=inline_keyboard.back_markup
    )
    await callback_query.answer()

@all.dp.callback_query(is_back_callback)
async def on_back_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    await callback_query.message.edit_text(
        text='hello',
        reply_markup=inline_keyboard.markup
    )
    await callback_query.answer()


