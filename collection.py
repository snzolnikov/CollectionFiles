''' collection and cleaning of repeated files '''
''' Программа производит поиск и копирование файлов с ресурса SOURCE_DIR по шаблонам и в каталоги 
    перечиленные в списке FILES_AND_DIRS добавляя в начало имени файла CRC + дату + время создания 
    на основе шаблона FORMAT_DATE_TIME. 
    В конце модуль del_empty_and_repeet() удаляет пустые и повторяющиеся файлы с одинаковой
    контрольной суммой файлов
'''

import datetime
import os.path
import shutil
import zlib
from os.path import getctime

FORMAT_DATE_TIME = '%Y_%d_%m-%H_%M'
SOURCE_DIR = 'd:\\files\\'
FILES_AND_DIRS = [['.png','d:\\PNG'], ['.docx','d:\\DOCX'], ['.xlsx','d:\\XLSX'],['.jpg','d:\\JPG'],['.pdf','d:\\PDF'],['.pub','d:\\PUB']]

# Функция расчета CRC файла
# получаем полное имя файла (file) а возвращаем его контрольную сумму
def crc32(file):
    with open(file, 'rb') as fh:
        hash = 0
        while True:
            s = fh.read(65536)
            if not s:
                break
            hash = zlib.crc32(s, hash)
        return "%08X" % (hash & 0xFFFFFFFF)

# Функция копирования файлов
# получаем полное имя файла источника  (source_file), имя целевого файла (destination_file) контрольную сумму (crc)
def copy(source_file, destination_file, crc):
    file_name = destination_file.split('\\')[-1]
    # print(file_name)
    if os.path.isfile(os.path.join(dir[1], destination_file)):
        print('Файл c таким именем:', destination_file, 'и контрольной суммой ', crcfile, 'уже есть!')
    else:
        shutil.copyfile(source_file, os.path.join(dir[1], file_name))
        print('Файл ', source_file, 'скопирован в ', file_name)

# Функция: удаление пустых и повторяющихся файлов

def del_empty_and_repeet():
    for address, dirs, files in os.walk(dir[1]):
        count = 0
        crc_search_elem = ''
        for file in files:
            crc = file[0:8]
            print('Контрольная сумма текущего файла ', crc)
            print('Контрольная сумма предыдущего файла ', crc_search_elem)
            if crc == '00000000':
                os.remove(os.path.join(dir[1], file))
                print('Пустой файл ', file, 'удален!')
                count += 1
            else:
                if crc_search_elem == crc:
                    print('Найдено совпадение контрольных сумм файлов!', crc, crc_search_elem)
                    os.remove(os.path.join(dir[1], file))
                    print('Повторяющийся файл ', file, 'удален!')
                    count += 1
                    continue
            crc_search_elem = crc
            continue
    print('Всего удалено ', count, ' файлов с расширением ', dir[0])



# Основная программа
for dir in FILES_AND_DIRS:
    print('Обрабатываем файлы с расширением', dir[0], 'копируем в целевой каталог ', dir[1] )
    if not os.path.exists(dir[1]):
        os.makedirs(dir[1])

    for address, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(dir[0]):
                fullname = ''
                date_time = datetime.datetime.fromtimestamp(getctime(os.path.join(address, file))).strftime(FORMAT_DATE_TIME)
                fullname = os.path.join(address, file)
                crcfile = crc32(fullname.replace('"', ''))
                newname = dir[1] + '\\' + crcfile + '_' + date_time + '_' + file
                copy(fullname, newname, crcfile)

    del_empty_and_repeet()


