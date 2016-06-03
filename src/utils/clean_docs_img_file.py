import os


rst_path = '/Users/robertatakenaka/github.com/scieloorg/PC-Programs/docs/source'
img_path = '/Users/robertatakenaka/github.com/scieloorg/PC-Programs/docs/source/img'

rst_content = ''.join([open(rst_path + '/' + f).read() for f in os.listdir(rst_path) if os.path.isfile(rst_path + '/' + f) and f.endswith('.rst')])
img_files = [f for f in os.listdir(img_path) if os.path.isfile(img_path + '/' + f)]

for img_file in img_files:
    if not img_file in rst_content:
        print('mv source/img/' + img_file + ' old_img/')
