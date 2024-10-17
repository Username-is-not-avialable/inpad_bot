import logging
from telegram import Update, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
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

CHOOSING1, VERSION, LICENSE_KEY, BUILD_NUMBER, SCREENSHOT,PROBLEM_SUBMITTED = range(6)


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

    return VERSION

async def revit_version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for revit version"""
    keyboard = [
        [InlineKeyboardButton("Revit 2019", callback_data="Revit_2019")],
        [InlineKeyboardButton("Revit 2020", callback_data="Revit_2020")],
        [InlineKeyboardButton("Revit 2021", callback_data="Revit_2021")],
        [InlineKeyboardButton("Revit 2022", callback_data="Revit_2022")],
        [InlineKeyboardButton("Revit 2023", callback_data="Revit_2023")],
        [InlineKeyboardButton("Revit 2024", callback_data="Revit_2024")],
        [InlineKeyboardButton("Revit 2025", callback_data="Revit_2025")],
    ]

    await update.message.reply_text(
        "Выберите версию Revit",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )

    return LICENSE_KEY

async def license_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for a license key"""

    await update.message.reply_text(
        "Введите, пожалуйста, ваш лицензионный ключ, который вы использовали",
        reply_markup=ReplyKeyboardRemove()
    )
    return BUILD_NUMBER


async def build_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for a build number"""

    license_key = update.message.text #TODO: добавить regex для парсинга ключа из сообщения
    print(f"License key is {license_key}")

    await update.message.reply_text(
        "Напишите, пожалуйста, номер сборки, которую вы установили",
        reply_markup=ReplyKeyboardRemove()
    )
    return SCREENSHOT


async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asks for a screenshot and problem description"""

    build_number = update.message.text #TODO: добавить regex для парсинга ключа из сообщения
    print(f"Build number is {build_number}")

    await update.message.reply_text(
        "Отправьте, пожалуйста, скриншот ошибки и опишите вашу проблему",
        reply_markup=ReplyKeyboardRemove()
    )
    return PROBLEM_SUBMITTED


async def problem_submitted(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Informs user about submitting of problem"""

    screenshot = update.message.photo
    problem_description = update.message.caption
    print(problem_description)

    await update.message.reply_text(
        "Данная ошибка была передана отделу разработок, в ближайшее время с вами свяжется специалист",
        reply_markup=ReplyKeyboardRemove()
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
            VERSION: [MessageHandler(
                filters.Regex(
                    "^(Ошибка при установке сборки|Не получается ввести ключ активации|Не получается зарегистрироваться)$"
                    ),
                revit_version
            )],
            LICENSE_KEY: [MessageHandler(filters.Regex("^(Revit 20(19|20|21|22|23|24|25))$"), license_key)],
            BUILD_NUMBER: [MessageHandler(filters.Regex("Лицензионный ключ"), build_number)],
            SCREENSHOT: [MessageHandler(filters.Regex("Номер сборки"), screenshot)],
            PROBLEM_SUBMITTED: [MessageHandler(filters.PHOTO & filters.CAPTION, problem_submitted)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    
    application.run_polling()