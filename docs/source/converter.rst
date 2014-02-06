.. pcprograms documentation master file, created by
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Converter
=========

- single-user program built in Visual Basic, to use only by a centralized server, denominated `local server <concepts.html#local-server>`_. It is mandatory only one installation by `SciELO collection or instance <concepts.html#scielo-collection-or-instance>`_.
- Converter reads the files from markup and body folders, and the databases in title and issue folders, then generates a ISIS database in base folder of the corresponding journal issue.

Opening the program
-------------------

Use the Windows menu to open the program.

.. image:: img/scielo_menu.png

Or by the path of the program:

  c:\\scielo\\bin\\convert\\convert.exe


Checking the program version
----------------------------

To check the version of the program, see `How to check the program version <common.html#how-to-check-program-version>`_.

Changing the language of the program
------------------------------------

To change the language of the program's  interface, see `Change the language of the program <common.html#how-to-change-the-langauge-of-the-program>`_.

Running the program
-------------------

#. Select Files > Open.

    .. image:: img/en/converter_open_files.png


#. Fill the fields:

    .. image:: img/en/converter_01.png



    - journal's title: select the title of the journal.
    - year: FILL ONLY if it is AHEAD or REVIEW number
    - volume: fill it in with the volume
    - supplement of volume: fill it in with the supplement of volume, if it exists
    - number: fill it in with the number. If it is an ahead or review/provisional number, use **ahead** or **review**, respectively
    - supplement of number: fill it in with the supplement of number, if it exists
    - part: fill it in, if it exists. Recently it is used to **press release**, fill it in with **pr**.


    .. image:: img/en/converter_issue_selected.png


3. Click on **OK** button.

4. Converter uses these data to identify the issue's, `markup and body folders <concepts.html#folders-structure>`_. If the data are correct, the program will list the markup files. 

   .. image:: img/en/converter_files_selected.png

5. Click on **Convert** button.

6. Converter will convert the selected files. 

    For each file, the program:

        - extracts the marked data
        - compares the issue's data in the markup file and in the issue database, managed by Title Manager->Issues. 

    If there is some conflicting data, the data are not converted to the database. It is a fatal error. The user must check and correct the data in the markup document (using Markup program) and/or in issue database (using Title Manager).

    If the issue's data is correct, the files are converted to the database and the result will be shown on the screen.

        .. image:: img/en/converter_resultado.jpg

    Results:

       - successfully converted: [], in red.
       - converted, with errors: [X], in blue before its name. They have some markup errors, but not fatal enough to avoid conversion. For example, markup error, probably identified by Parser, but not corrected by the user.   
       - not converted: at the inferior part, in green. It is usually related to issue's data, such as ISSN, abbreviated title, volume and number, which do not match in the markup file and in the issue database.

7. Clicking on each file in the result area and then on **Result** button, the user can see how the conversion run.

**Successfully converted**

        .. image:: img/en/converter_view_report.png

**Converted, but no fatal error: markup error**

        .. image:: img/en/converter_resultado2.jpg

**Converted, but no fatal error: some bibliographic references not identified**

    Converter locates each bibliographic reference of the markup file in the body file, identifying the points where **[Links]** must be inserted at the article page, in the website.

        .. image:: img/en/converter_resultado6.jpg

    Clicking on **[Links]**, a window is open to display a list of links to the referenced fulltext. 

        .. image:: img/en/converter_resultado6b.jpg

    If there are bibliographic reference location errors, Converter will present the result bellow:

        .. image:: img/en/converter_resultado5.jpg

**Not converted, because of fatal errors**

        .. image:: img/en/converter_resultado3.jpg

