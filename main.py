import argparse

import adderator as ad
import helpers as h

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Параметры запуска:')
    parser.add_argument('-i', '--fin', type=str, default='./students.csv',
                        help='Полный путь к входному файлу со студентами (по-умолчанию ./students.csv)')
    parser.add_argument('-o','--dout', type=str, default='.',
                        help='Полный путь к директории выходных файлов (по-умолчанию .)')
    parser.add_argument('-m', '--mode', type=int, default=0,
                        help='Режим запуска:\n'
                             '1 -- регистрация только в Redmine,\n'
                             '2 -- регистрация только в Gitlab,\n'
                             '0 -- регистрация во всех системах (по-умолчанию 0)')
    ns = parser.parse_args()
    print(ns)

    # читаем конфиги
    err_code, config = h.read_config('./settings.ini')
    if err_code != 0:
        print('Ошибка чтения настроечного файла settings.ini!')
        exit(err_code)
    else:
        print('Настроечный файл успешно прочитан...')

    # читаем студентов
    err_code, students = h.get_students(ns.fin)
    if err_code != 0:
        print('Ошибка чтения файла со студентами: '+ns.fin)
        exit(err_code)
    else:
        print('Файл со студентами успешно прочитан...')

    ad.add_students(students, ns.dout, ns.mode, config)


