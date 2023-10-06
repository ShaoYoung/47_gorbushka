#!/usr/bin/python3
from os.path import join, dirname
import configparser as cf


#
# Configuration -  Установка конфигурационных параметров
#
#
# Параметры хранятся в структуре config
# Извлекать параметры так
#   config[ <section> ][ <parameter> ]
#
# [common]
#   homedir
#   logfile
#   lockfile
#   log_maxtry
#
# [database]
#   dbname
#   host
#   user
#   pass
#
# [bot]
#   token
#
# [websocket]
#   listen
#   port
#


config = dict()


#
# 1 Структура заполняется значениями по умолчанию
# 2 Читается файл '../etc/config.ini', прочитанные параметры, обноаляются
#
def configuration():
    #
    # Имя файла по умолчанию
    #
    config_file = '../etc/config.ini'

    #
    # Config
    # значения по умолчанию
    #
    config['common'] = dict()
    config['database'] = dict()
    config['bot'] = dict()
    config['wsserver'] = dict()

    # general
    config['common'].update({"homedir": "./"})
    config['common'].update({"logfile": "logfile"})
    config['common'].update({"lockfile": "lockfile"})
    config['common'].update({"log_maxtry": 3})
    config['common'].update({"log_level": 'info'})

    # database
    config['database'].update({"host": ""})
    config['database'].update({"dbname": ""})
    config['database'].update({"user": ""})
    config['database'].update({"pass": ""})
    config['database'].update({"port": "5432"})

    # bot
    config['bot'].update({"username": ""})
    config['bot'].update({"token": ""})
    config['bot'].update({"dir": "telegramBot"})
    config['bot'].update({"update_timeout": "5"})

    # websocket
    config['wsserver'].update({"listen": "0.0.0.0"})
    config['wsserver'].update({"port": "8080"})
    config['wsserver'].update({"dir": "wsserver"})

    #
    #
    # config.ini
    # чтение
    #
    #
    ini = cf.ConfigParser()

    try:
        ini.read(config_file)

        # по всем секциям прочитанным конфиге
        for s in ini:
            # только для описанных у нас секций
            if s in config:
                for param in ini[s].keys():
                    config[s].update({param: ini[s][param]})

    except Exception as err:
        print("Can't read config file: " + str(err))
        exit(1)

    return config


if __name__ == "__main__":
    configuration()

    for s in config:
        print(s)
        for param in config[s].keys():
            print("\t" + param + "=" + str(config[s][param]))
