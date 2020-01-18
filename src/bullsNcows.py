#from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import random
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def getSecretDigits(m, l):
    a = list(range(m))
    r = []
    for i in range(l):
        n = random.choice(a)
        r.append(n)
        a.remove(n)
    return r

def eval(q, guess):
    q2 = q[:]
    g2 = guess[:]
    rsltA, rsltB = 0, 0
    for i in range(len(q)):
        if(q[i] == guess[i]):
            rsltA += 1
            a = guess[i]
            q2.remove(a)
            g2.remove(a)
    for i in range(len(q2)):
        if g2[i] in q2:
            rsltB += 1
    return "A%dB%d" % (rsltA,rsltB)

def checkInput(a, l):
    if len(a) != l:
        return False, "Cannot accept: enter %d digits" % l

    try:
        int(a)
    except:
        return False, "Cannot accept: not numbers"

    a_list = list(a)
    while len(a_list) > 0:
        n = a_list.pop()
        if n in a_list:
            return False, "Duplicated digit: %s" % n           

    return True, None

def bullsNcows():
    q = getSecretDigits(10, 4)
    cnt = 0

    while cnt < 10:
        guess_str = input('Your guess: ')
        while True:
            c, msg = checkInput(guess_str, 4)
            if c:
                break
            print(msg)
            guess_str = input('Your guess: ')           
        guess = list(map(int, guess_str))
        
        cnt += 1
        rslt = eval(q, guess)
        print("%d: The result is %s:%s" % (cnt,guess_str, rslt))

        if rslt == "A4B0":
            print("You Win!!")
            break
        
        if cnt == 10:
            print("I Win!! The numbers was %s" % q)


def help(update, context):
    """Send a message when the command /help is issued."""
    logger.info("도움!")
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    logger.info("불렀지")
    update.message.reply_text("나는야 따라쟁이: " + update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def gameStart(update, context):
    if 'guessCnt' in context.chat_data:
        update.message.reply_text('이미 시작 하셨구먼. 어서 %d번째 시도를 해보시구랴' 
                                   % context.chat_data['guessCnt'])
        return ON_GAME
    context.chat_data['guessCnt'] = 1
    context.chat_data['secretDigits'] = getSecretDigits(10, 4)
    update.message.reply_text('시작해볼까? 첫번째 시도를 해보시구랴')
    return ON_GAME

def gameEnd(update, context):
    update.message.reply_text('%d번째에 포기라니 아쉽구먼... 정답은 %s 였네' 
                               % (context.chat_data['guessCnt'], context.chat_data['secretDigits']))
    del context.chat_data['guessCnt']
    del context.chat_data['secretDigits']
    return ConversationHandler.END

def guess(update, context):
    guess_str = update.message.text
    c, msg = checkInput(guess_str, 4)
    if not c:        
        update.message.reply_text(msg)
        return ON_GAME
    
    secret = context.chat_data['secretDigits']
    guess = list(map(int, guess_str))
    rslt = eval(secret, guess)
    update.message.reply_text("%d| %s:%s" % (context.chat_data['guessCnt'], guess_str, rslt))

    if rslt == "A4B0":
        update.message.reply_text("자네가 이겼어. 좋은 게임이었네!!")
        context.chat_data['guessCnt'] = 1
        return ConversationHandler.END
    
    if context.chat_data['guessCnt'] == 10:
        update.message.reply_text("내가 이겼네 정답은 %s였다네" % secret)
        context.chat_data['guessCnt'] = 1
        return ConversationHandler.END

    context.chat_data['guessCnt'] += 1
    return ON_GAME

ON_GAME = 1
def main():
    #updater = Updater("489197787:AAEhOz-EvKUo8jdvC1TZRhn9obeREF56nsU", use_context=True)
    updater = Updater("905059867:AAFcGzq02N0iBLPwefq9dRj-61YWqrbSlfg", use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('go', gameStart)],

        states={
            #ON_GAME: [MessageHandler(Filters.regex('^[0-9]{4}$'), guess)]
            ON_GAME: [MessageHandler(Filters.text, guess)]
        },

        fallbacks=[CommandHandler('stop', gameEnd)]
    )

    dp.add_handler(conv_handler)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    #bullsNcows()
