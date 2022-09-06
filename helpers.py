import codecs
import configparser
import traceback

import gitlab
from redminelib import Redmine


def read_config(path):
    try:
        # загружаем настройки
        config = configparser.ConfigParser()  # создаём объекта парсера
        config.readfp(codecs.open(path, "r", "utf8")) # читаем конфиг

        if 'Redmine' not in config:
            raise AttributeError('Redmine config not found')
        if 'redmine_host' not in config['Redmine']:
            raise AttributeError('redmine_host not found')
        if 'redmine_key' not in config['Redmine']:
            raise AttributeError('redmine_key not found')

        if 'Gitlab' not in config:
            raise AttributeError('Gitlab config not found')
        if 'gitlab_host' not in config['Gitlab']:
            raise AttributeError('gitlab_host not found')
        if 'gitlab_token' not in config['Gitlab']:
            raise AttributeError('gitlab_token not found')

    except AttributeError as ae:
        print('Config error: ')
        print(ae)
        return 1, None
    except Exception as e:
        traceback.print_exc()
        return 2, None
    return 0, config


def get_redmine(config):
    try:
        return 0, Redmine(config['Redmine']['redmine_host'],
                          key = config['Redmine']['redmine_key'])
    except Exception as e:
        traceback.print_exc()
        return 1, None


def get_gitlab(config):
    try:
        # private token or personal token authentication (self-hosted GitLab instance)
        gl = gitlab.Gitlab(url=config['Gitlab']['gitlab_host'],
                           private_token=config['Gitlab']['gitlab_token'])

        # make an API request to create the gl.user object. This is not required but may be useful
        # to validate your token authentication. Note that this will not work with job tokens.
        gl.auth()
    except Exception as e:
        traceback.print_exc()
        return 1, None
    return 0, gl


def get_students(spath):
    with open(spath, 'r', encoding='UTF-8') as sfile:
        headers = sfile.readline().strip().split('\t')
        name_id = -1 if 'lastname firstname' not in headers else headers.index('lastname firstname')
        stud_id = -1 if 'stud_xx' not in headers else headers.index('stud_xx')
        email_id = -1 if 'xxx@student.bmstu.ru' not in headers else headers.index('xxx@student.bmstu.ru')
        if name_id == -1 or stud_id == -1 or email_id == -1:
            print('Ошибка чтения заголовка! '
                  'Должны быть указаны lastname firstname, stud_xx и xxx@student.bmstu.ru '
                  'через символ табуляции')
            return 1, None
        telegram_id = -1 if 'telegram_id' not in headers else headers.index('telegram_id')
        rocketchat_id = -1 if 'rocketchat_id' not in headers else headers.index('rocketchat_id')
        redmine_id = -1 if 'redmine_id' not in headers else headers.index('redmine_id')
        gitlab_id = -1 if 'gitlab_id' not in headers else headers.index('gitlab_id')
        eu_id = -1 if 'eu_id' not in headers else headers.index('eu_id')
        students = []
        for student in sfile.readlines():
            data = student.split('\t')
            name = data[name_id].strip().split(' ')
            if len(name) == 3:
                fname, lname = name[1] + ' ' + name[2], name[0]
            elif len(name) == 2:
                fname, lname = name[1], name[0]
            else:
                print('Странное ФИО у студента: '+data[name_id].strip()+'не два или три слова, пропускаем...')
                continue
            stud = data[stud_id].strip()
            email = data[email_id].strip()
            tg = -1
            rc = -1
            rm = -1
            gl = -1
            eu = -1
            if telegram_id != -1: tg = data[telegram_id].strip()
            if rocketchat_id != -1: rc = data[rocketchat_id].strip()
            if redmine_id != -1: rm = data[redmine_id].strip()
            if gitlab_id != -1: gl = data[gitlab_id].strip()
            if eu_id != -1: eu = data[eu_id].strip()
            students.append({
                'fname': fname, 'lname': lname,
                'stud_id': stud, 'email': email,
                'telegram_id': str(tg), 'rocketchat_id': str(rc),
                'redmine_id': str(rm), 'gitlab_id': str(gl),
                'eu_id': str(eu)
            })

        return 0, students
