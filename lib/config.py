from yaml import load, FullLoader
from os.path import join, dirname, realpath

__config_file_name = 'config.yml'

def read_config():
    return load(
        open(
            join(
                dirname(dirname(
                    realpath(__file__)
                )),
                __config_file_name
            ),
            'r',
            encoding='utf-8'
        ).read(),
        Loader=FullLoader
    )
