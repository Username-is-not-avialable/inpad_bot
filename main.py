import logging
from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from TOKEN import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CHOOSING1 = range(1)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiates dialogue"""
    keyboard = [
        [InlineKeyboardButton("Хочу задать вопрос касаемо работы плагина", callback_data = "вопрос")],
        [InlineKeyboardButton("Хочу сообщить об ошибке", callback_data = "ошибка")],
        [InlineKeyboardButton("Нужна помощь при установке/активации", callback_data = "помощь")]
    ]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                    text="Выберите пункт, по которому вам нужна помощь",
                                    reply_markup=markup)
    return CHOOSING1


async def plagin_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for a plagin category """
    keyboard = [
        [InlineKeyboardButton("Концепция", callback_data = "Концепция")],
        [InlineKeyboardButton("Архитектура", callback_data = "Архитектура")],
        [InlineKeyboardButton("Конструктив", callback_data = "Конструктив")],
        [InlineKeyboardButton("ОВ и ВК", callback_data = "ОВ и ВК")],
        [InlineKeyboardButton("Боксы и отверстия", callback_data = "Боксы и отверстия")],
        [InlineKeyboardButton("Общие", callback_data = "Общие")],
        [InlineKeyboardButton("Renga", callback_data = "Renga")],
    ]

    await update.message.reply_text(
        "Выберите из какой категории плагин, с которым вам нужна помощь",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

    return ConversationHandler.END


async def help_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for a help category """
    keyboard = [
        [InlineKeyboardButton("Ошибка при установке сборки", callback_data = "Ошибка при установке сборки")],
        [InlineKeyboardButton("Не получается зарегистрироваться", callback_data = "Не получается зарегистрироваться")],
        [InlineKeyboardButton("Не получается ввести ключ активации", callback_data = "Не получается ввести ключ активации")],
    ]

    await update.message.reply_text(
        "Выберите категорию, по которой вам нужна помощь",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('help', help)],
        states={
            CHOOSING1: [
                MessageHandler(
                    filters.Regex("^(Хочу задать вопрос касаемо работы плагина|Хочу сообщить об ошибке)$"), plagin_category
                ),
                MessageHandler(filters.Regex("^Нужна помощь при установке/активации$"), help_category)
            ],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    
    application.run_polling()