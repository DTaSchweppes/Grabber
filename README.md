## Пояснительная записка к работе "Проект GRABBER".
Данная программа, представляет собой ~~граббер~~ симбиоз решений для работы с контентом в интернет магазине. Приложение включает в себя не только "грабберы",  
но и инструменты для работы с данными, например сжатие JPG изображений (скаченных граббером),  анализ типа товаров по их наименованиям, сравнение загруженных  
граббером изображений по списку артикулов.
# Структура проекта
Файловая структура: Проект состоит из четырех .py файлов, пяти .txt файлов, одного excel файла и пяти папок для работы с данными
Т.к. проект главным образом представляет собой граббер, для корректной работы, и минимизации случаев прерывания работы грабберов, был ~~прикручен~~ **задействован**  
TOR браузер. В кратце, из него мы будем получать socks для дальнейших запросов нашего граббера, чтобы запросы были с разных IP адресов, так меньше шансов, что сервер сайта донора,
что-то заподозрит по частоте запросов с одного IP адреса, забанит/обрубит подключение.
Данные действия у нас описаны в функциях **_make_request(), setup_socks(),** в файле **HTTPconnectionRe.py**
В check_tor_browser() идет проверка включил ли пользователь TOR браузер, посредством проверки через checkip
```python
    def check_tor_browser():
        try:
                ip = requests.get('http://checkip.dyndns.org').content
                soup = BS(ip, 'html.parser')
                print('[УДАЧНО] VPN TOR браузера работает')
                print(soup.find('body').text)
        except:
                print('Вы не застили TOR браузер! Запустите его, а после запустите скрипт снова!')
                sys.exit()
```
Файл main.py Представляет собой главный файл проекта, содержит класс **GrabberMain**, в нем описаны методы, запускающие основной функционал, онисанный в классе **GrabEng**
В конструкторе запускается метод menu_change()
```python
    def __init__(self):
        self.menu_change()
```
Есть, к примеру метод menu_change(), в котором описана логика работы меню
```python
def menu_change(self):
        os.system("cls")
        print('Для корректной работы, требуется запустить TOR браузер')
        print('==========МЕНЮ============')
        print('1. Обновление цен по товарам фирмы Danfoss на сайте Tdkomfort')
        print('2. Товары сайт zubr48')
        print('3. Сжать JPG изображения для меньшего размера файлов изображений')
        print('4. Анализ наименований товаров на Тип товара')
        print('5. Парсер с сайта https://www.dveriregionov.ru/')
        print('6. Перечислить недозагруженные граббером файлы')
        print('7. Помощь по программе')
        i=False
        while i != True:
            change = int(input('Введите цифру(пункт меню) для запуска нужного процесса: '))
            if change == 1:
                os.system("cls")
                print("Файл со списком артикулов для обновления находится в корневой папке 'danfmarket.txt' ")
                print('Подождите, идет загрузка...')
                self.tdkomfort_price_grab()
                i=True
            elif
```
Т.к. приложение не имеет GUI, пользовательский интерфейс в нем польностью консольный, и взаимодействие с меню происходит путем ввода кнопок с клавиатуры.
Затем, помимо четких инструкций  
> Введите цифру(пункт меню) для запуска нужного процесса  
> Введите ссылку, Пример: https://www.dveriregionov.ru/catalog/metallicheskie_dveri/
>> Ошибка! Некорректный URL. Введите URL с доменом www.dveriregionov.ru
> Введите путь к файлу .txt с перечнем артикулов. Пример: C:\PycharmProjects\Grabber\zubr48grabber.txt
>> ОШИБКА ВВОДА. Введите корректный путь к файлу (Начинается с C: или D:)

присутствует фильтрация и контроль вводимых пользователем данных, во избежание ~~Все не так! Оно не работает! За что мы платим!~~ недопонимания пользователя с интерфейсом  
Как пример, метод check_input_path_file() класса GrabEng
```python
    def check_input_path_file(self, text):
        inp = False
        while inp != True:
            path = str(input(text))
            if 'C:' not in path and 'D:' not in path:
                print('ОШИБКА ВВОДА. Введите корректный путь к файлу (Начинается с C: или D:)')
            else:
                inp = True
        return path
```        
Так же main.py отвечает за отрисовку меню:  
![Alt-текст](https://i.ibb.co/RQY82fN/image.png)

И помимо подсказок в основном меню при запуске той или иной функции:
![Alt-текст](https://i.ibb.co/rwXsdy8/image.png "инструкция")

Есть еще полная помощь:

![Alt-текст](https://i.ibb.co/RNzQb4c/image.png "помощь") 

Пример метода запуска граббера: 
```python
    def tdkomfort_price_grab(self):
        HTTPconnectionRe.setup_socks()
        HTTPconnectionRe.check_tor_browser()
        self.r1.tdkomfort_price_grab()
```
Файл grabberEngine.py содержит класс GrabEng, в методах которого описана вся логика функций приложения
Как работают грабберы, некоторые по принципу формирования поискового URL на сайте доноре, и далее парсинг страницы: 
```python
r = requests.get('https://tdkomfort.ru/search/?q=' + article + '&r=Y&send=Y')
html = BS(r.content, 'html.parser')
```
Но, например граббер https://www.dveriregionov.ru/ работает опираясь не на список артикулов товаров для парсинга, а по данной на вход ему ссылке на категорию товаров
```python
r = requests.get(linkParse, verify=False)
html = BS(r.content, 'html.parser')
```
Сделано так, потому что по ТЗ нет четких указаний по артикулам, нужно просто собрать все, со всех категорий

Далее уже идет перебор по HTML разметке, например цена в карточках товаров на https://www.dveriregionov.ru/:
```python
                    for el in html.select('div.complect-price__value'):
                        price = el.text
```
По инструментам для работы с данными, разберем к примеру convert_images():
```python
def convert_images(self):
        path = os.path.dirname(os.path.abspath(__file__)) +'\\editImages\\'
        pathEdited = os.path.dirname(os.path.abspath(__file__)) +'\\editedImages\\'
        files = os.listdir(path)
        i=False
        while i !=True:
            qual = int(input('Введите качество сжатия при конвертации от 0 до 100 '))
            if qual>-1 and qual<101:
                for file in files:
                    foo = Image.open(path + file)
                    foo.save(pathEdited + file, optimize=True, quality=qual)
                print('Все файлы обработаны! Готово!')
                i=True
        print('[УСПЕШНО] Программа завершена')
        pse = input()
```
С помощью библиотеки:
> from PIL import Image
Мы редактируем изображение, а именно качество, для снижения его веса.
>> foo.save(pathEdited + file, optimize=True, quality=qual)
Обязательно проверяем введенный параметр качества:
```python
qual = int(input('Введите качество сжатия при конвертации от 0 до 100 '))
            if qual>-1 and qual<101:
```

В файле xlwtRe.py содежится класс ExcelWork, в котором описана вся логика работы с Эксель таблицами, а именно, сохранение в них результатов работы грабберов
```python
        def save_book(self):
        book.save("data.xls")
```
```python
    def zubr_char_write(self, ittcharsnames, strChar,itt,masnameall,strValue):
        sheet1.write(0, ittcharsnames, strChar)
        sheet1.write(itt, masnameall.index(strChar) + 8, strValue)
```
![Alt-текст](https://i.ibb.co/37zRNHh/image.png "эксель") 

# Результаты работы
Результат работы функции Обновление цен по товарам фирмы Danfoss на сайте Tdkomfort:

![Alt-текст](https://i.ibb.co/CsGtD3x/image.png "1")
![Alt-текст](https://i.ibb.co/JBDB1qs/image.png "1")
Результат работы функции Товары сайт zubr48
![Alt-текст](https://i.ibb.co/jfTv4GB/image.png "2")
![Alt-текст](https://i.ibb.co/HPBbRXP/image.png "2")
![Alt-текст](https://i.ibb.co/h27MdBC/image.png "2")

Результат работы функции Сжать JPG изображения для меньшего размера файлов изображений

![Alt-текст](https://i.ibb.co/PtjTNv5/image.png "3")
![Alt-текст](https://i.ibb.co/LY2vs40/image.png "3")

Результат работы функции Анализ наименований товаров на Тип товара

![Alt-текст](https://i.ibb.co/JyT2XvX/image.png "4")
![Alt-текст](https://i.ibb.co/BrvSy6j/image.png "4")

Результат работы функции Парсер с сайта https://www.dveriregionov.ru/

![Alt-текст](https://i.ibb.co/pQyvcts/image.png "5")
![Alt-текст](https://i.ibb.co/NTcGZw7/image.png "5")

Результат работы функции Перечислить недозагруженные граббером файлы

![Alt-текст](https://i.ibb.co/M62YF1c/image.png "6")

Меню помощи:

![Alt-текст](https://i.ibb.co/VpdJg91/image.png "7")
![Alt-текст](https://i.ibb.co/brMv05t/image.png "7")

# Используемые библиотеки
```python
import socks
import socket
import requests
import sys
from bs4 import BeautifulSoup as BS
import os
import xlwt
from PIL import Image
import urllib3
```
