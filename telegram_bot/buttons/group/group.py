from telegram import Update,  InlineKeyboardButton, InlineKeyboardMarkup,  ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
import sqlite3
import math


def data(offset, limit):
    """Function to retrieve data about people from the SQLite database for group button."""
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/users2.db')
    cmd = conn.cursor()
    query = f"SELECT * FROM Users LIMIT {limit} OFFSET {offset}"
    cmd.execute(query)
    rows = cmd.fetchall()
    conn.close()

    keyboard = []
    for row in rows:
        id = row[0]
        keyboard.append([InlineKeyboardButton(text=row[1], callback_data=f'person_{id}')])

    return keyboard

async def show_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    id = query.data.split('_')[1]
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/users2.db')
    cmd = conn.cursor()
    sql_query = f"SELECT Users.id, Users.name, users.birthday_text, users_info.telegram, users_info.github FROM Users JOIN users_info ON Users.id = users_info.user_id WHERE Users.id = {id}"
    cmd.execute(sql_query)
    rows = cmd.fetchall()
    conn.close()
    id = rows[0][0]
    name = rows[0][1]
    birthday = rows[0][2]
    telegram = rows[0][3]
    github = rows[0][4]
    person_text = f"{name}: \nНомер в группе: {id}\nДень рождения: {birthday}\nTelegram: {telegram}\nGithub: {github}"
    keyboard = []
    keyboard.append([InlineKeyboardButton("Назад", callback_data='<-')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(person_text, reply_markup=reply_markup)
    return 7

def generate_pagination_buttons(current_page, total_pages):
    buttons = []
    if current_page > 1:
        buttons.append(InlineKeyboardButton("<-", callback_data="<-"))
    if current_page < total_pages:
        buttons.append(InlineKeyboardButton("->", callback_data=f"->"))
    return buttons

async def group(update: Update, context: CallbackContext) -> int:
    """Function to show the first page of the group list."""
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/users2.db')
    cmd = conn.cursor()
    cmd.execute("SELECT COUNT(*) FROM Users")
    total_students = cmd.fetchone()[0]
    conn.close()

    current_page = 1
    limit = 10
    offset = 0

    keyboard = data(offset, limit)
    pagination_buttons = generate_pagination_buttons(current_page, math.ceil(total_students/limit))
    if pagination_buttons:
        keyboard.append(pagination_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_markup_with_back = ReplyKeyboardMarkup(
        [['Назад']],
        one_time_keyboard=False,
        resize_keyboard=True
    )
    await update.message.reply_text(
        "Список студентов группы БПМ-22-1",
        reply_markup=reply_markup_with_back
    )
    message = await update.message.reply_text(
        f"Страница {current_page}",
        reply_markup=reply_markup
    )
    context.user_data['current_page'] = current_page
    context.user_data['total_pages'] = math.ceil(total_students/limit)
    return 7

async def next_page(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    current_page = context.user_data.get('current_page', 1)
    total_pages = context.user_data.get('total_pages', 1)
    limit = 10
    offset = (current_page * limit)

    keyboard = data(offset, limit)
    pagination_buttons = generate_pagination_buttons(current_page+1, total_pages)
    if pagination_buttons:
        keyboard.append(pagination_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"Страница {current_page+1}",
        reply_markup=reply_markup
    )
    context.user_data['current_page'] = current_page+1
    return 7

async def prev_page(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    current_page = context.user_data.get('current_page', 1)
    total_pages = context.user_data.get('total_pages', 1)
    limit = 10
    offset = ((current_page - 2) * limit)

    keyboard = data(offset, limit)
    pagination_buttons = generate_pagination_buttons(current_page-1, total_pages)
    if pagination_buttons:
        keyboard.append(pagination_buttons)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"Страница {current_page-1}",
        reply_markup=reply_markup
    )
    context.user_data['current_page'] = current_page-1
    return 7
