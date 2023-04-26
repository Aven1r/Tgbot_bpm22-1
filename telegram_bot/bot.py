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

from handlers.links_handler import links
from handlers.start_handler import start
from buttons.group import group
from buttons.other_button.birthdays import birthdays
from buttons.other_button.admin_panel import admin_panel
from buttons.schedule_button.schedule import schedule, today_tommorow_schedule, choose_weekday, chosen_day
from buttons.other_button.other import other
from buttons.other_button.horoscope import horoscope
from stuff import telegram_token


tracemalloc.start()


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

MAIN_MENU, SCHEDULE_MENU, CHOOSE_WEEKDAY = range(3)
OTHER_MENU, USER_MENU, ADMIN_PANEL = range(3, 6)
ADMIN_HOMEWORK, GROUP_MENU, HOMEWORK_MENU, LINKS_MENU = range(6, 10)
classes = ['МА', 'ПЭ', 'ДМ', 'ИГ', 'ФЗ']



async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to show user profile"""
    reply_keyboard = [['Назад']]
    await update.message.reply_text(
        text="To be implemented",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return USER_MENU

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
    return HOMEWORK_MENU

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
    return HOMEWORK_MENU

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
        keyboard = [[InlineKeyboardButton("Назад", callback_data="Назад к списку предметов")]]
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

async def start_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start function to show the main menu."""
    reply_keyboard = [["Группа", "Ссылки", "Другое"], ["Расписание", "Домашка"]]
    await update.message.reply_text(
        text="Выберите команду",
        reply_markup= (ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, resize_keyboard=True
        )),
    )
    return MAIN_MENU

# __main__
if __name__ == '__main__':
    application = ApplicationBuilder().token(telegram_token.TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        MAIN_MENU: [
            MessageHandler(filters.Regex('^Расписание$'), schedule),
            MessageHandler(filters.Regex('^Другое$'), other),
            MessageHandler(filters.Regex('^Группа$'), group.group),
            MessageHandler(filters.Regex('^Домашка$'), homework),
            MessageHandler(filters.Regex('^Ссылки$'), links),
        ],
        SCHEDULE_MENU: [
            MessageHandler(filters.Regex('^(Сегодня|Завтра)$'), today_tommorow_schedule),
            MessageHandler(filters.Regex('^Другие дни$'), choose_weekday),
            MessageHandler(filters.Regex('^Назад$'), start_again),
        ],
        CHOOSE_WEEKDAY: [
            CallbackQueryHandler(chosen_day, pattern="^" + '.+_.+' "$"),
            MessageHandler(filters.Regex('^Назад$'), schedule),
        ],
        OTHER_MENU: [
            MessageHandler(filters.Regex('^Назад$'), start_again),
            MessageHandler(filters.Regex('^Дни рождения$'), birthdays),
            MessageHandler(filters.Regex('^Гороскоп$'), horoscope.horoscope),
            MessageHandler(filters.Regex('^Профиль$'), profile),
            MessageHandler(filters.Regex('^Админ$'), admin_panel.admin),
        ],
        USER_MENU: [
            MessageHandler(filters.Regex('^Назад$'), other),
        ],
        ADMIN_PANEL: [
            MessageHandler(filters.Regex('^Назад$'), other),
            MessageHandler(filters.Regex('^ДЗ$'), admin_panel.admin_homework),
            # MessageHandler(filters.Regex('^Уведомления$'), notifications_admin),
            # MessageHandler(filters.Regex('^Новости$'), news_admin),
        ],
        ADMIN_HOMEWORK: [
            MessageHandler(filters.Regex('^Назад$'), start_again),
            # MessageHandler(filters.Regex('^(МА|ПЭ|ДМ|ИГ|ФЗ)$'), update_homework),
        ],
        GROUP_MENU: [
            CallbackQueryHandler(group.show_student, pattern="^" + 'person_' + ".+"),
            CallbackQueryHandler(group.next_page, pattern="^" + '->' + "$"),
            CallbackQueryHandler(group.prev_page, pattern="^" + '<-' + "$"),
            MessageHandler(filters.Regex('^Назад$'), start_again),
        ],
        HOMEWORK_MENU: [
            CallbackQueryHandler(show_homework, pattern="^" + 'class_' + ".+"),
            CallbackQueryHandler(homework_back, pattern="^" + 'Назад к списку предметов' + "$"),
            MessageHandler(filters.Regex('^Назад$'), start_again)
        ],
        LINKS_MENU: [
            MessageHandler(filters.Regex('^Назад$'), start_again)
        ],
    },
    fallbacks=[MessageHandler(filters.Regex('^Расписание$'), schedule),
            MessageHandler(filters.Regex('^Другое$'), other),
            MessageHandler(filters.Regex('^Группа$'), group.group),
            MessageHandler(filters.Regex('^Домашка$'), homework),
            MessageHandler(filters.Regex('^Ссылки$'), links),
            MessageHandler(filters.Regex('/start'), start),
            CommandHandler('set_homework', set_homework)]
    )

    application.add_handler(conv_handler)
    
    application.run_polling()
