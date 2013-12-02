import os
import sys

from reuse.input_output.parameters import Parameters

# read parameters of execution 
parameter_list = ['script', 'source', 'destination']
parameters = Parameters(parameter_list)
if parameters.check_parameters(sys.argv):
    script_name, src, dest = sys.argv

    folders = [
        ('bases/artigo', 'bases'),
        ('bases/title', 'bases'),
        ('bases/issue', 'bases'),
        ('bases/newissue', 'bases'),
        ('htdocs/img/*', 'htdocs/img/revistas'),
        ('bases/pdf/*', 'bases/pdf'),
        ('bases/xml/*', 'bases/xml'),
    ]

    for folder in folders:
        cmd = 'rsync -CrvK ' + src + '/' + folder[0] + ' ' + dest + '/' + folder[1]
        os.system(cmd)
