mx db lw=99999 "pft=if v2='t' then ref(l(s(v1,'lab')),v4),'|',ref(l(s(v1,'hlp')),v4),'|',v3,#, fi" now | sort > wiki_title.seq
mx seq=wiki_title.seq lw=99999 "pft='=== ',v1,' ===',#,'Campo: ',v3,'[[BR]]',#,replace(v2,'vbCrlf','[[BR]]'),#,#" now > wiki_title_pt.txt

mx seq=wiki_title.seq lw=99999 "pft='||',s(f(1000+val(v3),1,0))*1,'||',v1,'||',replace(v2,'vbCrlf','[[BR]]'),'||',#" now |sort > wiki_title_bytag_pt.txt


mx db lw=99999 "pft=if v2='t' then ref(l(s(v1,'lab')),v2),'|',ref(l(s(v1,'hlp')),v2),'|',v3,#, fi" now | sort > wiki_title.seq
mx seq=wiki_title.seq lw=99999 "pft='=== ',v1,' ===',#,'Field: ',v3,'[[BR]]',#,replace(v2,'vbCrlf','[[BR]]'),#,#" now > wiki_title_en.txt

mx seq=wiki_title.seq lw=99999 "pft='||',s(f(1000+val(v3),1,0))*1,'||',v1,'||',replace(v2,'vbCrlf','[[BR]]'),'||',#" now |sort > wiki_title_bytag_en.txt

mx db lw=99999 "pft=if v2='t' then ref(l(s(v1,'lab')),v3),'|',ref(l(s(v1,'hlp')),v3),'|',v3,#, fi" now | sort > wiki_title.seq
mx seq=wiki_title.seq lw=99999 "pft='=== ',v1,' ===',#,'Campo: ',v3,'[[BR]]',#,replace(v2,'vbCrlf','[[BR]]'),#,#" now > wiki_title_es.txt

mx seq=wiki_title.seq lw=99999 "pft='||',s(f(1000+val(v3),1,0))*1,'||',v1,'||',replace(v2,'vbCrlf','[[BR]]'),'||',#" now |sort > wiki_title_bytag_es.txt