
import reuse.img_to_jpg as img_to_jpg
from reuse.input_output.parameters import Parameters
import sys
import os, shutil

required_parameters = ['', 'images path', 'jpg path' ]

parameters = Parameters(required_parameters)
if parameters.check_parameters(sys.argv):
    sys.argv = [ arg.replace('\\', '/') for arg in sys.argv  ]
    ign, img_path, jpg_path = sys.argv
    if not '/' in jpg_path:
        jpg_path = os.getcwd() + '/' + jpg_path
    if not '/' in img_path:
        img_path = os.getcwd() + '/' + img_path

    img_to_jpg.img_to_jpeg(img_path, jpg_path)

    print('\n'.join(os.listdir(jpg_path)))