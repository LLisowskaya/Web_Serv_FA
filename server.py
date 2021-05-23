import socket
from _thread import *
from email.utils import formatdate

# Текущий номер потока
ThreadCount = 0

# Функция для каждого потока
def ourserver(conn, threadcount):

  print("Starting Thread Number " + str(threadcount))

  # Читаем данные
  data = conn.recv(8192)

  # Если данных нет, ничего не делаем
  if not data:
   print("No data")
  else:
   # Если есть, выводим информацию
   print("DATA IS: " + str(data))

   # Получаем данные в виде строки
   msg = data.decode()
   # Делим на строки
   msglines = msg.splitlines()
   # Делим первую строку по пробелам
   msgfl = msglines[0].split(' ');
   # Второе значение - это ресурс, который нужно отобразить
   resour = msgfl[1];

   # Если это главная страница, то index.html
   if resour == '/':
     resour = '/index.html'

   # Копия названия ресурса, на случай, если нужно будет вывести ошибку
   cresour = resour
   # Имя файла, который нужно отобразить
   resour = "./DATA/" + resour
 
   # Заголовки
   headers = ""
   # Текущая дата
   headers = headers + "Date: " + formatdate(timeval=None, localtime=False, usegmt=True) + "\n"
   # Тип файла и его кодировка
   headers = headers + "Content-type: text/html; charset=UTF-8\n"
   # Описание сервера
   headers = headers + "Server: Our brand new Python Web Server\n"
   # Заголовок, сообщающий о том, что соединение нужно закрыть
   headers = headers + "Connection: close\n"

   # Пытаемся открыть нужный файл
   try:
       myfile = open(resour, "r")
       # Читаем данные
       data = myfile.read()
       # Получаем их размер
       datasize = len(data.encode())
       # Добавляем заголовок с размером данных
       headers = headers + "Content-Length: " + str(datasize) + "\n"
       # Отправляем код 200 + заголовки + данные
       resp = "HTTP/1.1 200 OK\n" + headers + "\n\n" + data
       # Закрываем файл
       myfile.close()
   except IOError:
       # Если файла нет, выдаем ошибку 404
       resp = "HTTP/1.1 404 Not Found\n" + headers + "\n\n" + "FILE " + cresour + " WAS NOT FOUND!"

   # Отправляем ответ
   conn.sendall(resp.encode())

  # Закрываем соединение
  print("Closing Thread Number " + str(threadcount) + "\n")
  conn.close()

# Подключаемся к порту 8080
sock = socket.socket()
sock.bind(('', 8080))
sock.listen(5)

# В бесконечном цикле
while True:
 # Если нашлось подключение
 conn, addr = sock.accept()
 print("Connected", addr)
 # Плюс один поток
 ThreadCount += 1
 # Запускаем обработчик потока
 start_new_thread(ourserver, (conn,ThreadCount))

# Закрываем сокет. Этого никогда не случится, так как цикл выше бесконечный
sock.close()
