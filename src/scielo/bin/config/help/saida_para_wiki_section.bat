mx db lw=99999 "pft=if v2='s' or v2='S' then ref(l(s(v1,'lab')),v4),'|',ref(l(s(v1,'hlp')),v4),'|',v3,#, fi" now | sort > wiki_section.seq
mx seq=wiki_section.seq lw=99999 "pft='=== ',v1,' ===',#,'Campo: ',v3,'[[BR]]',#,replace(v2,'vbCrlf','[[BR]]'),#,#" now > wiki_section_pt.txt
mx seq=wiki_section.seq lw=99999 "pft='||',s(f(1000+val(v3),1,0))*1,'||',v1,'||',replace(v2,'vbCrlf','[[BR]]'),'||',#" now |sort > wiki_section_bytag_pt.txt


mx db lw=99999 "pft=if v2='s' or v2='S' then ref(l(s(v1,'lab')),v2),'|',ref(l(s(v1,'hlp')),v2),'|',v3,#, fi" now | sort > wiki_section.seq
mx seq=wiki_section.seq lw=99999 "pft='=== ',v1,' ===',#,'Field: ',v3,'[[BR]]',#,replace(v2,'vbCrlf','[[BR]]'),#,#" now > wiki_section_en.txt
mx seq=wiki_section.seq lw=99999 "pft='||',s(f(1000+val(v3),1,0))*1,'||',v1,'||',replace(v2,'vbCrlf','[[BR]]'),'||',#" now |sort > wiki_section_bytag_en.txt

mx db lw=99999 "pft=if v2='s' or v2='S' then ref(l(s(v1,'lab')),v3),'|',ref(l(s(v1,'hlp')),v3),'|',v3,#, fi" now | sort > wiki_section.seq
mx seq=wiki_section.seq lw=99999 "pft='=== ',v1,' ===',#,'Campo: ',v3,'[[BR]]',#,replace(v2,'vbCrlf','[[BR]]'),#,#" now > wiki_section_es.txt
mx seq=wiki_section.seq lw=99999 "pft='||',s(f(1000+val(v3),1,0))*1,'||',v1,'||',replace(v2,'vbCrlf','[[BR]]'),'||',#" now |sort > wiki_section_bytag_es.txt
