from core.common import all
import core.config
import models.db
import aiogram.types
import aiogram.utils
import aiogram


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
    await models.db.User.get_or_create(
        tg_id=msg.from_user.id,
        coins=0,
    )
    await msg.answer(
        text='hello',
        reply_markup=inline_keyboard.markup,
    )

