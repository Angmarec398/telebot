import sqlite3
import sys
#
# collum = 'SDR' + input('Введите SDR')
# diameter = input('Введите диаметр')
# con = sqlite3.connect('rapts.db')
# cur = con.cursor()
# cur.execute(f'SELECT {collum} FROM calc where Diameter = ?', (diameter,))
# data = cur.fetchall()
#
# print(data[0][0])
#
#
# SDR = 'test1'
# diameter = 'test2'
# all_data = {SDR, diameter}
# print(type(all_data))

# a = '156 000 - 160 000'
# print(int((a.replace(' ', '')).split('-')[0]))


def utf8len(s):
    return len(s.encode('utf-8'))

a = '156000'
b = 156000
# print(utf8len(a))
print(sys.getsizeof(a))
print(sys.getsizeof(b))
