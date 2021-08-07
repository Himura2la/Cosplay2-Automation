import sys
from getpass import getpass
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from json import dumps
from base64 import b64encode


def get_cookie(email):
    try:
        req = Request(
            "https://api.nuclino.com/api/users/auth",
            dumps({'email': email,
                   'password': getpass('password for ' + email + ': '),
                   'mfaCode': ''}).encode('ascii'),
            {'X-Requested-With': 'XMLHttpRequest',
             'Content-Type': 'application/json'}
        )
        with urlopen(req) as resp:
            return resp.getheader('Set-Cookie')
    except HTTPError as e:
        print(e, file=sys.stderr)
        return None


print(b64encode(get_cookie(input('email: ')).encode()).decode())
