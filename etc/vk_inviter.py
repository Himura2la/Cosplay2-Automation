#!/usr/bin/env python3
# Author: Himura Kazuto <himura@tulafest.ru>

from time import sleep
from io import BytesIO
from urllib.request import urlopen

# sudo apt install python3-tk
# pip install --user --upgrade PyYAML Pillow vk
import tkinter as tk
from PIL import Image, ImageTk
import vk


class Inviter(object):
    def __init__(self, access_token, solve_captcha_function):
        self.VK = vk.API(vk.Session(access_token=access_token))
        self.vk_api_v = '5.126'
        self.solve_captcha_function = solve_captcha_function

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

        for i, user in enumerate(self.members_to_invite.items()):
            if i < start_at:
                continue
            self.__invite_member(i, user, target_group)
            sleep(0.34)

    def __invite_member(self, i, user, target_group, retry_count=0, captcha_sid=None, captcha_key=None):
            user_id, user_info = user
            print(f'[ {i}/{len(self.members_to_invite) - 1} | {user_info["first_name"]} {user_info["last_name"]} ]', end=' ', flush=True)
            if retry_count > 3:
                print(f'Too many retries ({retry_count}), giving up')
                return False
            try:
                invite_response = self.VK.groups.invite(v=self.vk_api_v,
                                                        group_id=target_group['id'],
                                                        user_id=user_id,
                                                        captcha_sid=captcha_sid,
                                                        captcha_key=captcha_key)
                if invite_response == 1:
                    print(f'Invited to "{target_group["name"]}"')
                else:
                    print(invite_response)
            except vk.exceptions.VkAPIError as e:
                print(f'{e.message} (code {e.code})')
                if e.code == e.CAPTCHA_NEEDED:
                    with urlopen(e.captcha_img) as f:
                        img_bytes = f.read()
                    captcha_key = self.solve_captcha_function(Image.open(BytesIO(img_bytes)))
                    self.__invite_member(i, user, target_group, retry_count + 1, e.captcha_sid, captcha_key)
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



if __name__ == '__main__':
    import os
    from yaml import load, FullLoader

    root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    config = load(
        open(os.path.join(root_dir, 'config.yml'), 'r', encoding='utf-8').read(),
        Loader=FullLoader)
    vk_token = config['vk_token']

    captcha_scale_factor = 3
    source_group = config['inviter_source_group']
    target_group = config['inviter_target_group']
    add_friends = config['inviter_add_friends']
    start_at = config['inviter_start_at']

    captcha_size = (130*captcha_scale_factor, 50*captcha_scale_factor)
    manual_solver = CaptchaManualSolver(tk.Tk(), captcha_size)
    inviter = Inviter(vk_token, manual_solver.solve_captcha)
    inviter.collect_members(source_group, add_friends)
    inviter.invite_all_members(target_group, start_at)
    print("Done!")
