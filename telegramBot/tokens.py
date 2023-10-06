#
# Tokens - структура содержащая поля для обработки одного запроса от пользователя
#


from telebot import types

import json
import re

import sys

sys.path.append('../core')
import core_log as log


# import keyscallback as keycb
# import os


#
#
# Parse - Получить Tokens из message. 
#
#
#
#
def parse_message(message):
    #
    # Приведём входные параметры от пользователя к единой структуре
    #
    Tokens = dict()
    Tokens['chat_id'] = None
    Tokens['user'] = dict()
    Tokens['request'] = dict()
    Tokens['answer'] = dict()

    #
    # dump
    #
    # try:
    #        dump( message )
    # except Exception as err:
    #        log.log( "\tdump          "+str(err),         severity="error", facility="worker" )

    try:

        #
        #
        # Если пришло нажатие с кнопки ОСТАВИТЬ, ВДРУГ В БУДУЩЕМ ПОНАДОБИТСЯ
        #
        #
        if message.callback_query:
            try:
                #
                # разберём общую часть - пользователь
                #
                Tokens['user']['id'] = message.callback_query.from_user.id
                Tokens['user']['first_name'] = message.callback_query.from_user.first_name
                Tokens['user']['last_name'] = message.callback_query.from_user.last_name
                Tokens['user']['username'] = message.callback_query.from_user.username

                # None меняем на ''
                if not Tokens['user']['first_name']:
                    Tokens['user']['first_name'] = ''
                if not Tokens['user']['last_name']:
                    Tokens['user']['last_name'] = ''

                # print(f"{Tokens['user']['last_name']} {Tokens['user']['first_name']}")

                #
                # Чат
                #
                Tokens['chat_id'] = message.callback_query.message.chat.id

                #
                # Тип сообщения
                #
                Tokens['request']['type'] = 'callback_query'
                Tokens['request']['id'] = message.callback_query.message.id
                Tokens['request']['date'] = message.callback_query.message.date
                Tokens['request']['text'] = message.callback_query.message.text
                Tokens['request']['data'] = message.callback_query.data

                # callback_txt = keycb.decode(Tokens, Tokens['request']['data'])
                # if callback_txt:
                #     Tokens['request']['data'] = callback_txt

            except Exception as err:
                log.log("\tParse callback_query          " + str(err), severity="error", facility="tokens")


        #
        #
        # Если пришёл текст
        # start <hash> - приходит как текст
        #
        else:
            #
            # разберём общую часть - пользователь
            #
            Tokens['user']['id'] = message.message.from_user.id
            # # для теста регистрации нового пользователя
            # Tokens['user']['id']=777777
            Tokens['user']['first_name'] = message.message.from_user.first_name
            Tokens['user']['last_name'] = message.message.from_user.last_name
            Tokens['user']['username'] = message.message.from_user.username

            # None меняем на ''
            if not Tokens['user']['first_name']:
                Tokens['user']['first_name'] = ''
            if not Tokens['user']['last_name']:
                Tokens['user']['last_name'] = ''

            # print(f"{Tokens['user']['last_name']} {Tokens['user']['first_name']}")

            #
            # Чат
            #
            Tokens['chat_id'] = message.message.chat.id

            #
            # Тип сообщения
            #
            Tokens['request']['type'] = 'text'
            Tokens['request']['id'] = message.message.id
            Tokens['request']['date'] = message.message.date
            Tokens['request']['text'] = message.message.text

        #
        # Посмотрим, что получилось
        #
        # text = json.dumps( Tokens, indent=4 )
        # log.log( str(Tokens['chat_id']) + "\tTokens: "+text,  severity="debug", facility="tokens" )


    except Exception as err:
        log.log(str(Tokens['chat_id']) + "Parsing message: " + str(err), severity="error", facility="tokens")

    return Tokens


#
# Prepare Answer  - подготовка сообщения
# 
# параметры перед отправкой
# parse_mode  = [ html | markdown | markdownv2 ]
# text        = 
# keys        = [  {keytext:"", callback_data:""}, ... ]
#
# задаётся параметрами
#
# clear_all         = True  - очищает все параметры (и текст и кнопки)
# update_text       = <text>
# update_parse_mode = [ html | markdown | markdownv2 ]
# add_key_text      = <text>
# add_key_callback  = <text>
# add_key_row       = True
# add_img_path      = None - добавление изображения. Изображения хранятся на сервере в директории /sovtrud/img.
# Пример добавления изображения:
#                 img = dict()
#                 img.update({'path' : '../img/cogwheel.png'}) # необходимо указывать относительный путь
#                 img.update({'caption' : 'Шестерёнка'}) # описание изображения (строка, длина не более 1024)
#                 Tokens = tokens.update_answer(Tokens, add_img=img) # обновление Tokens
# Ограничения:
# Формат файла - png (решение принято на собрании 18.03.2023 года
# Максимальный размер файла - 10 Мб (API Telegram)
# Суммарная ширина и высота изображения - не более 10000
# Соотношение ширины и высоты изображения - не более 20
# Описание изображения - строка длиной не более 1024 символа
# ВНИМАНИЕ, в будущем будет реализовано удаление изображения из директории /sovtrud/img после его вывода в ТГ-бот
def update_answer(Tokens, update_text=None, update_parse_mode=None, add_menu=None, add_key_text=None,
                  add_key_callback=None, add_key_row=False, clear_all=False, add_img=None):
    #
    # Clear All
    # удаляем весь answer и создаём пустой
    #
    if clear_all == True:
        del (Tokens['answer'])
        Tokens['answer'] = dict()

    #
    # update text
    # пока ограничим 2048 символов
    if update_text != None:
        tmp = ''
        try:
            tmp = Tokens['answer']['text'] + update_text
        except Exception:
            tmp = update_text
        Tokens['answer'].update({'text': tmp[0:2048]})

    #
    # update parse_mode
    #
    if update_parse_mode != None:
        Tokens['answer'].update({'parse_mode': update_parse_mode})

    #
    # Add keyboard
    #
    if add_menu != None:
        Tokens['answer'].update({'bottomKeys': add_menu})  # строки кнопок

    #
    # Add img
    #
    if add_img != None:
        path = add_img['path']
        # print(f'Добавил путь к img {path}')
        Tokens['answer'].update({'img': add_img})  # добавляем img

    #
    # Add Inline keyboard
    #
    if add_key_text != None:

        try:
            #
            # Если кнопки ещё не созданы создадим новые
            #
            if 'keys' not in Tokens['answer']:
                # Tokens['answer'].update( {'keys': types.InlineKeyboardMarkup()} )
                Tokens['answer'].update({'keys': list()})  # строка для кнопок
                Tokens['answer']['keys'].append(list())  # массив кнопок в строке
                Tokens['answer'].update({
                    'currentkeyrow': 0})  # количество строк с кнопками (кнопки всегда будем добавлять в последнюю строку)

            #
            # Если требуют создать новую строку
            #  но, если в текущей строке нет кнопок, то новую строку не добавляем
            #
            if add_key_row == True:
                # если в строке есть кнопки
                if len(Tokens['answer']['keys'][Tokens['answer']['currentkeyrow']]):
                    Tokens['answer']['currentkeyrow'] = Tokens['answer']['currentkeyrow'] + 1
                    Tokens['answer']['keys'].append(list())

            #
            # Если есть callback к кнопке добавляем
            #
            if add_key_callback != None:
                #
                # Запишем callback в БД, а вернувшийся hash поставим на callback кнопки. по возвращении расшифруем
                #
                callback_hash = keycb.encode(Tokens, add_key_callback)
                # callback_hash = ''
                if callback_hash:
                    # если хэш вернулся, значит значение кнопки сохранено в бд
                    Tokens['answer']['keys'][Tokens['answer']['currentkeyrow']].append(
                        types.InlineKeyboardButton(add_key_text, callback_data=callback_hash))
                else:
                    # если хэш пришёл пустой, то в БД ни чего не записалось. Оставим наш callback на кнопке
                    Tokens['answer']['keys'][Tokens['answer']['currentkeyrow']].append(
                        types.InlineKeyboardButton(add_key_text, callback_data=add_key_callback))


            #
            # Добавляем кнопку с текстом без каллбека
            #
            else:
                Tokens['answer']['keys'][Tokens['answer']['currentkeyrow']].append(
                    types.InlineKeyboardButton(add_key_text))


        except Exception as err:
            log.log(str(Tokens['chat_id']) + " Update answer. Add key " + str(add_key_text) + " callback " + str(
                add_key_callback) + ": " + str(err), severity="error", facility="tokens")

        #
        # add Key to Keyboard
        #
        try:

            Tokens['answer'].update({'keyboard': types.InlineKeyboardMarkup(Tokens['answer']['keys'])})


        except Exception as err:
            log.log(str(Tokens['chat_id']) + " Update answer. Prepare keyboard " + str(
                Tokens['answer']['keys']) + ": " + str(err), severity="error", facility="tokens")

        # log.log( str(Tokens['chat_id']) + " Keys "+str(Tokens['answer']['keys']), severity="debug", facility="tokens" )

    # try:
    #    dump( Tokens['answer']['keys']  )
    # except Exception:
    #    pass
    #
    # try:
    #    dump( Tokens['answer']['keyboard'] )
    # except Exception:
    #    pass

    return Tokens


#
#
#
#
#
#

#
# Send Answer - отправка подготовленного сообщения
#
#
#
def send_answer(bot, Tokens):
    try:
        # если не указан тип текста - html | markdown удалим тип текста
        if 'parse_mode' in Tokens['answer']:
            if Tokens['answer']['parse_mode'] != 'html' and Tokens['answer']['parse_mode'] != 'markdown' and \
                    Tokens['answer']['parse_mode'] != 'markdownv2':
                Tokens['answer']['parse_mode'] = None
        else:
            Tokens['answer']['parse_mode'] = None

        #
        # Разный набор параметров отправки c кнопками и без
        #
        if 'keyboard' in Tokens['answer']:
            try:
                bot.send_message(int(Tokens['chat_id']), Tokens['answer']['text'],
                                 parse_mode=Tokens['answer']['parse_mode'], reply_markup=Tokens['answer']['keyboard'])
            except Exception as err:
                # если клавиатура получилась слишком большая
                text_message = f'<b>Не могу отобразить все ваши дела!\nИх слишком много!</b>'
                bot.send_message(int(Tokens['chat_id']), text_message, parse_mode='html')
                log.log(str(Tokens['chat_id']) + " Send answer: " + str(err), severity="error", facility="tokens")


        #
        # Только текст
        #

        elif 'text' in Tokens['answer']:
            # Tokens['answer']['text'] = 'x' * 4097
            # если длина текстового сообщения > 4096 символов (ограничение телеграмма), то разбиваем на несколько сообщений по 4096 символов каждое
            if len(Tokens['answer']['text']) > 4096:
                for x in range(0, len(Tokens['answer']['text']), 4096):
                    bot.send_message(int(Tokens['chat_id']), Tokens['answer']['text'][x:x + 4096],
                                     parse_mode=Tokens['answer']['parse_mode'])
            else:
                bot.send_message(int(Tokens['chat_id']), Tokens['answer']['text'],
                                 parse_mode=Tokens['answer']['parse_mode'])

        #
        # Если нужны нижние кнопки
        #
        if 'bottomKeys' in Tokens['answer']:
            if Tokens['answer']['bottomKeys'] == 'tgbot_menu':
                get_tgbot_menu(bot, Tokens)
            # elif Tokens['answer']['bottomKeys'] == 'registration_menu':
            #     get_registration(bot, Tokens)

        #
        # Если есть img
        #
        if 'img' in Tokens['answer']:
            path = Tokens['answer']['img']['path']
            caption = Tokens['answer']['img']['caption']
            # print(f'Получил путь к img {path} и отправил боту')
            with open(path, 'rb') as img:
                res_send_photo = bot.send_photo(chat_id=int(Tokens['chat_id']), photo=img, caption=caption,
                                                protect_content=False)
            # после вывода изображения его необходимо удалить с сервера
            # пока закомментировано
            # if res_send_photo:
            #     # print(f'Удаляю файл {path}')
            #     os.remove(path)




    except Exception as err:
        log.log(str(Tokens['chat_id']) + " Send answer: " + str(err), severity="error", facility="tokens")


# Меню телеграм-бота. Формирует ReplyKeyboard (3+1 кнопки внизу, в два ряда)
def get_tgbot_menu(bot, Tokens):
    # Вместо надписи на кнопках можно вывести эмодзи или расположить кнопки в два ряда
    # \U0001F4E9
    btn_message = types.KeyboardButton(text='Команда_1')
    # btn_message = types.KeyboardButton(text='ᵐᵉˢˢᵃᵍᵉˢ')
    # btn_message = types.KeyboardButton(text='\U0001F4E9')
    # \U0001F4C4
    btn_reports = types.KeyboardButton(text='Команда_2')
    # btn_reports = types.KeyboardButton(text='ʳᵉᵖᵒʳᵗˢ')
    # btn_reports = types.KeyboardButton(text='\U0001F4C4')
    # \U00002699
    btn_settings = types.KeyboardButton(text='Команда_3')
    # btn_settings = types.KeyboardButton(text='ዛα⊂τρọūkน')
    # btn_settings = types.KeyboardButton(text='ˢᵉᵗᵗᶦᶰᵍˢ')
    # btn_settings = types.KeyboardButton(text='\U00002699')
    # \U00002753
    btn_help = types.KeyboardButton(text='Помощь')
    # btn_help = types.KeyboardButton(text='ʰᵉᶫᵖ')
    # btn_help = types.KeyboardButton(text='\U00002753')

    tgbot_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3, one_time_keyboard=False,
                                           input_field_placeholder='Выберите пункт меню')
    # tgbot_menu.add(btn_message, btn_reports, btn_settings, btn_help)
    # tgbot_menu.add({'keyboard':[[btn_message, btn_reports, btn_settings], [btn_help]]})
    # Добавляем ряд кнопок
    tgbot_menu.row(btn_message, btn_reports, btn_settings)
    # Добавляем ряд кнопок
    tgbot_menu.row(btn_help)
    # text_mess = 'Начало работы'
    #        Tokens['answer'].update({'keyboard': tgbot_menu})
    #        Tokens['answer'].update({'text': 'Начало работы'})
    # Tokens['answer'].update({'parse_mode': 'MarkdownV2'})
    bot.send_message(chat_id=int(Tokens['chat_id']), text='Используйте меню', reply_markup=tgbot_menu)
    #        tokens.send_answer(bot, Tokens)
    #        del (Tokens['answer'])
    # text_mess = '||Начало работы||'
    # bot.send_message(chat_id=int(Tokens['chat_id']), text=text_mess, parse_mode = 'MarkdownV2', reply_markup=tgbot_me
    # hideBoard = types.ReplyKeyboardRemove() # if sent as reply_markup, will hide the keyboard
    return ('get_tgbot_menu_OK')


# Регистрация. Формирует ReplyKeyboard (кнопка "Зарегистрировать" внизу)
# def get_registration(bot, Tokens):
#     btn_registration = types.KeyboardButton(text='Зарегистрировать')
#     tgbot_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=False,
#                                            input_field_placeholder='Для регистрации нажмите кнопку ниже')
#     # Добавляем ряд кнопок
#     tgbot_menu.row(btn_registration)
#     bot.send_message(chat_id=int(Tokens['chat_id']), text='Используйте меню', reply_markup=tgbot_menu)
#     return ('get_registration_OK')


# Удаление InlineKeyboard и сообщения
def del_inline_keyboard(bot, Tokens):
    # После нажатия на кнопку # InlineKeyboard, клавиатуру можно полностью удалить.
    # bot.edit_message_reply_markup(message.callback_query.message.chat.id, message.callback_query.message.message_id)
    bot.edit_message_reply_markup(Tokens['chat_id'], Tokens['request']['id'])
    # Можно удалить полностью сообщение вместе с кнопками
    bot.delete_message(Tokens['chat_id'], Tokens['request']['id'])


#
#
# dumps object
# функция для исследования объекта
# написана для объектов, которые не получается вывести ни одним из способов:
#       print( str(object) )
#       print( json.dumps( object, indent=4 ) )
#
# c помощью этой функции исследовали message передаваемый из telegram
# внутри объекта message содержатся классы и методы
#
# def dump(obj, tab=0):
#     flag = True
#
#     tab += 1
#     offset = '\t' * tab
#
#     if tab == 0:
#         log.log(offset + "Type    : " + str(type(obj)), severity="debug", facility="tokens")
#
#     # if str(type(obj))[0:6] == '<class':
#     if True:
#         if re.search('.types', str(type(obj))):
#             log.log(offset + "Class: " + str(dir(obj)), severity="debug", facility="tokens")
#             for attr in dir(obj):
#                 if attr[0:1] != "_":
#                     t = 'unknown'
#                     try:
#                         t = str(type(getattr(obj, attr)))
#
#                         if isinstance(getattr(obj, attr), dict) or isinstance(getattr(obj, attr), list) or re.search(
#                                 '.types', str(type(getattr(obj, attr)))):
#                             log.log(offset + attr + "\t\t\t" + t, severity="debug", facility="tokens")
#                             dump(getattr(obj, attr), tab)
#                         elif isinstance(getattr(obj, attr), str) or isinstance(getattr(obj, attr), int):
#                             log.log(offset + str(attr) + "\t= " + str(getattr(obj, attr)) + "\t\t\t" + t,
#                                     severity="debug", facility="tokens")
#                         else:
#                             log.log(offset + str(attr) + "\t\t\t" + t, severity="debug", facility="tokens")
#
#                     except Exception:
#                         t = 'attr type error'
#                         log.log(offset + str(attr) + "\t\t\t" + t, severity="debug", facility="tokens")
#
#
#         elif isinstance(obj, dict):
#             for attr in obj.keys():
#                 t = 'unknown'
#                 try:
#                     t = str(type(getattr(obj, attr)))
#
#                     if isinstance(getattr(obj, attr), dict) or isinstance(getattr(obj, attr), list) or re.search(
#                             '.types', str(type(getattr(obj, attr)))):
#                         log.log(offset + str(attr) + "\t\t\t" + t, severity="debug", facility="tokens")
#                         dump(getattr(obj, attr), tab)
#                     elif isinstance(getattr(obj, attr), str) or isinstance(getattr(obj, attr), int):
#                         log.log(offset + str(attr) + "\t= " + str(getattr(obj, attr)) + "\t\t\t" + t, severity="debug",
#                                 facility="tokens")
#                     else:
#                         log.log(offset + str(attr) + "\t\t\t" + t, severity="debug", facility="tokens")
#
#
#                 except Exception:
#                     t = 'attr type error'
#                     log.log(offset + str(attr) + "\t\t\t" + t + " =| ", severity="debug", facility="tokens")
#
#
#         elif isinstance(obj, list):
#             for attr in obj:
#                 if isinstance(attr, dict) or isinstance(attr, list) or re.search('.types', str(type(attr))):
#                     log.log(offset + str(attr) + "\t\t\t" + str(type(attr)) + " : ", severity="debug",
#                             facility="tokens")
#                     dump(attr, tab)
#                 else:
#                     log.log(offset + str(attr) + "\t\t\t" + str(type(attr)), severity="debug", facility="tokens")
#
#
#         else:
#             log.log(offset + str(obj) + "\t\t\t" + str(type(obj)), severity="debug", facility="tokens")
#