mx ..\..\..\serial\code\code lw=99999 "pft=if v1^l='pt' or a(v1^l) then ' * [wiki:SciELO_PCPrograms_Code#',replace(v1^*,' ','_'),' ',v1^*,']',# fi" now | sort > wiki_code.txt

mx ..\..\..\serial\code\code lw=99999 "pft=if v1^l='pt' or a(v1^l) then '=== ',v1^*,' === #',replace(v1^*,' ','_'),#,('||',v2^c,'||',v2^v,'||',#),#,#, fi" now >> wiki_code.txt
