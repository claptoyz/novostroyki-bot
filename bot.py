import os
import logging
from groq import Groq
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8748664569:AAFaXfDaLC8UQAloZi36I6ncX6PiOKF8LaE"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

def load_catalog():
    try:
        with open("catalog.txt", "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        logger.error(f"Не удалось прочитать catalog.txt: {e}")
        return "База объектов пуста."

async def send_main_menu(message):
    text = """🏠 <b>Добро пожаловать в ИИ-помощник по подбору новостроек!</b>

Я помогу вам выбрать надежную квартиру без скрытых угроз.

<b>Что я умею:</b>
✅ Подберу проверенные ЖК под ваш бюджет
✅ Покажу скрытые угрозы новостроек
✅ Связжу с экспертом для бесплатной консультации
🤖 <b>Отвечу на любые вопросы в чате!</b>

Выберите, что вам важно, или просто напишите свой вопрос:"""
    
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
/contact - Связаться с экспертом

Вы также можете написать мне любой вопрос о квартирах, и я подберу варианты из своей базы!"""
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
        text = "💰 <b>Инвестиции</b>\n\nОтлично! Для инвестиций важны ликвидность и рост цены.\n\nНапишите мне в чат ваш бюджет (например: 'Двушка до 10 млн для сдачи в аренду'), и я подберу варианты."
    elif query.data == 'for_life':
        text = "🏡 <b>Для себя</b>\n\nПонял! Для себя главное — комфорт и надежность.\n\nНапишите мне в чат ваши пожелания (например: 'Трешка в центре, рядом школа, до 15 млн'), и я найду лучшие ЖК."
    elif query.data == 'checklist':
        text = """📋 <b>Чек-лист: 7 скрытых угроз новостроек</b>
1️⃣ Тонкие стены
2️⃣ Окна на север (риск плесени)
3️⃣ Кривые стены под отделкой
4️⃣ Инфраструктура на бумаге
5️⃣ Дефицит парковок
6️⃣ Проблемы с фасадом
7️⃣ Юридические риски земли"""
    elif query.data == 'back_to_menu':
        await send_main_menu(query.message)
        return
        
    keyboard = [[InlineKeyboardButton("↩️ Назад в меню", callback_data='back_to_menu')]]
    await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not groq_client:
        await update.message.reply_text("⚠️ Ошибка: ИИ не подключен. Проверьте GROQ_API_KEY.")
        return

    user_text = update.message.text
    catalog = load_catalog()
    
    system_prompt = f"""Ты — профессиональный ИИ-риелтор. Ты вежлив, используешь эмодзи, отвечаешь кратко и по делу.
У тебя есть база объектов недвижимости:
{catalog}

Отвечай на вопросы клиента ТОЛЬКО на основе этой базы. 
Если подходящего объекта нет, честно скажи об этом и предложи связаться с живым экспертом (команда /contact).
Никогда не выдумывай объекты, которых нет в базе."""

    status_msg = await update.message.reply_text("🔍 Ищу лучшие варианты для вас...")

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_tokens=500
        )
        
        ai_response = chat_completion.choices[0].message.content
        
        await status_msg.delete()
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        logger.error(f"Ошибка Groq API: {e}")
        await status_msg.edit_text("⚠️ ИИ сейчас немного устал. Попробуйте переформулировать вопрос или напишите /contact.")

def main():
    logger.info("Запуск бота...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat))
    
    logger.info("Бот запущен успешно! ИИ и Меню готовы к работе.")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
