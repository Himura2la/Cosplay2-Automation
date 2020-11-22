#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import re
import sqlite3


class Validator(object):
    participant_number_fields = {'Количество участников', 'Количество представителей', 'Количество представителей (кроме помощников)'}
    capital_fields = {'Фамилия', 'Имя', 'Город'}
    required_participant_fields = capital_fields | {'Ник', 'Транскрипция ника (для ведущих)'}
    invalid_city_names = {'Орел', 'Щекино', 'Могилев', 'Королев'}

    members_sections = {'author', 'author_cosplay', 'members', 'members_cosplay', 'members_role'}
    optional_sections = members_sections | {'helpers'}

    def find_topic_section_ids(self, details, search_for):
        def check_section(s):
            if search_for == 'required':
                return '(необязательно' not in s['title'] and s['internal_name'] not in self.optional_sections
            if search_for == 'participants':
                return s['internal_name'] in self.members_sections
        return {s['id'] for s in details['sections'] if check_section(s)}

    def validate_participants(self, request, fields, details):
        errors = []
        try:
            expected_participants = filter(
                lambda f: f['title'] in self.participant_number_fields, fields).__next__()['value']
            expected_participants = int(expected_participants)
        except StopIteration:
            expected_participants = None
        except ValueError:
            errors.append('Не указано количество участников')
            expected_participants = None
        participant_topic_section_ids = self.find_topic_section_ids(details, 'participants')
        participant_request_section_ids = {int(rs['id']) for rs in details['reqsections'] if rs['topic_section_id'] in participant_topic_section_ids}
        if expected_participants is not None and expected_participants != len(participant_request_section_ids):
            errors.append('*Несоответствие количества участников*: заявлено: %d, добавлено: %d' %
                          (expected_participants, len(participant_request_section_ids)))
        unique_participants = set()
        for i, sec_id in enumerate(sorted(list(participant_request_section_ids))):
            p_data = list(filter(lambda f: f['request_section_id'] == sec_id, fields))
            participant_basic_info = tuple(f['value'] for f in sorted(filter(lambda f: f['title'] in self.capital_fields, p_data), key=lambda f: f['title']))
            if participant_basic_info in unique_participants:
                errors.append('Участник %s упоминается в заявке несколько раз' % (participant_basic_info,))
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
                errors.append('*Неправильное написание города*: %s' % city)

        for t, f in set((r['title'], r['value']) for r in filter(lambda f: f['title'] in self.capital_fields, fields)):
            if re.match(r'^[а-я].*', f):
                errors.append('%s *с маленькой буквы*: %s' % (t, f))

        required_sections = self.find_topic_section_ids(details, 'required')
        provided_sections = {rs['topic_section_id'] for rs in details['reqsections']}
        missing_sections = required_sections - provided_sections
        section_id_to_title = {f['id']: f['title'] for f in details['sections']}
        missing_section_titles = {section_id_to_title[missing_section_id] for missing_section_id in missing_sections}
        if missing_section_titles:
            errors.append('*Нет ни одной секции*: %s' % str(missing_section_titles))

        required_fields = {f['id'] for f in details['fields'] if '(необязательно' not in f['title'] and f['section_id'] in required_sections - missing_sections}
        image_sections = {s['id'] for s in details['sections'] if s['internal_name'] in ('image_main', 'files')}
        char_name_in_image = {f['id'] for f in details['fields'] if f['section_id'] in image_sections and f['type'] == 'text'}
        required_fields -= char_name_in_image
        provided_fields = {rf['topic_field_id'] for rf in details['reqvalues']}
        empty_fields = required_fields - provided_fields
        field_id_to_title = { f['id']: f['title'] for f in details['fields'] }
        empty_field_titles = { field_id_to_title[f_id] for f_id in empty_fields }
        if empty_field_titles:
            errors.append('*Пустые поля*: %s' % str(empty_field_titles))
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


if __name__ == '__main__':
    import os
    from yaml import load, FullLoader
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    config = load(open(os.path.join(root, 'config.yml'), 'r', encoding='utf-8').read(), Loader=FullLoader)
    db_path = config['db_path']
    report_path = config['report_path']
    report_md = "%s\n===\n\n" % os.path.basename(db_path)
    report_md += Validator().validate(db_path)
    try:
        import markdown
    except ImportError:
        print('[WARNING] Execute `pip install markdown` to generate true HTML !!!')
        report_html = '<pre>%s</pre>' % report_md
    else:
        print('Converting report to HTML...')
        report_html = markdown.markdown(report_md)
    report_html = '<!DOCTYPE html><html><head><meta charset="utf-8"></head>' \
                '<body>%s</body></html>' % report_html
    print('Saving report...')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_html)
