import random
import time
import data_base.database as db
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from lexicon.lexicon import LEXICON_RU
from aiogram import F, Router
from buttons import (kb_buttons, kb_inline_buttons, kb_buttons_rating, kb_buttons_return, kb_buttons_start,
                     kb_buttons_yes_no_credits, kb_buttons_countries, kb_buttons_reset)

# Инициализируем роутер уровня модуля
router: Router = Router()

# Список ответов пользователей по отзывам
users_answers: dict = {}

# Список ответов пользователей по анкете
users_answers_form: dict = {}

# Список чисел для теста возраста
age = [str(i) for i in range(18, 65)]

# Список первичных заявок пользователя
users_request: dict[int, dict[str, str | int | bool]] = {}

# Создаем экземпляр класса MemoryStorage (инициализируем хранилище)
storage: MemoryStorage = MemoryStorage()

# Создаём класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    fill_form_country = State() # Состояние ожидания ввода страны
    fill_form_credits = State() # Состояние ожидания ввода инфы о кредитах
    fill_form_age = State() # Состояние ожидания ввода инфы о возрасте
    fill_company_name = State() # Состояние ожидания ввода названия компании
    fill_ask_approval = State() # Состояние ожидания ввода результата одобрения
    fill_ask_conditions = State() # Состояние ожидания ввода информации по условиям кредита
    fill_ask_speed = State() # Состояние ожидания ввода информации по скорости зачисления средств


# этот хэндлер срабатывает на команду /start
# отправляет в чат клавиатуру с кнопкой "Заполнить заявку"
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'],
                         reply_markup=kb_buttons_start)
    form_status: str = 'started'
    data = (message.from_user.id, message.from_user.username, message.from_user.first_name,
            message.from_user.language_code, form_status, message.date)
    await db.cmd_start_db(message.from_user.id, data)


# Этот хэндлер срабатывает на команду "Заполнить заявку"
# Добавляет информацию о пользователе с словарь
# Задаёт дефолтное состояние и переводит в состояние ожидания ввода страны из списка
@router.message(F.text == LEXICON_RU['fill_form_btn'], StateFilter(default_state))
async def fill_form_command(message: Message, state: FSMContext):
    if message.from_user.id not in users_answers_form:
        users_answers_form[message.from_user.id] = {'username': message.from_user.username,
                                                    'name': message.from_user.first_name,
                                                    'country': None,
                                                    'age': None,
                                                    }
        await message.answer(text='Выберите вашу страну из списка в меню\n',
                             reply_markup=kb_buttons_countries)
        form_status: str = 'country_choice'
        await db.cmd_change_status_to_country_choice(form_status, message.from_user.id)
        # задаем состояние для следующего фильтра
        await state.set_state(FSMFillForm.fill_form_country)
        print(users_answers_form[message.from_user.id])

    elif (message.from_user.id in users_answers_form and
          users_answers_form[message.from_user.id]['country'].lower() in LEXICON_RU['ru']):
        await message.answer(text=LEXICON_RU['Сообщение о повторе заявки'])
        time.sleep(1)
        await message.answer(text=LEXICON_RU['Предложение РФ'], reply_markup=kb_buttons,
                             disable_web_page_preview=True)
    elif (message.from_user.id in users_answers_form and
          users_answers_form[message.from_user.id]['country'].lower() in LEXICON_RU['kz']):
        await message.answer(text=LEXICON_RU['Сообщение о повторе заявки'])
        time.sleep(1)
        await message.answer(text=LEXICON_RU['Предложение КЗ'], reply_markup=kb_buttons,
                             disable_web_page_preview=True)

# хэндлер срабатывает при переходе из состояния выбора страны
@router.message(StateFilter(FSMFillForm.fill_form_country),
                F.text.lower().in_(LEXICON_RU['Страны']))
async def fill_form_command_country(message: Message, state: FSMContext):
    users_answers_form[message.from_user.id]['country'] = message.text
    print(users_answers_form[message.from_user.id])
    await message.answer(text='Напишите в чат сколько вам полных лет?',
                             reply_markup=kb_buttons_reset)
    form_status: str = 'age_input'
    await db.cmd_change_status_to_age_input(form_status, message.from_user.id)
    # задаем состояние для следующего фильтра
    await state.set_state(FSMFillForm.fill_form_age)

# хэндлер срабатывает при переходе из состояния выбора возраста
@router.message(StateFilter(FSMFillForm.fill_form_age),
                lambda x: x.text and x.text.isdigit() and 18 <= int(x.text) <= 65)
async def fill_form_command_age(message: Message, state: FSMContext):
    users_answers_form[message.from_user.id]['age'] = message.text
    await db.cmd_add_age_db(message.text, message.from_user.id)
    print(users_answers_form[message.from_user.id])
    await message.answer(text='Есть ли у вас другие кредиты?',
                         reply_markup=kb_buttons_yes_no_credits)
    form_status: str = 'having_credits'
    await db.cmd_change_status_to_having_credits(form_status, message.from_user.id)
    # задаем состояние для следующего фильтра
    await state.set_state(FSMFillForm.fill_form_credits)

# хэндлер переходит из состояния выбора ответа по поводу имеющихся кредитов
# очищает состояние
@router.message(StateFilter(FSMFillForm.fill_form_credits),
                F.text.lower().in_(LEXICON_RU['credit_answ_btn']))
async def offers_command(message: Message, state: FSMContext):
    try:
        await message.answer(text='3 ...', reply_markup=kb_buttons_reset)
        time.sleep(1)
        await message.answer(text='2 ...')
        time.sleep(1)
        await message.answer(text='1 ...')
        time.sleep(1)
        if users_answers_form[message.from_user.id]['country'].lower() in LEXICON_RU['ru']:
            await message.answer(text=LEXICON_RU['Предложение РФ'],
                                        reply_markup=kb_buttons, disable_web_page_preview=True)
        elif users_answers_form[message.from_user.id]['country'].lower() in LEXICON_RU['kz']:
            await message.answer(text=LEXICON_RU['Предложение КЗ'],
                                 reply_markup=kb_buttons, disable_web_page_preview=True)
        form_status: str = 'completed'
        await db.cmd_add_completed_status_form_db(form_status, message.from_user.id)
        await state.clear()
    except KeyError:
        print('Пользователь прервал обработку заявки нажав кнопку "Сбросить заполнение"')

# хэндлер срабатывает при получении сообщения о сбросе заявки
# очищает состояние
# имеет параметр ~ (тильда) для состояния default_state
# сработает на любое состояние, кроме дефолтного, что и важно для сброса состояния
@router.message(F.text == LEXICON_RU['reset_btn'], ~StateFilter(default_state))
async def reset_form_command(message: Message, state: FSMContext):
    del users_answers_form[message.from_user.id]
    await message.answer(text=LEXICON_RU['Сброс заявки'],
                                 reply_markup=kb_buttons_start)
    await state.clear()

# ответ на некорретное сообщения в состоянии ввода страны
@router.message(StateFilter(FSMFillForm.fill_form_country))
async def incorrect_answer_command_fill_form_country(message: Message):
    await message.answer(text='Вы ввели некорректное значение.\n'
                              'Воспользуйтесь меню для выбора страны.',
                         reply_markup=kb_buttons_countries)

# ответ на некорретное сообщения в состоянии ввода возраста
@router.message(StateFilter(FSMFillForm.fill_form_age))
async def incorrect_answer_command_fill_form_age(message: Message):
    await message.answer(text='Вы ввели некорректное значение\n'
                              'Допустимый возраст от 18 до 65 лет.\n',
                         reply_markup=kb_buttons_reset)

# ответ на некорретное сообщения в состоянии ввода информации по кредиту
@router.message(StateFilter(FSMFillForm.fill_form_credits))
async def incorrect_answer_command_fill_form_credits(message: Message):
    await message.answer(text='Вы ввели некорректное значение.\n'
                              'Выберете вариант из меню или ответьте да/нет',
                         reply_markup=kb_buttons_yes_no_credits)


# хэндлер срабатывающий на команду оставить отзыв
@router.message(F.text == LEXICON_RU['feedback_btn'], StateFilter(default_state))
async def feedback_command(message: Message, state: FSMContext):
    # если пользователь заполнил анкету на кредит и его нет в списке уже оставивших отзыв, то
    # он сможет оставить отзыв
    if (message.from_user.id not in users_answers and
            message.from_user.id in users_answers_form):
        await message.answer(text=LEXICON_RU['Отзыв о компании'],
                             reply_markup=kb_buttons_rating)
        # задаем состояние для следующего фильтра
        await state.set_state(FSMFillForm.fill_company_name)
        users_answers[message.from_user.id] = {'username': message.from_user.username,
                                               'name': message.from_user.first_name,
                                               'company_name': None,
                                               'approval': None,
                                               'get_money': None
                                               }
    elif message.from_user.id not in users_answers_form:
        await message.answer('Вы ещё не оставляли заявку на подбор предложений по кредиту')
    else:
        await message.answer('Вы уже оставили отзыв о компании')

# Этот хэндлер срабатывает на сообщения пользователя "Вернуться в меню из состояния отзыва"
@router.message(F.text == LEXICON_RU['return_btn'], ~StateFilter(default_state))
async def return_to_menu_command_from_feedback_state(message: Message, state: FSMContext):
    del users_answers[message.from_user.id]
    await message.answer('Вы вернулись в меню',
                         reply_markup=kb_buttons)
    await state.clear()

# хэндлер сработает на название компании, ожидает ввод текста, перейдёт из состояния default
@router.message(StateFilter(FSMFillForm.fill_company_name), F.text)
async def feedback_company_insert(message: Message, state: FSMContext):
    users_answers[message.from_user.id]['company_name'] = message.text
    await message.answer('Одобрили ли вам займ ? (ответьте да/нет)',
                             reply_markup=kb_buttons_return)
    await state.set_state(FSMFillForm.fill_ask_approval)

# хэндлер сработает на ответ да / нет, переходит из состояния одобрения займа
@router.message(StateFilter(FSMFillForm.fill_ask_approval), F.text.lower().in_(['да', 'нет']))
async def feedback_answer_conditions_command(message: Message, state: FSMContext):
    users_answers[message.from_user.id]['approval'] = message.text
    await message.answer(text='Довольны ли вы условиями? (ответьте да/нет)',
                             reply_markup=kb_buttons_return)
    await state.set_state(FSMFillForm.fill_ask_conditions)

# хэндлер сработает на ответ да / нет, переходит из состояния информаиция об условиях
@router.message(StateFilter(FSMFillForm.fill_ask_conditions), F.text.lower().in_(['да', 'нет']))
async def feedback_answer_approval_command(message: Message, state: FSMContext):
    await message.answer(text='Вы быстро получили деньги на карту? (ответьте да/нет)',
                             reply_markup=kb_buttons_return)
    await state.set_state(FSMFillForm.fill_ask_speed)

# хэндлер сработает на ответ да / нет, переходит из состояния информации о получении средств
@router.message(StateFilter(FSMFillForm.fill_ask_speed), F.text.lower().in_(['да', 'нет']))
async def feedback_answer_speed_command(message: Message, state: FSMContext):
    users_answers[message.from_user.id]['get_money'] = message.text
    await message.answer(text='Спасибо за ваш отзыв!', reply_markup=kb_buttons)
    await state.clear()

# Этот хэндлер срабатывает на сообщения пользователя "Вернуться в меню"
@router.message(F.text == LEXICON_RU['return_btn'], )
async def return_to_menu_command_no_state(message: Message):
    await message.answer('Вы вернулись в меню',
                         reply_markup=kb_buttons)

# некорректный ввод названия компании для отзыва
@router.message(StateFilter(FSMFillForm.fill_company_name))
async def feedback_incorrect_name_command(message: Message):
    await message.answer(text='Вы ввели некорректный ответ.\n'
                              'Пожалуйста, напишите название компании.\n'
                              'Вводить можно только буквы и цифры')

# некорректный ввод для вопроса по отзыву
@router.message(StateFilter(FSMFillForm.fill_ask_approval))
async def feedback_incorrect_approval_command(message: Message):
    await message.answer(text='Вы ввели некорректный ответ.\n'
                              'Пожалуйста, ответьте да/нет')

# некорректный ввод для вопроса по отзыву
@router.message(StateFilter(FSMFillForm.fill_ask_conditions))
async def feedback_incorrect_conditions_command(message: Message):
    await message.answer(text='Вы ввели некорректный ответ.\n'
                              'Пожалуйста, ответьте да/нет')

# некорректный ввод для вопроса по отзыву
@router.message(StateFilter(FSMFillForm.fill_ask_speed))
async def feedback_incorrect_speed_command(message: Message):
    await message.answer(text='Вы ввели некорректный ответ.\n'
                              'Пожалуйста, ответьте да/нет')


# Этот хэндлер срабатывает на сообщения пользователя "Рейтинг МФО"
@router.message(F.text == LEXICON_RU['rating_btn'])
async def rating_command(message: Message):
    if (message.from_user.id in users_answers_form and
          users_answers_form[message.from_user.id]['country'].lower() in LEXICON_RU['ru']):
        await message.answer(text=LEXICON_RU['Рейтинг МФО РФ'],
                            reply_markup=kb_buttons_rating, disable_web_page_preview=True)
    elif (message.from_user.id in users_answers_form and
          users_answers_form[message.from_user.id]['country'].lower() in LEXICON_RU['kz']):
        await message.answer(text=LEXICON_RU['Рейтинг МФО КЗ'],
                            reply_markup=kb_buttons_rating, disable_web_page_preview=True)

# Этот хэндлер срабатывает на сообщения пользователя "Банкротство"
@router.message(F.text == LEXICON_RU['bankrot_btn'])
async def bankrot_command(message: Message):
    await message.answer(text=LEXICON_RU['Банкротство'],
                         reply_markup=kb_buttons)

# Этот хэндлер срабатывает на сообщения пользователя "Помощь"
@router.message(F.text == LEXICON_RU['help_btn'])
async def help_command(message: Message):
    await message.answer(text=LEXICON_RU['Помощь'],
                         reply_markup=kb_buttons)

# Этот хэндлер срабатывает на сообщения пользователя "О боте"
@router.message(F.text == LEXICON_RU['about_btn'])
async def otzivy_command(message: Message):
    await message.answer(text=LEXICON_RU['О боте'],
                         reply_markup=kb_buttons)
# Информация об отзывах
@router.message(F.text == LEXICON_RU['otzivy_btn'])
async def otzivy_command(message: Message):
    await message.answer(text=LEXICON_RU['Отзывы'],
                         reply_markup=kb_inline_buttons)

# Этот хэндлер срабатывает на сообщение пользователя "Партнеры"
@router.message(F.text == LEXICON_RU['agreement_btn'])
async def aggrement_command(message: Message):
    if (message.from_user.id in users_answers_form and
        users_answers_form[message.from_user.id]['country'].lower() in LEXICON_RU['ru']):
        await message.answer(text=LEXICON_RU['Партнеры РФ'],
                         reply_markup=kb_buttons)
    elif (message.from_user.id in users_answers_form and
          users_answers_form[message.from_user.id]['country'].lower() in LEXICON_RU['kz']):
        await message.answer(text=LEXICON_RU['Партнеры КЗ'],
                             reply_markup=kb_buttons)