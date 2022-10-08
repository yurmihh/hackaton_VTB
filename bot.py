import telebot
from telebot import types
from test2 import reader


TOKEN = "5709967064:AAHShAP-wOOCfVJlp23nAC-LTOaLJEnXVUM"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

ceo_words = ["рынок", "курс валюты", "зерно", "менеджмент", "акции", "биржа", "криптовалюта", "Финансы", "банки",
            "международные отношения на рынке труда", "зарплата", "сотрудники", "право", "продажи", "услуги", "переговоры", "клиенты","договоры"]
accountant_words = ['подрядный', 'многолетний', 'строительство', 'внеоборотный', 'капитальный', 'нормативный', 'способ', 'вложение', 'актив', 'земля', 'ключевой',
                    'переоценка', 'слово', 'цена', 'стоимость', 'насаждение', 'восстановительный', 'хозяйственный', 'застройщик', 'средство', 'первоначальный',
                    'лизинг', 'объект', 'основный', 'слово', 'консервация', 'лизинговый', 'аренда', 'карточка', 'срок', 'амортизационный', 'гудвилы',
                    'интеллектуальный', 'основной', 'ключевой', 'инвентарный', 'имущество', 'свидетельство', 'группа', 'остаточный', 'актив', 'объект', 'финансовый',
                    'ключевой', 'слово', 'патент', 'инвентаризация', 'обязательство', 'собственность', 'нематериальный', 'амортизация', 'хозяйство', 'первичный',
                    'график', 'крестьянский', 'рабочий', 'баланс', 'форма', 'мемориально–ордерный', 'документ', 'документооборот', 'пбу', 'объект', 'имущество',
                    'журналь–но–ордерный', 'бухгалтерский', 'план', 'фермерский', 'учёт']


all_news = reader("final_news.db")
ceo_news = []
accountant_news = []
ceo_count = 0
accountant_count = 0



def who_is_who(text):
    a = 0
    b = 0
    for i in text.split():
        #print(i)
        if i in ceo_words:
            a += 1
        if i in accountant_words:
            b += 1
    if a < b:
        return "accountant"
    elif a > b: return "ceo"
    else: return 0

print(len(all_news))
print(all_news[0:5])


for i in all_news:
    text = str(i[0])
    if i[2] != "None":
        text += str(i[2])
    if who_is_who(text) == "ceo":
        ceo_news.append([i[0], i[1], text])
    elif who_is_who(text) == "accountant":
        accountant_news.append([i[0], i[1], text])
    


print(ceo_news[0])
print(accountant_news)



#Часть с ботом
@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.send_message(message.chat.id, '''Какая проблема у вас возникла?''')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Бухгалтер")
    btn2 = types.KeyboardButton("❓ Главный администратор")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! \nЯ бот, что подберет для тебя самые интересные новости о произошедших событиях в мире.".format(message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id, text="Выбери свою должность в меню ниже:")


@bot.message_handler(content_types=['text'])
def func(message):
    global ceo_count, accountant_count
    try:
        if(message.text == "👋 Бухгалтер"):
            bot.send_message(message.chat.id, text="Ищем актуальные новости для тебя..!")
            bot.send_message(message.chat.id, text=str(ceo_news[ceo_count][0]) + "\n" + str(ceo_news[ceo_count][1]))
            ceo_count += 1
    except:
        ceo_count = 0
        bot.send_message(message.chat.id, text="Ищем актуальные новости для тебя..!")
        bot.send_message(message.chat.id, text=str(ceo_news[ceo_count][0]) + "\n" + str(ceo_news[ceo_count][1]))
        ceo_count += 1
    try:
        if(message.text == "❓ Главный администратор"):
            bot.send_message(message.chat.id, text="Ищем актуальные новости для тебя..!")
            bot.send_message(message.chat.id, text=str(accountant_news[accountant_count][0]) + "\n" + str(accountant_news[accountant_count][1]))
            accountant_count += 1
    except:
        accountant_count = 0
        bot.send_message(message.chat.id, text="Ищем актуальные новости для тебя..!")
        bot.send_message(message.chat.id, text=str(accountant_news[accountant_count][0]) + "\n" + str(accountant_news[accountant_count][1]))
        accountant_count += 1



bot.polling()
