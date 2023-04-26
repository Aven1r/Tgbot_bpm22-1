from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces = range(12)
marks = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
marks_rus = ['Овен', 'Телец', 'Близнецы', 'Рак', "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]

async def horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to get horoscope"""
    keyboard = []
    for i in range(6):
        keyboard.append([InlineKeyboardButton(text=marks_rus[i*2], callback_data=marks[i*2]), InlineKeyboardButton(text=marks_rus[i*2+1], callback_data=marks[i*2+1])])
    await update.message.reply_text(
        "Выберите знак зодиака",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return 4