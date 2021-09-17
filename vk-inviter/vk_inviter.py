#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

from time import sleep
from io import BytesIO
from urllib.request import urlopen

import tkinter as tk
from PIL import Image, ImageTk
import vk


class Inviter(object):
    def __init__(self, access_token, solve_captcha_function, captchas_dir=None):
        self.VK = vk.API(vk.Session(access_token=access_token))
        self.solve_captcha_function = solve_captcha_function
        self.captchas_dir = captchas_dir

        self.vk_api_v = '5.126'
        self.members_to_invite = dict()

    def collect_members(self, source_group, add_friends=True):
        self.members_to_invite = []
        if source_group:
            self.members_to_invite += self.__massive_collect(self.VK.groups.getMembers,
                                                            v=self.vk_api_v,
                                                            group_id=source_group,
                                                            fields='id')
        if add_friends:
            self.members_to_invite += self.__massive_collect(self.VK.friends.get,
                                                            v=self.vk_api_v,
                                                            fields='id')

        self.members_to_invite = sorted(self.members_to_invite, key=lambda x: x['id'])
        self.members_to_invite = {user_info['id']: user_info for user_info in self.members_to_invite}

    def invite_all_members(self, target_group, start_at=0):
        target_group = self.VK.groups.getById(v=self.vk_api_v, group_id=target_group, fields='id')[0]

        if self.captchas_dir:
            os.makedirs(self.captchas_dir, exist_ok=True)

        for i, user in enumerate(self.members_to_invite.items()):
            if i < start_at:
                continue
            self.__invite_member(i, user, target_group)
            sleep(0.34)

    def __dump(self, captcha):
        captcha['img'].save(os.path.join(self.captchas_dir, captcha['key'] + '.jpg'))

    def __invite_member(self, i, user, target_group, retry_count=0, captcha=None):
            user_id, user_info = user
            print(f'[ {i}/{len(self.members_to_invite) - 1} | {user_info["first_name"]} {user_info["last_name"]} ]', end=' ', flush=True)
            if retry_count > 4:
                print(f'Слишком много попыток ({retry_count}), забиваем и идём дальше...')
                return False
            try:
                try:
                    invite_response = self.VK.groups.invite(v=self.vk_api_v,
                                                            group_id=target_group['id'],
                                                            user_id=user_id,
                                                            captcha_sid=captcha['sid'] if captcha else None,
                                                            captcha_key=captcha['key'] if captcha else None)
                    if captcha:
                        self.__dump(captcha)
                    if invite_response == 1:
                        print(f'Приглашён в "{target_group["name"]}"')
                    else:
                        print(invite_response)
                except vk.exceptions.VkAPIError as e:
                    if captcha and e.code != e.CAPTCHA_NEEDED:
                        self.__dump(captcha)
                    raise e
            except vk.exceptions.VkAPIError as e:
                print(f'{e.message} (ошибка {e.code})')
                if e.code == e.CAPTCHA_NEEDED:
                    with urlopen(e.captcha_img) as f:
                        img_bytes = f.read()
                    captcha_img = Image.open(BytesIO(img_bytes))
                    captcha_key = self.solve_captcha_function(captcha_img)
                    captcha = {'sid': e.captcha_sid, 'img': captcha_img, 'key': captcha_key}
                    self.__invite_member(i, user, target_group, retry_count + 1, captcha)
                if e.code == 6:  # Too many requests per second
                    sleep(1)
                    self.__invite_member(i, user, target_group, retry_count + 1)

    @staticmethod
    def __massive_collect(api_function, **params):
        accumulator = []
        while True:
            api_response = api_function(offset=len(accumulator), **params)
            accumulator += api_response['items']
            if len(accumulator) >= api_response['count']:
                break
        return accumulator


class CaptchaManualSolver(tk.Frame):
    def __init__(self, master, img_size):
        super().__init__(master)
        self.pack()

        self.img_size = img_size
        self.canvas = tk.Canvas(master, width=img_size[0], height=img_size[1]) 
        self.canvas.pack()

        self.key_input = tk.Entry(master)
        self.key_input.pack()

        self.captcha_submitted = tk.BooleanVar()
        master.bind('<Return>', self.__submit_captcha)
        master.bind('<KP_Enter>', self.__submit_captcha)

    def solve_captcha(self, img: Image):
        img = img.resize(self.img_size, Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(img)
        image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.itemconfig(image_on_canvas, image=tk_image)
        self.key_input.delete(0, 'end')
        self.key_input.focus()
        self.wait_variable(self.captcha_submitted)
        self.captcha_submitted.set(False)
        return self.key_input.get()

    def __submit_captcha(self, _):
        self.captcha_submitted.set(True)

try:
    if __name__ == '__main__':
        import os
        from sys import exit
        from subprocess import call
        from yaml import load, FullLoader

        base_config = """
# Это настройки Приглашатора.
# Данный файл можно открывать и редактировать программой "Блокнот".

# Для начала, необходимо организовать Приглашатору доступ к Вашей странице ВК.
# Пожалуйста, перейдите по ссылке и разрешите приложению доступ.
# https://oauth.vk.com/authorize?v=5.126&response_type=token&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,groups&client_id=7728992

# Должна открыться белая страница с предупреждением.
# Скопируйте из адресной строки длинный набор букв и цифр между 'access_token=' и '&expires_in'.

# Вставьте его сюда между кавычками.
vk_token: ""

# Через 24 часа этот токен перестанет работать и придётся повторить процедуру.
# Никому его не показывайте: токен можно использовать вместо пароля от Вашей страницы ВК.


# Теперь укажите из какой группы приглашать людей.
# Сейчас указана группа https://vk.com/tulaanimefest
# Замените слово tulaanimefest между кавычками на id своей группы.
inviter_source_group: "tulaanimefest"

# Далее, аналогичным образом, укажите КУДА приглашать людей.
# Помните, что массово приглашать можно только в мероприятие, организатором
# которого является указанная выше группа, а Вы должны быть админом этой группы.
inviter_target_group: "yuki_no_odori_10"

# Если Вы не хотите приглашать своих
# собственных друзей, замените True на False
inviter_add_friends: True

# Приглашатор умеет начинать рассылку приглашений с середины,
# так что поглядывайте на текущий номер. Если работа программы внезапно
# прервётся, Вы сможете указать его тут и продолжить рассылку.
inviter_start_at: 0

# В процессе рассылки, Вам придётся много вводить капчу. Капча очень маленькая,
# и для удобства будет увеличиваться в указанное здесь число раз.
inviter_captcha_scale_factor: 3
"""

        def load_config():
            config_name = 'config.yml'
            config_encoding = 'utf-8'
            script_dir = os.path.dirname(os.path.realpath(__file__))

            config_path = os.path.join(os.path.dirname(script_dir), config_name)
            if os.path.isfile(config_path):
                config = load(open(config_path, 'r', encoding=config_encoding).read(), Loader=FullLoader)
                config['__file_path'] = config_path
                return config

            with open(config_path, 'w', encoding=config_encoding) as f:
                f.write(base_config)
            config_path = os.path.realpath(config_path)
            print('Добро пожаловать в Приглашатор! Мы не нашли файл с настройками и создали его ' + 
                f'вот здесь:\n\n{config_path}\n\nСейчас файл настроек должен был открыться ' +
                'рядом в программе Блокнот.\n\nПожалуйста,\nотредактируйте файл настроек,\n' + 
                'сохраните его,\nзакройте блокнот (это окно закроется вместе с ним),\n' + 
                'и запустите Приглашатор ещё раз.')
            call(['notepad', config_path])
            exit(1)


        config = load_config()
        vk_token = config['vk_token']
        source_group = config['inviter_source_group']
        target_group = config['inviter_target_group']
        add_friends = config['inviter_add_friends']
        start_at = config['inviter_start_at']
        captcha_scale_factor = config['inviter_captcha_scale_factor']

        captchas_dir_name = 'vk_captchas'
        if os.name == 'posix':
            home_dir = os.path.expanduser('~')
            home_dir_desc = f'в "{home_dir}"'
        else:
            home_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop') 
            home_dir_desc = 'на рабочий стол'
        captchas_dir = os.path.join(home_dir, captchas_dir_name)

        captcha_size = (130*captcha_scale_factor, 50*captcha_scale_factor)
        manual_solver = CaptchaManualSolver(tk.Tk(), captcha_size)
        inviter = Inviter(vk_token, manual_solver.solve_captcha, captchas_dir)
        try:
            inviter.collect_members(source_group, add_friends)
        except vk.exceptions.VkAPIError as e:
            print('Похоже, что токен не работает... Вот, что про него говорит ВК:\n\n' + 
                f'{e.message} (ошибка {e.code})\n\n' +
                'Пожалуйста,\nзамените vk_token в открытом файле настроек,\n' +
                'сохраните его,\nзакройте блокнот (это окно закроется вместе с ним),\n' +
                'и запустите Приглашатор ещё раз.')
            call(['notepad', config['__file_path']])
            exit(1)

        inviter.invite_all_members(target_group, start_at)

        print('\nГотово! Мы сохранили все введённые Вами капчи ' +
            f'{home_dir_desc} в папку "{captchas_dir_name}".\n\n' + 
            'Если Вы хотите поспособствовать разработке автоматического ' + 
            'распознавателя капчи, заархивируйте эту папку и скиньте Химуре ' +
            '(например, в телегу: https://t.me/Himura_Kazuto).\n' + 
            'Если нет, то можно просто её удалить :(')

except Exception as e:
    import traceback
    print("К сожалению, произошла неведомая фигня.\nВот немного технических деталей...\n" +
          "пожалуйста, свяжитесь с Химурой (например, в телеге: https://t.me/Himura_Kazuto), " + 
          "и покажите ему это..\n")
    traceback.print_exc()
    input("\nПрограмма закроется, если нажать Enter. Больше она уже ничего не умеет...")
