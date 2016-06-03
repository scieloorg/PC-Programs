# code = utf-8


def apply_encode(value):
    u = value.decode('utf-8')
    try:
        value = u.encode('cp1252')
    except Exception as e:
        try:
            value = u.encode('cp1252', 'replace')
            print(value)
        except Exception as e:
            print(e)
            print(value)
    return value


def english_country_codes():
    #code: alpha_2_code,alpha_3_code,numeric_code,independent,status,english_names,short_name_uppercase_en,full_name_en
    english_names = {}
    all_english_names = {}

    for item in open('country-codes.csv', 'r').readlines():
        item = item.strip()[1:]
        item = item[:-1]
        parts = item.split('","')

        if len(parts) > 1:
            if parts[4] == 'officially-assigned':
                # 5, 6, 7
                unique = ''
                for i in range(5, len(parts)):
                    name = parts[i]
                    if len(name) > 0:
                        all_english_names[name] = parts[0]
                        if unique == '':
                            unique = name
                            english_names[name] = parts[0]
    return (english_names, all_english_names)


def country_names():
    #name: alpha_2_code,alpha_3_code,numeric_code,language,short_name,short_name_uppercase,full_name
    codes = {}
    for item in open('country-names.csv', 'r').readlines():
        item = item.strip()[1:]
        item = item[:-1]
        parts = item.split('","')
        # 0, 4, 5, 6
        if len(parts) > 4:
            s = parts[0]
            for i in range(4, len(parts)):
                name = parts[i]
                if len(name) > 0:
                    codes[name] = s
    return codes


def save_br_locations():
    #name: alpha_2_code,alpha_3_code,numeric_code,language,short_name,short_name_uppercase,full_name
    new = []
    for item in open('old_br_locations.csv', 'r').readlines():
        state, ign, city = item.replace('"', '').split('\t')
        new.append(state + '\t' + city)
    open('br_locations.csv', 'w').write('\n'.join(new))


def current_wos_country_names():
    return sorted('Andorra\nU Arab Emirates\nAfghanistan\nAntigua and Barbuda\nAnguilla\nAlbania\nArmenia\nNetherlands Antilles\nAngola\nAntarctica\nArgentina\nOld style Arpanet\nAmerican Samoa\nAustria\nAustralia\nAruba\nAzerbaidjan\nBosnia-Herzegovina\nBarbados\nBangladesh\nBelgium\nBurkina Faso\nBulgaria\nBahrain\nBurundi\nBenin\nBermuda\nBrunei Darussalam\nBolivia\nBrazil\nBahamas\nBhutan\nBouvet Island\nBotswana\nBelarus\nBelize\nCanada\nCentral African Republic\nCongo\nSwitzerland\nIvory Coast\nCook Islands\nChile\nCameroon\nChina\nColombia\nCosta Rica\nFormer Czechoslovakia\nCuba\nCape Verde\nChristmas Island\nCyprus\nCzech Republic\nGermany\nDjibouti\nDenmark\nDominica\nDominican Republic\nAlgeria\nEcuador\nUSA Educational\nEstonia\nEgypt\nWestern Sahara\nEritrea\nSpain\nEthiopia\nFinland\nFiji\nFalkland Islands\nMicronesia\nFaroe Islands\nFrance\nFrance (European Territory)\nGabon\nGreat Britain\nGrenada\nGeorgia\nFrench Guyana\nGhana\nGibraltar\nGreenland\nGambia\nGuinea\nUSA Government\nGuadeloupe\nEquatorial Guinea\nGreece\nGuatemala\nGuinea Bissau\nGuyana\nHong Kong\nHonduras\nCroatia\nHaiti\nHungary\nIndonesia\nIreland\nIsrael\nIndia\nInternational\nIraq\nIran\nIceland\nItaly\nJamaica\nJordan\nJapan\nKenya\nKyrgyzstan\nCambodia\nKiribati\nComoros\nSaint Kitts & Nevis Anguilla\nNorth Korea\nSouth Korea\nKuwait\nCayman Islands\nKazakhstan\nLaos\nLebanon\nSaint Lucia\nLiechtenstein\nSri Lanka\nLiberia\nLesotho\nLithuania\nLuxembourg\nLatvia\nLibya\nMorocco\nMonaco\nMoldavia\nMadagascar\nMarshall Islands\nMacedonia\nMali\nMyanmar\nMongolia\nMacau\nNorthern Mariana Islands\nMartinique\nMauritania\nMontserrat\nMalta\nMauritius\nMaldives\nMalawi\nMexico\nMalaysia\nMozambique\nNamibia\nNew Caledonia\nNiger\nNetwork\nNorfolk Island\nNigeria\nNicaragua\nNetherlands\nNorway\nNepal\nNauru\nNeutral Zone\nNiue\nNew Zealand\nOman\nPanama\nPeru\nPolynesia\nPapua New Guinea\nPhilippines\nPakistan\nPoland\nSaint Pierre and Miquelon\nPitcairn Island\nPuerto Rico\nPortugal\nPalau\nParaguay\nQatar\nRomania\nRussia\nRwanda\nSaudi Arabia\nSolomon Islands\nSeychelles\nSudan\nSweden\nSingapore\nSaint Helena\nSlovenia\nSlovak Rep\nSierra Leone\nSan Marino\nSenegal\nSomalia\nSuriname\nSaint Tome and Principe\nEl Salvador\nSyria\nSwaziland\nTurks and Caicos Islands\nChad\nTogo\nThailand\nTadjikistan\nTokelau\nTurkmenistan\nTunisia\nTonga\nEast Timor\nTurkey\nTrinidad and Tobago\nTuvalu\nTaiwan\nTanzania\nUkraine\nUganda\nUnited Kingdom\nUnited States\nUruguay\nUzbekistan\nVatican City State\nSaint Vincent & Grenadines\nVenezuela\nVirgin Islands (British)\nVirgin Islands (USA)\nVietnam\nVanuatu\nSamoa\nYemen\nMayotte\nYugoslavia\nSouth Africa\nZambia\nZaire\nZimbabwe'.split('\n'))


def complete_wos_codes(wos_codes, english_names):
    _wos_codes = wos_codes.values()
    new = {}
    for name, code in english_names.items():
        if not code in _wos_codes:
            wos_codes[name] = code
            _wos_codes.append(code)
            new[name] = code
    return (wos_codes, new)


def set_wos_codes(curr_wos_country_names, english_names, all_names):
    _codes = {}
    _not_found = []
    for item in curr_wos_country_names:
        if english_names.get(item) is not None:
            _codes[item] = english_names.get(item)
        elif all_names.get(item) is not None:
            _codes[item] = all_names.get(item)
        else:
            _not_found.append(item)
    return (_codes, _not_found)


def save_country_attr(english_names):
    names = []
    codes = []
    a = []
    for name in sorted(list(set(english_names.keys()))):
        names.append(name)
        codes.append(english_names[name])
        a.append(name + '|' + english_names[name])
    open('country_attb.mds', 'w').write(apply_encode(';'.join(names) + '\n' + ';'.join(codes) + '\n'))
    open('country_attb.txt', 'w').write(apply_encode('\n'.join(a)))


def save_wos_codes(wos_country_name_code_items, not_found):
    names = []
    for name in sorted(wos_country_name_code_items.keys()):
        names.append(name + '|' + wos_country_name_code_items[name])
    open('wos_country_code.txt', 'w').write('\n'.join(names))
    open('wos_country_notfound.txt', 'w').write('\n'.join([name + '|' for name in sorted(not_found)]))


def save_ncountry_attr(items):
    open('wos_country_attr.txt', 'w').write(';'.join(items) + '\n' + ';'.join(items))


def save_all_names(items):
    new = {}
    for l in items:
        for name, code in l.items():
            new[name] = code
    items = []
    for name in sorted(new.keys()):
        items.append(name + '|' + new[name])
    open('all_names.txt', 'w').write('\n'.join(items))

#br_locations
save_br_locations()

#country list
#english_names, all_english_names = english_country_codes()
#all_names = country_names()
#save_all_names([all_english_names, all_names])

#MARKUP attributes
#save_country_attr(english_names)
#save_ncountry_attr(current_wos_country_names())

# WOS
#curr_wos_name_and_code_items = set_wos_codes(current_wos_country_names(), all_english_names, all_names)
#wos_country_name_code_items, new_codes = complete_wos_codes(curr_wos_name_and_code_items, english_names)
