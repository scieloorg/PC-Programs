# code = utf-8

new = []
for item in open('country-names', 'r').readlines():
    items = [c for c in item.strip()]
    items.reverse()
    new.append(''.join(items))
