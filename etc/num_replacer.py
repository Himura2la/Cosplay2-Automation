import re

doc_path = '/home/himura/Downloads/prog.md'
out = '/home/himura/Downloads/prog_done.md'

pattern = re.compile('(^)(\d{1,2})(\\\. )', re.MULTILINE)
replacements = {
    '1': '301'
}


def replacer(match):
    head, body, tail = match[1], match[2], match[3]
    return head + replacements[body] + tail

doc = open(doc_path, 'r', encoding='utf-8').read()
result = re.sub(pattern, replacer, doc)
open(out, 'w', encoding='utf-8').write(result)