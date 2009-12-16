<?xml version="1.0"?>
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:strip-space elements="abstract ack address annotation app app-group
                           array article article-categories article-meta
                           author-comment author-notes back bio body boxed-text
                           break caption chem-struct chem-struct-wrapper
                           citation col colgroup conference contrib contrib-group
                           copyright-statement date def def-item def-list
                           disp-quote etal fig fig-group fn fn-group front
                           gloss-group glossary glyph-ref graphic history hr
                           inline-graphic journal-meta kwd-group list list-item
                           media mml:math name nlm-citation note notes page-count
                           person-group private-char pub-date publisher ref
                           ref-list response sec speech statement sub-article
                           subj-group supplementary-material table table-wrap
                           table-wrap-foot table-wrap-group tbody tfoot thead
                           title-group tr trans-abstract verse-group
                           "/>
	<xsl:preserve-space elements="preformat"/>
	<!--  Run-time parameters -->
	<!--  This stylesheet accepts no run-time parameters.              -->
	<!-- Keys -->
	<!-- To reduce dependency on a DTD for processing, we declare
     a key to use in lieu of the id() function. -->
	<xsl:key name="element-by-id" match="*[@id]" use="@id"/>
	<!-- Conversely, we can retrieve referencing elements
     from the node they reference. -->
	<xsl:key name="element-by-rid" match="*[@rid]" use="@rid"/>
	<!-- Lookup table for person-type strings
     used in nlm-citations -->
	<xsl:variable name="person-strings" select="document('person-strings.xml')/*/util:map[@id='person-strings']/item"/>
	<util:map id="person-strings" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" >
		<item source="editor" singular="editor" plural="editors"/>
		<item source="assignee" singular="assignee" plural="assignees"/>
		<item source="translator" singular="translator" plural="translators"/>
		<item source="transed" singular="translator and editor" plural="translators and editors"/>
		<item source="guest-editor" singular="guest editor" plural="guest editors"/>
		<item source="compiler" singular="compiler" plural="compilers"/>
		<item source="inventor" singular="inventor" plural="inventors"/>
		<!-- value 'allauthors' puts no string out -->
	</util:map>
	
</xsl:transform>
