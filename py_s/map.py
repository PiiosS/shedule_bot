import sdata
import pymysql
import requests
import re


def del_sign(text):
    return re.sub(r'[!@#$%^&*\";:?]', '', text)
def conn():
    return pymysql.connect(host=sdata.HOST, user=sdata.USER, password=sdata.PASSWORD, database=sdata.DATABASE)
def schedule():
    #url = "https://api.xn--80aai1dk.xn--p1ai/api/schedule?range=1"  #&subdivision_cod=1&group_name=5134"
    url = "https://api.xn--80aai1dk.xn--p1ai/api/schedule?range=4&date_from=2024-07-01&date_to=2024-07-07"
    PAIR_TIMES = {
        '1': '08:30-10:00',
        '2': '10:15-11:45',
        '3': '12:20-13:50',
        '4': '14:00-15:30',
        '5': '15:45-17:15',
        '6': '17:30-19:00',
        '7': '19:10-20:40',
    }

    connection = conn()
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE TABLE schedule""")


    response = requests.get(url)
    data = response.json()
    print(f': {response.status_code} ({len(data)})')
    for schedule in data:
        DATEarr = schedule['date'].split('.')
        DATE = str(DATEarr[2] + '-' + DATEarr[1] + '-' + DATEarr[0])
        pair=PAIR_TIMES[schedule['pair'].strip()]
        subject = del_sign(schedule['subject'].strip())
        if subject=='':
            subject = del_sign(schedule['prim'].strip())
        signature = del_sign(schedule['signature'].strip())
        classroom = del_sign(schedule['classroom'].strip())
        classroom_building = del_sign(schedule['classroom_building'].strip())
        group_name = del_sign(schedule['group_name'].strip())

        insert_query = f"""
                INSERT INTO `schedule`
                (`sdate`, `pair`, `subject`, `signature`, `classroom`, `classroom_building`, `group_name`)
                VALUES ("{DATE}","{pair}","{subject}","{signature}","{classroom}","{classroom_building}","{group_name}")
                """
        connection = conn()
        cursor = connection.cursor()
        cursor.execute(insert_query)
# Подтверждение изменений в базе данных и закрытие соединения utf8_unicode_ci

        connection.commit()
    connection.close()



def update_teachers():
    connection = conn()
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE TABLE teachers""")

    s_code = [1,2,3,4,101,201]
    for sc in s_code:
        url = f"https://api.xn--80aai1dk.xn--p1ai/api/teachers?subdivision_cod={sc}&date_from=2024-07-01&date_to=2024-07-07"
        response = requests.get(url)
        data = response.json()
        print(f': {response.status_code} ({len(data)})')
        for tc in data:

            t_id = tc["id"]
            sub_code = sc
            t_FIO = del_sign(tc["title"].strip())
            insert_query=f"""
                INSERT INTO `teachers`(`t_id`, `sub_code`, `t_FIO`) VALUES ('{t_id}', '{sub_code}', '{t_FIO}')
                """
            cursor.execute(insert_query)
        connection.commit()
    connection.close()

def update_groups():
    connection = conn()
    cursor = connection.cursor()
    cursor.execute("""TRUNCATE TABLE a_group""")

    s_code = [1,2,3,4,101,201]

    for sc in s_code:
        url = f"https://api.xn--80aai1dk.xn--p1ai/api/groups?subdivision_cod={sc}&date_from=2024-07-01&date_to=2024-07-07"
        response = requests.get(url)
        data = response.json()
        print(f': {response.status_code} ({len(data)})')
        for gr in data:
            g_id = gr["id"]
            sub_code = sc
            g_name = del_sign(gr["title"].strip())
            insert_query=f"""
                INSERT INTO `a_group`
                (`g_id`, `sub_code`, `group_name`) VALUES ('{g_id}', '{sub_code}', '{g_name}')
                """
            cursor.execute(insert_query)
        connection.commit()
    connection.close()



#schedule()
