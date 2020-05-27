# coding = utf-8

import os
try:
    from PIL import Image
except:
    Image = None
from prodtools.utils import system
from prodtools.utils import encoding


#inkscape PATH/teste.svg --export-background=COLOR --export-area-drawing --export-area-snap --export-dpi=300 --export-png=PATH/leave2.png
def command():
    """
    Executa se instalado
    """
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
    new_files = []
    for svg_file in svg_files:
        name, ext = os.path.splitext(svg_file)
        src = os.path.join(image_path, svg_file)
        dest = os.path.join(image_path, name + '.png')

        if force is True or not os.path.isfile(dest):
            try:
                encoding.display_message(src + ' => ' + dest)
                system.run_command(comm.format(src, dest))
                if os.path.isfile(dest):
                    new_files.append((src, dest))
                encoding.display_message(src + ' => ' + dest)
            except:
                encoding.display_message('Unable to run inkscape')
    return new_files


def png2tiff(image_path, force=False):
    png_files = [png for png in os.listdir(image_path) if png.endswith('.png')]
    if len(png_files) == 0:
        encoding.display_message('\n'.join(sorted(os.listdir(image_path))))
        encoding.display_message('Nenhum arquivo .png')
        return
    new_files = []
    for png_file in png_files:
        name, ext = os.path.splitext(png_file)
        src = os.path.join(image_path, png_file)
        dest = os.path.join(image_path, name + '.tif')
        if force is True or not os.path.isfile(dest):
            try:
                encoding.display_message(src + ' => ' + dest)
                Image.open(src).save(dest, "TIFF")
                if os.path.isfile(dest):
                    new_files.append((src, dest))
                encoding.display_message(src + ' => ' + dest)
            except IOError as e:
                encoding.report_exception('svg_conversion.png2tiff()', e, ("cannot convert", src, dest))
    return new_files
