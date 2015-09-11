
XML generation files results
----------------------------

scielo_package
..............
    XML Files according to `SPS <http://docs.scielo.org/projects/scielo-publishing-schema/>`_

    purpose
        used by `XML Converter <xml_converter.html>`_
    location
        /<ANY_LOCATION>/<acron>/<issue_identification>/markup_xml/scielo_package

scielo_package_zips
...................
    Compacted files of `scielo_package`_

    purpose
        to send to SciELO
    location
        /<ANY_LOCATION>/<acron>/<issue_identification>/markup_xml/scielo_package_zips

errors
......
    Reports of XML files generation and validations

    purpose
        inform errors of the generation process
        inform errors found in XML files generated to be fixed by the user
    location
        /<ANY_LOCATION>/<acron>/<issue_identification>/markup_xml/errors
    note
        must be sent to SciELO with `scielo_package_zips`_

work
....
    Temporary folder used during the generation/validation of XML files

    purpose
        used to get any support from SciELO Team, otherwise can be deleted
    location
        /<ANY_LOCATION>/<acron>/<issue_identification>/markup_xml/work
