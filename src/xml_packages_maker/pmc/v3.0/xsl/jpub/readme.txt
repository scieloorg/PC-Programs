NLM/NCBI Journal Publishing 3.0 Preview XSLT stylesheets

For documentation on these stylesheets, see:

quickstart.pdf     -- "Bare bones" instructions
user-docs.pdf      -- User documentation including assumptions
                      and limitations
technical-docs.pdf -- More technical documentation, especially
                      for those who wish to customize their
                      environment or the stylesheets

Or the same documents in HTML format.

These same documents are included with tagging according to
Journal Publishing 3.0, from which the PDF and HTML was
generated:

quickstart.xml
user-docs.xml
technical-docs.xml

As such, they are suitable for testing the stylesheets.

The following top-level stylesheets are included:

jpub3-PMCcit-html.xsl
jpub3-APAcit-html.xsl
jpub3-PMCcit-web-html.xsl
jpub3-PMCcit-xhtml.xsl
jpub3-PMCcit-xslfo.xsl
jpub3-APAcit-xslfo.xsl
jpub3-PMCcit-print-fo.xsl

As described in the documentation, these are XSLT 2.0 with Saxon
extensions, and require a recent version of the Saxon processor
to run. (We tested with Saxon 9.1.0.5.)

Plus, there is a CSS stylesheet to be used with HTML results of
any of these processes (including the HTML versions of the
documentation):

jpub-preview.css

Finally, the following modules are included in subdirectories
(as described in the documentation):

[main]
jpub3-html.xsl
jpub3-xslfo.xsl
xhtml-tables-fo.xsl
shell-utility.xsl
[prep]
  jpub3-webfilter.xsl
  jpub3-printfilter.xsl
[citations-prep]
  jpub3-PMCcit.xsl
  jpub3-APAcit.xsl
[post]
  xhtml-ns.xsl

