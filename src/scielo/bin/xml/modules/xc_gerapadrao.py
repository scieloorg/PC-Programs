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


def read_collection_scilista(scilista_file):
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
    scilista_items = list(set([item.strip() for item in scilista_content.split('\n')]))
    scilista_items = [item for item in scilista_items if ' pr' in item] + [item for item in scilista_items if not ' pr' in item]
    return '\n'.join(scilista_items) + '\n'


def gerapadrao(args):
    script, collection_acron = gerapadrao_get_inputs(args)
    errors = gerapadrao_validate_inputs(collection_acron)
    if len(errors) > 0:
        print(errors)
    else:
        config = xc.get_configuration(collection_acron)
        if config is not None:
            if config.is_enabled_gerapadrao:
                if is_unblocked_gerapadrao(config.gerapadrao_permission_file):
                    config.update_title_and_issue()
                    scilista_content = read_collection_scilista(config.collection_scilista)
                    if scilista_content is None:
                        print(config.collection_scilista + ' is empty')
                    else:
                        scilista_content = sort_scilista(scilista_content)
                        print(scilista_content)

                        block_gerapadrao(config.gerapadrao_permission_file)
                        open(config.gerapadrao_scilista, 'w').write(scilista_content)
                        gerapadrao_cmd = gerapadrao_command(config.gerapadrao_proc_path, config.gerapadrao_permission_file)

                        mailer = xc.get_mailer(config)
                        if mailer is not None:
                            mailer.send_message(config.email_to, config.email_subject_gerapadrao, config.email_text_gerapadrao + scilista_content)

                        open('./gerapadrao.log', 'w').write(datetime.now().isoformat() + ' - inicio gerapadrao\n')
                        os.system(gerapadrao_cmd)
                        clean_collection_scilista(config.collection_scilista)
                        open('./gerapadrao.log', 'a+').write(datetime.now().isoformat() + ' - fim gerapadrao\n')

                        if config.is_enabled_transference:
                            open('./gerapadrao.log', 'a+').write(datetime.now().isoformat() + ' - inicio transf bases\n')
                            transfer_website_bases(config.local_web_app_path + '/bases', config.transference_user, config.transference_server, config.remote_web_app_path + '/bases')
                            open('./gerapadrao.log', 'a+').write(datetime.now().isoformat() + ' - fim transf bases\n')

                            #transfer_website_files(config.local_web_app_path + '/bases', config.transference_user, config.transference_server, config.remote_web_app_path + '/bases')
                            #open('./gerapadrao.log', 'a+').write(datetime.now().isoformat() + ' - fim transf\n')

                        if mailer is not None:
                            mailer.send_message(config.email_to, config.email_subject_website_update, config.email_text_website_update + scilista_content)

                else:
                    print('gerapadrao is running. Wait ...')


def gerapadrao_command(proc_path, gerapadrao_status_filename):
    return 'cd ' + proc_path + ';./GeraPadrao.bat;echo FINISHED>' + gerapadrao_status_filename


def transfer_website_bases(local_bases_path, user, server, remote_bases_path):
    folders = ['artigo', 'issue', 'newissue', 'title']

    for folder in folders:
        xc.run_remote_mkdirs(user, server, remote_bases_path + '/' + folder)
        xc.run_scp(local_bases_path + '/' + folder, user, server, remote_bases_path)
