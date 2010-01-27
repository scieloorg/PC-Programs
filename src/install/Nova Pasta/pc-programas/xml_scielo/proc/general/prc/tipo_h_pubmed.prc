'd30d52d53d58d83d54d55d56d57d37'
'd480d85d12'
'd70d11'


/* FIXED 20040504 
			Roberta Mayumi Takenaka
			Solicitado por Solange email: 20040429
			Inclusão de e-mail no arquivo XML.			
*/
(
	/* para resolver o problema do subcampo repetitivo */
	if p(v53) then
		'<53 0><![CDATA[',v53^*,']]>',|^n|v53^n,|^i|v53^i,'</53>'
	fi

)
/* acrescentado 20050112 - v52 */
(
	/* para resolver o problema do subcampo repetitivo */
	if p(v52) then
		'<52 0><![CDATA[',v52^*,']]>',|^d|v52^d,|^i|v52^i,'</52>'
	fi

)
(|<54 0>|v54^*|</54>|)
(|<55 0>|v55^*|</55>|)
(if p(v56) then '<56 0>',v56^*,|^e|v56^e,'</56>' fi)
(|<57 0>|v57^*|</57>|)
(
if p(v121) then
 '<122 0>',s(f(100000+val(v121),1,0))*1.5,'</122>',
 fi
)

/* campos com conteúdo de HTML */
(
	if p(v37) then
		'<37 0><![CDATA[',v37,']]>','</37>'
	fi
)
(
	if p(v30) then
		'<30 0><![CDATA[',v30,']]>','</30>'
	fi
)
(
	if p(v58) then
		if instr(v58,'^')=0 then
			'<58 0><![CDATA[',v58,']]>','</58>'
		else 
			'<58 0><![CDATA[',v58^*,']]>','^d',v58^d,'</58>'
		fi
	fi
)
(
	if p(v83) then
		'<83 0><![CDATA[',v83^a,']]>',|^l|v83^l,'</83>'
	fi
)
(
	if p(v12) then
		'<12 0><![CDATA[',v12^*,' ]]>',|^l|v12^l,'</12>'
	fi
)
(
	if p(v85) then
		'<85 0><![CDATA[',v85^k,']]>',|^l|v85^l,'</85>'
	fi
)


/* 36,480,880,936,121 */

(
 if p(v480) then
 '<480 0><![CDATA[',v480,']]></480>',
 fi
 )

(if p(v933) then
 '<933 0><![CDATA[',v933,']]></933>',
 fi
 ) 

ref(l('tipo=I'),
 (
 if p(v36) then
 '<36 0>',v36,'</36>',
 fi
 )
 (
 if p(v36) then
 '<37 0>',s(f(10000+val(v36*4.2),1,0))*1.4,'</37>',
 fi
)
)

ref(l('tipo=O'),
(
 if p(v91) then
 '<91 0>',v91,'</91>',
 fi
 )
 )
/*
'<19 0>',
ref(['TITLE']l(['TITLE']v35),
v691),
'</19>',

'<15 0>',
ref(['TITLE']l(['TITLE']v35),
v301),
'</15>',
*/


/* FIXED 20040504 
			Roberta Mayumi Takenaka
			Solicitado por Solange email: 20040429
			Inclusão de e-mail no arquivo XML.			
			*/
('<70 0>',
	if p(v70^e) then
		replace(v70,s('^e',v70^e), s('^e',v9072))
	else
		v70
	fi
,'</70>')

(
	if p(v11) and a(v11^n) and a(v11^s) then
		if p(v11^d) then
			'<11 0><![CDATA[',v11^*,']]>^d',v11^d,'</11>'
		else

			'<11 0><![CDATA[',v11,']]></11>'
		fi
	fi
)
