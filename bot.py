from logic import DB_Manager
from config import *
from telebot import TeleBot, types

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    classes = ['5А', '5Б', '6А', '6Б', '7А', '7Б','8А','8Б']  # список классов
    for cls in classes:
        markup.add(cls)
    bot.send_message(message.chat.id, "Привет, я расписание твоей школы. Выберите ваш класс:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['5А', '5Б', '6А', '6Б', '7А', '7Б','8А','8Б'])
def send_schedule(message):
    class_name = message.text
    # Здесь нужно получить расписание для выбранного класса
    # Предположим, есть функция get_schedule_for_class
    schedule = get_schedule_for_class(class_name)
    bot.send_message(message.chat.id, f"Расписание для {class_name}:\n{schedule}")

# Обработка команды /questions или других команд по необходимости
@bot.message_handler(commands=['questions'])
def questions_command(message):
    bot.send_message(message.chat.id, "Здесь можно добавить ответы на вопросы или другую информацию.")

# Предположим, что функция get_schedule_for_class реализована в вашем проекте
def get_schedule_for_class(class_name):
    # Здесь должна быть логика получения расписания из базы данных или другого источника
    # Для примера возвращаю фиктивное расписание
    return "Понедельник: Математика\nВторник: Физика\nСреда: История"

# Запуск бота
bot.polling()