import asyncio
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, PhotoSize
from aiogram.filters import Command, StateFilter
from lexicon.lexicon_admin import LEXICON_ADMIN
from math import *
import datetime as dt
from aiogram import F, Router
from buttons import (kb_buttons_admin_cancel, kb_buttons_admin_panel, kb_buttons_start,
                     kb_buttons_admin_newsletter_menu, kb_buttons_users_category,
                     kb_buttons_admin_run_newsletter_menu, kb_buttons_admin_reset)
from lexicon.lexicon_pswd import PASSWORD
import data_base.database as db

# Загружаем конфиг в переменную config
config: Config = load_config()

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
dp: Dispatcher = Dispatcher()


# Инициализируем роутер уровня модуля
router: Router = Router()

# Создаем экземпляр класса MemoryStorage (инициализируем хранилище)
storage: MemoryStorage = MemoryStorage()

# лимит на вход для пользователя
user_login_data: list = []

# сообщение пользователя для рассылки
user_message_for_sending: dict = {}


# Создаём класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMAdmin(StatesGroup):
    password_input = State() # Состояние ожидания ввода пароля
    newsletter_message_input = State() # Состояние ожидания ввода сообщения для рассылки
    send_photo_message_input = State() # Состояние ожидания добавления фото для рассылки
    select_users_category = State() # Состояние ожидания выбора категории для рассылки
    category_confirmation = State() # Состояние ожидания подтверждения выбора категории для рассылки
    start_newsletter = State() # Состояние ожидания запуска рассылки


# хэндлер срабатывает на команду /admin
# задается дефолтное состояние и затем переводится в состояние ввода пароля
@router.message(Command(commands='admin'), StateFilter(default_state))
async def admin_call_cmd(message: Message, state: FSMContext):
    # проверяем авторизовывался ли пользователь ранее
    # если нет, то добавляем его с список пользователей запросивших авторизацию
    if message.from_user.id not in user_login_data:
        user_login_data.append(message.from_user.id)
        await message.answer(text=LEXICON_ADMIN['Admin_login_message'],
                             reply_markup=kb_buttons_admin_cancel)
        await state.set_state(FSMAdmin.password_input)
    # если пользователь авторизовывался ранее
    # то сообщаем ему, что он уже авторизован
    elif message.from_user.id in user_login_data:
        await message.answer(text=LEXICON_ADMIN['just_authorized'],
                             reply_markup=kb_buttons_admin_panel)


# хэндлер срабатывает на ввод правильного пароля
# если пароль верный, то авторизовывает пользователя и очищает состояние
@router.message(StateFilter(FSMAdmin.password_input), F.text == PASSWORD)
async def password_input_cmd(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['login_successful_message'],
                         reply_markup=kb_buttons_admin_panel)
    await state.clear()


# хэндлер срабатывает при получении команды об отмене авторизации в админ-панель
# очищает состояние
@router.message(F.text == LEXICON_ADMIN['cancel_btn'], ~StateFilter(default_state))
async def cancel_login_cmd(message: Message, state: FSMContext):
    user_login_data.remove(message.from_user.id)
    await message.answer(text=LEXICON_ADMIN['Cancel_admin_panel_message'],
                         reply_markup=kb_buttons_start)
    await state.clear()

# хэндлер срабатывает на ввод некорректного пароля
@router.message(StateFilter(FSMAdmin.password_input))
async def incorrect_password(message: Message):
            await message.answer(text=LEXICON_ADMIN['incorrect_pass'],
                                 reply_markup=kb_buttons_admin_cancel)

# хэндлер срабатывает на команду Аналитика
@router.message(F.text == LEXICON_ADMIN['analytics_btn'])
async def analitycs_cmd(message: Message):
    # все пользователи
    all_users = await db.cmd_select_all_users()
    new_users_today = await db.cmd_select_users_for_today()
    # заполнившие анкеты
    users_form_completed = await db.cmd_select_completed_form_users()
    users_form_completed_today = await db.cmd_select_completed_form_users_today()
    # только запустили бота
    users_started_bot = await db.cmd_select_start_bot_users()
    users_started_bot_today = await db.cmd_select_start_bot_users_today()
    # выбор страны
    users_country_choice = await db.cmd_select_users_country_choice()
    users_country_choice_today = await (db.cmd_select_users_country_choice_today())
    # ввод возраста
    users_age_choice = await db.cmd_select_users_age_choice()
    users_age_choice_today = await db.cmd_select_users_age_choice_today()
    # наличие кредитов
    users_having_credits = await db.cmd_select_users_having_credits()
    users_having_credits_today = await db.cmd_select_users_having_credits_today()
    # статистика по странам
    users_from_ru = await db.cmd_select_ru_users()
    users_from_kz = await db.cmd_select_kz_users()
    if message.from_user.id in user_login_data:
        await message.answer(text=f'Статистика на {dt.date.today()}\n'
                 '\n'
                 f'<b>Общее кол-во пользователей бота: </b>{all_users} \n'
                 f'<b>Новых пользователей Сегодня: </b>{new_users_today}\n'
                 '\n'
                 f'<b>Заполнили анкету:</b>\n'
                 f'> Всего: {users_form_completed} — {floor((users_form_completed/all_users)*100)}%\n'
                 f'> Сегодня: {users_form_completed_today} —'
                 f' {floor((users_form_completed_today/new_users_today)*100)}%\n'
                 '\n'
                 f'<b>Остановились после запуска:</b>\n'
                 f'> Всего: {users_started_bot} — {floor((users_started_bot/all_users)*100)}%\n'
                 f'> Сегодня: {users_started_bot_today} — {floor((users_started_bot_today/new_users_today)*100)}%\n'
                 '\n'
                 f'<b>Остановились на выборе страны:</b>\n'
                 f'> Всего: {users_country_choice} — {floor((users_country_choice/all_users)*100)}%\n'
                 f'> Сегодня: {users_country_choice_today} —'
                 f' {floor((users_country_choice_today/new_users_today)*100)}%\n'
                 '\n'
                 f'<b>Остановились на вводе возраста:</b>\n'
                 f'> Всего: {users_age_choice} — {floor((users_age_choice/all_users)*100)}%\n'
                 f'> Сегодня: {users_age_choice_today} — {floor((users_age_choice_today/new_users_today)*100)}%\n'
                 '\n'
                 f'<b>Остановились на вопросе о наличии кредитов:</b>\n'
                 f'> Всего: {users_having_credits} — {floor((users_having_credits/all_users)*100)}%\n'
                 f'> Сегодня: {users_having_credits_today} — '
                 f'{floor((users_having_credits_today/new_users_today)*100)}%\n'
                 '\n'
                 f'<b>Пользователи из России:</b> '
                 f'{users_from_ru} — {floor((users_from_ru/all_users)*100)}%\n'
                 f'<b>Пользователи из Казахстана:</b> '
                 f'{users_from_kz} — {ceil((users_from_kz/all_users)*100)}%\n',
                             reply_markup=kb_buttons_admin_panel)
    else:
        await message.answer(text=LEXICON_ADMIN['not_login_and_newsletter'],
                             reply_markup=kb_buttons_start)

# хэндлер срабатывает на команду Создать рассылку
@router.message(F.text == LEXICON_ADMIN['newsletter_btn'], StateFilter(default_state))
async def newsletter_cmd(message: Message, state: FSMContext):
    if message.from_user.id in user_login_data:
        await message.answer(text=LEXICON_ADMIN['newsletter_start_message'],
                             reply_markup=kb_buttons_admin_reset)
        await state.set_state(FSMAdmin.newsletter_message_input)
    else:
        await message.answer(text=LEXICON_ADMIN['not_login_and_newsletter'],
                             reply_markup=kb_buttons_start)


# хэндлер срабатывает на команду Сбросить и очищает состояние,
# возрвращает в панель управления
@router.message(F.text.lower() == LEXICON_ADMIN['reset'], ~StateFilter(default_state))
async def reset_newletter_cmd(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['reset_neswletter_message'],
                          reply_markup=kb_buttons_admin_panel)
    await state.clear()

# хэндлер срабатывает при переходе из состояния Создать рассылку
# в состояние ввода сообщения для рассылки
@router.message(StateFilter(FSMAdmin.newsletter_message_input), F.text)
async def message_to_newsletter_cmd(message: Message, state: FSMContext):
    try:
        await state.update_data(message_text=message.text)
        await message.answer(text=LEXICON_ADMIN['newsletter_photo_message'],
                             reply_markup=kb_buttons_admin_reset)
        await state.set_state(FSMAdmin.send_photo_message_input)
    except TypeError:
        await message.reply(text=LEXICON_ADMIN['type_msg_not_maintain'])

# хэндлер срабатывает на добавление фото
@router.message(StateFilter(FSMAdmin.send_photo_message_input),
                F.photo[-1].as_('largest_photo'))
async def photo_to_newsletter_cmd(message: Message, state: FSMContext, largest_photo: PhotoSize):
    await state.update_data(photo_unique_id=largest_photo.file_unique_id,
                            photo_id=largest_photo.file_id)
    user_message_for_sending[message.from_user.id] = await state.get_data()
    await message.answer(text=LEXICON_ADMIN['newsletter_check_message'],
                         reply_markup=kb_buttons_admin_newsletter_menu)
    await state.clear()


# хэндлер срабатывает на команду Посмотреть сообщение
@router.message(F.text == LEXICON_ADMIN['show_message_btn'])
async def show_message_for_newsletter_cmd(message: Message, state: FSMContext):
    #if message.from_user.id in user_message_for_sending:
    await message.answer_photo(photo=user_message_for_sending[message.from_user.id]['photo_id'],
                                caption=user_message_for_sending[message.from_user.id]['message_text'],
                                reply_markup=kb_buttons_admin_newsletter_menu)
    # else:
    #     await message.answer(text=LEXICON_ADMIN['unfilled_message'], reply_markup=kb_buttons_admin_panel)

# хэндлер срабатывает на команду Запустить рассылку
@router.message(F.text.lower() == LEXICON_ADMIN['start_newsletter_from_menu'], StateFilter(default_state))
async def select_user_category_cmd(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['select_users_for_newsletter'],
                         reply_markup=kb_buttons_users_category)
    await state.set_state(FSMAdmin.category_confirmation)


# хэндлер срабатывает при переходе из состояния выбора категории
# в состояние подтверждения запуска рассылки
@router.message(StateFilter(FSMAdmin.category_confirmation),
                F.text.lower().in_(LEXICON_ADMIN['category_btns']))
async def users_category_confirmation_cmd(message: Message, state: FSMContext):
    if message.from_user.id in user_message_for_sending:
        user_message_for_sending[message.from_user.id]['category'] = message.text.lower()
        await message.answer(text=LEXICON_ADMIN['category_confirmation_message'],
                             reply_markup=kb_buttons_admin_run_newsletter_menu)
        await state.set_state(FSMAdmin.start_newsletter)
    else:
        await message.answer(text=LEXICON_ADMIN['category_error_message'])

# хэндлер срабатывает на команду Отправить сообщение и запускает рассылку по категориям
@router.message(StateFilter(FSMAdmin.start_newsletter),
                F.text.lower() == LEXICON_ADMIN['run_newsletter'])
async def start_newsletter_cmd(message: Message,  state: FSMContext):
    await message.answer(text=LEXICON_ADMIN['newsletter_waiting'], reply_markup=kb_buttons_admin_panel)
    try:
        if user_message_for_sending[message.from_user.id]['category'] == 'все пользователи':
            category: str = 'все пользователи'
            users_list: list = await db.cmd_select_users_with_status(category)
            for el in users_list:
                await bot.send_photo(chat_id=el, photo=user_message_for_sending[message.from_user.id]['photo_id'],
                                     caption=user_message_for_sending[message.from_user.id]['message_text'])
            await message.answer(text=LEXICON_ADMIN['newsletter_completed'], reply_markup=kb_buttons_admin_panel)
            await state.clear()
            del user_message_for_sending[message.from_user.id]
        elif user_message_for_sending[message.from_user.id]['category'] == 'заполнившие анкету':
            category: str = 'заполнившие анкету'
            users_list: list = await db.cmd_select_users_with_status(category)
            for el in users_list:
                await bot.send_photo(chat_id=el, photo=user_message_for_sending[message.from_user.id]['photo_id'],
                                     caption=user_message_for_sending[message.from_user.id]['message_text'])
            await message.answer(text=LEXICON_ADMIN['newsletter_completed'], reply_markup=kb_buttons_admin_panel)
            await state.clear()
            del user_message_for_sending[message.from_user.id]
        elif user_message_for_sending[message.from_user.id]['category'] == 'пользователи на этапе - запустили бота':
            category: str = 'пользователи на этапе - запустили бота'
            users_list: list = await db.cmd_select_users_with_status(category)
            for el in users_list:
                await bot.send_photo(chat_id=el, photo=user_message_for_sending[message.from_user.id]['photo_id'],
                                     caption=user_message_for_sending[message.from_user.id]['message_text'])
            await message.answer(text=LEXICON_ADMIN['newsletter_completed'], reply_markup=kb_buttons_admin_panel)
            await state.clear()
            del user_message_for_sending[message.from_user.id]
        elif user_message_for_sending[message.from_user.id]['category'] == 'пользователи на этапе - выбор страны':
            category: str = 'пользователи на этапе - выбор страны'
            users_list: list = await db.cmd_select_users_with_status(category)
            for el in users_list:
                await bot.send_photo(chat_id=el, photo=user_message_for_sending[message.from_user.id]['photo_id'],
                                     caption=user_message_for_sending[message.from_user.id]['message_text'])
            await message.answer(text=LEXICON_ADMIN['newsletter_completed'], reply_markup=kb_buttons_admin_panel)
            await state.clear()
            del user_message_for_sending[message.from_user.id]
        elif user_message_for_sending[message.from_user.id]['category'] == 'пользователи на этапе - ввод возраста':
            category: str = 'пользователи на этапе - ввод возраста'
            users_list: list = await db.cmd_select_users_with_status(category)
            for el in users_list:
                await bot.send_photo(chat_id=el, photo=user_message_for_sending[message.from_user.id]['photo_id'],
                                     caption=user_message_for_sending[message.from_user.id]['message_text'])
            await message.answer(text=LEXICON_ADMIN['newsletter_completed'], reply_markup=kb_buttons_admin_panel)
            await state.clear()
            del user_message_for_sending[message.from_user.id]
        elif user_message_for_sending[message.from_user.id]['category'] == 'пользователи на этапе - наличие кредитов':
            category: str = 'пользователи на этапе - наличие кредитов'
            users_list: list = await db.cmd_select_users_with_status(category)
            for el in users_list:
                await bot.send_photo(chat_id=el, photo=user_message_for_sending[message.from_user.id]['photo_id'],
                                     caption=user_message_for_sending[message.from_user.id]['message_text'])
            await message.answer(text=LEXICON_ADMIN['newsletter_completed'], reply_markup=kb_buttons_admin_panel)
            await state.clear()
            del user_message_for_sending[message.from_user.id]
        elif user_message_for_sending[message.from_user.id]['category'] == 'пользователи из россии':
            category: str = 'пользователи из россии'
            users_list: list = await db.cmd_select_users_with_status(category)
            for el in users_list:
                await bot.send_photo(chat_id=el, photo=user_message_for_sending[message.from_user.id]['photo_id'],
                                     caption=user_message_for_sending[message.from_user.id]['message_text'])
            await message.answer(text=LEXICON_ADMIN['newsletter_completed'], reply_markup=kb_buttons_admin_panel)
            await state.clear()
            del user_message_for_sending[message.from_user.id]
        elif user_message_for_sending[message.from_user.id]['category'] == 'пользователи из казахстана':
            category: str = 'пользователи из казахстана'
            users_list: list = await db.cmd_select_users_with_status(category)
            for el in users_list:
                await bot.send_photo(chat_id=el, photo=user_message_for_sending[message.from_user.id]['photo_id'],
                                     caption=user_message_for_sending[message.from_user.id]['message_text'])
            await message.answer(text=LEXICON_ADMIN['newsletter_completed'], reply_markup=kb_buttons_admin_panel)
            await state.clear()
            del user_message_for_sending[message.from_user.id]
    except Exception as e:
        print(e)
        await message.answer(text=LEXICON_ADMIN['newsletter_error'], reply_markup=kb_buttons_admin_panel)


# хэндлер срабатывает на некорректное сообщение на этапе выбора категории
@router.message(StateFilter(FSMAdmin.select_users_category))
async def incorrect_message_select_category(message: Message):
    await message.answer(text=LEXICON_ADMIN['incorrect_message'],
                         reply_markup=kb_buttons_admin_newsletter_menu)


# хэндлер срабатывает на некорректное сообщение на этапе подтверждения категории
@router.message(StateFilter(FSMAdmin.category_confirmation))
async def incorrect_message_category_confirmation(message: Message):
    await message.answer(text=LEXICON_ADMIN['incorrect_message'],
                         reply_markup=kb_buttons_users_category)

# хэндлер срабатывает на некорректное сообщение на этапе отправки сообщения в рассылку
@router.message(StateFilter(FSMAdmin.start_newsletter))
async def incorrect_message_start_newsletter(message: Message):
    await message.answer(text=LEXICON_ADMIN['incorrect_message'],
                         reply_markup=kb_buttons_admin_run_newsletter_menu)


# хэндлер срабатывает на некорректное сообщение на этапе отправки текста для рассылки
@router.message(StateFilter(FSMAdmin.newsletter_message_input))
async def incorrect_message_text(message: Message):
    await message.answer(text=LEXICON_ADMIN['incorrect_text_message'],
                         reply_markup=kb_buttons_admin_reset)


# хэндлер срабатывает на некорректное сообщение на этапе отправки фото для рассылки
@router.message(StateFilter(FSMAdmin.send_photo_message_input))
async def incorrect_message_photo(message: Message):
    await message.answer(text=LEXICON_ADMIN['incorrect_photo'],
                         reply_markup=kb_buttons_admin_reset)

# хэндлер срабатывает на команду Вернуться в меню
@router.message(F.text == LEXICON_ADMIN['return_to_main_menu_btn'])
async def return_to_main_menu_cmd(message: Message):
    await message.answer(text=LEXICON_ADMIN['return_menu_message'],
                         reply_markup=kb_buttons_admin_panel)

# хэндлер срабатывает на команду Выйти
@router.message(F.text == LEXICON_ADMIN['exit_btn'])
async def exit_from_admin_menu_cmd(message: Message):
    user_login_data.remove(message.from_user.id)
    await message.answer(text=LEXICON_ADMIN['exit_message'],
                         reply_markup=kb_buttons_start)
    if message.from_user.id in user_message_for_sending:
        del user_message_for_sending[message.from_user.id]