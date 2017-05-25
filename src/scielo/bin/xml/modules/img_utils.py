# coding=utf-8
import os

from PIL import Image

from . import svg_conversion

IMDEBUGGING = False


def is_tiff(img_filename):
    return os.path.splitext(img_filename)[1] in ['.tiff', '.tif']


def tiff_image(img_filename):
    if is_tiff(img_filename):
        if os.path.isfile(img_filename):
            try:
                return Image.open(img_filename)
            except:
                return None


def hdimg_to_jpg(source_image_filename, jpg_filename):
    if IMG_CONVERTER:
        try:
            im = Image.open(source_image_filename)
            im.thumbnail(im.size)
            im.save(jpg_filename, "JPEG")
        except Exception as inst:
            utils.display_message('Unable to generate ' + jpg_filename)
            utils.display_message(inst)


#FIXME
def hdimages_to_jpeg(source_path, jpg_path, force_update=False):
    if IMG_CONVERTER:

        for item in os.listdir(source_path):
            image_filename = source_path + '/' + item
            if item.endswith('.tiff') or item.endswith('.eps') or item.endswith('.tif'):
                jpg_filename = source_path + '/' + item[0:item.rfind('.')] + '.jpg'
                doit = True if not os.path.isfile(jpg_filename) else force_update is True

                if doit:
                    hdimg_to_jpg(image_filename, jpg_filename)


def svg2png(images_path):
    svg_conversion.svg2png(images_path)


def png2tiff(images_path):
    svg_conversion.png2tiff(images_path)

    