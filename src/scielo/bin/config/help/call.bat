set mx=mx
set p=
set p2=


call txt2db %mx% %p%db %p%TitleManager_gen_labels.txt %p%TitleManager02_help.txt 

call db2conf %mx% %p%db %p2%fields.ini %p2%en_fields.ini %p2%es_fields.ini %p2%pt_fields.ini
