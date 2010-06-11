mx null count=1 "pft=' = Índice = #index '/" now> wiki_code2.txt

mx ..\..\..\serial\code\code lw=99999 "pft=if v1^l='pt' or a(v1^l) then ' * [wiki:SciELO_PCPrograms_Code#',replace(v1^*,' ','_'),' ',v1^*,']',# fi" now | sort >> wiki_code2.txt
mx ..\..\..\serial\code\code lw=99999 "pft=if a(v1^l) then '=== ',v1^*,' === #',replace(v1^*,' ','_'),' [wiki:SciELO_PCPrograms_Code#index topo]',#,('||',v2^c,'||',v2^v,'||',#),#,#, fi" now >> wiki_code2.txt



mx ..\..\..\serial\code\code lw=99999 "pft=if p(v1^l) then (v1^*[1],'|',v2^c,'|',v1^l[1],'|',v2^v/) fi" now | sort > wiki_code2_sort.seq
mx seq=wiki_code2_sort.seq create=wiki_code2_sort now -all


mx wiki_code2_sort lw=99999 "pft=if v1<>ref(mfn-1,v1) then ,#,#,'=== ',v1,' === #' ,replace(v1,' ','_'),' [wiki:SciELO_PCPrograms_Code#index topo]'#,'||||English||Español||Português||',#,'||',v2,'||',v4,'||',else ,if v2<>ref(mfn-1,v2) then #,'||',v2,'||' ,fi,v4,'||',fi" now >>wiki_code2.txt
