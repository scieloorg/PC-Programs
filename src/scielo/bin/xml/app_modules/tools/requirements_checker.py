
def display_success(name):
    print('!'*30)
    print(name)
    print('Success')
    print('Requirements OK')
    print('!'*30)


def display_failure(name):
    print('?'*30)
    print(name)
    print('Failure')
    print('Requirements were not installed')
    print('?'*30)


try:
    import PIL
    display_success('PIL')
except:
    display_failure('PIL')


try:
    import packtools
    display_success('packtools')
except:
    display_failure('packtools')

