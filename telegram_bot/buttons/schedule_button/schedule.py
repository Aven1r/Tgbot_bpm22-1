from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import datetime
import sqlite3


days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт']
weeks = ['even', 'odd']
english_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
russian_days = ['Понедельник', 'Вторник', 'Среду', 'Четверг', 'Пятницу']

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to show the schedule menu."""
    reply_keyboard = [["Сегодня", "Завтра", "Другие дни"], ['Назад']]
    message = "Пожалуйста, выберите день"
    await update.message.reply_text(
        text=message,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, resize_keyboard=True
        ),
    )
    return 1

async def today_tommorow_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to show the timetable for the day."""
    user_text = update.message.text
    buttons = ["Сегодня", "Завтра"]
    day = weekday(update.message.date, buttons.index(user_text))
    week_desc = weeks[(update.message.date.isocalendar().week) % 2]
    message_text = schedule_query(day, week_desc)
    await update.message.reply_text(
        message_text)
    return 1

async def choose_weekday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to choose the day of the week to show"""
    text = "Выберите день недели\nВерхняя строка - для верхней недели, Нижняя - для нижней"
    keyboard = []
    for week in weeks:
        temp_keyboard = []
        for day in days:
            temp_keyboard.append(InlineKeyboardButton(day, callback_data=f'{day}_{week}'))
        keyboard.append(temp_keyboard)
    await update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))
    return 2

async def chosen_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to show the timetable for the chosen day."""
    user_text = update.callback_query.data
    user_text = user_text.split("_")
    day = english_days[(days.index(user_text[0]))]
    week = user_text[1]
    message_text = schedule_query(day, week)
    await update.callback_query.message.edit_text(message_text)
    return 1
    
def weekday(datetime, index):
    """Function identify user's message weekday."""
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
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

    day = russian_days[english_days.index(weekday)]

    text = f"Расписание на {day} \n \n"
    if week == 'even':
        text += "Верхняя неделя \n \n"
    else:
        text += "Нижняя неделя: \n \n"
    if not rows:
        text += "Занятий нет"
        return text
    for row in rows:
        text += f"{row[3]} пара ({row[4]} - {row[5]}) \n"
        text += f"{row[6]} ({row[7]}) \n{row[8]}\n{row[9]} \n \n"
    return text