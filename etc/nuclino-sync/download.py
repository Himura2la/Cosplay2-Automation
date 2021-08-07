import os
import sys
import shutil
from argparse import ArgumentParser
from urllib.error import HTTPError
from urllib.request import Request, urlopen

cookie_var = 'NUCLINO_AUTH_COOKIE'


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
    parser.add_argument('workspace-id', help='UUID from the EXPORT WORKSPACE link.')
    parser.add_argument('out-path', help='Path where to save the downloaded zip.')
    args = parser.parse_args(sys.argv[1:])

    if cookie_var not in os.environ:
        print(f'error: the {cookie_var} environment variable is required.', file=sys.stderr)
        exit(1)
    
    get_backup(os.environ[cookie_var], args.workspace_id, args.out_path)