#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import re
import sqlite3


class Validator(object):
    participant_fields = {'Ваши данные', 'Остальные участники', 'Авторы', 'Представители', 'Члены команды'}
    participant_number_fields = {'Количество участников', 'Количество представителей', 'Количество представителей (кроме помощников)'}
    capital_fields = {'Фамилия', 'Имя', 'Отчество', 'Город'}
    required_participant_fields = capital_fields | {'Ник', 'Транскрипция ника (для ведущих)'}
    invalid_city_names = {'Орел', 'Щекино', 'Могилев', 'Королев'}

    def validate_participants(self, request, fields, details):
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
        participant_sections = set(p['request_section_id'] for p in participants_data)
        if expected_participants is not None and expected_participants != len(participant_sections):
            errors.append('Несоответствие количества участников: заявлено: %d, добавлено: %d' %
                          (expected_participants, len(participant_sections)))
        unique_participants = set()
        for i, sec_id in enumerate(sorted(list(participant_sections))):
            p_data = list(filter(lambda f: f['request_section_id'] == sec_id, fields))
            participant_basic_info = tuple(f['value'] for f in sorted(filter(lambda f: f['title'] in self.capital_fields, p_data), key=lambda f: f['title']))
            if participant_basic_info in unique_participants:
                errors.append('Участник %s упомянается в заявке несколько раз' % (participant_basic_info,))
            else:
                unique_participants.add(participant_basic_info)
            ok_fields = set(d['title'] for d in p_data if d['value']
                                                          and (len(d['value']) > 1 or re.match(r'\w', d['value']))
                                                          and not d['value'].lower().startswith("нет"))
            all_fields = {f['title'] for f in details['fields']}
            not_applicable_fields = self.required_participant_fields - all_fields
            required_fields = self.required_participant_fields - not_applicable_fields
            empty_fields = required_fields - ok_fields
            if empty_fields:
                errors.append('У участника %d не ' % (i + 1) +
                             ('заполнены поля %s' % str(empty_fields) if len(empty_fields) > 1
                                                                      else "заполнено поле '%s'" % empty_fields.pop()))
        return errors

    def validate_fields(self, request, fields, details):
        errors = []
        for city in set(r['value'] for r in filter(lambda f: f['title'] == 'Город', fields)):
            if city in self.invalid_city_names:
                errors.append('Неправильное написание города: %s' % city)

        for t, f in set((r['title'], r['value']) for r in filter(lambda f: f['title'] in self.capital_fields, fields)):
            if re.match(r'^[а-я].*', f):
                errors.append('%s с маленькой буквы: %s' % (t, f))

        return errors

    def validate_request(self, request, fields, details_string):
        details = json.loads(details_string)
        validators = [
            self.validate_participants,
            self.validate_fields
        ]
        return [error for f in validators for error in f(request, fields, details)]

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
                    values = self.fetch_all(c)
                    c.execute("SELECT json FROM details WHERE request_id = ?", [req['id']])
                    details = c.fetchone()
                    errors = self.validate_request(req, values, details[0] if len(details) == 1 else None)
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
