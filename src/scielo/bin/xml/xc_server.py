# coding = utf-8

import sys


if len(sys.argv) == 3:
    action = sys.argv[1]

    if action in ['begin', 'end']:
        if action == 'begin':
            import modules.xc_receipt
            modules.xc_receipt.receive_xml_files(['receipt', sys.argv[2]])
        elif action == 'end':
            import modules.xc_gerapadrao
            modules.xc_gerapadrao.gerapadrao(['gerapadrao', sys.argv[2]])
    else:
        print('Unable to execute')
        print(sys.argv)
