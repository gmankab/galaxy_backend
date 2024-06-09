import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, Mock
from aiogram import types
from tg.game import on_message, inline_keyboard

async def test_on_message_user_not_subscribed():
    mock_bot = AsyncMock()
    mock_bot.get_chat_member.return_value = types.ChatMember(status='left')
    mock_message = AsyncMock(spec=types.Message)
    mock_message.from_user = types.User(id=12345, is_bot=False, first_name="Test")
    mock_message.text = "Hello"
    mock_message.chat = types.Chat(id=1, type='private')
    mock_message.date = datetime.now()
    mock_message.bot = mock_bot
    mock_message.answer = AsyncMock()

    await on_message(mock_message)
    mock_message.answer.assert_called_with(
        text='Please subscribe to our channel to start the game.',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[[
                types.InlineKeyboardButton(
                    text='Subscribe',
                    url=f'https://t.me/foo'
                )
            ]]
        )
    )
    return 'on message user not subscribed'

async def test_on_message_user_subscribed():
    mock_bot = AsyncMock()
    mock_bot.get_chat_member.return_value = types.ChatMember(status='member')
    mock_message = AsyncMock(spec=types.Message)
    mock_message.from_user = types.User(id=67890, is_bot=False, first_name="Test")
    mock_message.text = "Hello"
    mock_message.chat = types.Chat(id=1, type='private')
    mock_message.date = datetime.now()
    mock_message.bot = mock_bot
    mock_message.answer = AsyncMock()

    await on_message(mock_message)
    mock_message.answer.assert_called_with(
        text='hello',
        reply_markup=inline_keyboard.markup
    )
    return 'on message user subscribed'

async def test_on_message_no_user():
    mock_message = AsyncMock(spec=types.Message)
    mock_message.from_user = None
    mock_message.answer = AsyncMock()

    await on_message(mock_message)
    mock_message.answer.assert_not_called()
    return 'test on message no user'

# Run tests
if __name__ == '__main__':
    print(asyncio.run(test_on_message_user_not_subscribed()))
    print(asyncio.run(test_on_message_user_subscribed()))
    print(asyncio.run(test_on_message_no_user()))
