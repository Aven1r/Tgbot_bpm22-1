import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, ConversationHandler
import messages
import telegram_token
import sqlite3
import tracemalloc


tracemalloc.start()



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["/Group", "/Homework", "/Links", "/Schedule"]]

    # user = update.message.from_user
    # logger.info("User %s started the conversation.", user.first_name)
    await update.message.reply_text(
        text=messages.start,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    await context.bot.send_message(chat_id=update.effective_chat.id)

async def stuff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text="Ссылки на полезные материалы", 
        reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Google drive', url=messages.google)],
        [InlineKeyboardButton(text='Vk group', url=messages.vk)],
        ]))

START_ROUTES, END_ROUTES = range(2)

def data(page, limit):
    conn = sqlite3.connect('/Users/avenir/vscode/Python/Tgbot_bpm22-1/telegram_bot/users.db')
    cmd = conn.cursor()
    query = f"SELECT * FROM people LIMIT {limit} OFFSET {limit * page}"
    cmd.execute(query)
    rows = cmd.fetchall()
    conn.close()
    keyboard = []
    for row in rows:
        keyboard.append([InlineKeyboardButton(text=row[1], callback_data='person')])
        print('im here')
    return keyboard


async def group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = data(0, 10)
    keyboard.append([InlineKeyboardButton("->", callback_data='->2')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("List of people: page 1", reply_markup=reply_markup)
    return START_ROUTES

async def start_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = data(0, 10)
    keyboard.append([InlineKeyboardButton("->", callback_data='->2')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("List of people: page 1", reply_markup=reply_markup)
    return END_ROUTES

async def next_page_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = data(1, 10)
    keyboard.append([InlineKeyboardButton("->", callback_data='->3'), InlineKeyboardButton("<-", callback_data='1<-')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("List of people: page 2", reply_markup=reply_markup)
    return START_ROUTES

async def next_page_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = data(2, 10)
    keyboard.append([InlineKeyboardButton("<-", callback_data='2<-')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("List of people: page 3", reply_markup=reply_markup)
    return START_ROUTES

async def prev_page_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = data(0, 10)
    keyboard.append([InlineKeyboardButton("->", callback_data='->2')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("List of people: page 1", reply_markup=reply_markup)
    return START_ROUTES

async def prev_page_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = data(1, 10)
    keyboard.append([InlineKeyboardButton("->", callback_data='->3'), InlineKeyboardButton("<-", callback_data='1<-')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("List of people: page 2", reply_markup=reply_markup)
    return START_ROUTES



if __name__ == '__main__':
    application = ApplicationBuilder().token(telegram_token.TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    stuff_handler = CommandHandler('links', stuff)
    application.add_handler(stuff_handler)
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('group', group)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(next_page_2, pattern="^"+ '->2' + "$"),
                CallbackQueryHandler(next_page_3, pattern="^"+ '->3' + "$"),
                CallbackQueryHandler(prev_page_1, pattern="^"+ '1<-' + "$"),
                CallbackQueryHandler(prev_page_2, pattern="^"+ '2<-' + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_again, pattern="^" + 'person' + "$")
            ],
        },
        fallbacks=[CommandHandler("group", group)],
    )
    application.add_handler(conv_handler)
    
    application.run_polling()
