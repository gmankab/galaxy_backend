from tg.parse_langs import get_tr, Lang
from core.common import all
import aiogram.exceptions
import core.config
import tg.hello


def is_bonus_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'bonus'

def is_main_back_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'main_back'

def is_join_channel_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'join_channel'

def is_check_subscription_callback(query: aiogram.types.CallbackQuery) -> bool:
    return query.data == 'check_subscription'


def get_task_markup(tr: Lang):
    join_channel_button = aiogram.types.InlineKeyboardButton(
        text=tr.join_our_channel,
        callback_data='join_channel'
    )
    invite_friend_button = aiogram.types.InlineKeyboardButton(
        text=tr.invite_friend_button,
        callback_data='invite_friend'
    )
    main_back_button = aiogram.types.InlineKeyboardButton(
        text=tr.back,
        callback_data='main_back'
    )
    return aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[join_channel_button], [invite_friend_button], [main_back_button]]
    )


def get_join_markup(tr: Lang):
    channel_link = f'https://t.me/{core.config.env.channel_username}'
    join_button = aiogram.types.InlineKeyboardButton(
        text=tr.join,
        url=channel_link
    )
    channel_check_button = aiogram.types.InlineKeyboardButton(
        text=tr.check,
        callback_data='check_subscription'
    )
    main_back_button = aiogram.types.InlineKeyboardButton(
        text=tr.back,
        callback_data='main_back'
    )
    return aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[join_button], [channel_check_button], [main_back_button]]
    )


@all.dp.callback_query(is_bonus_callback)
async def on_bonus_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    assert callback_query.from_user
    assert callback_query.from_user.language_code
    tr = get_tr(callback_query.from_user.language_code)
    await callback_query.message.edit_text(
        text=tr.coins_for_tasks,
        reply_markup=get_task_markup(tr),
    )
    await callback_query.answer()


@all.dp.callback_query(is_join_channel_callback)
async def on_join_channel_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    assert callback_query.from_user
    assert callback_query.from_user.language_code
    tr = get_tr(callback_query.from_user.language_code)
    await callback_query.message.edit_text(
        text=tr.click_to_join,
        reply_markup=get_join_markup(tr),
    )
    await callback_query.answer()


@all.dp.callback_query(is_main_back_callback)
async def on_back_button_press(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    assert callback_query.from_user
    assert callback_query.from_user.language_code
    tr = get_tr(callback_query.from_user.language_code)
    current_text = callback_query.message.text
    if current_text == tr.thanks_for_joining:
        new_text = tr.coins_for_tasks
        new_markup = get_task_markup(tr)
    elif current_text == tr.click_to_join:
        new_text = tr.coins_for_tasks
        new_markup = get_task_markup(tr)
    else:
        new_text = tr.hello
        new_markup = tg.hello.get_hello_markup(tr)

    await callback_query.message.edit_text(
        text=new_text,
        reply_markup=new_markup
    )
    await callback_query.answer()


@all.dp.callback_query(is_check_subscription_callback)
async def on_check_subscription(callback_query: aiogram.types.CallbackQuery):
    assert isinstance(callback_query.message, aiogram.types.Message)
    assert callback_query.from_user
    assert callback_query.from_user.language_code
    assert callback_query.bot
    tr = get_tr(callback_query.from_user.language_code)
    try:
        member = await callback_query.bot.get_chat_member(
            f'@{core.config.env.channel_username}',
            callback_query.from_user.id,
        )
    except aiogram.exceptions.TelegramAPIError:
        await callback_query.answer('not subscribed')
        return
    main_back_button = aiogram.types.InlineKeyboardButton(
        text=tr.back,
        callback_data='main_back'
    )
    check_markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[main_back_button]]
    )
    if member.status in ['member', 'administrator', 'creator']:
        await callback_query.message.edit_text(
            text=tr.thanks_for_joining,
            reply_markup=check_markup,
        )
    else:
        await callback_query.message.edit_text(
            text='not subscribed',
            reply_markup=get_join_markup(tr)
        )
    await callback_query.answer()

