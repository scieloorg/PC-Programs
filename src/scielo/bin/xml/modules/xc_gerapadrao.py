# coding=utf-8

import os
from datetime import datetime

import xc


def gerapadrao_get_inputs(args):
    # python gerapadrao.py <collection_acron>
    script = None
    collection_acron = None
    if len(args) == 2:
        script, collection_acron = args
    return (script, collection_acron)


def gerapadrao_validate_inputs(collection_acron):
    errors = []
    if collection_acron is None:
        errors.append('Missing collection acronym')
    return errors


def is_unblocked_gerapadrao(permission_file):
    ret = False
    if permission_file is not None:
        if os.path.isfile(permission_file):
            status = open(permission_file, 'r').read()
        else:
            status = 'FINISHED'
        if status != 'running':
            ret = True
    return ret


def block_gerapadrao(permission_file):
    open(permission_file, 'w').write('running')


def consume_collection_scilista(scilista_file):
    content = None
    if scilista_file is not None:
        if os.path.isfile(scilista_file):
            content = open(scilista_file, 'r').read()
            if not isinstance(content, unicode):
                content = content.decode('utf-8')
            os.unlink(scilista_file)
    return content


def clean_collection_scilista(scilista_file):
    if scilista_file is not None:
        if os.path.isfile(scilista_file):
            os.unlink(scilista_file)


def sort_scilista(scilista_content):
    scilista_items = list(set([item.strip() for item in scilista_content.split('\n') if len(item) if ' ' in item]))
    scilista_items = [item for item in scilista_items if item.endswith('pr')] + [item for item in scilista_items if not item.endswith('pr')]
    return '\n'.join(scilista_items) + '\n'


def gerapadrao(args):
    script, collection_acron = gerapadrao_get_inputs(args)
    errors = gerapadrao_validate_inputs(collection_acron)
    if len(errors) > 0:
        print(errors)
    else:
        config = xc.get_configuration(collection_acron)
        if config is not None:
            mailer = xc.get_mailer(config)
            start_time = datetime.now().isoformat()[11:11+5].replace(':', '')
            log_filename = './gerapadrao_' + collection_acron + '-' + start_time + '.log'
            if config.is_enabled_gerapadrao:
                if is_unblocked_gerapadrao(config.gerapadrao_permission_file):
                    config.update_title_and_issue()
                    scilista_content = consume_collection_scilista(config.collection_scilista)

                    if scilista_content is None:
                        print(config.collection_scilista + ' is empty')
                    else:
                        scilista_content = sort_scilista(scilista_content)
                        print(scilista_content)
                        scilista_items = scilista_content.split('\n')
                        print(scilista_items)

                        block_gerapadrao(config.gerapadrao_permission_file)
                        open(config.gerapadrao_scilista, 'w').write(scilista_content)
                        gerapadrao_cmd = gerapadrao_command(config.gerapadrao_proc_path, config.gerapadrao_permission_file)

                        if mailer is not None:
                            mailer.send_message(config.email_to, config.email_subject_gerapadrao.replace('Gerapadrao', 'Gerapadrao ' + start_time + ' '), config.email_text_gerapadrao + scilista_content)

                        open(log_filename, 'a+').write(datetime.now().isoformat() + ' ' + start_time + ' - inicio gerapadrao\n')
                        open(log_filename, 'a+').write(gerapadrao_cmd)
                        open(log_filename, 'a+').write(scilista_content)
                        os.system(gerapadrao_cmd)
                        #clean_collection_scilista(config.collection_scilista)
                        open(log_filename, 'a+').write(datetime.now().isoformat() + ' ' + start_time + ' - fim gerapadrao\n')

                        if config.is_enabled_transference:
                            open(log_filename, 'a+').write(datetime.now().isoformat() + ' ' + start_time + ' - inicio transf bases\n')
                            transfer_website_bases(config.local_web_app_path + '/bases', config.transference_user, config.transference_servers, config.remote_web_app_path + '/bases', log_filename)
                            open(log_filename, 'a+').write(datetime.now().isoformat() + ' ' + start_time + ' - fim transf bases\n')
                            open(log_filename, 'a+').write(datetime.now().isoformat() + ' ' + start_time + ' - inicio transf files\n')
                            transfer_website_files(config.local_web_app_path, config.transference_user, config.transference_servers, config.remote_web_app_path, scilista_items, log_filename)
                            open(log_filename, 'a+').write(datetime.now().isoformat() + ' ' + start_time + ' - fim transf files\n')
                        if mailer is not None:
                            mailer.send_message(config.email_to, config.email_subject_website_update.replace('Gerapadrao', 'Gerapadrao ' + start_time + ' '), config.email_text_website_update + scilista_content)
                else:
                    print('gerapadrao is running. Wait ...')
                    if mailer is not None:
                        if os.path.isfile(config.collection_scilista):
                            mailer.send_message(config.email_to_adm, 'gerapadrao is busy', open(config.collection_scilista, 'r').read())


def gerapadrao_command(proc_path, gerapadrao_status_filename):
    return 'cd ' + proc_path + ';./GeraPadrao.bat;echo FINISHED>' + gerapadrao_status_filename


def transfer_website_bases(local_bases_path, user, servers, remote_bases_path, log_filename):
    folders = ['artigo', 'issue', 'newissue', 'title']

    for folder in folders:
        for server in servers:
            xc.run_remote_mkdirs(user, server, remote_bases_path + '/' + folder, log_filename)
            xc.run_scp(local_bases_path + '/' + folder, user, server, remote_bases_path, log_filename)


def transfer_website_files(local_web_app_path, user, servers, remote_web_app_path, scilista_items, log_filename):
    scilista_items = [item.strip().split(' ') for item in scilista_items if ' ' in item]
    for acron, issue_id in scilista_items:
        for server in servers:
            transfer_issue_files(acron, issue_id, local_web_app_path, user, server, remote_web_app_path, log_filename)


def transfer_issue_files(acron, issue_id, local_web_app_path, user, server, remote_web_app_path, log_filename):
    # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
    issue_id_path = acron + '/' + issue_id

    folders = ['/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']

    for folder in folders:
        dest_path = remote_web_app_path + folder + issue_id_path
        source_path = local_web_app_path + folder + issue_id_path
        xc.run_remote_mkdirs(user, server, dest_path, log_filename)
        xc.run_rsync(source_path, user, server, dest_path, log_filename)
