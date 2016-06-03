import os


cmd = 'nohup rsync -r homolog.scielo.br:/var/www/xml_scielo_br/bases/xml/$acron_issue_id/*.xml /bases/xml.000/serial/$acron_issue_id/base_xml/base_source&'

serial_path = '/bases/xml.000/serial/'

for acron in os.listdir(serial_path):
    if os.path.isdir(serial_path + '/' + acron):
        for issueid in os.listdir(serial_path + '/' + acron):
            acron_issue_id = acron + '/' + issueid
            if os.path.isdir(serial_path + '/' + acron_issue_id):
                print(acron_issue_id)
                if not os.path.isdir(serial_path + '/' + acron_issue_id + '/base_xml/base_source'):
                    os.makedirs(serial_path + '/' + acron_issue_id + '/base_xml/base_source')
                print(cmd.replace('$acron_issue_id', acron_issue_id))
                os.system(cmd.replace('$acron_issue_id', acron_issue_id))
