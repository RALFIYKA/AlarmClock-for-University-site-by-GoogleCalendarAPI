from __future__ import print_function
import datetime
import os.path
import re
import string
import requests
import telebot
import config
import urllib.parse
from telebot import types
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

bot = telebot.TeleBot(config.TOKEN)

SCOPES = ['https://www.googleapis.com/auth/calendar']

group = ''


def main(group):
    days, corr, corrtime, ans, creds = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница',
                                        'Суббота'), [], [], [], None
    thissite = (requests.get(url='https://eners.kgeu.ru/apish2.php?group=' + group + '&week=17&type=one').text)
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
    for el in thissite.split():
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


if __name__ == '__main__':
    main(input())

# @bot.message_handler(content_types=['text'])
# def get_messages(message):
#     if message.text == '/start':
#         bot.send_message(message.from_user.id,
#                          "Привет! Я бот⏱. В нем ты сможешь автоматически ставить будильники для начала пар.В ответ пришли мне номер группы.")
#     else:
#         group = message.text
#         bot.send_message(message.from_user.id, main(urllib.parse.quote(group)))
#
#
# bot.polling(none_stop=True)
