import logging
import sqlite3
import tracemalloc
import datetime
import sys

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
sys.path.insert(1, '/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/stuff')
sys.path.insert(2, '/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/db')

import telegram_token
import messages


tracemalloc.start()


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

START_ROUTES, END_ROUTES = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start function to show the main menu."""
    reply_keyboard = [["/Group", "/Homework", "/Links", "/Schedule", "/Other"]]
    await update.message.reply_text(
        text=messages.start,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

async def stuff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to show useful links."""
    await update.message.reply_text(
        text="Ссылки на полезные материалы",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Google drive', url=messages.google)],
            [InlineKeyboardButton(text='Vk group', url=messages.vk)],
            [InlineKeyboardButton(text='LMS', url=messages.lms)],
            [InlineKeyboardButton(text='Microsoft teams', url=messages.teams)]
        ])
    )

async def other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to show the other functions menu."""
    await update.message.reply_text("To be implemented")

# /Group Button
def data(page, limit):
    """Function to retrieve data about people from the SQLite database for group button."""
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/users.db')
    cmd = conn.cursor()
    query = f"SELECT * FROM people LIMIT {limit} OFFSET {limit * page}"
    cmd.execute(query)
    rows = cmd.fetchall()
    conn.close()

    keyboard = []
    for row in rows:
        id = row[0]
        keyboard.append([InlineKeyboardButton(text=row[1], callback_data=f'person_{id}')])

    return keyboard

async def group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Function to show the first page of the group list."""
    keyboard = data(0, 10)
    keyboard.append([InlineKeyboardButton("->", callback_data='->2')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Страница 1", reply_markup=reply_markup)
    return START_ROUTES

async def start_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    id = query.data.split('_')[1]
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/users.db')
    cmd = conn.cursor()
    sql_query = f"SELECT * FROM people WHERE people.id = {id}"
    cmd.execute(sql_query)
    rows = cmd.fetchall()
    conn.close()
    id = rows[0][0]
    name = rows[0][1]
    telegram = rows[0][2]
    # github = rows[0][3]
    # birhday = rows[0][4]
    # person_text = f"{name}: \nНомер в группе: {id}\nTelegram: {telegram}\nGithub: {github}\nBirhday: {birhday}"
    keyboard = []
    keyboard.append([InlineKeyboardButton("Назад", callback_data='1<-')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"{name}: \nTelegram: {telegram}", reply_markup=reply_markup)
    return START_ROUTES

async def next_page_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = data(1, 10)
    keyboard.append([InlineKeyboardButton("->", callback_data='->3'), InlineKeyboardButton("<-", callback_data='1<-')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Страница 2", reply_markup=reply_markup)
    return START_ROUTES

async def next_page_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = data(2, 10)
    keyboard.append([InlineKeyboardButton("<-", callback_data='2<-')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Страница 3", reply_markup=reply_markup)
    return START_ROUTES

async def prev_page_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = data(0, 10)
    keyboard.append([InlineKeyboardButton("->", callback_data='->2')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Страница 1", reply_markup=reply_markup)
    return START_ROUTES

async def prev_page_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = data(1, 10)
    keyboard.append([InlineKeyboardButton("->", callback_data='->3'), InlineKeyboardButton("<-", callback_data='1<-')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Страница 2", reply_markup=reply_markup)
    return START_ROUTES

# /Homework Button
async def homework(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = ['Математический анализ', 'Персональная эффективность', 'Дискретная математика', 'Инженерная графика', 'Физика']
    keyboard = []
    id = 0
    for button in buttons:
        id += 1
        keyboard.append([InlineKeyboardButton(button, callback_data=f'class_{id}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите предмет:", reply_markup=reply_markup)
    return START_ROUTES

async def homework_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    buttons = ['Математический анализ', 'Персональная эффективность', 'Дискретная математика', 'Инженерная графика', 'Физика']
    keyboard = []
    id = 0
    for button in buttons:
        id += 1
        keyboard.append([InlineKeyboardButton(button, callback_data=f'class_{id}')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Выберите предмет:", reply_markup=reply_markup)
    return START_ROUTES

def get_homework_text(class_id):
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/homework.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM homework WHERE id = {class_id}")
    result = c.fetchone()
    conn.close()
    return result[2]

async def show_homework(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    id = query.data.split('_')[1]
    homework_text = get_homework_text(id)
    if homework_text:
        keyboard = [[InlineKeyboardButton("Назад", callback_data="Назад")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.edit_text(homework_text, reply_markup=reply_markup, parse_mode='markdown')

def set_homework_text(text, id):
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/homework.db')
    c = conn.cursor()
    c.execute("UPDATE homework SET text_hw = ? WHERE id = ?", (text, id,))
    conn.commit()
    conn.close()

def get_class_index(message):
    my_classes = ['МА', 'ПЭ', 'ДМ', 'ИГ', 'ФЗ']
    for i, class_name in enumerate(my_classes):
        if class_name in message:
            print( i+1 ) 
            return (i + 1)

async def set_homework(update: Update, context: CallbackContext):
    """Function to set homework for particular class."""
    if (update.effective_user.id == 340175659) or (update.effective_user.id == 1044793628):
        new_text = update.message.text.replace("/set_homework ", "")
        class_id = get_class_index(new_text)
        my_classes = ['МА', 'ПЭ', 'ДМ', 'ИГ', 'ФЗ']
        for classes in my_classes:
            new_text = new_text.replace(classes, "", 1)
        set_homework_text(new_text, class_id)
        await update.message.reply_text("Homework updated successfully.")
    else:
        await update.message.reply_text("You are not authorized to use this command.")

# /Schedule Button
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to show the schedule menu."""
    reply_keyboard = [["Сегодня", "Завтра", "Расписание"]]
    message = "Пожалуйста, выберите неделю"
    await update.message.reply_text(
        text=message,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, resize_keyboard=True
        ),
    )

    return 0

async def choose_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to show the timetable for the day."""
    user_text = update.message.text
    buttons = ["Сегодня", "Завтра"]
    week = ["even", "odd"]
    if user_text not in buttons:
        await update.message.reply_text(
            "Пожалуйста, попробуйте снова"
        )
    else:
        day = weekday(update.message.date, buttons.index(user_text))
        week_desc = week[(update.message.date.isocalendar().week) % 2]
        message_text = schedule_query(day, week_desc)
        await update.message.reply_text(
            message_text
        )

def weekday(datetime, index):
    """Function identify user's message weekday."""
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    day = weekdays[datetime.weekday() + index]
    return day

def schedule_query(weekday, week):
    """Function to receive data about classes on particular days of the week."""
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/schedule.db')
    cmd = conn.cursor()
    query = f"SELECT * FROM classes WHERE week = '{week}' AND day = '{weekday}' ORDER BY position"
    cmd.execute(query)
    rows = cmd.fetchall()
    conn.close()

    text = f"Расписание на {weekday} \n \n"
    if week == 1:
        text += "Нижняя неделя \n \n"
    else:
        text += "Верхняя неделя: \n \n"
    for row in rows:
        text += f"{row[3]} пара ({row[4]} - {row[5]}) \n"
        text += f"{row[6]} ({row[7]}) \n {row[8]} \n {row[9]} \n \n"
    return text

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("To be implemented")


# __main__
if __name__ == '__main__':
    application = ApplicationBuilder().token(telegram_token.TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    stuff_handler = CommandHandler('links', stuff)
    application.add_handler(stuff_handler)
    
    group_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('group', group)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(next_page_2, pattern="^"+ '->2' + "$"),
                CallbackQueryHandler(next_page_3, pattern="^"+ '->3' + "$"),
                CallbackQueryHandler(prev_page_1, pattern="^"+ '1<-' + "$"),
                CallbackQueryHandler(prev_page_2, pattern="^"+ '2<-' + "$"),
                CallbackQueryHandler(start_again, pattern="^" + 'person_' + ".+")
            ],
        },
        fallbacks=[CommandHandler("group", group)],
    )
    application.add_handler(group_conv_handler)

    hw_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('homework', homework)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(show_homework, pattern="^" + 'class_' + ".+"),
                CallbackQueryHandler(homework_back, pattern="^" + 'Назад' + "$")
            ],
        },
        fallbacks=[CommandHandler("homework", homework)],
    )
    application.add_handler(hw_conv_handler)

    set_hw_handler = CommandHandler('set_homework', set_homework)
    application.add_handler(set_hw_handler)

    schedule_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("schedule", schedule)],
        states={
            0: [MessageHandler(filters.ALL, choose_day)],
        },
        fallbacks=[CommandHandler("schedule", schedule)],
        )
    application.add_handler(schedule_conv_handler)
    
    other_handler = CommandHandler('other', other)
    application.add_handler(other_handler)
    
    application.run_polling()
