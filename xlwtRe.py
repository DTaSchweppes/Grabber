import xlwt
import xlrd
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1",cell_overwrite_ok=True)
sheet2 = book.add_sheet("Sheet 2",cell_overwrite_ok=True)


class ExcelWork():

    def tdkomfortprice_print(self, itt, article, masname):
        try:
            sheet1.write(itt, 1, masname[0])
            sheet1.write(itt, 0, article)
        except IndexError:
            sheet1.write(itt, 0, article)
            sheet1.write(itt, 1, ' ')

    def save_book(self):
        book.save("data.xls")

    def zubr_char_write(self, ittcharsnames, strChar,itt,masnameall,strValue):
        sheet1.write(0, ittcharsnames, strChar)
        sheet1.write(itt, masnameall.index(strChar) + 8, strValue)

    def zubr_char_write_new(self, strChar,itt,masnameall,strValue):
        sheet1.write(itt, masnameall.index(strChar) + 8, strValue)

    def zubr_names_table(self):
        sheet1.write(0, 0, 'Артикул')
        sheet1.write(0, 1, 'Количество')
        sheet1.write(0, 3, 'Цена руб.')
        sheet1.write(0, 4, 'Иерархия каталога 1')
        sheet1.write(0, 5, 'Иерархия каталога 2')
        sheet1.write(0, 6, 'Иерархия каталога 3')
        sheet1.write(0, 7, 'Наименование товара')