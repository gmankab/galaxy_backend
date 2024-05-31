from core.common import all
import aiogram.types
import aiogram.utils
import aiogram
import core.config


class inline_keyboard:
    button = aiogram.types.InlineKeyboardButton(
        text='start game',
        web_app=aiogram.types.WebAppInfo(
            url=core.config.web.url,
        ),
    )
    markup = aiogram.types.InlineKeyboardMarkup(
        inline_keyboard=[[button]]
    )


@all.dp.message()
async def on_message(
    msg: aiogram.types.Message,
) -> None:
    await msg.answer(
        text='hello',
        reply_markup=inline_keyboard.markup,
    )


def my_pass():
    pass

