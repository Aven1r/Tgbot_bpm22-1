from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

### ADMIN PANEL ###

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to access the admin panel"""
    if (update.effective_user.id != 340175659) and (update.effective_user.id != 1044793628):
        reply_keyboard = [['Назад']]
        await update.message.reply_text(
            text="У вас нет доступа к этой команде (Как вы сюда попали?)",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )
        return 5

    reply_keyboard = [['ДЗ', 'Новости', 'Уведомления'],['Назад']]
    await update.message.reply_text(
        text="Вы в панели администратора. Пожалуйста, выберите команду\n\nДЗ - изменить домашнее задание\nНовости - отправить/удалить новость\nУведомление - @all как в вк",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return 5

### Admin panel: change homework ###

async def admin_homework(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to pick the class to change the homework"""
    reply_keyboard = [['МА', 'ПЭ', 'ДМ', 'ИГ', 'ФЗ'], ['Назад']]
    await update.message.reply_text(
        text="Выберите домашнее задание, которое нужно изменить",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )
    return 6