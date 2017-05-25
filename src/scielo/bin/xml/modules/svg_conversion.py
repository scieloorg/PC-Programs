# code = utf-8

import sys
import os

from PIL import Image


#inkscape PATH/teste.svg --export-background=COLOR --export-area-drawing --export-area-snap --export-dpi=300 --export-png=PATH/leave2.png

def command():
    INKSCAPE_PATH = 'inkscape'
    commands_parts = [
        INKSCAPE_PATH,
        '{}',
        '--export-background=COLOR',
        '--export-area-drawing',
        '--export-area-snap',
        '--export-dpi=300',
        '--export-png={}'
    ]
    return ' '.join(commands_parts)


def svg2png(image_path, force=False):
    svg_files = [svg for svg in os.listdir(image_path) if svg.endswith('.svg')]

    if len(svg_files) == 0:
        print('\n'.join(sorted(os.listdir(image_path))))
        print('Nenhum arquivo .svg')
        return

    comm = command()
    for svg_file in svg_files:
        src = image_path + '/' + svg_file
        dest = image_path + '/' + svg_file.replace('.svg', '.png')

        if force is True or not os.path.isfile(dest):
            try:
                os.system(comm.format(src, dest))
                print(src + ' => ' + dest)
            except:
                print('Unable to run inkscape')


def png2tiff(image_path, force=False):
    png_files = [png for png in os.listdir(image_path) if png.endswith('.png')]

    if len(png_files) == 0:
        print('\n'.join(sorted(os.listdir(image_path))))
        print('Nenhum arquivo .png')
        return

    for png_file in png_files:
        src = image_path + '/' + png_file
        dest = image_path + '/' + png_file.replace('.png', '.tif')

        if force is True or not os.path.isfile(dest):
            try:
                Image.open(src).save(dest, "TIFF")
                print(src + ' => ' + dest)
            except IOError:
                print("cannot convert", src, dest)

"""
if len(sys.argv) == 2:
    script, image_path = sys.argv
    if os.path.isdir(image_path):
        svg2png(image_path)
else:
    print('Usage: python {} <image path>'.format(sys.argv[0]))
"""
