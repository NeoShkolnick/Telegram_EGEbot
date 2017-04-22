import json
import random

import telebot
from EGEbot.models import User, Task
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from telebot import types

TelegramBot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
random.seed()


@TelegramBot.message_handler(commands=['start'])
def greeting(message):
    u = User(telegram_id=message.chat.id)
    u.save()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    bt1 = types.InlineKeyboardButton(text="Весь тест", callback_data="0")
    bt2 = types.InlineKeyboardButton(text="или определённое задание", callback_data="continue_of_choice")
    keyboard.add(bt1, bt2)
    TelegramBot.send_message(message.chat.id, message.from_user.first_name + ", что вы хотите прорешать?",
                             reply_markup=keyboard)


@TelegramBot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "continue_of_choice":
        keyboard = types.InlineKeyboardMarkup(row_width=5)
        keyboard.add(types.InlineKeyboardButton(text="1", callback_data="1"),
                     types.InlineKeyboardButton(text="2", callback_data="2"),
                     types.InlineKeyboardButton(text="3", callback_data="3"),
                     types.InlineKeyboardButton(text="4", callback_data="4"),
                     types.InlineKeyboardButton(text="5", callback_data="5"),
                     types.InlineKeyboardButton(text="6", callback_data="6"),
                     types.InlineKeyboardButton(text="7", callback_data="7"),
                     types.InlineKeyboardButton(text="8", callback_data="8"),
                     types.InlineKeyboardButton(text="9", callback_data="9"),
                     types.InlineKeyboardButton(text="10", callback_data="10"),
                     types.InlineKeyboardButton(text="11", callback_data="11"),
                     types.InlineKeyboardButton(text="12", callback_data="12"),
                     types.InlineKeyboardButton(text="13", callback_data="13"),
                     types.InlineKeyboardButton(text="14", callback_data="14"),
                     types.InlineKeyboardButton(text="15", callback_data="15"),
                     types.InlineKeyboardButton(text="16", callback_data="16"),
                     types.InlineKeyboardButton(text="17", callback_data="17"),
                     types.InlineKeyboardButton(text="18", callback_data="18"),
                     types.InlineKeyboardButton(text="19", callback_data="19"),
                     types.InlineKeyboardButton(text="20", callback_data="20"),
                     types.InlineKeyboardButton(text="21", callback_data="21"),
                     types.InlineKeyboardButton(text="22", callback_data="22"),
                     types.InlineKeyboardButton(text="23", callback_data="23")
                     )
        TelegramBot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=keyboard, text="Выберите задание:")
    else:
        u = User.objects.get(telegram_id=int(call.message.chat.id))
        u.state = int(call.data)
        u.save()
        if call.data == "0":
            text = "выбран весь тест"
        else:
            text = "выбранно %s задание" % call.data
        TelegramBot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=text)
        give_me_task(call.message)


@TelegramBot.message_handler(commands=['task'])
def give_me_task(message):
    user = User.objects.get(telegram_id=message.chat.id)
    number = user.state
    if number == 0:
        if user.current_task is not None:
            number = user.current_task.number + 1
            if number > 23:
                number = 1
        else:
            number = 1
    tasks = Task.objects.filter(number=number)
    user.current_task = tasks[random.randint(0, tasks.count() - 1)]
    user.save()
    ph = user.current_task.photo
    if ph is not None:
        if ph.file_id == '':
            with open(settings.MEDIA_ROOT + '/' + ph.file.url, mode='rb') as f:
                ph.file_id = TelegramBot.send_photo(message.chat.id, f).photo[0].file_id
                ph.save()
        else:
            TelegramBot.send_photo(message.chat.id, ph.file_id)
    TelegramBot.send_message(message.chat.id, user.current_task.text)


@TelegramBot.message_handler(commands=['pass'])
def next_task(message):
    user = User.objects.get(telegram_id=message.chat.id)
    if user.state == -1:
        return
    answer = user.current_task.answer
    TelegramBot.send_message(message.chat.id, 'Ответ на прошлое задание: ' + answer)
    give_me_task(message)


@TelegramBot.message_handler(content_types=['text'])
def check_answer(message):
    answer = User.objects.get(telegram_id=message.chat.id).current_task.answer
    if message.text == answer:
        TelegramBot.send_message(message.chat.id, 'Верно!')
        give_me_task(message)
    else:
        TelegramBot.send_message(message.chat.id, 'Неправильный ответ. Попробуйте ещё раз!')


class CommandReceiveView(View):
    def post(self, request, bot_token):
        if bot_token != settings.TELEGRAM_BOT_TOKEN:
            return HttpResponseForbidden('Invalid token')

        try:
            payload = json.loads(request.body.decode('utf-8'))
        except ValueError:
            return HttpResponseBadRequest('Invalid request body')
        else:
            update = telebot.types.Update.de_json(payload)
            TelegramBot.process_new_updates([update])
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
