from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from aiogram import Router
from buttons import kb_buttons, kb_buttons_start

# Инициализируем роутер уровня модуля
router: Router = Router()

# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команды "/start"
@router.message()
async def answer_user_message(message: Message):
    try:
        await message.reply(f'Пожалуйста, используйте кнопки бота для отправки сообщений. \n'
                             f'Отправленное вами сообщение не поддерживается.',
                             reply_markup=kb_buttons_start)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'], reply_markup=kb_buttons_start)
