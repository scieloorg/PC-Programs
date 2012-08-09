import Image
import os

class ImageConverter:

    def __init__(self):
        pass

    def img_to_jpeg(self, img_path, jpg_path, replace = False):
        files = os.listdir(img_path)
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)

        for f in files:
            if f.endswith('.tif') or f.endswith('.tiff') or f.endswith('.eps'):
                tiff_filename = img_path + '/'+ f
                jpg_filename = jpg_path + '/'+ f[0:f.rfind('.')] + '.jpg'

                doit = True
                if os.path.exists(jpg_filename):
                    if replace:
                        os.unlink(jpg_filename)
                    else:
                        doit = False
                
                if doit:
                    try:
                        im = Image.open(tiff_filename)
                        im.thumbnail(im.size)
                        im.save(jpg_filename, "JPEG")
                    except Exception, e:
                        print e
                        print jpg_filename
                