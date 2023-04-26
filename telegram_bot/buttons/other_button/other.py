from telegram import ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram import Update

async def other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to show the schedule menu."""
    reply_keyboard = [["Дни рождения", "Гороскоп", "Профиль"], ['Назад']]
    if (update.effective_user.id == 340175659) or (update.effective_user.id == 1044793628):
        reply_keyboard = [["Дни рождения", "Гороскоп", "Профиль", "Админ"], ['Назад']]
    message = "Пожалуйста, выберите команду"
    await update.message.reply_text(
        text=message,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return 3