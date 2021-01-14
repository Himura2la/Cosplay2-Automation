import vk              # pip install --upgrade vk
from PIL import Image,ImageTk  # pip install --upgrade Pillow
import urllib.request
from io import BytesIO
import tkinter as tk
from time import sleep

class Application(tk.Frame):
    vk_api_v = '5.126'
    # https://oauth.vk.com/authorize?v=5.126&response_type=token&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,groups&client_id=7727805
    token = ""
    source_group = "tulaanimefest"
    target_group = "yuki_no_odori_10"
    add_friends = False
    start_at = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.canvas = tk.Canvas(master, width=130, height=50) 
        self.canvas.pack()

        self.captcha_code = tk.Entry(master)
        self.captcha_code.pack()

        self.captcha_submitted = tk.BooleanVar()
        self.master.bind('<Return>', self.submit_captcha)
        self.master.bind('<KP_Enter>', self.submit_captcha)

        self.inv = Inviter(self.vk_api_v, self.token)
        self.inv.collect_members(self.source_group, self.add_friends)
        self.inv.invite_all_members(self.target_group, self.input_captcha, self.start_at)
        self.master.destroy()

    def input_captcha(self, img):
        tk_image = ImageTk.PhotoImage(img)
        image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.itemconfig(image_on_canvas, image=tk_image)
        self.captcha_code.delete(0, 'end')
        self.captcha_code.focus()
        self.wait_variable(self.captcha_submitted)
        self.captcha_submitted.set(False)
        return self.captcha_code.get()

    def submit_captcha(self, _):
        self.captcha_submitted.set(True)


class Inviter(object):
    def __init__(self, vk_api_v, access_token):
        self.VK = vk.API(vk.Session(access_token=access_token))
        self.vk_api_v = vk_api_v

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

    def invite_all_members(self, target_group, solve_captcha_function, start_at=0):
        target_group = self.VK.groups.getById(v=self.vk_api_v, group_id=target_group, fields='id')[0]

        for i, user in enumerate(self.members_to_invite.items()):
            if i < start_at:
                continue
            self.__invite_member(i, user, target_group, solve_captcha_function)
            sleep(0.34)

    def __invite_member(self,
                        i,
                        user,
                        target_group,
                        solve_captcha_function,
                        retry_count=0,
                        captcha_sid=None,
                        captcha_key=None):
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
                print(e.message)
                if e.code == e.CAPTCHA_NEEDED:
                    with urllib.request.urlopen(e.captcha_img) as f:
                        img_bytes = f.read()
                    captcha_key = solve_captcha_function(Image.open(BytesIO(img_bytes)))
                    self.__invite_member(i, user, target_group, solve_captcha_function, retry_count + 1, e.captcha_sid, captcha_key)
                if e.code == 6:  # Too many requests per second
                    sleep(1)
                    self.__invite_member(i, user, target_group, solve_captcha_function, retry_count + 1)
                else:
                    pass

    @staticmethod
    def __massive_collect(api_function, **params):
        accumulator = []
        while True:
            api_response = api_function(offset=len(accumulator), **params)
            accumulator += api_response['items']
            if len(accumulator) >= api_response['count']:
                break
        return accumulator

Application(master=tk.Tk()).mainloop()
