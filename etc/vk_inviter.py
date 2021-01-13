import vk              # pip install --upgrade vk
from PIL import Image  # pip install --upgrade Pillow
import urllib.request
from io import BytesIO
import tkinter as tk
from time import sleep

class Application(tk.Frame):
    # https://oauth.vk.com/authorize?v=5.126&response_type=token&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,groups&client_id=6707298
    token = ""
    source_group = "tulaanimefest"
    target_group = "yuki_no_odori_10"

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.inv = Inviter(self.token)
        self.inv.collect_members(None, True)
        self.inv.invite_all(self.target_group, self.input_captcha)

    def input_captcha(self, img):
        
        return ""


class Inviter(object):
    vk_api_v = '5.126'

    def __init__(self, access_token):
        self.VK = vk.API(vk.Session(access_token=access_token))

    def invite_all(self, target_group, input_captcha, skip_first=0):
        target_group = self.VK.groups.getById(v=self.vk_api_v, group_id=target_group, fields='id')[0]

        for i, user in enumerate(self.members_to_invite.items()):
            if i < skip_first:
                continue
            self.invite_member(i, user, target_group, input_captcha)
            #sleep(0.3)

    def invite_member(self, i, user, target_group, input_captcha, retry_count=0):
            user_id, user_info = user
            print(f'[ {i}/{len(self.members_to_invite)} | {user_info["first_name"]} {user_info["last_name"]} ]', end=' ', flush=True)
            if retry_count > 2:
                print('Too many retries, giving up')
                return False
            try:
                invite_response = self.VK.groups.invite(v=self.vk_api_v, group_id=target_group['id'], user_id=user_id)
                if invite_response == 1:
                    print(f'Invited to "{target_group["name"]}"')
                else:
                    print(invite_response)
            except vk.exceptions.VkAPIError as e:
                if e.code == e.CAPTCHA_NEEDED:
                    with urllib.request.urlopen(e.captcha_img) as f:
                        img_bytes = f.read()
                    img = Image.open(BytesIO(img_bytes))
                    captcha_code = input_captcha(img)
                    pass # todo
                if e.code == 6:  # Too many requests per second
                    print(e.message)
                    sleep(0.5)
                    self.invite_member(i, user, target_group, retry_count + 1)
                else:
                    print(e.message)

    def collect_members(self, source_group, add_friends=True):
        self.members_to_invite = []
        if source_group:
            self.members_to_invite += self.massive_collect(self.VK.groups.getMembers, v=self.vk_api_v, group_id=source_group, fields='id')
        if add_friends:
            self.members_to_invite += self.massive_collect(self.VK.friends.get, v=self.vk_api_v, fields='id')

        self.members_to_invite = sorted(self.members_to_invite, key=lambda x: x['id'])
        self.members_to_invite = {user_info['id']: user_info for user_info in self.members_to_invite}

    @staticmethod
    def massive_collect(api_call, **params):
        accumulator = []
        while True:
            api_response = api_call(offset=len(accumulator), **params)
            accumulator += api_response['items']
            if len(accumulator) >= api_response['count']:
                break
        return accumulator


app = Application(master=tk.Tk())
app.mainloop()



