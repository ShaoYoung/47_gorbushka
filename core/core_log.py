#
# логирование сообщений 
#
##########################

from os.path import join, dirname
import os
from datetime import datetime
import time

import sys
# sys.path.append('..\\core')
import core_config as cf


# import core.core_config as cf

#
# Формат записей в логе
#
# DataTime  Severity    Facility    text
# где
#   Datatime  - текущее время Функция логирования возьмёт сама на момент поступления сообщения
#   Severity  - серьёзность события. Чем выше, тем серьёзней.  Основной момент. До Error - продолжать работать можно, выше приложение продолжить работу не может.
#               emergency/critical
#               error
#               warning     - возможно, что-то не указано, но система взяла значения по умолчанию и продолжает работать
#               notice      -
#               info        - по умолчанию
#               debug
#
#   facility  - система/модуль/функция, которая отправляет сообщение
#
def log(text, severity='info', facility="none"):
    #
    # читаем конфигурацию
    #
    config = cf.configuration()

    #
    # лог файл
    #
    # log_file    = "./websocket.log"
    log_file = config['common']['homedir'] + config['common']['logfile']
    # print(log_file)
    # log_path = dirname(__file__).replace('sovtrud/core', 'sovtrud/log')
    # log_file = join(log_path, config['common']['logfile'])
    # print(log_file)

    #
    # Файл блокировки (lock)
    # в одно время только один кто-то может писать в файл, иначе он испортится.
    # для этого процесс выставляет Флаг (Lock), пишет в файл, удаляет Флаг (unlock)
    # Остальные ждут пока предыдущий снимет блокировку
    #
    # lock_file   = "./websocket.lock"
    lock_file = config['common']['homedir'] + config['common']['lockfile']

    #
    # Чтобы не зависнуть в ожидании блокировки навечно сделаем счётчик максимального количества попыток
    # если он пройдёт - просто выйдем из функции без записи в лог
    #
    max_try = 7

    #
    # ждём удаления предыдущей блокировки
    #
    while os.path.exists(lock_file) and max_try > 0:
        time.sleep(1)
        max_try -= 1

    #
    # Если блокировка снята, но не максимальное кол-во попыток исчерпано
    #
    if max_try > 0:

        try:
            #
            # Мы выставляем Lock
            #

            # lock = open( lock_file, "x" )
            # Переписал работу с lock_file
            with open(lock_file, 'x') as lock_fhndl:
                # формируем запись
                lock_fhndl.write('BLOCK')

            #
            # берём текущую дату
            #
            dt = datetime.now()
            today = dt.strftime("%Y-%m-%d %H:%M:%S")

            #
            # PID
            #
            pid = os.getpid()

            #
            # открываем log файл для записи
            #
            with open(log_file, 'a') as log_fhndl:
                # log_fhndl       = open( log_file, "a" )
                # формируем запись
                s = f'{today}\t{str(severity):10} '
                if len(str(facility)) < 10:
                    s += f'{str(facility):10} '
                else:
                    s += f'{str(facility)} '
                s += f'[{str(pid)}]\t{str(text)}\n'
                log_fhndl.write(s)
            # log_fhndl.close ()

            # print(f'Core_log. Запись в {log_file} сделана')


        except Exception as err:
            pass

        #
        # unlock
        #
        try:
            os.remove(lock_file)
            # print(f'Core_log. {lock_file} удалён')
        except Exception as err:
            # print(f'Core_log. Не получилось удалить {lock_file}. Ошибка {err}')
            pass


if __name__ == '__main__':
    log('text')
