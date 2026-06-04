import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8748664569:AAFaXfDaLC8UQAloZi36I6ncX6PiOKF8LaE"

async def send_main_menu(message):
    text = """🏠 <b>Добро пожаловать в ИИ-помощник по подбору новостроек!</b>

Я помогу вам выбрать надежную квартиру без скрытых угроз.

<b>Что я умею:</b>
✅ Подберу проверенные ЖК под ваш бюджет
✅ Покажу скрытые угрозы новостроек
✅ Рассчитаю инвестиционную привлекательность
✅ Связжу с экспертом для бесплатной консультации

Выберите, что вам важно:"""
    
    keyboard = [
        [InlineKeyboardButton("💰 Инвестиции", callback_data='invest')],
        [InlineKeyboardButton("🏡 Для себя", callback_data='for_life')],
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
/about - О сервисе
/contact - Связаться с экспертом"""
    
    await update.message.reply_text(text, parse_mode='HTML')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """ℹ️ <b>О сервисе</b>

Мы — команда экспертов по недвижимости.

<b>Наша миссия:</b>
Помочь вам купить квартиру без скрытых угроз и переплат.

<b>✅ Что мы проверяем:</b>
• Надежность застройщика
• Качество строительства
• Юридическую чистоту
• Инвестиционную привлекательность"""
    
    await update.message.reply_text(text, parse_mode='HTML')

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """📞 <b>Связаться с экспертом</b>

Хотите персональную консультацию?

<b>Как получить консультацию:</b>
1. Пройдите подбор через бота (нажмите /start)
2. Оставьте контакт в конце
3. Эксперт свяжется с вами в течение 15 минут

<b>Или напишите напрямую:</b>
📱 WhatsApp: +7 (999) 000-00-00
📧 Email: info@example.com"""
    
    keyboard = [
        [InlineKeyboardButton("↩️ Назад в меню", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'invest':
        text = """💰 <b>Инвестиции в новостройки</b>

Отлично! Для инвестиций важны ликвидность и рост цены.

<b>Какой бюджет рассматриваете?</b>

1️⃣ До 7 млн ₽
2️⃣ 7-12 млн ₽
3️⃣ Свыше 12 млн ₽

Напишите цифру, и я подберу варианты."""
        
        keyboard = [
            [InlineKeyboardButton("↩️ Назад в меню", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
    elif query.data == 'for_life':
        text = """🏡 <b>Покупка для себя</b>

Понял! Для себя главное — комфорт и надежность.

<b>Какой район или метро вам интересно?</b>
<b>Какой бюджет рассматриваете?</b>

Напишите в свободной форме, и я подберу варианты."""
        
        keyboard = [
            [InlineKeyboardButton("↩️ Назад в меню", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
    elif query.data == 'checklist':
        text = """📋 <b>Чек-лист: 7 скрытых угроз новостроек</b>

1️⃣ <b>Тонкие стены</b> — стукните по стене. Глухой звук = хорошо, звонкий = слышимость 100%.
2️⃣ <b>Окна на север</b> — риск плесени и сырости.
3️⃣ <b>Кривые стены под отделкой</b> — через год плитка отвалится.
4️⃣ <b>Школа на карте может оказаться ТЦ</b> — проверяйте ПЗЗ участка.
5️⃣ <b>Парковок не хватит</b> — даже с подземным паркингом.
6️⃣ <b>Трещины фасада</b> — скрываются за вентфасадом.
7️ <b>Земля в залоге</b> — проверяйте проектную документацию.

<b>💡 Хотите, чтобы на просмотре с вами был профессиональный приемщик?</b>
Нажмите /contact"""
        
        keyboard = [
            [InlineKeyboardButton("↩️ Назад в меню", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
    elif query.data == 'back_to_menu':
        await send_main_menu(query.message)
        return
    
    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode='HTML')

def main():
    logger.info("Запуск бота...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("Бот запущен успешно!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
