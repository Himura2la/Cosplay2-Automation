from thefuzz import process


def main(items_string):
    items = [i.lower().replace('the ', '') for i in items_string.split('\n') if i]
    for item in items:
        
        # if len(item) > 17 or len(item) < 5:
        #     print(item)
        # continue

        rest = [i for i in items if i != item]
        candidates = process.extract(item, rest, limit=3)
        if any((c[1] > 75 for c in candidates)):
            print(item, candidates)
        pass

main("""

""")