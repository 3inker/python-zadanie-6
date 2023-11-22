from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import sqlite3

app = FastAPI()

connection = sqlite3.connect('1_database.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS friends (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
phone TEXT
)
''')
connection.commit()

#   1
def addfriend(name, email, phone):
    cursor.execute('''
    INSERT INTO friends (name, email, phone) VALUES (?, ?, ?)
    ''', (name, email, phone))
    connection.commit()
    print()
    print('Друг добавлен')
    print()

#   2    
def viewallfriends():
    cursor.execute('SELECT * FROM friends')
    friends = cursor.fetchall()
    print()
    print('Список всех друзей:')
    for friend in friends:
        print(friend)
    print()
    return friends

#   3        
def searchbyname(name):
    cursor.execute('SELECT * FROM friends WHERE name = ?', (name,))
    friend = cursor.fetchall()
    if friend:
        print()
        print('Найден друг:')
        print(friend)
        print()
        return friend
    else:
        print()
        print('Друг не найден')
        print()

#   4
def updateemail(name, newemail):
    cursor.execute('UPDATE friends SET email = ? WHERE name = ?', (newemail, name))
    connection.commit()
    print()
    print('Email друга обновлен')
    print()

#   5
def deletefriend(name):
    cursor.execute('DELETE FROM friends WHERE name = ?', (name,))
    connection.commit()
    print()
    print('Друг удален')
    print()
    
#   меню
while True:
    print('Выберите действие:')
    print('1. Добавить нового друга')
    print('2. Просмотреть всех друзей')
    print('3. Поиск друга по имени')
    print('4. Обновить email друга')
    print('5. Удалить друга')
    print('0. Выйти')
    print()
    choice = input('Введите номер действия: ')

    if choice == '1':
        name = input('Введите имя друга: ')
        email = input('Введите email друга: ')
        phone = input('Введите телефон друга: ')
        addfriend(name, email, phone)

    elif choice == '2':
        viewallfriends()

    elif choice == '3':
        name = input('Введите имя друга для поиска: ')
        searchbyname(name)

    elif choice == '4':
        name = input('Введите имя друга для обновления email: ')
        new_email = input('Введите новый email: ')
        updateemail(name, new_email)

    elif choice == '5':
        name = input('Введите имя друга для удаления: ')
        deletefriend(name)

    elif choice == '0':
        break

    else:
        print('Неверный ввод. Пожалуйста, введите правильный номер действия.')
        
class FriendCreate(BaseModel):
    name: str
    email: str
    phone: str
    
@app.post("/addfriend/")
async def add_friend(friend: FriendCreate):
    addfriend(friend.name, friend.email, friend.phone)
    return {"message": "Друг добавлен"}

@app.get("/viewallfriends/")
async def view_all_friends():
    friends = viewallfriends()
    return {"friends": friends}

@app.get("/searchbyname/{name}")
async def search_by_name(name: str):
    friend = searchbyname(name)
    if friend:
        return {"friend": friend}
    else:
        return {"message": "Друг не найден"}

@app.put("/updateemail/{name}")
async def update_email(name: str, new_email: str):
    updateemail(name, new_email)
    return {"message": "Email друга обновлен"}

@app.delete("/deletefriend/{name}")
async def delete_friend(name: str):
    deletefriend(name)
    return {"message": "Друг удален"}