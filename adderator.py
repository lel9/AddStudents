import random
import string
import traceback
from os.path import join
import helpers as h


def add_to_gitlab(student, gitlab):
    try:
        user = gitlab.users.create({'email': student['email'],
                                    'password': student['passw'],
                                    'username': student['stud_id'],
                                    'name': student['lname'] + ' ' + student['fname'],
                                    'external': True,
                                    'skip_confirmation': True})
        student['gitlab_id'] = str(user.id)

    except Exception:
        traceback.print_exc()
        return -1, student

    return 0, student


def add_to_redmine(student, redmine):
    try:
        user = redmine.user.create(
            login = student['stud_id'],
            password = student['passw'],
            firstname = student['fname'],
            lastname = student['lname'],
            mail = student['email'],
            mail_notification = 'none',
            must_change_passwd = True)
        student['redmine_id'] = str(user.id)

    except Exception:
        traceback.print_exc()
        return -1, student

    return 0, student


def random_pass(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def write_all(student, mode, gl_fpass, rm_fpass, stud_res):
    if mode == 1 or mode == 0:
        rm_fpass.write('\t'.join([student['lname'] + ' ' + student['fname'],
                                  student['stud_id'], student['passw']]))
        rm_fpass.write('\n')

    if mode == 2 or mode == 0:
        gl_fpass.write('\t'.join([student['lname'] + ' ' + student['fname'],
                                  student['stud_id'], student['passw']]))
        gl_fpass.write('\n')

    stud_res.write('\t'.join([student['stud_id'], student['email'], student['telegram_id'],
                              student['rocketchat_id'], student['redmine_id'],
                              student['gitlab_id'], student['eu_id']]))
    stud_res.write('\n')


def add_students(students, dout, mode, config):
    gl_passw_fname = 'gitlab_passw.csv'
    rm_passw_fname = 'redmine_passw.csv'
    stud_res_fname = 'students.csv'
    passw_len = 8

    try:
        err_code, gitlab = h.get_gitlab(config)
        if err_code != 0:
            print('Ошибка доступа к Gitlab!')
            return -1

        err_code, redmine = h.get_redmine(config)
        if err_code != 0:
            print('Ошибка доступа к Redmine!')
            return -1

        with open(join(dout, gl_passw_fname), 'w', encoding='UTF-8') as gl_fpass, \
                open(join(dout, rm_passw_fname), 'w', encoding='UTF-8') as rm_fpass, \
                open(join(dout, stud_res_fname), 'w', encoding='UTF-8') as stud_res:

            stud_res.write(
                'stud_xx	xxx@student.bmstu.ru	telegram_id	rocketchat_id	redmine_id	gitlab_id	eu_id\n')

            for student in students:

                student['passw'] = random_pass(passw_len)

                # в Redmine
                if mode == 1 or mode == 0:
                    err_code, student = add_to_redmine(student, redmine)
                    if err_code != 0:
                        print('Ошибка добавления студента '+student['stud_id']+' в Redmine!')
                        continue
                    else:
                        print('Студент '+student['stud_id']+' успешно добавлен в Redmine, '
                                                            'присвоен id='+student['redmine_id']+'...')


                # в Gitlab
                if mode == 2 or mode == 0:
                    err_code, student = add_to_gitlab(student, gitlab)
                    if err_code != 0:
                        print('Ошибка добавления студента '+student['stud_id']+' в Gitlab!')
                        continue
                    else:
                        print('Студент '+student['stud_id']+' успешно добавлен в Gitlab, '
                                                            'присвоен id='+student['gitlab_id']+'...')

                write_all(student, mode, gl_fpass, rm_fpass, stud_res)


    except Exception:
        traceback.print_exc()
        return 1

    return 0