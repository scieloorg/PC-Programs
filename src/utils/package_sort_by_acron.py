
all_files = []
files = {}
for item in open('/Users/robertatakenaka/Documents/pacotes.txt', 'r').readlines():
    item = item.strip()
    if item.endswith('pr.zip'):
        pass
    elif 'ahead' in item:
        pass
    else:
        all_files.append(item)
        if len(item) > 0:
            print(item)
            name = item.split('-')
            print(name)
            if len(name) > 3:
                acron = name[2]
            else:
                acron = '_'
            if files.get(acron) is None:
                files[acron] = []
            files[acron].append(item)

w = []
for acron in sorted(files.keys()):
    for item in sorted(files[acron]):
        w.append(item)
open('/Users/robertatakenaka/Documents/pacotes_ordenados.txt', 'w').write('\n'.join(w))

controle = []
selection = []
not_found = []
sh = []
for item in open('/Users/robertatakenaka/Documents/reproc_v30.txt', 'r').readlines():
    item = item.strip()
    if not 'ahead' in item:
        print(item)
        if ' ' in item:
            found = False
            acron, issue = item.split(' ')
            if files.get(acron) is not None:
                if not issue.endswith('spe'):
                    issue = issue.replace('s', '-s')
                if 'v' in issue:
                    issue = issue.replace('v', '-')

                name = acron + issue.replace('n', '-0') + '.'
                print(name)

                for f in files[acron]:
                    print(f)
                    if name in f:
                        selection.append(f)
                        controle.append(item + '\t' + f)
                        found = True
                        sh.append('cp ' + f + ' ../xc2015_downloads')
                name = acron + issue.replace('n', '-') + '.'
                print(name)
                for f in files[acron]:
                    print(f)
                    if name in f:
                        selection.append(f)
                        found = True
                        controle.append(item + '\t' + f)
                        sh.append('cp ' + f + ' ../xc2015_downloads')
            if not found:
                controle.append(item + '\t')
                not_found.append(item)

selection = sorted(list(set(selection)))
not_selected = []
for item in all_files:
    if not item in selection:
        not_selected.append(item)

open('/Users/robertatakenaka/Documents/copy_pacotes_para_reprocessar.sh', 'w').write('mkdir -p ../reproc_v30\n' + '\n'.join(['mv ' + item + ' ../reproc_v30 ' for item in selection]))

open('/Users/robertatakenaka/Documents/pacotes_para_reprocessar.txt', 'w').write('\n'.join(selection))
open('/Users/robertatakenaka/Documents/pacotes_para_reprocessar_scilista_item_not_found.txt', 'w').write('\n'.join(not_found))
open('/Users/robertatakenaka/Documents/pacotes_para_reprocessar_file_not_selected.txt', 'w').write('\n'.join(not_selected))
open('/Users/robertatakenaka/Documents/pacotes_para_reprocessar_controle.txt', 'w').write('\n'.join(sorted(list(set(controle)))))
open('/Users/robertatakenaka/Documents/copy.txt', 'w').write('\n'.join(sh))
