#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sqlite3

db_path = r"C:\Users\glago\Desktop\18-12-08_05-00-05.db"

event_name = 'tulafest'
participant_fields = {'Ваши данные', 'Остальные участники', 'Авторы', 'Представители', 'Члены команды'}
participant_number_fields = {'Количество участников', 'Количество представителей'}
required_fields = {'Фамилия', 'Имя', 'Отчество', 'Ник', 'Город'}


def validate_participants(_, fields):
    validation_result = True
    try:
        expected_participants = filter(lambda f: f['title'] in participant_number_fields, fields).__next__()['value']
        expected_participants = int(expected_participants)
    except StopIteration:
        expected_participants = 1
    except ValueError:
        print('Не указано количество участников')
        expected_participants = None
        validation_result = False
    participants_data = list(filter(lambda f: f['section_title'] in participant_fields, fields))
    real_participant_ids = set(p['request_section_id'] for p in participants_data)
    if expected_participants is not None and expected_participants != len(real_participant_ids):
        print("Несоответствие количества участников: заявлено: %d, добавлено: %d" %
              (expected_participants, len(real_participant_ids)))
        validation_result = False
    for i, sec_id in enumerate(sorted(list(real_participant_ids))):
        p_data = list(filter(lambda f: f['request_section_id'] == sec_id, fields))
        ok_fields = set(d['title'] for d in p_data if len(d['value']) > 0 and not d['value'].lower().startswith("нет"))
        empty_fields = required_fields - ok_fields
        if empty_fields:
            print('У участника %d не' % (i + 1) +
                  ('заполнены поля %s' % str(empty_fields) if len(empty_fields) > 1
                                                           else "заполнено поле '%s'" % empty_fields.pop()))
            validation_result = False
    return validation_result


def validate_required_fields(request, fields):
    validation_result = True
    if request['status'] != 'review':
        return True

    return validation_result


def validate_request(request, fields):
    validators = [
        validate_participants
        #validate_required_fields
    ]
    return all((f(request, fields) for f in validators))


def fetch_all(cursor):
    return [{cursor.description[i][0]: v for i, v in enumerate(d)} for d in c.fetchall()]


print('База данных: %s\n' % os.path.basename(db_path))
with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute("SELECT * FROM list")
    for topic in fetch_all(c):
        c.execute("SELECT * FROM requests WHERE topic_id = ? AND status != 'disapproved'", [topic['id']])
        for req in fetch_all(c):
            c.execute("SELECT * FROM [values] WHERE request_id = ?", [req['id']])
            if not validate_request(req, fetch_all(c)):
                print("В заявке раздела '%s' [№ %d](https://%s.cosplay2.ru/orgs/requests/request/%s)\n" %
                      (topic['title'], req['number'], event_name, req['id']))
    print('Done')

