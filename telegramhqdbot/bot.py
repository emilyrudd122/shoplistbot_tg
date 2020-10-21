# -*- coding: utf-8 -*-
from sqlalchemy.orm import query
from telebot.types import InputMediaPhoto
import telegramhqdbot.config as config
from telegramhqdbot.config import States
import telegramhqdbot.dbworker as dbworker
import telegramhqdbot.messages as messages
import telebot
from telebot import types 
from telegramhqdbot.dbalchemy import session, User, Tovar
from telegramhqdbot.messages import DEFAULT_MESSAGE


bot = telebot.TeleBot(config.TOKEN)


auth_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
auth_keyboard.row(messages.AUTH_KEYBOARD)

default_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
default_menu_keyboard.row(messages.MENU_TOVARI_KEYBOARD, messages.MENU_KUPIT_KEYBOARD)
default_menu_keyboard.row(messages.MENU_BALANCE_KEYBOARD, messages.MENU_ABOUT_KEYBOARD)

choices = {}


@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, messages.START_MESSAGE, reply_markup=auth_keyboard)
    dbworker.set_state(message.chat.id, config.States.S_NEED_AUTH.value)

# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, messages.RETRY_MESSAGE, reply_markup=auth_keyboard)
    dbworker.set_state(message.chat.id, config.States.S_NEED_AUTH.value)

# message.from_user.id

@bot.message_handler(func=lambda message: message.text == messages.GET_BACK_MESSAGE)
def cmd_getback(message):
    bot.send_message(message.chat.id, messages.DEFAULT_MESSAGE, reply_markup=default_menu_keyboard)
    dbworker.set_state(message.chat.id, config.States.S_DEFAULT.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_NEED_AUTH.value)
def cmd_auth(message):
    if message.text.lower() == messages.AUTH_KEYBOARD.lower():
        id = message.from_user.id
        query = session.query(User).filter_by(telegram_id=id).first()
        if query is None:
            user = User(telegram_id=int(message.from_user.id), balance=0)
            session.add(user)
            session.commit()
        bot.send_message(message.chat.id, messages.AUTH_MESSAGE, reply_markup=default_menu_keyboard)
        dbworker.set_state(message.chat.id, config.States.S_DEFAULT.value)
        

    
def cmd_tovari(message):
    # bot.send_message(message.chat.id, 'Товары: ')
    tovars = session.query(Tovar).all()
    text = "Товары:\n"
    for tovar in tovars:
        asd = f"{tovar.name}: {tovar.amount}шт. цена: {tovar.cost}р./шт.\n"
        text += asd
    bot.send_message(message.chat.id, text)
    # https://ibb.co/GRLF6q7
    # https://ibb.co/8rqyvMs
    # https://ibb.co/VqbRr5J

    IMG_URLS = [
        'AgACAgIAAxkDAAIBdl-PWLDMNhdz4mlac5lOqJEOvQ5MAAJirzEbx_h4SNXZelGYQeQ0m6zrly4AAwEAAwIAA3gAA14JAgABGwQ',
        'AgACAgIAAxkDAAIBeF-PWLDl67c6iViG_hxhMxDr41X6AAJjrzEbx_h4SFmns-q3adzdqSfNly4AAwEAAwIAA3kAAyrcAQABGwQ',
        'AgACAgIAAxkDAAIBel-PWLBCzoLjFCfAz-r0LHrppwHUAAJkrzEbx_h4SCyWq44R01HEyWNQmC4AAwEAAwIAA3gAA_b1AQABGwQ'
    ]

    bot.send_media_group(message.chat.id, [
        InputMediaPhoto(IMG_URLS[0]),
        InputMediaPhoto(IMG_URLS[1]),
        InputMediaPhoto(IMG_URLS[2]),
        ])

    dbworker.set_state(message.chat.id, config.States.S_DEFAULT.value)


def cmd_kupit(message):
    bot.send_message(message.chat.id, 'Купить: ')

    kupit_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    query = session.query(Tovar).filter(Tovar.amount>0)
    for q in query:
        btn = types.KeyboardButton(q.name)
        kupit_keyboard.add(btn)
    kupit_keyboard.add(messages.GET_BACK_MESSAGE)
    bot.send_message(message.chat.id, "Что вы хотите купить", reply_markup=kupit_keyboard)

    dbworker.set_state(message.chat.id, config.States.S_KUPIT_CHOICE.value)

def cmd_about(message):
    bot.send_message(message.chat.id, messages.ABOUT_MESSAGE)
    dbworker.set_state(message.chat.id, config.States.S_DEFAULT.value)

def cmd_balance(message):
    balance_message = "Ваш баланс: "
    # bot.send_message(message.chat.id, 'Баланс: ')
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if user is not None:
        bot.send_message(message.chat.id, balance_message + str(user.balance))
    dbworker.set_state(message.chat.id, config.States.S_DEFAULT.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_KUPIT_CHOICE.value)
def cmd_kupit_choice(message):
    query = session.query(Tovar).filter_by(name=message.text).first()
    if query is not None:
        text = f"Доступно {query.amount}шт.\nНапишите, сколько вы хотите купить"
        choices.update({message.from_user.id:message.text})
        bot.send_message(message.chat.id, text)
        dbworker.set_state(message.chat.id, config.States.S_KUPIT_AMOUNT.value)
    else:
        text = "Что - то не так попробуйте еще раз"
        bot.send_message(message.chat.id, text)
        cmd_getback(message)
    

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_KUPIT_AMOUNT.value)
def cmd_kupit_choice(message):
    # TODO: Доделатб
    pass


    
    


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_DEFAULT.value)
def cmd_menu(message):
    if message.text.lower() == messages.MENU_TOVARI_KEYBOARD.lower():
        dbworker.set_state(message.chat.id, config.States.S_TOVARI.value)
        cmd_tovari(message)
        return

    elif message.text.lower() == messages.MENU_KUPIT_KEYBOARD.lower():
        dbworker.set_state(message.chat.id, config.States.S_KUPIT.value)
        cmd_kupit(message)
        return

    elif message.text.lower() == messages.MENU_BALANCE_KEYBOARD.lower():
        dbworker.set_state(message.chat.id, config.States.S_BALANCE.value)
        cmd_balance(message)
        return

    elif message.text.lower() == messages.MENU_ABOUT_KEYBOARD.lower():
        dbworker.set_state(message.chat.id, config.States.S_ABOUT.value)
        cmd_about(message)
        return

    bot.send_message(message.chat.id, messages.DEFAULT_MESSAGE, reply_markup=default_menu_keyboard)



if __name__ == '__main__':
     bot.polling(none_stop=True)