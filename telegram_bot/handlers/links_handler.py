from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from stuff import messages



async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    return 9