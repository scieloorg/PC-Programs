# code = utf-8
import os

scilista = '/bases/scl.000/serial/scilistaxml.lst'
registered_filename = '/tmp/registered.txt'
issue_db = '/bases/scl.000/serial/issue/issue'
pft = "v930,' ',if v32='ahead' then v65*0.4, fi,|v|v31,|s|v131,|n|v32,|s|v132,v41/ "
cmd = 'mx ' + issue_db + ' ' + '"pft=' + pft + '" now | sort -u > ' + registered_filename

print(scilista)
#print(cmd)
os.system(cmd)

scilista_issues = None
registered_issues = None

if os.path.isfile(registered_filename):
    registered_issues = open(registered_filename, 'r').read()
    if not isinstance(registered_issues, unicode):
        registered_issues = registered_issues.decode('utf-8')
    registered_issues = registered_issues.lower()

if os.path.isfile(scilista):
    scilista_issues = open(scilista, 'r').read()
    if not isinstance(scilista_issues, unicode):
        scilista_issues = scilista_issues.decode('utf-8').split('\n')

if scilista_issues is None:
    print('not found scilista')

if registered_issues is None:
    print('not found registered')

if scilista_issues is not None and registered_issues is not None:
    missing = []
    for issue in sorted(scilista_issues):
        issue = issue.strip().lower()
        if not issue in registered_issues:
            missing.append(issue)
    if len(missing) > 0:
        print('\n'.join(missing))
print('FIM')
