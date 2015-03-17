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


def is_enabled(permission_file):
    ret = False
    if permission_file is not None:
        status = open(permission_file, 'r').read()
        if status != 'running':
            ret = True
    return ret


def disable(permission_file):
    open(permission_file, 'w').write('running')


def read_scilista(scilista_file):
    content = None
    if scilista_file is not None:
        if os.path.isfile(scilista_file):
            content = open(scilista_file, 'r').read()
            os.unlink(scilista_file)
    return content


def sort_scilista(scilista_content):
    scilista_items = list(set([item.strip() for item in scilista_content.split()]))
    return [item for item in scilista_items if ' pr' in item] + [item for item in scilista_items if not ' pr' in item]


def gerapadrao(args):
    collection_acron = gerapadrao_get_inputs(args)
    errors = gerapadrao_validate_inputs(collection_acron)
    if len(errors) > 0:
        print(errors)
    else:
        config = xc.get_configuration(collection_acron)
        if config is not None:
            if config.is_enabled_gerapadrao:
                if is_enabled(config.gerapadrao_permission_file):
                    config.update_title_and_issue()
                    scilista_content = read_scilista(config)
                    if len(scilista_content) > 0:
                        disable(config.gerapadrao_permission_file)
                        s = sort_scilista(scilista_content) + '\n'
                        print(s)
                        open(config.gerapadrao_scilista, 'w').write(s)
                        gerapadrao_cmd = gerapadrao_command(config.gerapadrao_proc_path, config.gerapadrao_permission_file)

                        open('./gerapadrao.log', 'w').write(datetime.now().isoformat() + ' - inicio gerapadrao')
                        os.system(gerapadrao_cmd)
                        open('./gerapadrao.log', 'a+').write(datetime.now().isoformat() + ' - fim gerapadrao')

                        if config.is_enabled_transference:
                            open('./gerapadrao.log', 'a+').write(datetime.now().isoformat() + ' - inicio transf')

                            for item in s.split('\n'):
                                item = item.strip()
                                acron, issue_id = item.split(' ')
                                transfer_website_files(acron, issue_id, config.local_web_app_path, config.transference_user, config.transference_server, config.remote_web_app_path)

                            transfer_website_bases(config.local_web_app_path + '/bases', config.transference_user, config.transference_server, config.remote_web_app_path + '/bases')
                    else:
                        print('scilista_file is empty')
                else:
                    print('gerapadrao is busy. Wait ...')


def gerapadrao_command(proc_path, gerapadrao_status_filename):
    return 'cd ' + proc_path + ';./GeraPadrao.bat;echo FINISHED> ' + gerapadrao_status_filename


def run_remote_mkdirs(user, server, path):
    os.system('ssh ' + user + '@' + server + ' "mkdir -p ' + path + '"')


def run_rsync(source, user, server, dest):
    os.system('nohup rsync -CrvK ' + source + '/* ' + user + '@' + server + ':' + dest + '&')


def transfer_website_files(acron, issue_id, local_web_app_path, user, server, remote_web_app_path):
    # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
    issue_id_path = acron + '/' + issue_id

    folders = ['/htdocs/reports/', '/htdocs/img/revistas/', '/bases/pdf/', '/bases/xml/']

    for folder in folders:
        dest_path = remote_web_app_path + folder + issue_id_path
        source_path = local_web_app_path + folder + issue_id_path
        run_remote_mkdirs(user, server, dest_path)
        run_rsync(source_path, user, server, dest_path)


def transfer_website_bases(local_bases_path, user, server, remote_bases_path):
    # 'rsync -CrvK img/* user@server:/var/www/...../revistas'
    folders = ['artigo', 'issue', 'newissue', 'title']

    for folder in folders:
        run_remote_mkdirs(user, server, remote_bases_path)
        run_rsync(local_bases_path + '/' + folder, user, server, remote_bases_path)
