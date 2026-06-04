import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8748664569:AAFaXfDaLC8UQAloZi36I6ncX6PiOKF8LaE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """Здравствуйте! 👋 Я ИИ-помощник по подбору новостроек.

Вот 7 скрытых угроз, которые нужно проверить перед покупкой:

1️⃣ Тонкие стены — стукните по стене. Глухой звук = хорошо, звонкий = слышимость 100%.
2️⃣ Окна на север — риск плесени и сырости.
3️⃣ Кривые стены под отделкой — через год плитка отвалится.
4️⃣ Школа на карте может оказаться ТЦ — проверяйте ПЗЗ участка.
5️⃣ Парковок не хватит даже с подземным паркингом.
6️⃣ Трещины фасада скрываются за вентфасадом.
7️⃣ Земля может быть в залоге у банка.

Не хотите рисковать? Выберите, что вам важнее:"""
    
    keyboard = [
        [InlineKeyboardButton("Инвестиции", callback_data='invest')],
        [InlineKeyboardButton("Для себя", callback_data='for_life')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'invest':
        text = """Отлично! Для инвестиций важны ликвидность и рост цены.

Какой бюджет рассматриваете?

1 — До 7 млн
2 — 7-12 млн
3 — Свыше 12 млн

Напишите цифру, и я подберу варианты."""
    else:
        text = """Понял! Для себя главное — комфорт и надежность.

Какой район или метро вам интересно? И какой бюджет?

Напишите в свободной форме, и я подберу варианты."""
    
    await query.message.reply_text(text)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == '__main__':
    main()
