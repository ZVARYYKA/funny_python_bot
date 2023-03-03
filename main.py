import telebot
from telebot import types
import t0ken
import random
import time

bot = telebot.TeleBot(t0ken.TOKKEN())

message_count = {}


@bot.message_handler(commands=['start'])
# /start на ввод...
def start(message):
    if message.chat.type == 'private':
        markup_buttons1 = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Возможность пользоваться клавиатурой
        btn1 = types.KeyboardButton("👋 Поздороваться")  # Создание кнопки
        markup_buttons1.add(btn1)  # Добавление кнопки

        bot.send_message(message.from_user.id,
                         f"👋Здравствуйте, {message.from_user.username}! Вас приветствует funny bot!(В данный момент "
                         f"на этапе разработки). Для начала работы поменяйте токен и назначьте бота 'Администратором' "
                         f"в группе",
                         reply_markup=markup_buttons1)  # Текстовое сообщение
        bot.send_photo(message.from_user.id,
                       'https://cameralabs.org/media/lab16/post/10-16/11/fotografii-dikoy-prirody_24.jpg',
                       reply_markup=markup_buttons1)


# Фукнция, которая отвечает на команду /sum_bot в беседе
@bot.message_handler(commands=['sum_group'])
def sum(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        bot.send_message(message.chat.id, "Введите первое число")
        bot.register_next_step_handler(message, get_first_number_group)  # передаем объект сообщения message


def get_first_number_group(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        try:
            global a
            a = int(message.text)
            bot.send_message(message.chat.id, "Введите второе число")
            bot.register_next_step_handler(message, get_second_number_group)  # передаем объект сообщения message
        except Exception as e:
            bot.send_message(message.chat.id, "Введите число")


def get_second_number_group(message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        try:
            global b
            b = int(message.text)
            bot.send_message(message.chat.id, str(a + b))
        except Exception as e:
            bot.send_message(message.chat.id, "Введите число")


# Функция, которая считает сумму двух чисел на команду /sum, ответ приходит в лс
@bot.message_handler(commands=['sum'])
def sum(message):
    if message.chat.type == 'private':
        bot.send_message(message.from_user.id, "Введите первое число")
        bot.register_next_step_handler(message, get_first_number)  # следующий шаг – функция get_first_number


def get_first_number(message):
    if message.chat.type == 'private':
        try:
            global a
            a = int(message.text)
            bot.send_message(message.from_user.id, "Введите второе число")
            bot.register_next_step_handler(message, get_second_number)
        except Exception as e:
            bot.send_message(message.from_user.id, "Введите число")


def get_second_number(message):
    if message.chat.type == 'private':
        try:
            global b
            b = int(message.text)
            bot.send_message(message.from_user.id, str(a + b))
        except Exception as e:
            bot.send_message(message.from_user.id, "Введите число")


# message.chat.id - в чате
# message.from_user.id - в личку


# Функция для бана за запретки
@bot.message_handler(content_types=['text'])
def zapretki(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    arr_zapretki = ["реально", "ок", "внатуре", "ладно", "лан", "реал"]
    arr_mat = ["Ахуенно зашло, спс"]
    arr_zapretki_message = ["Следи за языком", "Завали свой еблет", "Начни читать книги, ублюдок",
                            "Повышай свой словарный запас", "Я запрещаю тебе пользоваться телеграмом"]
    file = open("list.txt", 'r', encoding='utf-8')
    arr_list_mat = file.readlines()

    for i in range(len(arr_list_mat)):  # убрать \n
        arr_list_mat[i] = arr_list_mat[i].replace("\n", "")
    for i in range(len(arr_list_mat)):
        if arr_list_mat[i] in message.text.lower():
            bot.send_message(message.chat.id, arr_list_mat[random.randint(0, len(arr_list_mat) - 1)])
    file.close()
    for i in range(len(arr_zapretki)):
        if arr_zapretki[i] in message.text.lower().split():
            # chat_id = message.chat.id
            # user_id = message.from_user.id
            chat_member = bot.get_chat_member(chat_id, user_id)
            if chat_member.status in ["administrator", "creator"]:
                bot.send_message(message.chat.id, "Он сука администратор!")
            else:
                if user_id not in message_count:
                    message_count[user_id] = 1
                else:
                    message_count[user_id] += 1
                if message_count[user_id] == 3:
                    message_count[user_id] = 0
                    for i in range(3, 0, -1):
                        bot.send_message(message.chat.id, f"Блокировка через {int(i)}...")
                        time.sleep(1)

                    bot.send_message(message.chat.id, "Вы заблокированы на 60 секунд! Меньше пиздеть надо ")
                    bot.restrict_chat_member(chat_id, user_id, until_date=int(time.time()) + 60,
                                             can_send_messages=False)
                    break
                bot.send_message(message.chat.id,
                                 f"{message.from_user.username}, вы будете заблокированы, после написания {int(3)}х запретных слова")
                bot.send_message(message.chat.id,
                                 arr_zapretki_message[random.randint(0, len(arr_zapretki_message) - 1)])


@bot.message_handler(commands=['help'])
def help(message):
    if message.chat.type == 'private':
        bot.send_message(message.from_user.id,
                         "Для началы работы с ботом,добавьте его в группу и назначьте 'Администратором'")


bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть

# Для запуска прописываем команду в консоль: py main.py
