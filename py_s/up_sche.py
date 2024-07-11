import pymysql
import map

err_user = ''

def user_sche(message):
    user_id = message.chat.id
    connection = map.conn()
    cursor = connection.cursor()

    msg_split = message.text.split(" ") #Разбиение сообщения на слова
    if msg_split[1].lower() == 'студент': #Проверка будущего типа пользователя
        user_type = 0
    elif msg_split[1].lower() == 'преподаватель':
        user_type = 1
    else:
        err_user = 'Не верно указан Ваш тип. ' #Если не верно написать тип, то будет ошибка
    if user_type == 0:
        query = f"""SELECT `g_id` FROM `a_group` WHERE `a_group`.`group_name` LIKE '{msg_split[2].upper()}%' LIMIT 1;""" #Запрос поиска кода группы
        cursor.execute(query)
        rows = cursor.fetchone()
        id_type = rows[0] #Помещаем код группы в переменную
    elif user_type == 1:
        try:
            teacher_name = (msg_split[2].capitalize() + " " + msg_split[3].upper())
        except: teacher_name = msg_split[2].capitalize()
        query = f"""SELECT `t_id`  FROM `teachers` WHERE `teachers`.`t_FIO` LIKE '{teacher_name}%' LIMIT 1;""" #Запрос поиска кода преподавателя
        cursor.execute(query)
        rows = cursor.fetchone()
        id_type = rows[0] #Помещаем код преподавателя в переменную
    else:
        err_user+='Не верно указана группа/ФИО преподавателя'



    query = f"""SELECT `user_id` FROM `user_group` WHERE `user_id` = '{user_id}' LIMIT 1;"""
    if cursor.execute(query) == 1:  #Если найдена одна запись по запросу
        query = f"""UPDATE `user_group` SET `user_type`='{user_type}',`id_type`='{id_type}' WHERE `user_group`.`user_id`='{user_id}'""" #Помещаем итоговые данные в запрос

    #Добавление нового пользователя
    elif cursor.execute(query) == 0: #Если не найдено ни одной записи
        query = f"""INSERT INTO `user_group`(`user_id`, `user_type`, `id_type`) VALUES ('{user_id}','{user_type}','{id_type}')"""
    try:
        cursor.execute(query)
        connection.commit()
    except: print(err_user)


    connection.close()

#user_sche()
