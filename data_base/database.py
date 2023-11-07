import sqlite3 as sq
from sqlite3 import Cursor
import datetime as dt

# создаем подключение к бд
connection = sq.connect('data_base/skoringBot.db')
# connection.row_factory = sq.Row
# для выполнения выражений SQL и получения данных из БД, необходимо создать курсор
cursor = connection.cursor()


# добавление таблицы Users в БД, если таблица ещё не создана
async def db_start():
    cursor.execute('CREATE TABLE IF NOT EXISTS Users('
                   'Id INTEGER PRIMARY KEY AUTOINCREMENT, '
                   'user_tg_id INTEGER, '
                   'username TEXT, '
                   'name TEXT, '
                   'age INTEGER, '
                   'country TEXT, '
                   'form_status TEXT, '
                   'joining_date timestamp)')
    connection.commit()


# добавление пользователя в БД при вводе команды /start
async def cmd_start_db(user_id, data):
    user: Cursor = cursor.execute('SELECT * FROM Users WHERE user_tg_id = ?', (user_id,)).fetchone()
    if not user:
        cursor.execute('INSERT INTO Users (user_tg_id, username, name, country, form_status, joining_date) '
                       'VALUES (?, ?, ?, ?, ?, ?)', data)
        connection.commit()


# добавление возраста в БД после ввода возраста
async def cmd_add_age_db(age, user_id):
    cursor.execute('UPDATE Users SET age = ? WHERE user_tg_id = ?', (age, user_id))
    connection.commit()


# добавление статуса пользователю - Completed, если он завершил заполнение анкеты
async def cmd_add_completed_status_form_db(status, user_id):
    cursor.execute('UPDATE Users SET form_status = ? WHERE user_tg_id = ?', (status, user_id))
    connection.commit()


# изменить статус пользователя на "country_choice"
async def cmd_change_status_to_country_choice(status, user_id):
    cursor.execute('UPDATE Users SET form_status = ? WHERE user_tg_id = ?', (status, user_id))
    connection.commit()


# изменить статус пользователя на "age_input"
async def cmd_change_status_to_age_input(status, user_id):
    cursor.execute('UPDATE Users SET form_status = ? WHERE user_tg_id = ?', (status, user_id))
    connection.commit()


# изменить статус пользователя на "having_credits"
async def cmd_change_status_to_having_credits(status, user_id):
    cursor.execute('UPDATE Users SET form_status = ? WHERE user_tg_id = ?', (status, user_id))
    connection.commit()


# получить информацию об общем кол-ве пользователей
async def cmd_select_all_users():
        rows_all_count_users: list = cursor.execute('SELECT count(*) as count FROM Users').fetchone()
        return rows_all_count_users[0]


# получить информацию об общем кол-ве пользователей за сегодня
async def cmd_select_users_for_today():
    # Вычисляем дату, представляющую текущую дату минус один день
    time_now = dt.date.today()
    rows_today_count_users: list = cursor.execute('SELECT count(*) as count FROM Users WHERE joining_date >= ?',
                                                  (time_now,)
                                                  ).fetchone()
    return rows_today_count_users[0]


# получить информацию о кол-ве пользователей, который заполнили анкету польностью
async def cmd_select_completed_form_users():
    rows_completed_form_users: list = cursor.execute("SELECT count(*) as count FROM Users "
                                                     "WHERE form_status = 'completed'").fetchone()
    return rows_completed_form_users[0]


# получить информацию о кол-ве пользователей, которые остановились после команды "/start"
async def cmd_select_start_bot_users():
    rows_start_bot_users: list = cursor.execute("SELECT count(*) as count FROM Users "
                                                "WHERE form_status = 'started'").fetchone()
    return rows_start_bot_users[0]


# получить информацию о кол-ве пользователей, которые остановились на выборе страны
async def cmd_select_users_country_choice():
    row_country_choice: list = cursor.execute("SELECT count(*) as count FROM Users "
                                              "WHERE form_status = 'country_choice'").fetchone()
    return row_country_choice[0]


# получить информацию о кол-ве пользователей, который остановились на выборе возраста
async def cmd_select_users_age_choice():
    row_age_choice: list = cursor.execute("SELECT count(*) as count FROM Users "
                                          "WHERE form_status = 'age_input'").fetchone()
    return row_age_choice[0]


async def cmd_select_users_having_credits():
    row_having_choice: list = cursor.execute("SELECT count(*) as count FROM Users "
                                             "WHERE form_status = 'having_credits'").fetchone()
    return row_having_choice[0]


# получить информацию о кол-ве пользователей из России
async def cmd_select_ru_users():
    row_ru_users: list = cursor.execute("SELECT count(*) as count FROM Users "
                                        "WHERE country IN ('ru', 'uk')").fetchone()
    return row_ru_users[0]


# получить информацию о кол-ве пользователей из Казахстана
async def cmd_select_kz_users():
    row_kz_users: list = cursor.execute("SELECT count(*) as count FROM Users "
                                        "WHERE country = 'kz'").fetchone()
    return row_kz_users[0]


# получить никнэймы пользователей для рассылки по статусам
async def cmd_select_users_with_status(category):
    try:
        if category == 'все пользователи':
            users = cursor.execute('SELECT user_tg_id FROM Users WHERE user_tg_id NOT NULL').fetchall()
            clear_users: list = []
            for el_list in users:
                for el in el_list:
                    clear_users.append(el)
            return clear_users
        elif category == 'заполнившие анкету':
            status: str = 'completed'
            users = cursor.execute('SELECT user_tg_id FROM Users WHERE form_status = ? AND user_tg_id NOT NULL',
                                   (status,)).fetchall()
            clear_users: list = []
            for el_list in users:
                for el in el_list:
                    clear_users.append(el)
            return clear_users
        elif category == 'пользователи на этапе - запустили бота':
            status: str = 'started'
            users = cursor.execute('SELECT user_tg_id FROM Users WHERE form_status = ? AND user_tg_id NOT NULL',
                                   (status,)).fetchall()
            clear_users: list = []
            for el_list in users:
                for el in el_list:
                    clear_users.append(el)
            return clear_users
        elif category == 'пользователи на этапе - выбор страны':
            status: str = 'country_choice'
            users = cursor.execute('SELECT user_tg_id FROM Users WHERE form_status = ? AND user_tg_id NOT NULL',
                                   (status,)).fetchall()
            clear_users: list = []
            for el_list in users:
                for el in el_list:
                    clear_users.append(el)
            return clear_users
        elif category == 'пользователи на этапе - ввод возраста':
            status: str ='age_input'
            users = cursor.execute('SELECT user_tg_id FROM Users WHERE form_status = ? AND user_tg_id NOT NULL',
                                   (status,)).fetchall()
            clear_users: list = []
            for el_list in users:
                for el in el_list:
                    clear_users.append(el)
            return clear_users
        elif category == 'пользователи на этапе - наличие кредитов':
            status: str = 'having_credits'
            users = cursor.execute('SELECT user_tg_id FROM Users WHERE form_status = ? AND user_tg_id NOT NULL',
                                   (status,)).fetchall()
            clear_users: list = []
            for el_list in users:
                for el in el_list:
                    clear_users.append(el)
            return clear_users
        elif category == 'пользователи из россии':
            country_ru: str = 'ru'
            country_uk: str = 'uk'
            users = cursor.execute('SELECT user_tg_id FROM Users WHERE country IN (?, ?) AND user_tg_id NOT NULL',
                                   (country_ru, country_uk)).fetchall()
            clear_users: list = []
            for el_list in users:
                for el in el_list:
                    clear_users.append(el)
            return clear_users
        elif category == 'пользователи из казахстана':
            country: str = 'kz'
            users = cursor.execute('SELECT user_tg_id FROM Users WHERE country = ? AND user_tg_id NOT NULL',
                                   (country,)).fetchall()
            clear_users: list = []
            for el_list in users:
                for el in el_list:
                    clear_users.append(el)
            return clear_users
    except Exception as e:
        print(e)
