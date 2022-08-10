from __future__ import print_function
import datetime
import os.path
import re
import string
import requests
import telebot
from telebot import types
import config
import urllib.parse

# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials

bot = telebot.TeleBot(config.TOKEN)

SCOPES = ['https://www.googleapis.com/auth/calendar']
allgroupsun = []
libofgroups = ['ЭУЭ', 'АУС', 'ПМ', 'РСО', 'АТ', 'Т', 'ТРП', 'ВИЭ', 'ЭХП', 'ЭС', 'ИЭСм', 'ПМД', 'ЭПТ', 'ПИ', 'ИЗ', 'АУБ',
               'ЭЖКХ', 'ПОВТ', 'ПЭ', 'ЭП', 'МР', 'ЭУЭм', 'ЭО', 'ПТС', 'КЭФ', 'Э', 'ИЗм', 'УИТ', 'ВЭ', 'ХТ', 'АВБ',
               'ЭМК', 'ТВН']
for i in range(len(libofgroups)):
    allgroupsun.append(libofgroups[i] + '-1-18')
    allgroupsun.append(libofgroups[i] + '-1-19')
    allgroupsun.append(libofgroups[i] + '-1-20')
    allgroupsun.append(libofgroups[i] + '-1-21')
    allgroupsun.append(libofgroups[i] + '-1-22')
    allgroupsun.append(libofgroups[i] + '-2-18')
    allgroupsun.append(libofgroups[i] + '-2-19')
    allgroupsun.append(libofgroups[i] + '-2-20')
    allgroupsun.append(libofgroups[i] + '-2-21')
    allgroupsun.append(libofgroups[i] + '-2-22')
print(allgroupsun)


def site(group):
    thissite = (requests.get(url='https://eners.kgeu.ru/apish2.php?group=' + group + '&week=17&type=one').text)
    return thissite


def main():
    days, corr, corrtime, ans, creds = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница',
                                        'Суббота'), [], [], [], None
    """Shows basic usage of the Google Calendar API.
    # Prints the start and name of the next 10 events on the user's calendar.
    # """
    # creds = None
    # if os.path.exists('torenhere'):
    #     creds = Credentials.from_authorized_user_file('sametokenhere', SCOPES)
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'clientsecretoftokenhere', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     with open('sametokenhere', 'w') as token:
    #         token.write(creds.to_json())
    #
    # service = build('calendar', 'v3', credentials=creds)

    # Editin string of site
    for el in site(group).split():
        let = str(list(string.ascii_letters))
        new_string = el.translate(str.maketrans('', '', string.punctuation))
        s1 = re.sub(let, '', new_string)
        if s1 != '':
            corr.append(s1)
    for i in range(len(corr)):
        for el in days:
            if len(corr[i]) == 4 and corr[i - 6] == el:
                if len(corr[i - 5]) != 8:
                    ans.append('0' + corr[i - 5][0] + '-' + corr[i - 5][1:3] + '-' + corr[i - 5][3:7] + ' ' + corr[i][
                                                                                                              :2] + ':' +
                               corr[i][2:])
                else:
                    ans.append(
                        corr[i - 5][:2] + '-' + corr[i - 5][2:4] + '-' + corr[i - 5][4:8] + ' ' + corr[i][:2] + ':' +
                        corr[i][2:])
    for i in range(len(ans)):
        cmall = datetime.datetime.strptime(ans[i], "%d-%m-%Y %H:%M")
        cm = str(cmall)
        cmall -= datetime.timedelta(minutes=30)
        cmalls = str(cmall)
        event = {
            'summary': 'Первая пара, проснись!!!',
            'start': {'dateTime': cmalls[:10] + 'T' + cmalls[11:] + '.000+03:00'},
            'end': {'dateTime': cm[:10] + "T" + cm[11:] + '.000+03:00'},
        }
        # event = (service.events().insert(calendarId='primary', body=event).execute())
        # print('Event created: %s' % (event.get('htmlLink')))
        return ans


def chgngfortelegram(ans):
    corrans = '\n'.join(ans)
    return corrans


@bot.message_handler(commands=['start'])
def welcomin(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id,
                         "Привет! Я AlarminBot. В нем ты сможешь автоматически ставить будильники для начала пар.Привязать группу можно через команду /setting")


@bot.message_handler(commands=['setting'])
def setts(message):
    ass = (message.text)[:9]
    if ass == '/setting':
        bot.send_message(message.from_user.id, 'Введи группу')
    global group
    group = message.text[9:]
    if group in allgroupsun:
        bot.send_message(message.from_user.id, "Твоя группа " + group)
    else:
        bot.send_message(message.from_user.id, 'Это не название группы')


@bot.message_handler(content_types=['text'])
def get_text(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    pn = (main()[0])
    vt = (main()[1])
    sr = (main()[2])
    ct = (main()[3])
    pt = (main()[4])
    allweek = 'Вся неделя'
    sb = []
    if len(main()) == 6:
        sb = (main()[5])
        markup.add(pn[:5], vt[:5], sr[:5], ct[:5], pt[:5], sb[:5], allweek)
    else:
        markup.add(pn[:5], vt[:5], sr[:5], ct[:5], pt[:5], allweek)

    bot.send_message(message.from_user.id,
                     "Хорошо, выберите день на который хотите поставить будильник, Пройдите аунтефикацию в гугл",
                     reply_markup=markup)
    if message.text == pn[:5]:
        bot.send_message(message.from_user.id, "Все готово на понедельник стоит будильник, приятного пробуждения)))")
    elif message.text == vt[:5]:
        bot.send_message(message.from_user.id, "Все готово на вторник стоит будильник, приятного пробуждения)))")
    elif message.text == sr[:5]:
        bot.send_message(message.from_user.id, "Все готово на среду стоит будильник, приятного пробуждения)))")
    elif message.text == vt[5:]:
        bot.send_message(message.from_user.id, "Все готово на четверг стоит будильник, приятного пробуждения)))")
    elif message.text == pt[5:]:
        bot.send_message(message.from_user.id, "Все готово на пятницу стоит будильник, приятного пробуждения)))")
    elif message.text == sb[5:]:
        bot.send_message(message.from_user.id, "Все готово на субботу стоит будильник, приятного пробуждения)))")
    else:
        bot.send_message(message.from_user.id, "Все готово на всю неделю стоит будильник, приятного пробуждения)))")
bot.polling(none_stop=True)
