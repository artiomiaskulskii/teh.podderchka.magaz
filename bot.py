from logic import DB_Manager
from config import *
from telebot import TeleBot

bot = TeleBot(TOKEN)
manager = DB_Manager(DATABASE)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-менеджер по поддержке. Напиши команду /info, чтобы узнать, что я умею делать.""")

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
"""
Вот команды, которые могут тебе помочь:
/new_question - задать новый вопрос поддержки ✅
/questions - посмотреть свои вопросы 🗒️
/delete_question - удалить вопрос ❌
/help - помощь и инструкции
Также ты можешь просто написать свой вопрос, и я его зафиксирую!""")

@bot.message_handler(commands=['new_question'])
def new_question(message):
    bot.send_message(message.chat.id, "Введите ваш вопрос:")
    bot.register_next_step_handler(message, save_question)

def save_question(message):
    user_id = message.from_user.id
    question_text = message.text
    # Добавляем вопрос в базу данных
    manager.add_question(
        name=question_text[:20],
        description=question_text,
        id_of_question=0,
        status='new',
        user_id=user_id
    )
    bot.send_message(message.chat.id, "Ваш вопрос сохранен. Специалист свяжется с вами скоро.")

@bot.message_handler(commands=['questions'])
def list_questions(message):
    user_id = message.from_user.id
    questions = manager.get_questions(user_id)
    if questions:
        response = "Ваши вопросы:\n"
        for q in questions:
            response += f"{q[0]}: {q[2]} (Статус: {q[4]})\n"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "У вас пока нет вопросов.")

@bot.message_handler(commands=['delete_question'])
def delete_question(message):
    user_id = message.from_user.id
    questions = manager.get_questions(user_id)
    if questions:
        questions_list = [f"{q[0]}: {q[2]}" for q in questions]
        bot.send_message(message.chat.id, "
