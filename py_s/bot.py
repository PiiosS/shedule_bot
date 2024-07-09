import telebot
import pymysql
from datetime import datetime, date, timedelta
import sdata
import map
import csv

#testing
bot = telebot.TeleBot(sdata.TOKEN)
connection = pymysql.connect(host=sdata.HOST, user=sdata.USER, password=sdata.PASSWORD, database=sdata.DATABASE)
cursor = connection.cursor()
message = ''
message_text = ''

def conn(query):
    connection = pymysql.connect(host=sdata.HOST, user=sdata.USER, password=sdata.PASSWORD, database=sdata.DATABASE)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()
#Решить проблему закрывания (разрыва) соединения
def log(user_id, first_name, user_name, user_message, bot_response):
    insert_query = f"""INSERT INTO log_m (time_m, user_id, first_name, user_name, user_message, bot_response)
     VALUES (NOW(),'{user_id}','{first_name}','{user_name}','{user_message}','{bot_response}')"""
    map.del_sign(insert_query)
    try:
        conn(insert_query)
    except: bot_response="Ошибка подключения к БД для логирования "+bot_response
    file_path = 'id.csv'
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, first_name, user_name, user_message, bot_response])
        print(user_id, first_name, user_name, user_message, bot_response)
def schedule_date(s_date, message):
    connection = pymysql.connect(host=sdata.HOST, user=sdata.USER, password=sdata.PASSWORD, database=sdata.DATABASE)
    cursor = connection.cursor()
    query=f"SELECT `sdate`, `pair`, `subject`, `signature`, `classroom`, `classroom_building`, `group_name` FROM `schedule` WHERE `sdate` = '{s_date}' LIMIT 5"
    cursor.execute(query)
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows)
        if rows:
            message_text = "Данные на текущий день:\n"
            for row in rows:
                sdate, pair, subject, signature, classroom, classroom_building, group_name = row
                message_text += f"Дата: {sdate},\n Время занятия: {pair},\n Преподаватель: {signature},\n Предмет: {subject},\n Кабинет: {classroom},\n Учебный корпус: {classroom_building}\n\n"
        else:
            message_text = f"На {s_date} данных нет"
    except:
        message_text = f"На {s_date} данных нет"
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)

@bot.message_handler(commands=['group'])
def go_group(message):
    bot.send_message(message.chat.id,'Обновляю')
    try:
        map.update_groups()
        message_text = 'Список групп успешно обновлён'
    except: message_text = 'Ошибка обновления списка'
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)

@bot.message_handler(commands=['teach'])
def go_group(message):
    bot.send_message(message.chat.id,'Обновляю')
    try:
        map.update_teachers()
        message_text = 'Список преподавателей успешно обновлён'
    except: message_text = 'Ошибка обновления списка'
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)

@bot.message_handler(commands=['update'])
def start_message(message):
    bot.send_message(message.chat.id,'Обновляю')
    try:
        map.schedule()
        message_text='Обновлено'
    except:
        message_text='Ошибка обновления'
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)


@bot.message_handler(commands=['start'])
def start_message(message):
    message_text='Для вывода данных на текущий день напиши /today, для вывода данных на следующий день напиши /next_day'
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)

@bot.message_handler(commands=['help'])
def help_message(message):
    message_text="Для вывода данных на текущий день напиши /today, для вывода данных на следующий день напиши /next_day"
    bot.send_message(message.chat.id,message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)

    #print('Гит не гитится, идея не идеется')

@bot.message_handler(commands=['today'])
def get_today_data(message):
    current_date = date.today()
    print(message.chat.id, "Запросил", current_date)
    schedule_date(current_date, message)


@bot.message_handler(commands=['next_day'])
def get_next_day_data(message):
    next_date = date.today() + timedelta(days=1)
    print(message.chat.id, "Запросил", next_date)
    schedule_date(next_date, message)


@bot.message_handler(commands=['стоп'])
def stop_msg(message):
    print('Протокол "пока"')
    message_text = "Ня, пока"
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)
    bot.stop_bot()

@bot.message_handler(commands=['Ксюша'])
def ksenia_msg(message):
    print('Отправляю 962847585')
    message_text = "Ксюша, тебе приходят сообщения от бота?"
    img = open('cat.jpg', 'rb')
    bot.send_photo(5169161016, img)
    bot.send_message(message.chat.id, message_text)
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)

@bot.message_handler()
def all_message(message):
    log(message.chat.id, message.from_user.first_name, message.from_user.username, message.text, message_text)

bot.polling()




