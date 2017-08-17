# coding = utf-8

import os
from PIL import Image

from . import system
from . import encoding


#inkscape PATH/teste.svg --export-background=COLOR --export-area-drawing --export-area-snap --export-dpi=300 --export-png=PATH/leave2.png
def command():
    INKSCAPE_PATH = 'inkscape'
    commands_parts = [
        INKSCAPE_PATH,
        '"{}"',
        '--export-background=COLOR',
        '--export-area-drawing',
        '--export-area-snap',
        '--export-dpi=300',
        '--export-png="{}"'
    ]
    return ' '.join(commands_parts)


def svg2png(image_path, force=False):
    svg_files = [svg for svg in os.listdir(image_path) if svg.endswith('.svg')]

    if len(svg_files) == 0:
        encoding.display_message('\n'.join(sorted(os.listdir(image_path))))
        encoding.display_message('Nenhum arquivo .svg')
        return

    comm = command()
    for svg_file in svg_files:
        src = image_path + '/' + svg_file
        dest = image_path + '/' + svg_file.replace('.svg', '.png')

        if force is True or not os.path.isfile(dest):
            try:
                system.run_command(comm.format(src, dest))
                encoding.display_message(src + ' => ' + dest)
            except:
                encoding.display_message('Unable to run inkscape')


def png2tiff(image_path, force=False):
    png_files = [png for png in os.listdir(image_path) if png.endswith('.png')]

    if len(png_files) == 0:
        encoding.display_message('\n'.join(sorted(os.listdir(image_path))))
        encoding.display_message('Nenhum arquivo .png')
        return

    for png_file in png_files:
        src = image_path + '/' + png_file
        dest = image_path + '/' + png_file.replace('.png', '.tif')

        if force is True or not os.path.isfile(dest):
            try:
                Image.open(src).save(dest, "TIFF")
                encoding.display_message(src + ' => ' + dest)
            except IOError as e:
                encoding.report_exception('svg_conversion.png2tiff()', e, ("cannot convert", src, dest))


def convert_svg2png(img_filename, destination=None, force=False):
    if os.path.isfile(img_filename) and img_filename.endswith('.svg'):
        if destination is None:
            destination = os.path.dirname(img_filename)
        if not os.path.isdir(destination):
            os.makedirs(destination)
        fname = os.path.basename(img_filename)
        dest_filename = destination + '/' + fname + '.png'
        if force or not os.path.isfile(dest_filename):
            try:
                comm = command()
                system.run_command(comm.format(img_filename, dest_filename))
                encoding.display_message(img_filename + ' => ' + dest_filename)
            except:
                encoding.display_message('Unable to run inkscape')


def convert_png2tiff(img_filename, destination=None, force=False):
    if os.path.isfile(img_filename) and img_filename.endswith('.png'):
        if destination is None:
            destination = os.path.dirname(img_filename)
        if not os.path.isdir(destination):
            os.makedirs(destination)
        fname = os.path.basename(img_filename)
        dest_filename = destination + '/' + fname + '.tif'
        if force or not (os.path.isfile(dest_filename) or os.path.isfile(dest_filename + 't')):
            try:
                Image.open(img_filename).save(dest_filename, "TIFF")
                encoding.display_message(img_filename + ' => ' + dest_filename)
            except IOError as e:
                encoding.report_exception(
                    'convert_png2tiff()', e,
                    ("cannot convert", img_filename, dest_filename))
