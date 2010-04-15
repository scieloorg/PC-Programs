mx db lw=99999 "pft=if v2='i' or v2='I' then ref(l(s(v1,'lab')),v4),'|',ref(l(s(v1,'hlp')),v4),'|',v3,#, fi" now | sort > wiki_issue.seq
mx seq=wiki_issue.seq lw=99999 "pft='=== ',v1,' ===',#,'Campo: ',v3,'[[BR]]',#,replace(v2,'vbCrlf','[[BR]]'),#,#" now > wiki_issue.txt


mx seq=wiki_issue.seq lw=99999 "pft='||',s(f(1000+val(v3),1,0))*1,'||',v1,'||',replace(v2,'vbCrlf','[[BR]]'),'||',#" now |sort > wiki_issue_bytag.txt
