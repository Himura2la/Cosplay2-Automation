import sys
from os import environ
from getpass import getpass
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from json import dumps
from base64 import b64encode, b64decode

cred_var = 'NUCLINO_CRED_BASE64'
cookie_var = 'NUCLINO_AUTH_COOKIE_BASE64'


def help():
    msg = f'usage: {sys.argv[0]} login|logout\n' + \
          f'env vars: - {cred_var} for login (optional)\n' + \
          f'          - {cookie_var} for logout'
    print(msg, file=sys.stderr)
    exit(1)


def get_cookie(cred):
    try:
        req = Request(
            "https://api.nuclino.com/api/users/auth",
            cred.encode('ascii'),
            {'X-Requested-With': 'XMLHttpRequest',
             'Content-Type': 'application/json'}
        )
        with urlopen(req) as resp:
            return resp.getheader('Set-Cookie')
    except HTTPError as e:
        print(e, file=sys.stderr)
        return None



def logout(cookie):
    try:
        req = Request(
            "https://api.nuclino.com/api/users/me/logout",
            method='POST',
            headers={'Cookie': cookie,
                     'X-Requested-With': 'XMLHttpRequest',
                     'Content-Type': 'application/json'}
        )
        with urlopen(req) as resp:
            return f'{resp.status} {resp.msg}: {resp.read().decode()}'
    except HTTPError as e:
        print(e, file=sys.stderr)
        return None



def input_cred():
    email = input('email: ')
    passwd = getpass('password for ' + email + ': ')
    return dumps({'email': email,
                  'password': passwd,
                  'mfaCode': ''})


if len(sys.argv) == 2:
    if sys.argv[1] == 'login':
        cred = environ.get(cred_var)
        cred = b64decode(cred).decode() if cred else input_cred()
        #base64_cred = b64encode(cred.encode())
        print(b64encode(get_cookie(cred).encode()).decode())
    elif sys.argv[1] == 'logout':
        cookie = environ.get(cookie_var)
        cookie = b64decode(cookie).decode() if cookie else help()
        print(logout(cookie))
    else:
        help()
else:
    help()

