import telebot
import requests

bot = telebot.TeleBot('1627093848:AAGDktI4RfLqLoj2BFw8OpKklXhDvOvSCl0')

url = 'http://api.openweathermap.org/data/2.5/weather'
url_novosti = "https://newsapi.org/v2/top-headlines?country=ru&apiKey=e0b50d483b7d4c6aacce6656eb13c536"
url3 = "https://www.cbr-xml-daily.ru/daily_json.js"
api_weather = 'dcc3afcf3f26758949b42ecdef868808'
api_telegram = '1627093848:AAGDktI4RfLqLoj2BFw8OpKklXhDvOvSCl0'

bot = telebot.TeleBot(api_telegram)


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard1 = telebot.types.ReplyKeyboardMarkup()
    keyboard1.row('Погода', 'Курс валют')
    keyboard1.row('Новости')
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start', reply_markup=keyboard1)
    keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)


@bot.message_handler(commands=['help'])
def welcome(message):
    bot.send_message(message.chat.id,
                     '/start запуск бота\n/help команды бота\nчтоб узнать погоду напишите в чат название города')


@bot.message_handler(content_types=['text'])
def test(message):
    if message.text == "Погода":
        bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.first_name) + ',' + '\n' +
                         'чтоб узнать погоду напишите в чат название города,но в начале поставьте точку (Пример: .Москва)')

    if message.text == "Курс валют":
        a = requests.get(url3)
        a = a.json()
        for key, value in a.items():
            print(key, ":", value)
        bot.send_message(message.chat.id,"Доллар 1$ = " + str(a['Valute']['USD']['Value']) + "₽" )
        bot.send_message(message.chat.id, "Евро 1€ = " + str(a['Valute']['EUR']['Value']) + "₽")
        bot.send_message(message.chat.id, "Белорусский рубль = " +str(a['Valute']['BYN']['Value']) + "₽")
        bot.send_message(message.chat.id, "Казахстанских тенге = " + str(a['Valute']['KZT']['Value']) + "₽")
        bot.send_message(message.chat.id, "Китайский юань = " + str(a['Valute']['CNY']['Value']) + "₽")
        bot.send_message(message.chat.id, "Польский злотый = " + str(a['Valute']['PLN']['Value']) + "₽")


    if message.text == "Новости":
        b= requests.get(url_novosti)
        b = b.json()
        for key, value in b.items():
            key, ":", value
        for i in range(10):
            bot.send_message(message.chat.id,"Источник: " + b["articles"][i]['source']["name"])
            bot.send_message(message.chat.id, b["articles"][i]["title"])
            bot.send_message(message.chat.id, "Ссылка на новость: " + b["articles"][i]["url"])
    if message.text == "Задачи":
        pass
    if message.text.startswith("."):
        city_name = message.text[1:]
        try:
            params = {'APPID': api_weather, 'q': city_name, 'units': 'metric', 'lang': 'ru'}
            result = requests.get(url, params=params)
            weather = result.json()


            if weather["main"]['temp'] < 0:
                status = "Сейчас холодно!"
            elif weather["main"]['temp'] <= 10:
                status = "Сейчас прохладно!"
            elif weather["main"]['temp'] <= 20:
                status = "Сейчас тепло!"
            elif weather["main"]['temp'] >= 25:
                status = "Сейчас жарко!"
            else:
                status = "Сейчас отличная погода!"

            bot.send_message(message.chat.id, "В городе " + str(weather["name"]) + " температура " + str(
                float(weather["main"]['temp'])) + "\n" +
                             "Максимальная температура " + str(float(weather['main']['temp_max'])) + "\n" +
                             "Минимальная температура  " + str(float(weather['main']['temp_min'])) + "\n" +
                             "Скорость ветра - " + str(float(weather['wind']['speed'])) + "\n" +
                             "Давление - " + str(float(weather['main']['pressure'])) + "\n" +
                             "Влажность - " + str(int(weather['main']['humidity'])) + "%" + "\n" +
                             "Видимость - " + str(weather['visibility']) + "\n" +
                             "Описание: " + str(weather['weather'][0]["description"]) + "\n\n" + status)

        except:
            bot.send_message(message.chat.id, "Город " + city_name + " не найден")

bot.polling()
