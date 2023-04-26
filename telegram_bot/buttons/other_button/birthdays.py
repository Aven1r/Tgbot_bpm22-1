from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import sqlite3
import datetime


async def birthdays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to get birthdays"""
    reply_keyboard = [['Назад']]
    telegram = update.message.from_user.username
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/users2.db')
    cmd = conn.cursor()
    now = datetime.datetime.now()

    # Execute the query to retrieve the data
    query = f"SELECT name, birthday_text FROM Users WHERE birthday LIKE '__-{now.month:02d}' ORDER BY birthday ASC"
    cmd.execute(query)
    rows = cmd.fetchall()
    conn.close()

    text = "Именинники в этом месяце:\n"
    for row in rows:
        text += f"\n{row[0]}: {row[1]}"
    
    await update.message.reply_text(
        text=text, reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return 4