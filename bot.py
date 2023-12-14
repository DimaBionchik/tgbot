import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto


bot = telebot.TeleBot('6321308129:AAF0c8Ej2TL7IZ7QewIZA7EFMWhAQSByNsE');


question = {"Когда началась первая мировая?": {"options":["1939","1941","1942","1940"],"correct_answer":"1939" },
            "Когда закончилась вторая мировая война?": {
        "options": ["1945", "1944", "1946", "1949"],
        "correct_answer": "1945"
    }}



users_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} {message.from_user.last_name}")
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, давай сыграем в игру")
        bot.send_message(message.chat.id, "Я буду задавать тебе вопросы и буду давать варианты ответа.")
        bot.send_message(message.chat.id, "За каждый правильный ответ тебе начисляется 1 балл. Удачи!")


        current_question_text = "Когда началась первая мировая?"
        send_question(message.chat.id, current_question_text)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(call):
    user_id = call.from_user.id

    if user_id not in users_data:
        users_data[user_id] = {"score": 0, "current_question": None}

    current_question_text = users_data[user_id]["current_question"]

    question_data = question.get(current_question_text, {"options": [], "correct_answer": None})
    correct_answer = question_data["correct_answer"]

    if call.data == correct_answer:
        users_data[user_id]["score"] += 1
        bot.send_message(call.message.chat.id, f"Правильно! Ваш счет: {users_data[user_id]['score']}")

    next_question_text = get_next_question(current_question_text)
    users_data[user_id]["current_question"] = next_question_text


    send_question(call.message.chat.id, next_question_text)


def get_next_question(current_question_text):
    if current_question_text == "Когда началась первая мировая?":
        return "Когда закончилась вторая мировая война?"
    else:
        return "Когда закончилась вторая мировая война?"


def send_question(chat_id, question_text):
    question_data = question.get(question_text, {"options": [], "correct_answer": None})
    answer_options = question_data["options"]

    keybord = types.InlineKeyboardMarkup(row_width=2)
    for i, option in enumerate(answer_options):
        button_label = f"Ответ {i + 1}: {option}"
        keybord.add(types.InlineKeyboardButton(text=button_label, callback_data=str(option)))

    bot.send_message(chat_id, f"{question_text}", reply_markup=keybord)


print("Ready")
bot.polling(none_stop=True)