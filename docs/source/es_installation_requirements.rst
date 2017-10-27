
==========
Requisitos
==========

Los requisitos son procedimientos ya que deben haber sido ejecutados antes de la instalación de SciELO PC Programs. 

Una vez que los requisitos están siendo atendidos, no es necesario ejecutar los requisitos cada vez que se instala SciELO PC Programs.


Verificar los requisitos
========================

Verificar la ubicación y situación de la carpeta serial
-------------------------------------------------------

**Solamente** para los programas de **gestión de colección**, que deben estar instalador en un servidor local.

Este servidor debe haber acceso a la carpeta **serial** y esta carpeta tiene que estar actualizada (title, section, issue etc) antes de ejecutar la instalación de SciELO PC Programs.

    .. warning:: 

        **No actualizar** el contenio de la carpeta **serial** después de la instalación. Hacerlo antes de la instalación. 


Verificar la instalación de Python + pip
----------------------------------------

1. **Siempre abrir una nueva** ventana de Terminal para garantizar que las actualizaciones esten aplicadas en la sesión del terminal.

2. Ejecutar el comando en el terminal:

    .. image:: img/installation_python_test.png


3. Verificar si el comando presenta la versión de Python. Por exemplo:

    .. image:: img/installation_python_resultado.png


  .. note::

     al ejecutar este comando la versión de Python no necesariamente tiene que ser igual a de la imagen


4. Por si acaso el resultado no es lo esperado, repetir todas las instrucciones anteriores.

5. Ejecutar el comando en el terminal:

    .. image:: img/installation_pip_test.png


6. Verificar si el comando presenta la versión del pip. Por exemplo:

    .. image:: img/installation_pip_resultado.png


  .. note::

     al ejecutar este comando la versión de pip no necesariamente tiene que ser igual a de la imagen


7. Por si acaso el resultado no es lo esperado, **reinstalar Python**.


Verificar la instalación de Pillow 
----------------------------------

Pillow es requisito **solamente** para **versiones anteriores la SciELO PC Programs 4.0.094**.

Verificar si fue correctamente instalado, ejecutando los comandos en el terminal:

1. Ejecutar python:

    .. image:: img/installation_python.png
    

2. Verificar que el resultado esperado será la presentación del **terminal de Python**. 

    .. image:: img/installation_python_terminal.png


  .. note::

     al ejecutar este comando la versión de python no necesariamente tiene que ser igual a de la imagen

    

3. Ejecutar *import PIL* (letras mayúsculas):

    .. image:: img/installation_import_pil.png
    

4. Verificar que el resultado esperado es:

    .. image:: img/installation_import_pil_resultado.png
   

   Pero si el mensaje es similar a

        .. code-block:: text

            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            ImportError: No module named PIL


   **reinstalar pillow**.
    

5. Ejecutar *exit()* para salir del terminal de Python

   .. image:: img/installation_python_exit.png


6. Verificar que salió del terminal de Python

   .. image:: img/installation_python_exited.png


Verificar la instalación Java
-----------------------------

1. Ejecutar en el terminal:

    .. code-block:: text

        java -version


2. Verificar si el resultado presentado es similar a:

    .. image:: img/howtoinstall_path_conferir-java.jpg



    .. note::

      al ejecutar este comando la versión de **java** no necesariamente tiene que ser igual a de la imagen



    Por si acaso el mensaje sea: *java no es un comando reconocido ...*, repetir las instrucciones de esta sección.



Instalar los requisitos
=======================


Cómo instalar Python y pip igual ou superior la 2.7.10
------------------------------------------------------

Primeiramente, garantizar que tenga **solamente uma** versión de Python 2.7.x instalada. Por si acaso sea necesario instalar una versión más reciente de Python, remover la anterior antes de proseguir.

Al instalar Python, seleccione todas las opciones disponibles, especialmente:
    
    - Add Python to PATH
    - pip


    .. image:: img/installation_add_python_to_path.png
       :height: 500
       :width: 500


Cómo instalar Pillow
--------------------

Es requisito solamente para **versiones anteriores la SciELO PC Programs 4.0.094**.

Ejecutar el comando en el terminal:

    .. image:: img/installation_pip_install_pillow.png


Cómo instalar Java
------------------

Después de instalar Java, abrir la "Configuración del Sistema", indicar la ubicación del Java instalado para la variável de ambiente PATH.


.. _add-paths:

Add aplicación en el PATH
,,,,,,,,,,,,,,,,,,,,,,,,,

Use el atallo to open that window is: Windows + Pause Break key.

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

Coloque el cursor en le final de la línea, añadir el caracter punto-y-coma (;) y la ubicación de Java instalado.

.. image:: img/installation_java.png


