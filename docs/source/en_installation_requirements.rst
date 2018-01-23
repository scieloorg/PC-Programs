
============
Requirements
============

The requirements are procedures that have to have been executed before the SciELO PC Programs installation. 

Once the requirements are been complied with, there is no need to execute them again or every time SciELO PC Programs is installed/updated. 


Checking the requirements
=========================

Checking the location and status of the serial folder
-----------------------------------------------------

**Only** for the **Collection Manager** programs, which must be installed in the local server.

This server must have acces to the **serial** folder and this folder must be updated (title, section, issue etc) before executing the SciELO PC Programs installation.

    .. warning:: 

        **Do not update** **serial** folder contents after the SciELO PC Programs installation. Do it before the SciELO PC Programs installation. 


Checking the Python + pip installation 
--------------------------------------

1. **Always open a new** terminal window to have a session with the configurations applied.

2. Execute the command on the terminal:

    .. image:: img/installation_python_test.png


3. Checking if the command presents the Python version. For instance:

    .. image:: img/installation_python_resultado.png


  .. note::

     As executing this command the Python version is not necessarily the same as the image


4. If the result is not the expected, repeat the instructions to install Python and pip.

5. Execute the command on the terminal:

    .. image:: img/installation_pip_test.png


6. Checking if the command presents pip version. For instance:

    .. image:: img/installation_pip_resultado.png


  .. note::

     As executing this command the pip version is not necessarily the same as the image


7. If the result is not the expected, repeat the instructions to install Python and pip.


Checking the Pillow installation 
----------------------------------

Pillow is requirement **only** for **previous version of SciELO PC Programs 4.0.094**.

Checking if it is properly installed, executing the commands on the terminal:

1. Execute python:

    .. image:: img/installation_python.png
    

2. The result is the presentation of  **Python terminal**. 

    .. image:: img/installation_python_terminal.png


  .. note::

     As executing this command the Python version is not necessarily the same as the image

    

3. Execute * import PIL * (uppercase letters):

    .. image:: img/installation_import_pil.png
    

4. Checking that the expected result is:

    .. image:: img/installation_import_pil_resultado.png
   

   But if the message is similar to:

        .. code-block:: text

            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            ImportError: No module named PIL


   **reinstall pillow**.
    

5. Execute *exit()* to exit from Python terminal

   .. image:: img/installation_python_exit.png


6. Note you have exited the Python terminal

   .. image:: img/installation_python_exited.png


Checking the Java installation 
------------------------------

1. Execute on the terminal:

    .. code-block:: text

        java -version


2. Checking if the result is similar to:

    .. image:: img/howtoinstall_path_conferir-java.jpg



    .. note::

      As executing this command the **java** version is not necessarily the same as the image



    If the message is similar to: *java is not a recognized command ...*, repeat the instructions to install Java.



Install the requirements
========================


How to install Python and pip >= 2.7.10
---------------------------------------

First of all, be sure the computer have **only one** Python version 2.7.x installed. If it is necessary to install a new version of Python, remove the old before installing a new one.

As installing Python, select all the options, specially:
    
    - Add Python to PATH
    - pip


    .. image:: img/installation_add_python_to_path.png
       :height: 500
       :width: 500


How to install Pillow
---------------------

It is a requirement only for **previous versions of SciELO PC Programs 4.0.094**.

Execute the command on the terminal:

    .. image:: img/installation_pip_install_pillow.png


How to install Java
-------------------

After installing Java, open the "System configuration", set the Java location to PATH.


.. _add-paths:

Add a program to PATH
,,,,,,,,,,,,,,,,,,,,,

Use the shortcut to open that window is: Windows + Pause Break key.

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

Put the cursor at the end of the line, insert the character ";" and complete with the program path.

It means, insert the character ";" and complete with the JAVA path.

.. image:: img/installation_java.png

