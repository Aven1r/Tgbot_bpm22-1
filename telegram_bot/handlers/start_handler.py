from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

start_message = """Привет!

Это Telegram Бот-Компаньон группы БПМ-22-1.

Здесь можно в удобном формате узнать домашнее задание, расписание, \
получить доступ к полезным ссылкам и контактам одногруппников.

Команды бота:

Группа - список студентов группы
Домашка - список домашних заданий
Ссылки - ссылки на полезные материалы и не только
Расписание - расписание пар
Другое - информация о боте и экспериментальные функции
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start function to show the main menu."""
    reply_keyboard = [["Группа", "Ссылки", "Другое"], ["Расписание", "Домашка"]]
    await update.message.reply_text(
        text=start_message,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, resize_keyboard=True
        ),
    )
    return 0