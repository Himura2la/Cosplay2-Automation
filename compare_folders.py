import os
from zlib import crc32

orig_dir = r"D:\Fests Local\Yuki no Odori 7\Tracks0"
new_dir = r"D:\Fests Local\Yuki no Odori 7\Tracks"


orig_tree, new_tree = ({os.path.join(dirpath, filename).replace(root + os.sep, '') for dirpath, dirnames, filenames in os.walk(root) 
                                                                                   for filename in filenames} 
                       for root in (orig_dir, new_dir))

absent_in_orig = new_tree - orig_tree
absent_in_new = orig_tree - new_tree


common_files = new_tree & orig_tree

def csum(path):
    """ http://j2py.blogspot.ru/2014/09/python-generates-crc32-and-adler32.html """
    f = open(path, 'rb')
    csum = None
    try:
        chunk = f.read(1024)
        if len(chunk) > 0:
            csum = crc32(chunk)
            while True:
                chunk = f.read(1024)
                if len(chunk) > 0:
                    csum = crc32(chunk, csum)
                else:
                    break
    finally:
        f.close()
    if csum is not None:
        csum = csum & 0xffffffff
    return csum

different_files = set()
for path in common_files:
    print(path, end=' ', flush=True)
    orig_path, new_path = (os.path.join(root, path) for root in (orig_dir, new_dir))
    orig_size, new_size = (os.path.getsize(path) for path in (orig_path, new_path))
    orig_hash, new_hash = (csum(path) for path in (orig_path, new_path))
    if orig_size == new_size and orig_hash == new_hash:
        print('[ok]')
    else:
        print('[!!! DIFFERENT !!!]')
        different_files.add(path)

print('\n---')
print('absent_in_orig:', absent_in_orig)
print('absent_in_new:', absent_in_new)
print('different_files:', different_files)