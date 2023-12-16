import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import InputMediaPhoto
import gspread


bot = telebot.TeleBot('6321308129:AAF0c8Ej2TL7IZ7QewIZA7EFMWhAQSByNsE');



questions = {
    "Когда началась Вторая мировая война?": {"options": ["1938", "1941", "1942", "1940", "1939"], "correct_answer": 4},
    "Когда закончилась Вторая мировая война?": {"options": ["1945", "1944", "1946", "1949", "1950"], "correct_answer": 0},
    "Кто начал Вторую мировую войну?": {"options": ["Германия", "СССР", "Франция", "Великобритания", "Италия"], "correct_answer": 0},
    "Откуда Том Ям?":{"options":["Шри-Ланка","Тайланд ","Япония","Сингапур"], "correct_answer":1},
    "Кто из этих известных композиторов был глухим?":{"options":["Бах","Моцарт","Бетховен","Гендель"],"correct_answer":2},
     "Кто выиграл золотую бутсу по количеству голов на Евро-2016?":{"options":["Антуан Гризманн","Криштиану Роналду"," Гарри Кейн","Роберт Левандовски"], "correct_answer":0}}

user_data = {}

@bot.message_handler(commands=['start', 'quiz'])
def handle_start(message):
    user_id = message.from_user.id
    user_data[user_id] = {"score": 0, "current_question": 0}
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Давай сыграем в квиз.")
    send_question(message.chat.id, user_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    answer_index = int(call.data)

    if user_id not in user_data:
        user_data[user_id] = {"score": 0, "current_question": 0}

    if "answers" not in user_data[user_id]:
        user_data[user_id]["answers"] = {"correct": 0, "incorrect": 0}

    current_question_index = user_data[user_id]["current_question"]
    if current_question_index < len(questions):
        question_data = list(questions.values())[current_question_index]

        if "correct_answer" in question_data:
            correct_answer_index = question_data["correct_answer"]

            if answer_index == correct_answer_index:
                user_data[user_id]["score"] += 1
                user_data[user_id]["answers"]["correct"] += 1
            else:
                user_data[user_id]["answers"]["incorrect"] += 1

            user_data[user_id]["current_question"] += 1
            send_question(call.message.chat.id, user_id)
        else:
            bot.send_message(call.message.chat.id, "Ошибка: Нет правильного ответа для текущего вопроса.")


def send_question(chat_id, user_id):
    current_question_index = user_data[user_id]["current_question"]

    if current_question_index < len(questions):
        question_text, question_data = list(questions.items())[current_question_index]
        answer_options = question_data["options"]
        markup = types.InlineKeyboardMarkup(row_width=1)

        for i, option in enumerate(answer_options):
            callback_data = str(i)
            markup.add(types.InlineKeyboardButton(text=option, callback_data=callback_data))

        bot.send_message(chat_id, f"{question_text}", reply_markup=markup)
    else:
        total_questions = len(questions)
        correct_answers = user_data[user_id]["answers"]["correct"]
        incorrect_answers = user_data[user_id]["answers"]["incorrect"]
        score = user_data[user_id]["score"]
        percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        result_message = (
            f"Игра завершена.\n"
            f"Правильных ответов: {correct_answers}\n"
            f"Неправильных ответов: {incorrect_answers}\n"
            f"Общий счет: {score}\n"
            f"Процент правильных ответов: {percentage:.2f}%"
        )
        bot.send_message(chat_id, result_message)
        #score = user_data[user_id]["score"]
        #bot.send_message(chat_id, f"Игра завершена. Ваш счет: {score}")


print("ready")
bot.polling(none_stop=True)