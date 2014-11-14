import xpmaker

xpmaker.load_markup_tags()
print(xpmaker.markup_tags)


print(xpmaker.fix_uppercase_tag('<BOLD></BOLd>'))
print(xpmaker.fix_uppercase_tag('<ITALIC ALT=""></BOLd>'))
