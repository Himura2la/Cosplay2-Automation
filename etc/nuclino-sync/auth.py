import sys
from os import environ
from getpass import getpass
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from json import dumps
from base64 import b64encode, b64decode

cred_var = 'NUCLINO_CRED_BASE64'


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


def input_cred():
    email = input('email: ')
    passwd = getpass('password for ' + email + ': ')
    return dumps({'email': email,
                  'password': passwd,
                  'mfaCode': ''})


cred = environ.get(cred_var)
cred = b64decode(cred).decode() if cred else input_cred()
#base64_cred = b64encode(cred.encode())
print(b64encode(get_cookie(cred).encode()).decode())
