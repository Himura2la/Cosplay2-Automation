import re


def proc(string):
    r = re.compile(r"^\w{1,2} \d{3}[\.,] .*?$", re.MULTILINE)
    for match in re.findall(r, string):
        print(match)

proc("""

""")