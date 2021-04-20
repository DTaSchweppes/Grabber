import HTTPconnectionRe
from grabberEngine import GrabEng
import os


class GrabberMain():
    r1 = GrabEng()

    def __init__(self):
        self.menu_change()

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
            elif change == 2:
                os.system("cls")
                print('Файл со списком артикулов для парсинга находится в корневой папке zubr48grabber.txt ')
                print('Подождите, идет загрузка...')
                self.zubr48_grab()
                i=True
            elif change ==3:
                os.system("cls")
                self.convert_images()
                i=True
            elif change ==4:
                os.system("cls")
                self.analysis_item_name()
                i=True
            elif change ==5:
                os.system("cls")
                self.r1.dveri_regionov_grab()
                i=True
            elif change ==6:
                os.system("cls")
                self.r1.check_dwnd_images_in_price()
                i=True
            elif change ==7:
                os.system("cls")
                self.help_menu()
                i=True
            else:
                print('ОШИБКА ВВОДА! Введите цифру, соответствующую пункту меню!')

    def tdkomfort_price_grab(self):
        HTTPconnectionRe.setup_socks()
        HTTPconnectionRe.check_tor_browser()
        self.r1.tdkomfort_price_grab()

    def zubr48_grab(self):
        HTTPconnectionRe.setup_socks()
        HTTPconnectionRe.check_tor_browser()
        self.r1.zubr_48_grab()

    def convert_images(self):
        print('Папка для исходных изображений /editImages находится в корневой папке программы')
        print('Сохраняются обработанные изображения в папке /editedImages')
        self.r1.convert_images()

    def help_menu(self):
        print('=====================Меню помощи=====================')
        print('1. Обновление цен по товарам фирмы Danfoss на сайте Tdkomfort')
        print('2. Товары сайт zubr48')
        print('3. Сжать JPG изображения для меньшего размера файлов изображений')
        print('4. Анализ наименований товаров на Тип товара')
        print('5. Парсер с сайта https://www.dveriregionov.ru/ ')
        print('6. Перечислить недозагруженные граббером файлы')
        i = False
        change=''
        while change != 'exit':
            change = str(input('Введите цифру(пункт меню) для получения помощи по нужному процессу: '))
            if change == '1':
                os.system("cls")
                print('Информация о функции программы: Данная функция обновляет нужные нам актуальные цены')
                print('на список товаров, который задан артикулами.')
                print("Файл со списком артикулов для обновления находится в корневой папке 'danfmarket.txt' ")
                print('Выйти в главное меню: exit')
            elif change == '2':
                os.system("cls")
                print('Информация о функции программы: Данная функция загружает информацию по заданному списку артикулов товаров')
                print('Собирает: Цену, Категорию товара, Наименование, Характеристики в Экселевской таблице.')
                print('Файл со списком артикулов для парсинга находится в корневой папке zubr48grabber.txt ')
                print('Выйти в главное меню: exit')
            elif change == '3':
                os.system("cls")
                print('Информация о функции программы: Данная функция сжимает качество JPG файлов,')
                print('в конечном итоге уменьшается и размер файла, в ходе оптимизации.')
                print('Папка для исходных изображений /editImages находится в корневой папке программы')
                print('Сохраняются обработанные изображения в папке /editedImages')
                print('Выйти в главное меню: exit')
            elif change == '4':
                os.system("cls")
                print('Информация о функции программы: Данная функция анализирует список названий товаров,')
                print('отбирает товары подходящие к таким типам, как: Затирка, Алебастр, Клей, Штукатурка гипсовая, ')
                print('Плиточный клей, Шпатлевка, Стяжка, Пескобетон, Штукатурка фасадная')
                print('Сохраняются обработанные изображения в папке ГотовоАнализНазваний.txt')
                print('Выйти в главное меню: exit')
            elif change =='5':
                os.system("cls")
                print('Информация о функции программы: Данная функция парсит товары с сайта https://www.dveriregionov.ru/')
                print('Собирает названия, цены, характеристики по товарам.')
                print('Список артикулов не нужен, при старте нужно ввести ссылку на директорию в каталоге. Пример: https://www.dveriregionov.ru/catalog/metallicheskie_dveri/')
                print('Выйти в главное меню: exit')
            elif change =='6':
                os.system("cls")
                print('Информация о функции программы: Данная функция считает файлы по названию в папке \downloandedImages')
                print('Затем берет txt файл со списком артикулов (артикулы строго построчны, например копия столбца из excel)')
                print('Далее в файл done.txt сохраняет артикулы, изображения по каторым не были загружены граббером')

        self.menu_change()

    def analysis_item_name(self):
        print('Документ с исходным перечнем товаров находится в исходной папке программы - АнализНазваний.txt ')
        print('Результат сохраняется в ГотовоАнализНазваний.txt ')
        self.r1.analysis_item_name()


app = GrabberMain()


