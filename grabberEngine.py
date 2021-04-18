import os
import requests
import xlrd
import shutil
from xlwtRe import ExcelWork, sheet2, sheet1
from bs4 import BeautifulSoup as BS
from urllib.request import urlretrieve
from PIL import Image

class GrabEng:
    files = []
    excel = ExcelWork()

    def check_old(self,path):
        directory = path
        self.files = os.listdir(directory)
        print(self.files)

    def tdkomfort_price_grab(self):
        f = open('danfmarket.txt', encoding='UTF8')
        itt = 1
        for line in f:
            masname = []
            masValue = []
            print('Артикул открыт: ')
            article = line.replace("\n", "")
            CharName = article
            r = requests.get('https://tdkomfort.ru/search/?q=' + article + '&r=Y&send=Y')
            print('Артикул '+str(article) +' загружен. Сохранен')
            html = BS(r.content, 'html.parser')
            newPriceItem = ''
            for el in html.select('a.price.changePrice'):
                if 'Старая цена:' in el.text:
                    oldPrice = el.text.replace(" руб.											 / шт", " ")
                    indReg = oldPrice.index('Старая цена:')
                    itPrTxt = indReg
                    while itPrTxt < len(oldPrice):
                        newPriceItem += str(oldPrice[itPrTxt])
                        itPrTxt += 1
                    newPriceItem = newPriceItem.replace("Старая цена:", "").replace(" руб.", "")
                    masname.append(newPriceItem)
                else:
                    oldPrice = int(el.text)
                    masname.append(oldPrice)
            self.excel.tdkomfortprice_print(itt, article, masname)
            itt += 1
            self.excel.save_book()
        print('[УСПЕШНО] Программа завершена')
        pse=input()

    def zubr_48_grab(self):
        path = os.path.dirname(os.path.abspath(__file__)) +'\\downloandedImages'
        print(path)
        self.check_old(path)
        f = open('zubr48grabber.txt', encoding='UTF8')
        itt = 1
        scht = 0
        masnameall = []
        ittcharsnames = 8
        self.excel.zubr_names_table()
        for line in f:
            scht += 1
            name = line.replace("\n", "")
            if name + '.jpg' not in self.files:
                print('Товар с артикулом '+ str(name) +' взят в обработку')
                r = requests.get(
                    'https://zubr48.ru/poisk/result?setsearchdata=1&category_id=0&search_type=all&search=' + name)
                html = BS(r.content, 'html.parser')
                imgarr = []
                charsstr = ''
                mascateg = []
                masChars = []
                masValue = []
                masValueAll = []
                pricee = 'not'
                string = ''
                for el in html.select('div.product-title a'):
                    link = el.attrs["href"]
                    r = requests.get('https://zubr48.ru' + link)
                    html2 = BS(r.content, 'html.parser')
                    # (img.img-responsive)
                    for el in html2.select('div.productfull-info-description li'):  # характеристики для фильтров
                        strChar = ''
                        strValue = ''
                        charsstr = el.text  # Делим строку на до двоиточия
                        if ':' in charsstr:
                            indReg = charsstr.index(':')
                            itPrTxt = 0
                            while itPrTxt < indReg:
                                strChar += str(charsstr[itPrTxt])
                                itPrTxt += 1
                            masChars.append(strChar.replace("-", ""))
                            indReg = charsstr.index(':')  # Делим строку после двоиточия
                            itPrTxt = indReg
                            while itPrTxt < len(charsstr):
                                strValue += str(charsstr[itPrTxt])
                                itPrTxt += 1
                            masValue.append(strValue.replace("-", ""))
                            if strChar not in masnameall:
                                masnameall.append(strChar)
                                masValueAll.append(strValue)
                                self.excel.zubr_char_write(ittcharsnames, strChar,itt,masnameall,strValue)
                                ittcharsnames += 1
                            else:
                                self.excel.zubr_char_write_new(strChar,itt,masnameall,strValue)
                    for el in html2.select('div.product-main-image img'):
                        find = 1
                        img = el.attrs["src"]
                        imgarr.append(img)
                    for el in html2.select('h1.productfull-header'):
                        nameitem = el.text
                    for el in html2.select('div.productfull-info-price span'):
                        pricee = el.text
                    for el in html2.select('div.moduletable span'):
                        mascateg.append(el.text)
                    if not imgarr:
                        sheet2.write(itt, 0, name)
                    else:
                        linkdwnld = imgarr[0].replace(" ", "%20")
                        destination = os.path.dirname(os.path.abspath(__file__)) +'\\downloandedImages\\' + name.replace("/","-").replace(".","-").replace(" ","-") + '.jpg'
                        print('Ссылка на изображение ' + linkdwnld)
                        print('Путь каталога ' + destination)
                        urlretrieve(linkdwnld, destination)
                        if '/' in name:
                            sheet1.write(itt, 0, name.replace("/", "-"))
                        else:
                            if '.' in name:
                                sheet1.write(itt, 0, name.replace(".", "-"))
                            else:
                                sheet1.write(itt, 0, name)
                        sheet1.write(itt, 1, charsstr)
                        sheet1.write(itt, 2, string)
                        if pricee != 'not':
                            sheet1.write(itt, 3, pricee)
                        sheet1.write(itt, 4, mascateg[0])
                        sheet1.write(itt, 5, mascateg[1])
                        sheet1.write(itt, 6, mascateg[2])  # nameitem
                        sheet1.write(itt, 7, nameitem)
                    self.excel.save_book()
                    itt += 1
                    imgarr = []
        pse = input()


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

    def analysis_item_name(self):
        f = open('АнализНазваний.txt', encoding='UTF8')
        s = open('ГотовоАнализНазваний.txt', "w")
        lineIter = 1
        for line in f:
            name = line.replace("\n", "").lower()
            if 'штукат' in name:
                if 'гипсовая' in name:
                    s.write('Штукатурка гипсовая')
                else:
                    if 'цемент' in name:
                        s.write('Штукатурка цементная')
                    else:
                        if 'фасад' in name:
                            s.write('Штукатурка фасадная')
                        else:
                            s.write('Штукатурка')
            else:
                if 'затирка' in name:
                    s.write('Затирка')
                else:
                    if 'клей' in name:
                        if 'плит' in name:
                            s.write('Плиточный клей')
                        else:
                            if 'монтаж' in name:
                                s.write('Монтажный клей')
                            else:
                                s.write('Клей')
                if 'шпатл' in name:
                    s.write('Шпатлевка')
                if 'смесь' in name:
                    s.write('Смесь')
                if 'грунтовка' in name:
                    s.write('Грунтовка')
                if 'алебастр' in name:
                    s.write('Алебастр')
                if 'цемент ' in name:
                    s.write('Цемент')
                if 'шпаклевка' in name:
                    s.write('Шпатлевка')
                if 'стяжка' in name:
                    s.write('Стяжка')
                if 'пескобетон' in name:
                    s.write('Пескобетон')
                if 'смывка' in name:
                    s.write('Смывка')
                if 'раствор' in name:
                    s.write('Раствор')
            s.write('\n')
            lineIter += 1
        print('[УСПЕШНО] Программа завершена')
        pse = input()

    def dveri_regionov_grab(self):
        linkParse = str(input('Введите ссылку, Пример: https://www.dveriregionov.ru/catalog/metallicheskie_dveri/'))
        while 'www.dveriregionov.ru' not in linkParse:
            print('Ошибка! Некорректный URL. Введите URL с доменом www.dveriregionov.ru')
            linkParse = str(input('Введите ссылку, Пример: https://www.dveriregionov.ru/catalog/metallicheskie_dveri/'))
        else:
            itt = 1
            masnameall = []
            ittcharsnames = 2
            r = requests.get(linkParse, verify=False)
            html = BS(r.content, 'html.parser')
            masname = []
            tdmas = []
            iterItem = 0
            print('Начало')
            for el in html.select('div.card__product-name a'):
                name = el.attrs["href"]
                masname.append(name)
                maschar = []
                masvalue = []
                while iterItem < len(masname):
                    link = masname[iterItem]
                    r = requests.get('https://www.dveriregionov.ru' + link, verify=False)
                    html = BS(r.content, 'html.parser')
                    for el in html.select('div.complect-price__value'):
                        price = el.text
                    for el in html.select('h1.title-h1'):
                        title = el.text
                    for el in html.select('td'):
                        td = el.text
                        tdmas.append(td)
                    i = 0
                    while i < len(tdmas):
                        maschar.append(tdmas[i])
                        masvalue.append(tdmas[i + 1])
                        i += 2
                    sheet1.write(itt, 0, title)
                    sheet1.write(itt, 1, price)
                    iterItem2 = 0
                    while iterItem2 < len(maschar):
                        nameChar = maschar[iterItem2]
                        if nameChar not in masnameall:
                            masnameall.append(nameChar)
                            sheet1.write(0, ittcharsnames, nameChar)
                            sheet1.write(itt, masnameall.index(nameChar) + 2, masvalue[iterItem2])
                            ittcharsnames += 1
                            iterItem2 += 1
                        else:
                            sheet1.write(itt, masnameall.index(nameChar) + 2, masvalue[iterItem2])
                            iterItem2 += 1
                    itt += 1
                    iterItem += 1
                    self.excel.save_book()
        print('[УСПЕШНО] Программа завершена')
        pse = input()

