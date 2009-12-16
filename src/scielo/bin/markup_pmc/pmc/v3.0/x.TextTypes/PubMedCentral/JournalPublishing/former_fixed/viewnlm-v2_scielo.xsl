<?xml version="1.0"?>
<!-- ============================================================= -->
<!--  MODULE:    HTML View of NLM Journal Article                  -->
<!--  VERSION:   0.2                                               -->
<!--  DATE:      November 2005                                      -->
<!--                                                               -->
<!-- ============================================================= -->
<!-- ============================================================= -->
<!--  SYSTEM:    NCBI Archiving and Interchange Journal Articles   -->
<!--                                                               -->
<!--  PURPOSE:   Provide an HTML preview of a journal article,     -->
<!--             in a form suitable for reading.                   -->
<!--                                                               -->
<!--  CONTAINS:  Documentation:                                    -->
<!--               D1) Change history                              -->
<!--               D2) Structure of this transform                 -->
<!--               D3) Design of the output                        -->
<!--               D4) Constraints on the input                    -->
<!--                                                               -->
<!--             Infrastructure:                                   -->
<!--               1) Transform element and top-level settings     -->
<!--                  including parameters, variables, keys, and   -->
<!--                  look-up tables                               -->
<!--               2) Root template                                -->
<!--               3) Document template (and make-a-piece)         -->
<!--               4) Utility templates                            -->
<!--               5) Formatting elements                          -->
<!--               6) Suppressed elements                          -->
<!--             Called templates for article parts:               -->
<!--               7) make-html-header                             -->
<!--               8) make-front                                   -->
<!--               9) make-body                                    -->
<!--              10) make-back                                    -->
<!--              11) make-post-publication                        -->
<!--              12) make-end-metadata                            -->
<!--             Narrative content and common structures:          -->
<!--              13) paragraph                                    -->
<!--              14) section                                      -->
<!--              15) list                                         -->
<!--              16) display-quote                                -->
<!--              17) speech                                       -->
<!--              18) statement                                    -->
<!--              19) verse-group                                  -->
<!--              20) boxed-text                                   -->
<!--              21) preformat                                    -->
<!--              22) supplementary-material                       -->
<!--              23) display-formula and chem-struct-wrapper      -->
<!--             Inline Elements:                                  -->
<!--              24) formatting elements                          -->
<!--              25) semantic elements                            -->
<!--              26) break and horizontal rule                    -->
<!--             Display Objects:                                  -->
<!--              27) chem-struct                                  -->
<!--              28) tex-math and math                            -->
<!--              29) graphic and media                            -->
<!--              30) array                                        -->
<!--              31) captioning                                   -->
<!--              32) figure (mode put-at-end)                     -->
<!--              33) table-wrap (mode put-at-end)                 -->
<!--             Front mode:                                       -->
<!--              34) journal-meta                                 -->
<!--              35) article-meta                                 -->
<!--              36) title-group                                  -->
<!--              37) the parts of contrib element                 -->
<!--             Back (no mode):                                   -->
<!--              38) Acknowledgements                             -->
<!--              39) Appendix                                     -->
<!--              40) Footnote-group and fn                        -->
<!--              41) Notes                                        -->
<!--              42) Glossary                                     -->
<!--             Links:                                            -->
<!--              43) Target of a reference                        -->
<!--              44) xref                                         -->
<!--              45) external links                               -->
<!--             Titles:                                           -->
<!--              46) Main article divisions                       -->
<!--              47) First-level subdivisions and default         -->
<!--              48) make-abstract-title                          -->
<!--             Unmoded data elements:                            -->
<!--              49) Miscellaneous (epage, series, etc.)          -->
<!--              50) Parts of a date                              -->
<!--              51) Parts of a name                              -->
<!--             Citation and nlm-citation (NLM templates):        -->
<!--              52) ref-list                                     -->
<!--              53) ref                                          -->
<!--              54) citation                                     -->
<!--              55) nlm-citation                                 -->
<!--              56) citation sub-parts                           -->
<!--              57) citation-tag-ends                            -->
<!--                                                               -->
<!--  PROCESSOR DEPENDENCIES:                                      -->
<!--             None: standard XSLT 1.0                           -->
<!--             Tested under Apache Xalan 2.5.1                   -->
<!--                                                               -->
<!--  COMPONENTS REQUIRED:                                         -->
<!--             1) This stylesheet                                -->
<!--             2) CSS styles defined in ViewNLM.css              -->
<!--                                                               -->
<!--  INPUT:     An XML document valid with the NLM                -->
<!--             Publishing DTD.                                   -->
<!--                                                               -->
<!--  OUTPUT:    An HTML preview of the article.                   -->
<!--                                                               -->
<!--  ORIGINAL CREATION DATE:                                      -->
<!--             October 2003                                      -->
<!--                                                               -->
<!-- ============================================================= -->
<!-- ============================================================= -->
<!--  D1) STYLESHEET VERSION / CHANGE HISTORY                      -->
<!-- =============================================================

 No.  CHANGE (reason for / description)   [who]       VERSION DATE

  5.  Changed documentation style from comments
      to (example) doc:documentation/doc:p      v02.04 2005-08-10

  4.  Revised to produce XHTML.                 v02.03 2005-08-10

  3.  Revised to accommodate DTD changes        v02.02 2005-08-22

      - Added mml namespace declaration for MathML
      - Changed the namespace prefix for the utilities
        internal to this transform, from "m" to "util",
        [to avoid confusion with the MathML use of "m",
        which the NLM DTD overrides to "mml" for the sake
        of backwards compatibility].

  2.  Revised to fix typos and infelicities.    v02.01 2005-08-08

      - Reorganized transform for easier reading
          e.g., consolidated mode="none" templates (applied to loose
        bibref models when XML source doesn't provide punctuation).

      - Replaced xsl:text making newlines with a call-template,
        for easier reading and so these can be suppressed
        (conditionally or unconditionally) if desired. Also, now
        a search on xsl:text will find only (real) generated text.

      - Diagnosed issue with display of title-in-left-column,
        content-in-right-column in IE, Firefox.
      - Corrected behavior of many small parts, e.g.,
        self-uri, product/contrib and product/collab, etc.
      - Regularized the mode names and usage for front and back.
      - Set up structure anticipating sub-article and response
        (both of which have same top-level parts as article,
        and are themselves -within- article).
      - Improved punctuation and display of xrefs
        (fn, table-fn, bibr)
      - Corrected behavior of generated text on abstract types.
      - In templates for author-notes and descendents, made
        provision for the presence of a title/label.
      - In template for author name, corrected "pref" to "prefix"
      - In template for speech, corrected logic on excluding speaker
      - Tightened up the test for mode="none" on citation/ref.

      - Changed xsl:output indent to yes (was no)
      - Changed xsl:strip-space element list (was *)
      - Added xsl:preserve-space element list

      - Added doctype calls for Strict HTML DTD (in prep for
        producing XHTML).

  1.  v0.1.                                     v01 2003-11-03

      Based on transform downloaded from NCBI website 10/23/03.

      This version (v0.1) produces readable output
      for a sample set of publishing and archiving articles.
      There is more to do with respect to scope (e.g., the
      permissible variations in content allowed by the
      Archiving DTD).

                                                                   -->
<!-- ============================================================= -->
<!-- ============================================================= -->
<!--  D2) STRUCTURE OF THIS TRANSFORM                              -->
<!-- ============================================================= -->
<!--  The main transform is organized into sections as enumerated
      above.

      It is sometimes preferable to separate element templates,
      named templates, and moded templates. In this case, however,
      that would reduce rather than increase legibility. It is
      easier to follow what the front-matter template is doing
      when the named templates and modes it uses are ready to hand;
      similarly for the back matter and, especially, the references.

      The design gives considerable importance to clarity and
      maintainability, resulting in conventions such as generally
      giving each element type its own template, in preference to
      more concise alternatives.

      In addition, the transform produces explicit new-lines
      to improve legibility of the serialized output. (These are
      in the form <xsl:call-template name="nl-2"/>. )

      This transform is commented to explain the mappings used,
      and (intermittently) the content combinations being handled.
                                                                   -->
<!-- ============================================================= -->
<!--  D3) DESIGN OF THE OUTPUT                                     -->
<!-- ============================================================= -->
<!-- Purpose: An HTML preview of an article, to assist the
              author or editor in finalizing and approving
              the tagging.

     Characteristics arising from purpose:

              - link/target pairs display the ID as a label,
                rather than generating an explicit number.
              - the running-head text, if any, is displayed
                below the title


     Organization of Display:

     A. HTML setup
       1. HTML Metadata

     B. Article

       1. Front: Publication metadata (journal and article)

       2. Content metadata:
                 Title
                 Contributor(s)
                 Abstract(s)

       3. Body:  Sections &c.

       4. Back:  a) From XML "back": acknowledgements,
                   glossary, references, and back-matter notes.

                 b) Figs-and-tables. These are collected from
                    throughout the front, body, and back.

                 c) Content metadata for retrieval - keywords,
                    subject categories. &c.

     C. Sub-article or response, if any

        Has the same 5-part structure as "B. Article".


     Typographic notes:

     A red rule separates the four document divisions listed
     above for article. The major divisions -within- those parts
     are separated by a black rule.

     Content that is composed of repeated alternations of
     minor heading and text - such as the contributor section,
     the figures section, and the references section - is
     displayed as a two-column table, with the title/heading/label
     in the left column and the substance in the right column.

     Generated text is displayed in gray, to distinguish it
     from text derived from the source XML.

-->
<!-- ============================================================= -->
<!--  D4) CONSTRAINTS ON THE INPUT                                 -->
<!-- ============================================================= -->
<!--

1. The present transform doesn't handle:
     - sub-article or response
     - a full-featured narrative in supplementary-material
     - the attributes and elements pertaining to -groups-
       of figures or tables (fig-group, table-wrap-group).
       Their contained fig/table-wrap -are- handled.
     - col, colgroup

2. Article-meta that is not displayed at the top or end
   of the article:

                volume-id
                issue-id
                issue-title
                supplement
                page-range
                conference/conf-num
                conference/conf-sponsor
                conference/conf-theme

3. xlink attributes are suppressed *except for* xlink:href,
   which becomes an href or src attribute as follows:

      a) For inline-graphic, graphic, media:

           <img src="..."> & apply-templates

      b) For phrase-level elements

          <a href="..."> & apply-templates

      c) For block containers and grouping elements:

          <a href="..."> around whatever is being displayed
          as the object identifier, e.g.,

           - label or caption (for a graphic),
           - title (for a bio),
          or, if none such is available,
           - around the generated string "[link]"

4. Attributes and child elements displayed for graphic:

    The id and xlink:href attributes are displayed.
    The label, caption, and alt-text child elements are displayed.

5. Location of media files

   Transform assumes the @xlink:href value is an absolute
   path, not a relative one. To change this assumption:

   a) In the transform, create a variable which records
      the location of the graphics, e.g.,

      <xsl:variable name="graphics-dir"
                    select="'file:///c:/books/mybook/pix'"/>

   b) In the XML, use relative paths:

      <graphic xlink:href="poodle.jpg"/>

   c) Edit the appropriate template(s) in the transform
      to combine these two values:

      <img src="{concat($graphics-dir}, '/', {@xlink:href})"/>

5. Supplementary-material

   Transform assumes that the purpose & scope
   when tagging supplementary-material are:

     - point to an external file, such as a PDF or map
     - perhaps providing a paragraph or two of description
     - not using any of the much-manipulated elements,
       i.e., footnotes, tables, figures, and references.
-->
<!-- ============================================================= -->
<!--  1. TRANSFORM ELEMENT AND TOP-LEVEL SETTINGS                  -->
<!-- ============================================================= -->
<xsl:transform version="1.0" id="ViewNLM-v2-04.xsl" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:util="http://dtd.nlm.nih.gov/xsl/util" xmlns:mml="http://www.w3.org/1998/Math/MathML" exclude-result-prefixes="util xsl">
	<xsl:include href="includes/viewnlm-v2_scielo_01_config.xsl"/>
	<!-- ============================================================= -->
	<!--  2. ROOT TEMPLATE - HANDLES HTML FRAMEWORK                    -->
	<!-- ============================================================= -->
	<xsl:include href="includes/viewnlm-v2_scielo_02_html.xsl"/>
	<!-- ============================================================= -->
	<!--  3. DOCUMENT ELEMENT                                          -->
	<!-- ============================================================= -->
	<xsl:include href="includes/viewnlm-v2_scielo_03_doc.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_03_doc_html.xsl"/>
	<!-- 4 -->
	<xsl:include href="includes/viewnlm-v2_scielo_04_util.xsl"/>
	<!-- ============================================================= -->
	<!-- 6. SUPPRESSED ELEMENTS                                        -->
	<!-- ============================================================= -->
	<!-- suppressed in no-mode (processed in mode "front") -->
	<xsl:template match="journal-meta | article-meta"/>
	<!-- not handled by this transform -->
	<xsl:template match="sub-article | response"/>
	<!-- xlink attributes are generally suppressed; note however that
     @xlink:href is used in some element templates. -->
	<xsl:template match="@xlink:*"/>
	<!-- Tables and figures are displayed at the end of the document,
     using mode "put-at-end".
     So, in no-mode, we suppress them: -->
	<xsl:template match="fig | fig-group | table-wrap | table-wrap-group"/>
	<!-- ============================================================= -->
	<!--  article_categories-->
	<!-- ============================================================= -->
	
	<xsl:include href="includes/viewnlm-v2_scielo_article_categories.xsl"/>

	
	<!-- ============================================================= -->
	<!--  Keywords                                                     -->
	<!-- ============================================================= -->
	<xsl:include href="includes/viewnlm-v2_scielo_05_keywords.xsl"/>
	<!-- ============================================================= -->
	<!--  Related article                                              -->
	<!-- ============================================================= -->
	<xsl:include href="includes/viewnlm-v2_scielo_related_articles.xsl"/>
	<!-- ============================================================= -->
	<!--  Conference                                                   -->
	<!-- ============================================================= -->
	<xsl:include href="includes/viewnlm-v2_scielo_06_conference.xsl"/>
	<!-- ============================================================= -->
	<!--  NARRATIVE CONTENT AND COMMON STRUCTURES                      -->
	<!-- ============================================================= -->
	<xsl:include href="includes/viewnlm-v2_scielo_narrative.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_person_names.xsl"/>

	<!-- ============================================================= -->
	<!--  13. PARAGRAPH WITH ITS SUBTLETIES                            -->
	<!-- ============================================================= -->
	
	<!-- ============================================================= -->
	<!--  22. SUPPLEMENTARY MATERIAL                                   -->
	<!-- ============================================================= -->
	<xsl:include href="includes/viewnlm-v2_scielo_supplmat.xsl"/>
	<!-- ============================================================= -->
	<!--  23. DISPLAY FORMULA, CHEM-STRUCT-WRAPPER                     -->
	<!-- ============================================================= -->
	<!-- both are grouping elements to keep parts together -->
	<xsl:include href="includes/viewnlm-v2_scielo_dispformula.xsl"/>

	<!-- ============================================================= -->
	<!--  24. FORMATTING ELEMENTS                                      -->
	<!-- ============================================================= -->
	<xsl:include href="includes/viewnlm-v2_scielo_format.xsl"/>
	
	<!-- ============================================================= -->
	<!--  24. SEMANTICS ELEMENTS                                      -->
	<!-- ============================================================= -->
	<xsl:include href="includes/viewnlm-v2_scielo_26_semantics.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_xyz.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_array.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_caption.xsl"/>

	<xsl:include href="includes/viewnlm-v2_scielo_fig_at_the_end.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_table_at_the_end.xsl"/>
	
	<xsl:include href="includes/viewnlm-v2_scielo_mode_front.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_mode_back.xsl"/>

	<xsl:include href="includes/viewnlm-v2_scielo_titles.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_48_words.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_misc.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_citations.xsl"/>
	<xsl:include href="includes/viewnlm-v2_scielo_end_citation.xsl"/>
</xsl:transform>
