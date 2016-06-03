# coding = utf-8

import os
from PIL import Image


IMAGE_FORMATS = ['gif', 'jpg', 'png', 'tif']
VIDEO_FORMATS = ['mp4', 'mpeg', 'avi', 'wmv']
AUDIO_FORMATS = ['mp3', 'wav', 'mpa', 'wma']
TEXT_FORMATS = ['html', 'txt']


SIMPLE_IMAGE = 'imagem simples'
COMPLEX_IMAGE = 'imagem complexa'
IMAGE_TYPE = 'image'
VIDEO_TYPE = 'video'
AUDIO_TYPE = 'audio'
OTHER_TYPE = 'outro'
TEXT_TYPE = 'text'

web_path = '/var/www/scielo_br/'
web_path_alt = '/bases/xml.000/'
dam_folders = ['htdocs/img/revistas/']
result_file = '/home/roberta.takenaka/dam.csv'


def x_rgb(img_path):
    _rgb = {}
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            k = '-'.join([str(9000 + item)[1:] for item in [r, g, b]])
            if not k in _rgb.keys():
                _rgb[k] = 0
            _rgb[k] += 1
    return _rgb


def rgb(img_path):
    _rgb = []
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            k = '-'.join([str(9000 + item)[1:] for item in [r, g, b]])
            if not k in _rgb:
                _rgb.append(k)
            if len(_rgb) > 4:
                break
        if len(_rgb) > 4:
            break
    return _rgb


def image_type(_rgb):
    if len(_rgb) > 4:
        dam_type = COMPLEX_IMAGE
    else:
        dam_type = SIMPLE_IMAGE
    return dam_type


def evaluate_rgb(_rgb):
    colors_count = len(_rgb)
    r = []
    if isinstance(_rgb, list):
        r = [str(len(_rgb))]
    elif isinstance(_rgb, dict):
        for k in sorted(_rgb.keys()):
            r.append(k + '\t' + str(_rgb[k]))
    return str(colors_count) + '\n' + '\n'.join(r)


def find_out_type(dam_file, format):
    if format in IMAGE_FORMATS:
        dam_type = IMAGE_TYPE
    elif format in AUDIO_FORMATS:
        dam_type = AUDIO_TYPE
    elif format in VIDEO_FORMATS:
        dam_type = VIDEO_TYPE
    elif format in TEXT_FORMATS:
        dam_type = TEXT_TYPE
    else:
        dam_type = OTHER_TYPE
    return dam_type

open(result_file, 'w').write('')
main_path = web_path if os.path.isdir(web_path) else web_path_alt
for dam_folder in dam_folders:
    dam_path = main_path + dam_folder
    for journal_acron in os.listdir(dam_path):
        journal_dam_path = dam_path + '/' + journal_acron
        if os.path.isdir(journal_dam_path):
            for issue_id in os.listdir(journal_dam_path):
                if os.path.isdir(journal_dam_path):
                    issue_dam_path = journal_dam_path + '/' + issue_id
                    dam_items = []
                    for doc_dam_file in os.listdir(issue_dam_path):
                        # src, formato, tipo (imagem, video, audio), natureza, manifestacoes, tamanho
                        doc_dam_path = issue_dam_path + '/' + doc_dam_file
                        print(doc_dam_path)
                        if os.path.isfile(doc_dam_path):
                            dam_info = os.stat(doc_dam_path)
                            r = []
                            eval_rgb = ''
                            r.append(journal_acron)
                            r.append(issue_id)
                            r.append(issue_dam_path)
                            r.append(doc_dam_file)
                            format = doc_dam_file[doc_dam_file.rfind('.')+1:].lower().replace('jpeg', 'jpg').replace('tiff', 'tif')
                            r.append(format)
                            dam_type = find_out_type(doc_dam_path, format)
                            if dam_type == IMAGE_TYPE:
                                _rgb = rgb(doc_dam_path)
                                dam_type = image_type(_rgb)
                                eval_rgb = evaluate_rgb(_rgb)
                            r.append(eval_rgb)
                            r.append(dam_type)
                            r.append(str(dam_info.st_size))
                            print(r)
                            dam_items.append('\t'.join(r))
                        else:
                            for html_item in os.listdir(doc_dam_path):
                                r = []
                                r.append(journal_acron)
                                r.append(issue_id)
                                r.append(doc_dam_path)
                                r.append(html_item)
                                format = html_item[html_item.rfind('.')+1:].lower().replace('jpeg', 'jpg').replace('tiff', 'tif').replace('htm', 'html')
                                r.append(format)
                                r.append(find_out_type(html_item, format))
                                r.append('')
                                r.append(str(dam_info.st_size))
                                dam_items.append('\t'.join(r))

                    content = '\n'.join(dam_items)
                    open(result_file, 'a+').write(content.encode('utf-8'))
