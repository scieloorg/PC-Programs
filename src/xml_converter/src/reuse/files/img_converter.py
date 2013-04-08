import Image
import os, shutil

class ImageConverter:

    def __init__(self):
        pass

    def img_to_jpeg(self, img_path, jpg_path):
        errors = []
        files = os.listdir(img_path)
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)

        for f in files:
            jpg_filename = jpg_path + '/'+ f[0:f.rfind('.')] + '.jpg'
            img_filename = img_path + '/'+ f
            
            if f.endswith('.jpg'):
                if img_filename != jpg_filename:
                    shutil.copyfile(img_filename, jpg_filename)
            elif f.endswith('.tiff') or f.endswith('.tif') or f.endswith('.eps'):
                try:
                    im = Image.open(img_filename)
                    im.thumbnail(im.size)
                    im.save(jpg_filename, "JPEG")
                
                except Exception, e:
                    errors.append('Unable to convert ' + img_filename)
        return errors