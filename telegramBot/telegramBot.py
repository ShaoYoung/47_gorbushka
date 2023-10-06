#!/usr/bin/python3


import os
import sys
import signal
import re
import telebot
import threading

# sys.path.append("..")
sys.path.append("../core")
import core_log as log
import core_config as cf

# import core.core_log    as log
# import core.core_config as cf


# import housekeeper
import offer

if __name__ == "__main__":
    config = cf.configuration()

    #
    #
    # Signal to Ignore
    # if parent is not INIT
    #

    # COMMENT
    # if os.getppid() != 1:
    #     signal.signal( signal.SIGTTOU, signal.SIG_IGN )
    #     signal.signal( signal.SIGTTIN, signal.SIG_IGN )
    #     signal.signal( signal.SIGTSTP, signal.SIG_IGN )


    # COMMENT
    # os.chdir( config['common']['homedir'] + config['bot']['dir'])
    # os.umask(0x17)

    #
    #
    # Demon
    # fork new process
    #

    # COMMENT
    # try:
    #     pid = os.fork()
    #     if pid != 0:
    #         #
    #         # close parent process
    #         sys.exit(0)
    # except Exception as err:
    #     log.log( "Can't fork() process: " + str(err), severity="error", facility="bot" )
    #     sys.exit(1)

    #
    #
    # Child process there
    #
    #

    # COMMENT
    # pid = os.getpid()

    # get lead group

    # COMMENT
    # os.setsid()

    # log.log( "Daemon statrted", severity="info", facility="bot" )

    #
    # close all filedescriptor
    #

    # COMMENT
    # os.closerange( 0,1024 )

    #
    #
    # Tokens struct
    # Управляющая структура
    #
    Tokens = dict()

    # -------- Подключаем бота ---------
    #
    #
    bot = None
    # print(config['bot']['token'])

    try:
        bot = telebot.TeleBot(config['bot']['token'])
        log.log("Connected to telegram chat.", severity="info", facility="bot")

    except Exception as err:
        log.log("Bot can't connected. It's runnig now may be. Error: " + str(err), severity="error", facility="bot")
        sys.exit(1)

    #
    # номер следующего обновления с сообщениями
    # нужно указывать в функции get_update при чтении обновлений с сервера
    #
    offset = 0

    #
    # Вечный цикл
    #
    while True:
        #
        # Check client message
        #
        try:
            # получаем новые сообщения
            messages = bot.get_updates(offset=offset, timeout=int(config['bot']['update_timeout']))
            #
            # Два пути:
            # 1) Если новые сообщения пришли - запускаем Workers
            # 2) Если новых сообщений нет    - запускаем housekeeper
            #
            if len(messages) > 0:
                # Путь 1
                #
                # Заускаем Workers для каждого сообщения в отдельном потоке
                #
                for message in messages:
                    #
                    # New Thread
                    #
                    try:
                        # print('message')
                        new_offer = threading.Thread(target=offer.start, args=(bot, message,))
                        # update offset
                        if offset <= message.update_id:
                            offset = message.update_id + 1
                        #
                        # ---- Action ---- запускаем поток
                        #
                        new_offer.start()
                    except Exception as err:
                        log.log("Can't create Worker: " + str(err), severity="error", facility="bot")
            #
            # Путь 2
            # запускаем housekeeper (например, для рассылки сообщений)
            #
            else:
                # пока pass
                pass
                # housekeeper.start(bot)
        except Exception as err:
            log.log("get update error: " + str(err), severity="error", facility="bot update")
