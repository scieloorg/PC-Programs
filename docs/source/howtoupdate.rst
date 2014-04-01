.. pcprograms documentation master file, created by
 sphinx-quickstart on Tue Mar 27 17:41:25 2012.
 You can adapt this file completely to your liking, but it should at least
 contain the root `toctree` directive.


How to update
==============

1. Download the `installer <download.html>`_
2. Check if you have all the current `requirements <howtoinstall.html#requirements>`_ already installed
3. Have a backup of the application and data folders. E.g.: c:\\scielo

  The application folder is the folder which contains:

  - bin
  - xml_scielo (optional)
  - export

  The data folder is the folder which contains:

  - serial

4. Run the installer
5. Follow the instructions given in each screen


.. attention:: Use a drive in which the user can have full access 


.. warning:: DO NOT use names with spaces


6. Complete the data of the installation. Use the same path for the application and data folders. Otherwise, it is not an update, it is a new installation.

.. image:: img/installation_setup.jpg

7. Select the programs you want to install in your computer, according to the purpose of the computer:

- Local server (only one computer)

  - Title Manager: program to manage journal and issues data
  - Markup: program to identify the bibliographic elements in the articles/texts
  - Markup - Automata files (optional): examples of files for automatic markup
  - Converter: program to load the marked documents in the database
  - XML SciELO: (optional) program to create XML format for PubMed and ISI

- Markup Computer (one or more computers)

  - Markup: program to identify the bibliographic elements in the articles/texts
  - Markup - Automata files (optional): examples of files for automatic markup


FAQ about update
----------------

Does updating changes any databases (title, section, issue)?
............................................................

No. If you use the Title Manager after the updating and you can not see the list of journals, it is possible there was an error in the step 3, or the requirements were not installed.


After updating, I tried to open Title Manager and I got an error message.
..........................................................................

It usually happens because after updating, the serial folder from "other installation" is copied on the "new installation".
If you want to update, using a copy of serial folder, do the copy first, then the update, because updating does not delete or overwrite the databases: title, section, issue, newcode, but it can update their indexes, and update other databases which are not related to the journals, issues and articles.


----------------

Last update of this page: Feb 28, 2014

