#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import sqlite3


class Validator(object):
    participant_fields = {'Ваши данные', 'Остальные участники', 'Авторы', 'Представители', 'Члены команды'}
    participant_number_fields = {'Количество участников', 'Количество представителей', 'Количество представителей (кроме помощников)'}
    capital_fields = {'Фамилия', 'Имя', 'Отчество', 'Город'}
    required_fields = capital_fields | {'Ник'}
    invalid_city_names = {'Орел', 'Щекино', 'Могилев', 'Королев'}
    required_in_scenic_fields = {'Транскрипция ника (для ведущих)'}
    scenic_topic_ids = {3926, 3941, 3925, 3942, 3943, 3948, 3949, 3903, 3937, 3940, 3950, 3904, 3938, 3939, 3944}

    def validate_participants(self, request, fields):
        errors = []
        try:
            expected_participants = filter(
                lambda f: f['title'] in self.participant_number_fields, fields).__next__()['value']
            expected_participants = int(expected_participants)
        except StopIteration:
            expected_participants = 1
        except ValueError:
            errors.append('Не указано количество участников')
            expected_participants = None
        participants_data = list(filter(lambda f: f['section_title'] in self.participant_fields, fields))
        real_participant_ids = set(p['request_section_id'] for p in participants_data)
        if expected_participants is not None and expected_participants != len(real_participant_ids):
            errors.append('Несоответствие количества участников: заявлено: %d, добавлено: %d' %
                          (expected_participants, len(real_participant_ids)))
        for i, sec_id in enumerate(sorted(list(real_participant_ids))):
            p_data = list(filter(lambda f: f['request_section_id'] == sec_id, fields))
            ok_fields = set(d['title'] for d in p_data if d['value']
                                                          and (len(d['value']) > 1 or re.match(r'\w', d['value']))
                                                          and not d['value'].lower().startswith("нет"))
            required_fields = self.required_fields | (
                self.required_in_scenic_fields if request['topic_id'] in self.scenic_topic_ids else set())
            empty_fields = required_fields - ok_fields
            if empty_fields:
                errors.append('У участника %d не ' % (i + 1) +
                             ('заполнены поля %s' % str(empty_fields) if len(empty_fields) > 1
                                                                      else "заполнено поле '%s'" % empty_fields.pop()))
        return errors

    def validate_fields(self, _, fields):
        errors = []
        for city in set(r['value'] for r in filter(lambda f: f['title'] == 'Город', fields)):
            if city in self.invalid_city_names:
                errors.append('Неправильное написание города: %s' % city)

        for t, f in set((r['title'], r['value']) for r in filter(lambda f: f['title'] in self.capital_fields, fields)):
            if re.match(r'^[а-я].*', f):
                errors.append('%s с маленькой буквы: %s' % (t, f))

        return errors

    def validate_request(self, request, fields):
        validators = [
            self.validate_participants,
            self.validate_fields
        ]
        return [error for f in validators for error in f(request, fields)]

    def validate(self, db_path):
        report = ''
        with sqlite3.connect(db_path, isolation_level=None) as db:
            c = db.cursor()
            c.execute("PRAGMA encoding = 'UTF-8'")
            c.execute("SELECT [value] FROM settings WHERE key = 'subdomain'")
            event_name = c.fetchone()[0]
            c.execute("SELECT * FROM list")
            for topic in self.fetch_all(c):
                topic_report = ''
                c.execute("SELECT * FROM requests WHERE topic_id = ? AND status != 'disapproved'", [topic['id']])
                for req in self.fetch_all(c):
                    c.execute("SELECT * FROM [values] WHERE request_id = ?", [req['id']])
                    errors = self.validate_request(req, self.fetch_all(c))
                    if errors:
                        topic_report += "- В заявке [№ %d](https://%s.cosplay2.ru/orgs/requests/request/%s) %s :\n" % \
                              (req['number'], event_name, req['id'], self.iconize_status(req['status']))
                        prefix = '    - '
                        topic_report += prefix + ('\n' + prefix).join(errors) + '\n'
                if topic_report:
                    report += "\n### В разделе '%s':\n" % topic['title'] + topic_report
        return report

    @staticmethod
    def fetch_all(cursor):
        return [{cursor.description[i][0]: v for i, v in enumerate(d)} for d in cursor.fetchall()]

    @staticmethod
    def iconize_status(status):
        return {'pending':     '<span title="Проверяется">🗎</span>',
                'waiting':     '<span title="Нужен отклик">❓</span>',
                'materials':   '<span title="Досыл">⏳</span>',
                'review':      '<span title="Рассмотрена">👌</span>',
                'approved':    '<span title="Принята">✔️</span>',
                'disapproved': '<span title="Отклонена">❌</span>'}[status]
