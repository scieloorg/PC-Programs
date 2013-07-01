.. pcprograms documentation master file, created by
 sphinx-quickstart on Tue Mar 27 17:41:25 2012.
 You can adapt this file completely to your liking, but it should at least
 contain the root `toctree` directive.

Requirements
============
JAVA
PYTHON 2.7.x

How to install
==============

1. Download the last version
2. Run the program
3. Follow the instructions given in each screen
4. Configure

  **application's name**
    Examples: SciELO Brazil, SciELO Chile, SciELO v4.0, etc., or just SciELO.

  URL
    production website address
    Example: www.scielo.br

  destination data folder
    folder which have serial folder

  .. image:: img/en/00_setup.jpg


5. Select the programs you want to install in your computer, considering if it is the local server or the markup computer.

Programs for local server 
-------------------------

- Code Manager: program to manager tables of codes/labels. For example, countries table: BR (code) and Brazil (label) 
- Title Manager: program to manager journal data that are part of the collection, their issues and sections of table of contents
- Converter: program responsible for loading the CDS / ISIS databaseusing complete text documents previously marked 
- Markup: program to identify each bibliographic element on articles and texts
- SGML Parser: program to identify possible markup errors on the marked files. It is always installed.
- XML SciELO: program (optional) to create XML format accepted byPubMed and ISI

Programs for Markup Computer
----------------------------

- Markup: program to identify each bibliographic element on articles and texts
- SGML Parser: program to identify possible markup errors on the marked files. It is always installed.

Note: Markup - automata files are examples of automatas. Its installation is optional. 

  .. image:: img/en/00_selecao.jpg


6. For local server installation, set the environment variable BAP as OS23470a.

7. By Windows menu go to: Control Panel -> Performance and Maintenance -> System -> Advanced Settings -> Environment variables.
8. Check if the variable already exists. 
9. If it does not, click New and enter the data.

   .. image:: img/en/00_bap.jpg

10. Install Java and set its location in PATH.
11. The shortcurts are created to administrator user, so copy the shortcuts for all the users.
12. Give the write permission to non-admin users on C: (for Parser usage) and all the folders below the bin folder, because the programs generate files in these folders.
13. Select the C: drive and click on Properties option.

  .. image:: img/en/permissao001.png

14. Open the security tab

  .. image:: img/en/permissao002.png

15. Select **users** (common users)

  .. image:: img/en/permissao003.png

16. Click on Edit button

  .. image:: img/en/permissao004.png

17. Check all the permissions. Then click on Apply to set the permissions.

  .. image:: img/en/permissao005.png

