import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Marc")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ayudaaa")


async def macros(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Macros")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6111049756:AAEDkKcpj-f-wa8tmb9wE8ix-X7xLW11k6s').build()
    
    start_handler = CommandHandler('start', start)
    author_handler = CommandHandler('author', author)
    help_handler = CommandHandler('help', help)
    macros_handler = CommandHandler('macros', macros)
    application.add_handler(start_handler)
    application.add_handler(author_handler)
    application.add_handler(help_handler)
    application.add_handler(macros_handler)

    
    application.run_polling()