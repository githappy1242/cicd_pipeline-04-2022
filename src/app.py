#!/bin/python3
from flask import Flask, request
import pymysql.cursors
import json
import os

app = Flask(__name__)

db_connection = pymysql.connect(
  host=os.environ.get('DB_HOST'),
  user=os.environ.get('DB_USER'),
  password=os.environ.get('DB_PASSWORD'),
  db=os.environ.get('DB_NAME'),
  charset='utf8mb4',
  cursorclass=pymysql.cursors.DictCursor
)

db_cursor = db_connection.cursor()


def db_get(sql): #Definiert Methode db_get mit Parameter 1 und 2, values??
    db_cursor.execute(sql) #Führt db_cursor mit den übergenenen Variablen aus.
    return db_cursor.fetchall() #Gibt die Abholung von db_cursor zurück

def db_post(sql, values): #Definiert Methode db_get mit Parameter 1 und 2, values??
    db_cursor.execute(sql, values) #Führt db_cursor mit den übergenenen Variablen aus.
    return db_cursor.fetchall() #Gibt die Abholung von db_cursor zurück



@app.route('/')
def test():
    return("Hallo Welt")

@app.route('/api/v1/book', methods=['GET', 'POST'])
def books():
  result = None
  if request.method == 'GET':
    sql = 'SELECT * FROM books'
    result = db_get(sql)
  if request.method == 'POST': #Post funktioniert noch nicht, Nonetype object is not subscriptable
    print(request.json)
    body = request.json
    sql = 'INSERT INTO books (title, year_written, author) VALUES (%s, %s, %s)'
    result = db_post(sql, (body['title'], body['year_written'], body['author']))
  return json.dumps(result)


#.


@app.route('/api/v1/book/<int:id>', methods=['GET', 'DELETE']) #DELETE in Methods
def single_book(id):
    result = None
    if request.method == 'GET':
        sql = 'SELECT * FROM books WHERE id=%s' %id
        result = db_get(sql)
        return json.dumps(result)



    if request.method == 'DELETE': #Request-Methode wird definiert
        sql = 'SELECT * FROM books WHERE id=%s' #ID wird als Kriterium definiert
        #result = request.delete(body['title'], body['year_written'], body['author']) #oder single book?
        result = db_post(sql, id) #ausgabe
    return json.dumps(result)




@app.route('/api/v1/book/year/<string:year_written>', methods=['GET']) #Pfrad, String wird zugewiesen
def years(year_written): #years wird definiert, year_written wird übergeben
    result = None #keine Ausgabe ohne die If-Anweisung
    if request.method == 'GET': #Wenn GET, dann
        sql = 'SELECT * FROM books WHERE year_written=%s' %year_written #Einträge werden aus der Datenbank abgerufen
        result = db_get(sql) #ergebnis wird ausgeworfen mit den Variablen
    return json.dumps(result)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Erhalte den Port aus der Environment Variable, sonst benutze 80
    app.run(host='0.0.0.0', port=port)      # Starte die App