import Image
import os, shutil


def img_to_jpeg(img_path, jpg_path):
    files = os.listdir(img_path)
    if not os.path.exists(jpg_path):
        os.makedirs(jpg_path)

    for f in files:
        jpg_filename = jpg_path + '/'+ f[0:f.rfind('.')] + '.jpg'
        hd_image_filename = img_path + '/'+ f
        
        if os.path.exists(jpg_filename):
            os.unlink(jpg_filename)
        
        if f.endswith('.jpg'):
            shutil.copyfile(hd_image_filename, jpg_filename)
        else:
            try:
                im = Image.open(hd_image_filename)
                im.thumbnail(im.size)
                im.save(jpg_filename, "JPEG")
            
            except Exception, e:
                print e
                print jpg_filename
        