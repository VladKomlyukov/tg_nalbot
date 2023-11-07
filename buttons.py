from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


# Инициализируем объект билдера
kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_start: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_rating: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_return: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_yes_no_credits: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_countries: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_reset: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_agreement: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Объекты билдера для админки
kb_builder_admin_cancel: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_admin_reset: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_admin_panel: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_admin_newsletter_menu: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_admin_users_category: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
kb_builder_admin_run_newsletter_menu: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Инициализируем объект билдера для инлайн клавиатуры
kb_inline_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

# Создаем объекты кнопок
btn_set_app: KeyboardButton = KeyboardButton(text='Заполнить анкету 📋')
btn_otzivy: KeyboardButton = KeyboardButton(text='Отзывы 🗣')
btn_rating: KeyboardButton = KeyboardButton(text='Рейтинг МФО 📊')
btn_bankrotstvo: KeyboardButton = KeyboardButton(text='Банкротство 🆘')
btn_help: KeyboardButton = KeyboardButton(text='Помощь ❔')
btn_about: KeyboardButton = KeyboardButton(text='О боте 🤖')
btn_feedback: KeyboardButton = KeyboardButton(text='Оценить компанию 💬')
btn_return: KeyboardButton = KeyboardButton(text='Вернуться в меню ◀️')
btn_yes_credit: KeyboardButton = KeyboardButton(text='Да, есть ☑️')
btn_no_credit: KeyboardButton = KeyboardButton(text='Кредитов нет ❌')
btn_russia: KeyboardButton = KeyboardButton(text='Россия 🇷🇺')
btn_kazah: KeyboardButton = KeyboardButton(text='Казахстан 🇰🇿')
btn_reset: KeyboardButton = KeyboardButton(text='Сбросить заполнение ✖️')
btn_agreement: KeyboardButton = KeyboardButton(text='Партнеры')

# Кнопки для админки
btn_admin_cancel: KeyboardButton = KeyboardButton(text='Отменить')
btn_admin_analitycs: KeyboardButton = KeyboardButton(text='Аналитика')
btn_admin_newsletter: KeyboardButton = KeyboardButton(text='Создать рассылку')
btn_admin_show_message: KeyboardButton = KeyboardButton(text='Посмотреть сообщение')
btn_admin_reset: KeyboardButton = KeyboardButton(text='Сбросить')
btn_admin_all_users: KeyboardButton = KeyboardButton(text='Все пользователи')
btn_admin_users_fill_form: KeyboardButton = KeyboardButton(text='Заполнившие анкету')
btn_admin_users_started: KeyboardButton = KeyboardButton(text='Пользователи на этапе - Запустили бота')
btn_admin_users_select_country: KeyboardButton = KeyboardButton(text='Пользователи на этапе - Выбор страны')
btn_admin_users_age_input: KeyboardButton = KeyboardButton(text='Пользователи на этапе - Ввод возраста')
btn_admin_users_credits_having: KeyboardButton = KeyboardButton(text='Пользователи на этапе - Наличие кредитов')
btn_admin_users_from_ru: KeyboardButton = KeyboardButton(text='Пользователи из России')
btn_admin_users_from_kz: KeyboardButton = KeyboardButton(text='Пользователи из Казахстана')
btn_admin_start_newsletter: KeyboardButton = KeyboardButton(text='Запустить рассылку')
btn_admin_run_newsletter: KeyboardButton = KeyboardButton(text='Отправить сообщение')
btn_admin_return_to_newsletter_menu: KeyboardButton = KeyboardButton(text='Вернуться в меню')
btn_admin_exit: KeyboardButton = KeyboardButton(text='Выйти')

# Создаем объект инлайн-кнопки
btn_video_otzyv: InlineKeyboardButton = InlineKeyboardButton(text='ОТЗЫВЫ',
                                                            url='https://t.me/otziv_clients')
btn_chat: InlineKeyboardButton = InlineKeyboardButton(text='ЧАТ',
                                                      url='https://t.me/OOOnalchat')

# Добавляем кнопки в билдер методом row
kb_builder.row(btn_set_app, btn_otzivy, btn_rating, btn_bankrotstvo, btn_help, btn_about, btn_agreement,
               width=2)
kb_builder_rating.row(btn_feedback, btn_return, width=1)
kb_builder_return.row(btn_return, width=1)
kb_builder_start.row(btn_set_app, width=1)
kb_builder_yes_no_credits.row(btn_yes_credit, btn_no_credit, btn_reset, width=2)
kb_builder_countries.row(btn_russia, btn_kazah, btn_reset, width=2)
kb_builder_reset.row(btn_reset, width=1)
kb_builder_admin_cancel.row(btn_admin_cancel, width=1)
kb_builder_admin_reset.row(btn_admin_reset, width=1)
kb_builder_admin_panel.row(btn_admin_analitycs, btn_admin_newsletter, btn_admin_exit, width=2)
kb_builder_admin_newsletter_menu.row(btn_admin_show_message, btn_admin_start_newsletter,
                                     btn_admin_return_to_newsletter_menu, width=2)
kb_builder_admin_users_category.row(btn_admin_all_users, btn_admin_users_fill_form, btn_admin_users_started,
                                    btn_admin_users_select_country, btn_admin_users_age_input,
                                    btn_admin_users_credits_having, btn_admin_users_from_ru, btn_admin_users_from_kz,
                                    btn_admin_reset, width= 2)
kb_builder_admin_run_newsletter_menu.row(btn_admin_run_newsletter,
                                           btn_admin_reset, width=2)


# Добавляем инлайн кнопки в билдер методом row
kb_inline_builder.row(btn_video_otzyv, btn_chat, width=2)

# Создаем клавиатуру из добавленных в билдер кнопок
kb_buttons: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
kb_buttons_rating: ReplyKeyboardMarkup = kb_builder_rating.as_markup(resize_keyboard=True)
kb_buttons_return: ReplyKeyboardMarkup = kb_builder_return.as_markup(resize_keyboard=True)
kb_buttons_start: ReplyKeyboardMarkup = kb_builder_start.as_markup(resize_keyboard=True)
kb_buttons_yes_no_credits: ReplyKeyboardMarkup = kb_builder_yes_no_credits.as_markup(resize_keyboard=True)
kb_buttons_countries: ReplyKeyboardMarkup = kb_builder_countries.as_markup(resize_keyboard=True)
kb_buttons_reset: ReplyKeyboardMarkup = kb_builder_reset.as_markup(resize_keyboard=True)
kb_buttons_admin_cancel: ReplyKeyboardMarkup = kb_builder_admin_cancel.as_markup(resize_keyboard=True)
kb_buttons_admin_reset: ReplyKeyboardMarkup = kb_builder_admin_reset.as_markup(resize_keyboard=True)
kb_buttons_admin_panel: ReplyKeyboardMarkup = kb_builder_admin_panel.as_markup(resize_keyboard=True)
kb_buttons_admin_newsletter_menu: ReplyKeyboardMarkup = kb_builder_admin_newsletter_menu.as_markup(resize_keyboard=True)
kb_buttons_users_category: ReplyKeyboardMarkup = kb_builder_admin_users_category.as_markup(resize_keyboard=True)
kb_buttons_admin_run_newsletter_menu: ReplyKeyboardMarkup = (
    kb_builder_admin_run_newsletter_menu.as_markup(resize_keyboard=True))

# Создаем объект инлайн-клавиаутуры
kb_inline_buttons: InlineKeyboardMarkup = kb_inline_builder.as_markup(resize_keyboard=True)

