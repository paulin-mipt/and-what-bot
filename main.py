from telegram.ext import Updater, MessageHandler, Filters
import logging
from random import choice

from secret_data import TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


triggers = ('если', 'когда', 'в случае')
starters = ('А ', 'И ', 'Или ', '')


def make_question(mention):
    try:
        return mention.strip().replace('-то', '').replace(' ты ', ' я ') + '?'
    except Exception as e:
        logger.warning(e)
        return None


def format_questions(questions):
    logger.debug(questions)
    if not questions:
        return None

    answer = ''
    answer += questions[0].capitalize()
    for q in questions[1:]:
        if q:
            answer += ' {}{}'.format(choice(starters), q)
    logger.debug(answer)
    return answer


def make_reply(text):
    questions = []
    i = 0
    while i < len(text):
        for trigger in triggers:
            if text[i:].lower().startswith(trigger):
                mention = ''
                while i < len(text) and (text[i].isalnum() or text[i] in ' -'):
                    mention += text[i]
                    i += 1
                questions.append(make_question(mention))
        i += 1

    return format_questions(questions)


def echo(bot, update):
    logger.debug('Got a message!')
    text = update.message.text
    answer = make_reply(text)
    if answer is not None:
        return bot.send_message(chat_id=update.message.chat_id, text=answer)    


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()