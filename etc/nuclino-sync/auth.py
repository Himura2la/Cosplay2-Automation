from getpass import getpass
from urllib.error import HTTPError
from urllib.request import urlopen, Request
from json import dumps

def get_cookie(email):
    try:
        with urlopen("https://api.nuclino.com/api/users/auth",
                     dumps({'email': email,
                            'password': getpass('Password for ' + email + ': '),
                            'mfaCode': ''})
                     .encode('ascii')) as r:
            return r.getheader('Set-Cookie')
    except HTTPError as e:
        print(e)
        return None

print(get_cookie(input('email: ')))
