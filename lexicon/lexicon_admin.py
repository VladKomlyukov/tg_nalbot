import data_base.database as db
import asyncio
from math import *
import datetime as dt



# все пользователи
all_users = asyncio.run(db.cmd_select_all_users())
new_users_today = asyncio.run(db.cmd_select_users_for_today())
# заполнившие анкеты
users_form_completed = asyncio.run(db.cmd_select_completed_form_users())
users_form_completed_today = asyncio.run(db.cmd_select_completed_form_users_today())
# только запустили бота
users_started_bot = asyncio.run(db.cmd_select_start_bot_users())
users_started_bot_today = asyncio.run((db.cmd_select_start_bot_users_today()))
# выбор страны
users_country_choice = asyncio.run(db.cmd_select_users_country_choice())
users_country_choice_today = asyncio.run((db.cmd_select_users_country_choice_today()))
# ввод возраста
users_age_choice = asyncio.run(db.cmd_select_users_age_choice())
users_age_choice_today = asyncio.run((db.cmd_select_users_age_choice_today()))
# наличие кредитов
users_having_credits = asyncio.run(db.cmd_select_users_having_credits())
users_having_credits_today = asyncio.run((db.cmd_select_users_having_credits_today()))
# статистика по странам
users_from_ru = asyncio.run(db.cmd_select_ru_users())
users_from_kz = asyncio.run(db.cmd_select_kz_users())




LEXICON_ADMIN: dict[str, str | list] = {
    'cancel_btn': 'Отменить',
    'analytics_btn': 'Аналитика',
    'newsletter_btn': 'Создать рассылку',
    'exit_btn': 'Выйти',
    'show_message_btn': 'Посмотреть сообщение',
    'return_to_main_menu_btn': 'Вернуться в меню',
    'Admin_login_message': 'Для входа в панель администратора введите пароль\n',
    'login_successful_message': 'Вы вошли в панель администратора',
    'Cancel_admin_panel_message': 'Вы отменили вход в панель администратора',
    'just_authorized': 'Вы уже вошли в админ панель',
    'incorrect_pass': 'Вы ввели некорректный пароль\n'
                      'Попробуйте ввести правильный пароль\n',
    'not_login_and_newsletter': 'Для использования данной команды необходимо войти в панель администратора.\n',
    'exit_message': 'Вы вышли из панели администратора',
    'return_menu_message': 'Вы вернулись в меню',
    'unfilled_message': 'Вы ещё не создавали сообщение для рассылки.\n'
                        '\n'
                        'Нажмите кнопку - "Создать рассылку" для создания сообщения рассылки.',
    'analytics': f'Статистика на {dt.date.today()}\n'
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
    'newsletter_start_message': 'ШАГ 1. Введите ТЕКСТ сообщения для рассылки, БЕЗ ФОТО',
    'newsletter_photo_message': 'ШАГ 2. Добавьте только ФОТО для рассылки, БЕЗ ТЕКСТА',
    'newsletter_check_message': 'Фото добавлено к сообщению для рассылки.\n'
                                '\n'
                                'Чтобы посмотреть созданное сообщение, нажмите кнопку — "Посмотреть сообщение"',
    'type_msg_not_maintain': 'Данный тип сообщения не поддерживается в Telegram.',
    'message_exists': 'Вы уже создали сообщение для рассылки\n'
                      '\n'
                      '⬇️⬇️⬇️',
    'incorrect_message': 'Вы ввели некорректное сообщение.\n'
                         'Пожалуйста, используйте меню бота для отправки сообщений\n',
    'incorrect_text_message': 'Вы отправили не только текст.\n'
                       '\n'
                       'Отправьте только ТЕКСТ, чтобы прикрепить его к сообщению.',
    'incorrect_photo': 'Вы отправили что-то непохожее на фото.\n'
                       '\n'
                       'Отправьте только ФОТО, чтобы прикрепить его к сообщению.',
    'edit_message': 'изменить сообщение',
    'start_newsletter_from_menu': 'запустить рассылку',
    'run_newsletter': 'отправить сообщение',
    'reset': 'сбросить',
    'back_to_categories': 'Вернуться к категориям',
    'reset_neswletter_message': 'Создание рассылки сброшено, вы вернулись в панель управления',
    'select_users_for_newsletter': 'Выберите категорию пользователей для рассылки. \n'
                                   '\n'
                                   'Можно сделать рассылку по пользователям на определенных этапах, на которых они '
                                   'остановились при использовании бота\n',
    'category_btns': ['все пользователи', 'заполнившие анкету', 'пользователи на этапе - запустили бота',
                      'пользователи на этапе - выбор страны', 'пользователи на этапе - ввод возраста',
                      'пользователи на этапе - наличие кредитов', 'пользователи из россии',
                      'пользователи из казахстана'],
    'category_confirmation_message': 'Категория успешно выбрана. \n'
                                     '\n'
                                     'Отправить сообщение получателям?',
    'newsletter_completed': 'Сообщение отправлено получателям.\n'
                            '\n'
                            'Рассылка завершена.',
    'category_error_message': 'Перезайдите в панель администратора - /admin\n'
                              'Нельзя выбрать категорию без созданного сообщения для расссылки.',
    'newsletter_waiting': 'Рассылка запущена. \n'
                          '\n'
                          'Ожидайте окончания рассылки в сообщении от бота.\n',
    'newsletter_error': 'Во время рассылки произошла ошибка. \n'
                        '\n'
                        'Рассылка не завершена.'
}