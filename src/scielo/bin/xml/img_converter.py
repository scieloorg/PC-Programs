# coding=utf-8
import os
import sys

try:
    from PIL import Image
    IMG_CONVERTER = True
except:
    IMG_CONVERTER = False

valid_img_ext = ['.eps', '.tif', '.tiff']

src_path = ''
destination_path = ''

if len(sys.argv) == 3:
    ign, src_path, destination_path = sys.argv
elif len(sys.argv) == 2:
    src_path = sys.argv[1]
    destination_path = src_path

if src_path:
    if IMG_CONVERTER:

        if not os.path.isdir(destination_path):
            os.makedirs(destination_path)

        if os.path.isdir(src_path):
            print(os.listdir(src_path))
            images = [img for img in os.listdir(src_path) if img[img.rfind('.'):].lower() in valid_img_ext]
            print(images)

            for img in images:
                name = img[0:img.rfind('.')] + '.jpg'
                
                print(name)
                not_jpg_img = src_path + '/' + img
                jpg_img = destination_path + '/' + name

                try:
                    im = Image.open(not_jpg_img)
                    im.thumbnail(im.size)
                    im.save(jpg_img, "JPEG")
                except Exception as inst:
                    print('Unable to convert ')
                    print(not_jpg_img)
                    print('to')
                    print(jpg_img)
                    print(inst)
                    print('')
    else:
        print('PIL is not installed.')
else:
    print('Usage:')
    print('python img_converter.py <images_folder> <jpg_folder>')
