import base64
import os
import sys
import shutil
from argparse import ArgumentParser
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from base64 import b64decode

cookie_var = 'NUCLINO_AUTH_COOKIE_BASE64'


def get_backup(cookie, workspace_id, zip_path):
    try:
        req = Request(
            f"https://files.nuclino.com/export/brains/{workspace_id}.zip?format=md",
            headers={'Cookie': cookie}
        )
        with urlopen(req) as response, open(zip_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return True
    except HTTPError as e:
        print(e, file=sys.stderr)
        return False


if __name__ == "__main__":
    parser = ArgumentParser(description='Nuclino workspace downloader')
    parser.add_argument('workspace_id', help='UUID from the EXPORT WORKSPACE link.')
    parser.add_argument('out_path', help='Path where to save the downloaded zip.')
    args = parser.parse_args(sys.argv[1:])

    if cookie_var not in os.environ:
        print(f'error: the {cookie_var} environment variable is required.', file=sys.stderr)
        exit(1)

    success = get_backup(b64decode(os.environ[cookie_var]).decode(), args.workspace_id, args.out_path)

    exit(0 if success else 2)
