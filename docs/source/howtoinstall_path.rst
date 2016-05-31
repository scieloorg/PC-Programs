
============
Requirements
============

- JAVA
- PYTHON 2.7.x
- Pillow (http://effbot.org/downloads/PIL-1.1.7.win32-py2.7.exe)

Add Java and Python paths to PATH (environment variable).


.. _add-paths:

How to add Java and Python paths to Path
========================================

After downloading the file PYTHON and JAVA you have to open the System Configuration.

Use a shortcut to open that window is: Windows + Pause Break key.

.. image:: img/howtoinstall_path_atalho.jpg

Or click on **Computer** with right button of the mouse.

.. image:: img/howtoinstall_path_computer.png

Then click on **Properties**.

.. image:: img/howtoinstall_path_computer_properties.png




**Computer System Configuration**


.. image:: img/howtoinstall_path_variavel.jpg

 
Click on Advanced Settings.

.. image:: img/howtoinstall_path_conf-advanc.jpg

Then click on Environment Variables. 

.. image:: img/howtoinstall_path_open-variavel.jpg

Find Path variable in the list.

.. image:: img/howtoinstall_path_search-path.jpg

Select Path, then click on **Edit** button.

.. image:: img/howtoinstall_path_select_variable.png

Put the cursor at the end of the line, insert the character ";" and complete with the Python path. Do the same to JAVA.

It means, insert the character ";" and complete with the JAVA path.

.. image:: img/howtoinstall_path_edit-path-insert2.jpg


.. test_requirements:

How to test the requirements are correctly installed
====================================================

Make sure that this procedure was done correctly using a **NEW** window of DOS terminal. Do not use any which is already open. 
Open a **NEW** window of DOS terminal and type:

.. code-block:: code
 
 	python -V

Expected:

.. image:: img/howtoinstall_path_conferir-python.jpg


Then check Pillow:

Continue in the DOS terminal or Open a **NEW** window and type:


.. code-block:: code
 
 	python
 	import PIL
 	exit()
 	


Expected:


.. code-block:: code

	Python 2.7.8 (default, Jun 30 2014, 16:03:49) [MSC v.1500 32 bit (Intel)] on win32
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import PIL
	>>> exit()


If you have a message similar to:

.. code-block:: code

	Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
	ImportError: No module named PIL
	
Install Pillow. If you have Python 32bits, Pillow must be 32 bits too. If you have Python 64 bits, use Pillow 64 bits.


Then check Java:

.. code-block:: code

	java -version

Expected:

.. image:: img/howtoinstall_path_conferir-java.jpg


With Java and Python installed and added to Path, the Markup program is almost ready for use.
