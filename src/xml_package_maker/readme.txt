XML PACKAGE MAKER

Given a set of XML files according to SciELO guidelines, it:

- Creates SciELO and PMC XML Packages, renaming the href of the images, images names, and filenames.

- Validates XML for SciELO and PMC

- Generates jpg from tif or eps (optional, if PIL is installed)

- Creates a preview of fulltext of SciELO and PMC


Requirements:
java
python
PIL (optional)


Installation:
1. Create a new folder, for instance, c:\xml_package_maker.
2. Extract the content of xml_package_maker.zip inside this folder.

Usage:
python c:\xml_package_maker\xml\generate_xml_packages.py PARAM1 PARAM2 PARAM3 PARAM4 PARAM5 

PARAM1 = full path of the folder which contains XML files, images, pdf, etc
PARAM2 = full path of SciELO package
PARAM3 = full path of PMC package
PARAM4 = full path of the reports
PARAM5 = acron

Note:
Inside of path of PMC package, there will be .tiff or .eps only, not .jpg
