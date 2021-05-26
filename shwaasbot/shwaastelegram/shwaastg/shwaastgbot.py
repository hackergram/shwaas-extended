# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
# from shwaastgbot.xpal import *
from . import xpal
from . import utils
import requests, json

# from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
#                          ConversationHandler)
from telegram.ext import (CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler, CallbackContext)
from telegram import ReplyKeyboardMarkup, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update, ReplyKeyboardRemove
import xetrapal
from xetrapal import telegramastras
import os

#import sys

#sys.path.append("/opt/xetrapal")


memberbotconfig = xetrapal.karma.load_config(configfile="/opt/shwaasbot-appdata/shwaastgbot.conf")
shwaastgbot = xetrapal.telegramastras.XetrapalTelegramBot(config=memberbotconfig, logger=xpal.shwaastgbotxpal.logger)
logger = shwaastgbot.logger
GETMOBILE, PROCESS_MESSAGE = range(2)

send_contact_text = u'\U0001F4CD Send Contact'

loop_text = u'\U0001F960 Loop'
exit_text = u'\U0001F44B Bye'
#contact_keyboard = [
#                    [{'text': send_contact_text, 'request_contact': True}]
#                    ]
#member_base_keyboard = [
#                        [exit_text]
#                        ]

main_menu_header_text = '''\
    Hi! My name is ShwaasBot.\n
'''

def facts_to_str(user_data):
    facts = list()
    logger.info("Converting facts to string")
    for key, value in user_data.items():
        facts.append(u'{} - {}'.format(key, repr(value)))
    logger.info("Converted facts to string")
    return "\n".join(facts).join(['\n', '\n'])

def get_rasa_response(username,message_text,hostname="http://localhost"):
    logger.info("Trying")
    resturl=":5005/webhooks/rest/webhook"
    jsondata={}
    jsondata['sender']=username
    jsondata['message']=message_text
    response=requests.post(hostname+resturl,json=jsondata)
    return response.json()


def main_menu(update: Update, context: CallbackContext):
    logger.info(context.user_data)
    user_data = context.user_data
    try:
        #user_data['member'] = xpal.get_member_by_tgid(update.message.from_user.id)
        user_data['member'] = xpal.get_member_by_username(update.message.from_user.username)
        logger.info(u"{}".format(user_data))
        if user_data['member'] is None:
            update.message.reply_text("Sorry, this service is for whitelisted members only. \nYou can find some useful videos at http://hackergram.org/ramal/covidlocalvids.html\nThere is also a list of reading material at https://hackergram.org/ramal/covidlocaldocs.html")
            #return ConversationHandler.END
            return GETMOBILE
        logger.info("Main Menu presented to member {}".format(user_data['member'].username))
        update.message.reply_text(main_menu_header_text,  parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        return PROCESS_MESSAGE
    except Exception as e:
        logger.error("{} {}".format(type(e), str(e)))


def loop(update: Update, context: CallbackContext):
    logger.info(context.user_data)
    if update.message.text=="/bye":
        return exit(update,context)
    #text = os.popen("fortune").read()
    logger.info("{} {}".format(context.user_data['member'].username,update.message.text))
    text=get_rasa_response(username=context.user_data['member'].username, message_text=update.message.text,hostname="http://localhost")

    logger.info(str(text[0]))
    update.message.reply_text(text[0]['text'], parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    return PROCESS_MESSAGE

def set_mobile(update: Update, context: CallbackContext):
    logger.info(u"{}".format(update.message.contact))
    member = xpal.get_member_by_mobile(update.message.contact.phone_number.lstrip("+"))
    if member:
        member.tgid = update.message.contact.user_id
        member.save()
        user_data['member'] = member
        logger.info("Main Menu presented to member {}".format(user_data['member'].username))
        markup = ReplyKeyboardMarkup(member_base_keyboard, one_time_keyboard=True)
        update.message.reply_text(main_menu_header_text, reply_markup=markup, parse_mode=ParseMode.HTML)
        return PROCESS_MESSAGE
    else:
        update.message.reply_text("Sorry, you don't seem to be listed!")
        return ConversationHandler.END


def cancel(bot, update, user_data):
    logger.info(u"Cancelling Update {}".format(user_data))
    markup = ReplyKeyboardMarkup(member_base_keyboard, one_time_keyboard=True)
    update.message.reply_text(u'Cancelled!', reply_markup=markup)
    return PROCESS_MESSAGE


def exit(update: Update, context: CallbackContext):
    update.message.reply_text("Bye!")
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


states={
    GETMOBILE: [MessageHandler(Filters.text,
                               exit,
                               pass_user_data=True),
                MessageHandler(Filters.contact,
                               set_mobile,
                               pass_user_data=True),
                ],
    PROCESS_MESSAGE: [
                    MessageHandler(Filters.text, loop, pass_user_data=True)
                    #CallbackQueryHandler(open_xchange_button, pass_user_data=True),
                  ],

}


def setup():
    # Create the Updater and pass it your bot's token.
    updater = shwaastgbot.updater
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu)],
        states=states,
        fallbacks=[]#[RegexHandler('^[dD]one$', exit, pass_user_data=True)]
    )
    dp.add_handler(conv_handler)
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    # updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


def single_update():
    p = shwaastgbot.get_latest_updates()
    for update in p:
        shwaastgbot.updater.dispatcher.process_update(update)
    return p


if __name__ == '__main__':
    setup()
    shwaastgbot.updater.start_polling()
    shwaastgbot.updater.idle()
