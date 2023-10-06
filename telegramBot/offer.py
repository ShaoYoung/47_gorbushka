# from telebot import types
#
import json
# import re
import datetime
import sys

sys.path.append('../core')
import core_log as log
# import core_profile     as p

import tokens


# import route


#
# Start - пришло сообщение - обрабатываем и выдаём ответ
#         одно сообщение обрабатывает один процесс (worker). У worker одна входящя функция - Start
#
# на входе   bot     - id бота. Надо знать к какому боту мы привязаны, кому отправлять сообщения
#            message - сообщение от телеграм, со всеми параметрами (как документации)
#
# на выходе  - функция ни чего не возвращает, но ответ готовит в token['answer']
#
def start(bot, message):
    #
    # 1 Парсим входящее сообщение
    # 2 выполняем действия
    # 3 Отправляем ответ
    #

    #
    #
    # 1 Парсим входящее сообщение
    #
    #
    try:

        #
        # 1 Парсим входящее сообщение
        #

        Tokens = tokens.parse_message(message)

        # print(Tokens)

        # =============================================================================================================
        # если пользователь отправил photo, voice, audio, document, то получаем, именуем и раскладываем по директориям согласно типу файла
        try:
            # print(f'{message=}')
            if message.message:
                # photo
                if message.message.photo:
                    # print("Photo")
                    path_photo = '../received_files/photo/'
                    path_photo += str(Tokens['chat_id'])
                    path_photo += datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')

                    fileID = message.message.photo[-1].file_id
                    file_info = bot.get_file(fileID)

                    # print(f'file_info.file_path - {file_info.file_path}')
                    file_ext = file_info.file_path[-4:]
                    # print(f'file_ext - {file_ext}')
                    path_photo += file_ext
                    # print(f'path_photo - {path_photo}')

                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(path_photo, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    Tokens['request']['text'] = 'file_delivered'
                # voice
                elif message.message.voice:
                    # print("Voice")
                    path_voice = '../received_files/voice/'
                    path_voice += str(Tokens['chat_id'])
                    path_voice += datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')

                    fileID = message.message.voice.file_id
                    file_info = bot.get_file(fileID)

                    file_ext = file_info.file_path[-4:]
                    # print(f'file_ext - {file_ext}')
                    path_voice += file_ext
                    # print(f'path_voice - {path_voice}')

                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(path_voice, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    Tokens['request']['text'] = 'file_delivered'
                # audio
                elif message.message.audio:
                    # print("Audio")
                    path_audio = '../received_files/audio/'
                    path_audio += str(Tokens['chat_id'])
                    path_audio += datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')

                    fileID = message.message.audio.file_id
                    file_info = bot.get_file(fileID)

                    file_ext = file_info.file_path[-4:]
                    # print(f'file_ext - {file_ext}')
                    path_audio += file_ext
                    # print(f'path_audio - {path_audio}')

                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(path_audio, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    Tokens['request']['text'] = 'file_delivered'
                # document
                elif message.message.document:
                    # print("Document")
                    path_document = '../received_files/document/'
                    path_document += str(Tokens['chat_id'])
                    path_document += datetime.datetime.now().strftime('_%Y_%m_%d_%H_%M_%S')

                    file_ext = message.message.document.file_name[-4:]
                    # print(f'file_ext - {file_ext}')
                    path_document += file_ext
                    # print(f'path_document - {path_document}')

                    # print(f'path_document - {path_document}')
                    fileID = message.message.document.file_id
                    file_info = bot.get_file(fileID)
                    downloaded_file = bot.download_file(file_info.file_path)
                    with open(path_document, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    Tokens['request']['text'] = 'file_delivered'

                # # TODO разобрать подпись к файлу. Пока можно сделать пересылку по полученному chat_id или через поиск в тексте caption
                # # Если есть подпись к файлу
                # if message.message.caption:
                #     try:
                #         print(f'Подпись к файлу: {message.message.caption = }')
                #         input_caption = message.message.caption.lower()
                #         if 'brig' in input_caption or 'бриг' in input_caption:
                #             # TODO можно сделать выборку получателей из БД. Отдельной функцией. Пригодится для каждого типа файлов.
                #             # пока стоит мой telegram_id
                #             chat_id_to_send = 5107502329
                #             caption = f'Файл от пользователя {Tokens["chat_id"]}'
                #             # img = dict()
                #             # img.update({'path': '../img/work_in_progress.gif'})
                #             # img.update({'caption': 'Ведутся работы по настройке сервиса'})
                #             # Tokens = tokens.update_answer(Tokens, add_img=img)
                #             print(f'{chat_id_to_send = }')
                #             # print(f'{path_photo = }')
                #             # print(f'{caption = }')
                #             # TODO сделать пересылку всех типов файлов (фото, аудио, голос и документ)
                #             with open(path_photo, 'rb') as file_to_send:
                #                 # res_send_photo = bot.send_photo(chat_id=int(Tokens['chat_id']), photo=img, caption=caption, protect_content=False)
                #                 res_send_photo = bot.send_photo(chat_id=chat_id_to_send, photo=file_to_send, caption=caption, protect_content=False)
                #                 # res_send_document = bot.send_document(chat_id=chat_id, document=file_to_send, caption=caption, protect_content=False)
                #     except Exception as e:
                #         print(f'Ошибка {e = }')

        except Exception as err:
            log.log(str(Tokens['chat_id']) + " Save user file: " + str(err), severity="error", facility="offer")
        # =============================================================================================================

        # Если пришёл ответ с кнопок (callback) -  удаляем InlineKeyboard вместе с заголовком
        # if 'request' in Tokens and 'type' in Tokens['request'] and Tokens['request']['type'] == 'callback_query':
        #     tokens.del_inline_keyboard(bot, Tokens)

        #
        # Find user_id by telegramId
        #
        # try:
        #     user_id = p.get_id_by_telegramid(Tokens['user']['id'])
        #
        #     # print(f'user_id = {user_id}')
        #     # user_id = 172
        #
        #     if user_id:
        #         Tokens.update({"user_id": user_id})
        # except Exception as err:
        #     log.log(str(Tokens['chat_id']) + " Can't define user: " + str(err), severity="error", facility="worker")

        #
        # Посмотрим, что получилось
        text = json.dumps(Tokens, indent=4)
        log.log(str(Tokens['chat_id']) + "\tTokens: " + text, severity="debug", facility="worker")


    except Exception as err:
        log.log(str(Tokens['chat_id']) + " Parsing message: " + str(err), severity="error", facility="worker")

    #
    #
    # 2 Выполняем действия
    #   Отправляем router для поиска нужной функции
    #
    try:
        #
        # Пока готовим эхо
        #
        text = 'Bot "Gorbushka" reseived your message \n"' + Tokens['request']['text'] + '"\n and send you HELLO !!!'
        log.log(str(Tokens['chat_id']) + "\tTokens: "+text,  severity="debug", facility="offer")
        #
        #
        # answer. new answer
        # Tokens = tokens.update_answer(Tokens, clear_all=True)
        #
        Tokens = tokens.update_answer(Tokens, clear_all=True, update_text=text)
        #
        #
        # Отправляем запрос на отработку
        #
        # Tokens = route.route( bot, Tokens )

        pass
        # Tokens = route.route(Tokens)



    except Exception as err:
        log.log(str(Tokens['chat_id']) + " Prepare answer: " + str(err), severity="error", facility="worker")

    #
    # 3 Отправляем ответ
    #
    #
    #
    try:

        tokens.send_answer(bot, Tokens)


    except Exception as err:
        log.log(str(Tokens['chat_id']) + " Send answer: " + str(err), severity="error", facility="offer")
