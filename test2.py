import sqlite3

def reader(name):
    answ = []
    try:
        sqlite_connection = sqlite3.connect(name)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sqlite_select_query = """SELECT * from NEWS"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Всего строк:  ", len(records))
        print("Вывод каждой строки")
        for row in records:
            answ.append([row[1], row[2],row[3]])
            #print("ID:", row[0])
            #print("Имя:", row[1])
            #print("Почта:", row[2])
            #print("Добавлен:", row[3])

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
            return answ



