import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Attivo il logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Qualche comando
def start(update, context):
    update.message.reply_text('Hi!')


# Fornisce l'id della chat
def chatinfo(update, context):
    update.message.reply_text(update.message.chat.id)


# Invia il logo di Telegram
def image(update, context):
    context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://telegram.org/img/t_logo.png')


# Ripete quello che dici
def echo(update, context):
    update.message.reply_text(update.message.text)


# Log degli errori
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater("5284401191:AAFc3Qa9kGBZr8eDGRywelldERnKFMUvwkY", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("chatinfo", chatinfo))
    dp.add_handler(CommandHandler("image", image))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    # Dovessimo effettivamente hostarlo da qualche parte sarebbe meglio usare un webhook
    updater.start_polling()

    # PORT = int(os.environ.get('PORT', '443'))
    # HOOK_URL = 'URL' + '/' + TOKEN
    # updater.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN, webhook_url=HOOK_URL)

    updater.idle()


if __name__ == '__main__':
    main()
