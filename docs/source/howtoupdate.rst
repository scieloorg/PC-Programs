.. pcprograms documentation master file, created by
 sphinx-quickstart on Tue Mar 27 17:41:25 2012.
 You can adapt this file completely to your liking, but it should at least
 contain the root `toctree` directive.

=============
How to update
=============

Before updating the programs for the local server
-------------------------------------------------

1. Be sure **where** the programs (**bin** folder) are installed. E.g.: c:\\scielo.
2. Be sure **where** the data (**serial** folder) are stored. E.g.: c:\\scielo.
3. Be sure you have the all the databases in **serial** folder before updating. DO NOT copy **serial** contents after updating.


FAQ about updating
------------------

Does updating changes any databases (title, section, issue)?
............................................................

No. If you use the Title Manager after the updating and you can not see the list of journals, it is possible there was an error in the step 3, or the requirements were not installed.


After updating, I open Title Manager and I got an error message.
................................................................

It usually happens because after updating, the serial folder from "other installation" is copied on the "new installation".
If you want to update, using a copy of serial folder, do the copy first, then the update, because updating does not delete or overwrite the databases: title, section, issue, newcode, but it can update their indexes, and update other databases which are not related to the journals, issues and articles.
