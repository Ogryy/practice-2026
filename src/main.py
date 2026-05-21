import telebot
from telebot import types

TOKEN = '8831893618:AAE6xtPxfLUzP1H9l42Qdnx7dq24IZDt000' 
bot = telebot.TeleBot(TOKEN)

QUESTIONS = [
    {
        "text": "1️⃣ Как ты обычно готовишься к экзаменам или зачетам?",
        "answers": [
            ("Учу всё заранее", "1"),
            ("В самую последнюю ночь", "2"),
            ("Учу усердно каждый день", "3"),
            ("Надеюсь на автомат и удачу", "4"),
            ("Учу спокойно и не торопясь", "5")
        ]
    },
    {
        "text": "2️⃣ Представь, что у тебя завтра первая пара в субботу. Твои действия?",
        "answers": [
            ("Лягу спать пораньше", "1"),
            ("Опять просплю её", "2"),
            ("Приду вовремя в любом случае", "3"),
            ("Пойду гулять, а там как пойдет", "4"),
            ("Поставлю 5 будильников", "5")
        ]
    },
    {
        "text": "3️⃣ Твой идеальный перерыв между парами — это...",
        "answers": [
            ("Повторить материал к следующей паре", "1"),
            ("Позалипать в мемы в телефоне", "2"),
            ("Сбегать в столовую хорошенько поесть", "3"),
            ("Устроить бурное обсуждение с друзьями", "4"),
            ("Посидеть в тишине на лавочке", "5")
        ]
    },
    {
        "text": "4️⃣ Какую роль ты чаще всего занимаешь в групповых проектах?",
        "answers": [
            ("Тот, кто всё проверяет и оформляет", "1"),
            ("Тот, кто делает свою часть в дедлайн", "2"),
            ("Лидер, который делает больше всех", "3"),
            ("Тот, кто отвечает за креатив и дизайн", "4"),
            ("Тот, кто тихо и мирно делает задачу", "5")
        ]
    },
    {
        "text": "5️⃣ Как ты реагируешь, если получаешь сложную задачу по учебе?",
        "answers": [
            ("Сразу ищу план и методичку", "1"),
            ("Паникую, но потом как-то решаю", "2"),
            ("Сажусь за работу прямо сейчас", "3"),
            ("Ищу, у кого можно списать", "4"),
            ("Разбираюсь медленно и вдумчиво", "5")
        ]
    }
]

RESULTS = {
    "1": "«Семь раз отмерь, один раз отрежь» — Ты студент-перфекционист! Любишь порядок, детально планируешь подготовку и перепроверяешь задания перед сдачей.",
    "2": "«Работа не волк, в лес не убежит» — Твой девиз! Прокрастинация — твое второе имя, но в режиме экстремального дедлайна ты способна сотворить чудо.",
    "3": "«Без труда не выловишь и рыбку из пруда» — Ты настоящий труженик! Ответственно подходишь к учебе, не боишься сложностей и всегда выручаешь группу.",
    "4": "«Кашу маслом не испортишь» — Ты творческая и яркая натура! Любишь, чтобы в твоих проектах всего было много, креативно и с красивым визуалом.",
    "5": "«Тише едешь — дальше будешь» — Ты воплощение спокойствия! Твой подход — делать все без суеты, размеренно, сохраняя нервы и двигаясь к цели в своем темпе."
}

USER_STATES = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_link = types.KeyboardButton("🔗 Ссылка на основного бота")
    btn_info = types.KeyboardButton("📝 Описание проекта")
    btn_fun = types.KeyboardButton("🎉 Тест: Какая ты пословица?")
    markup.add(btn_link, btn_info)
    markup.add(btn_fun)
    
    welcome_text = (
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я — мини-бот для учебной практики.\n"
        "Выбирай пункт в меню 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_menu(message):
    if message.text == "🔗 Ссылка на основного бота":
        inline_markup = types.InlineKeyboardMarkup()
        inline_btn = types.InlineKeyboardButton("👉 Запустить языкового бота", url="https://t.me/SpeakLearnPlayBot")
        inline_markup.add(inline_btn)
        bot.send_message(message.chat.id, "Нажимай на кнопку ниже, чтобы оценить наш основной проект:", reply_markup=inline_markup)
        
    elif message.text == "📝 Описание проекта":
        description = (
            "📚 *Наш главный проект* — это интерактивный Telegram-бот для изучения русского языка как иностранного!\n\n"
            "✨ *Особенности и преимущества:*\n"
            "• *Игровая форма:* Изучение грамматики через квесты.\n"
            "• *Живой язык:* Помогаем освоить реальную разговорную речь.\n"
            "• *Удобный интерфейс:* Пошаговые задания, которые подходят для всех студентов!"
        )
        bot.send_message(message.chat.id, description, parse_mode="Markdown")
        
    elif message.text == "🎉 Тест: Какая ты пословица?":
        USER_STATES[message.chat.id] = {"current_question": 0, "scores": []}
        send_question(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используй кнопки меню! 🤖")


def send_question(chat_id):
    user_data = USER_STATES[chat_id]
    q_index = user_data["current_question"]
    
    question = QUESTIONS[q_index]

    markup = types.InlineKeyboardMarkup()
    for text, score in question["answers"]:
        callback_data = f"quiz_{score}"
        markup.add(types.InlineKeyboardButton(text, callback_data=callback_data))
        
    bot.send_message(chat_id, question["text"], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz_'))
def handle_quiz_answer(call):
    chat_id = call.message.chat.id
    
    if chat_id not in USER_STATES:
        bot.send_message(chat_id, "Ой, тест устарел. Нажми кнопку в меню, чтобы начать заново! ✨")
        return

    score = int(call.data.split("_")[1])
    USER_STATES[chat_id]["scores"].append(score)
    
    USER_STATES[chat_id]["current_question"] += 1
    q_index = USER_STATES[chat_id]["current_question"]
    
    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    
    if q_index < len(QUESTIONS):
        send_question(chat_id)
    else:
        finish_quiz(chat_id)

def finish_quiz(chat_id):
    scores = USER_STATES[chat_id]["scores"]
    
    most_common_score = str(max(set(scores), key=scores.count))
    
    result_text = RESULTS.get(most_common_score, RESULTS["1"])
    
    final_message = (
        "🏁 *Тест завершен!*\n\n"
        "Анализируем твои студенческие привычки...\n\n"
        f"🔮 *Твой результат:* {result_text}"
    )
    bot.send_message(chat_id, final_message, parse_mode="Markdown")
    
    del USER_STATES[chat_id]

if __name__ == '__main__':
    print("Бот успешно запущен...")
    bot.infinity_polling()