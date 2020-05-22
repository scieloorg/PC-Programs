import sys

from prodtools import xc
from prodtools.utils import encoding


def requirements_checker():
    required = []
    try:
        import PIL
    except:
        required.append('PIL')
    try:
        import packtools
    except:
        required.append('packtools')
    return required


if __name__ == '__main__':
    parameters = encoding.fix_args(sys.argv)
    reqs = requirements_checker()
    if reqs:
        print('\n'.join(['not found: {}'.format(req) for req in reqs]))
    xc.call_converter(parameters, '1.1')
