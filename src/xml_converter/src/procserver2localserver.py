import os, sys

acron = sys.argv[1]
issue_label = sys.argv[2]

serial = '/Volumes/nasshare/Shares/APP-ppe/SciELO/serial/'

issue_path = serial + '/' + acron + '/' + issue_label + '/base'

if os.path.exists(serial):
	if not os.path.exists(issue_path):
		os.makedirs(issue_path)

	os.system('rsync roberta.takenaka@192.168.1.82:/bases/xml.000/xmldata/col/scl/4proc/serial/' + acron + '/' + issue_label + '/windows/* ' + issue_path)


else:
	print('Conectar ao servidor local')
