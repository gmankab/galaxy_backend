from core.common import all, tg
import core.config
import models.db
import aiogram.types
import aiogram.utils
import aiogram

require_channel_subscription: str = core.config.env.channel_username

class inline_keyboard:
    button = aiogram.types.InlineKeyboardButton(
        text='start game',
        web_app=aiogram.types.WebAppInfo(
            url=core.config.env.game_url,
        ),
    )
    markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[button]]
    )

@all.dp.message()
async def on_message(
    msg: aiogram.types.Message,
) -> None:
    if not msg.from_user:
        return

    try:
        user_status = await msg.bot.get_chat_member(
            chat_id=require_channel_subscription,
            user_id=msg.from_user.id
        )

        if user_status.status not in ['member', 'administrator', 'creator']:
            await msg.answer(
                text='Please subscribe to our channel to start the game.',
                reply_markup=aiogram.types.InlineKeyboardMarkup(
                    inline_keyboard=[[
                        aiogram.types.InlineKeyboardButton(
                            text='Subscribe',
                            url=f'https://t.me/{require_channel_subscription.lstrip("@")}'
                        )
                    ]]
                )
            )
            return
    except aiogram.exceptions.TelegramBadRequest as e:
        await msg.answer(f"Error: {str(e)}")
        return

    await models.db.User.get_or_create(
        tg_id=msg.from_user.id,
        coins=0,
    )
    await msg.answer(
        text='hello',
        reply_markup=inline_keyboard.markup,
    )
