..\bin\cfg\mx "seq=..\bin\markup_pmc\pt_bars.mds;" create=pt_bars now -all

..\bin\cfg\mx pt_bars lw=9999 "pft=if p(v5) then '<element name=\"',v1,'\"><annotation><documentation>',v2,'</documentation></annotation></element>',# fi" now >> annotationFromMarkup.xml

