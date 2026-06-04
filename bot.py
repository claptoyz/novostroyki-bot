import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8748664569:AAGJvSmjZ8HG66Xoy-Xg1A0QhnyLCTlSlt8"

async def send_main_menu(message):
    text = """ <b>Добро пожаловать в ИИ-помощник по подбору новостроек!</b>

Я помогу вам выбрать надежную квартиру без скрытых угроз.

<b>Что я умею:</b>
✅ Подберу проверенные ЖК под ваш бюджет
✅ Покажу скрытые угрозы новостроек
✅ Связжу с экспертом для бесплатной консультации

Выберите, что вам важно:"""
    
    keyboard = [
        [InlineKeyboardButton("💰 Инвестиции", callback_data='invest')],
        [InlineKeyboardButton(" Для себя", callback_data='for_life')],
        [InlineKeyboardButton("📋 Получить чек-лист", callback_data='checklist')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_main_menu(update.message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """<b>Команды бота:</b>
/start - Начать работу с ботом
/help - Показать это меню
/contact - Связаться с экспертом"""
    await update.message.reply_text(text, parse_mode='HTML')

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """📞 <b>Связаться с экспертом</b>
Хотите персональную консультацию?
📱 WhatsApp: +7 (999) 000-00-00
📧 Email: info@example.com"""
    
    keyboard = [[InlineKeyboardButton("↩️ Назад в меню", callback_data='back_to_menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'invest':
        text = "💰 <b>Инвестиции</b>\n\nОтлично! Для инвестиций важны ликвидность и рост цены.\n\nНапишите нам в WhatsApp: +7 (999) 000-00-00 и мы подберем варианты."
    elif query.data == 'for_life':
        text = "🏡 <b>Для себя</b>\n\nПонял! Для себя главное — комфорт и надежность.\n\nНапишите нам в WhatsApp: +7 (999) 000-00-00 и мы найдем лучшие ЖК."
    elif query.data == 'checklist':
        text = """📋 <b>Чек-лист: 7 скрытых угроз новостроек</b>
1️⃣ Тонкие стены
2️⃣ Окна на север (риск плесени)
3️ Кривые стены под отделкой
4️⃣ Инфраструктура на бумаге
5️⃣ Дефицит парковок
6️⃣ Проблемы с фасадом
7️⃣ Юридические риски земли"""
    elif query.data == 'back_to_menu':
        await send_main_menu(query.message)
        return
        
    keyboard = [[InlineKeyboardButton("↩️ Назад в меню", callback_data='back_to_menu')]]
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

def main():
    logger.info("Запуск бота...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("Бот запущен успешно!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
