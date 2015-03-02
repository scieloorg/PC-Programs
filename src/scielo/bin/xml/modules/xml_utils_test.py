# coding=utf-8
import xml_utils
import isis

import article


def format_value(value):
    r = xml_utils.strip(value)
    if isinstance(value, unicode):
        r = value.encode('utf-8')
    return r


filename = '/Users/robertatakenaka/Documents/vm_dados/scielo_data/serial/icse/v18n49/base_source/1807-5762-icse-1807-576220130227.xml'
xml, e = xml_utils.load_xml(filename)

print(e)
art = article.Article(xml)

print([a.text for a in art.abstracts])

for a in art.article_meta.findall('.//abstract'):
    print(a)
    print('\na.text')
    print(a.text)
    text = xml_utils.etree.tostring(a)
    print('\ntostring')
    print(text)
    text = xml_utils.preserve_xml_entities(text)
    print('\npreserve_xml_entities')
    print(text)
    text = xml_utils.all_ent_to_char(text)
    print('\nall_ent_to_char')
    print(text)
    text, replaced_named_ent = xml_utils.named_ent_to_char(text)
    print('\nnumber_ent_to_char')
    print(text)
    text = xml_utils.restore_xml_entities(text)
    print('\nrestore_xml_entities')
    print(text)

    print(xml_utils.all_ent_to_char('&#91;&atilde;'))
    print('\nstrip')
    print(xml_utils.strip(text))

for a in art.abstracts:
    print(isis.format_value(a.text))
