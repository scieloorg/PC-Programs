# coding=utf-8

from . import article


class Aff(object):

    def __init__(self, app_institutions_manager):
        self.app_institutions_manager = app_institutions_manager

    def query_institutions(self, aff_xml):
        aff = aff_xml.aff
        norm_aff = None
        found_institutions = None
        orgnames = [item.upper() for item in [aff.orgname, aff.norgname] if item is not None]
        if aff.norgname is not None or aff.orgname is not None:
            found_institutions = self.app_institutions_manager.validate_organization(aff.orgname, aff.norgname, aff.country, aff.i_country, aff.state, aff.city)

        if found_institutions is not None:
            if len(found_institutions) == 1:
                valid = found_institutions
            else:
                valid = []
                # identify i_country
                if aff.i_country is None and aff.country is not None:
                    country_info = {norm_country_name: norm_country_code for norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name in found_institutions if norm_country_name is not None and norm_country_code is not None}
                    aff.i_country = country_info.get(aff.country)

                # match norgname and i_country in found_institutions
                for norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name in found_institutions:
                    if norm_orgname.upper() in orgnames:
                        if aff.i_country is None:
                            valid.append((norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name))
                        elif aff.i_country == norm_country_code:
                            valid.append((norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name))

                # mais de uma possibilidade, considerar somente norgname e i_country, desconsiderar city, state, etc
                if len(valid) > 1:
                    valid = list(set([(norm_orgname, None, None, norm_country_code, None) for norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name in valid]))

            if len(valid) == 1:
                norm_orgname, norm_city, norm_state, norm_country_code, norm_country_name = valid[0]

                if norm_orgname is not None and norm_country_code is not None:
                    norm_aff = article.Affiliation()
                    norm_aff.id = aff.id
                    norm_aff.norgname = norm_orgname
                    norm_aff.city = norm_city
                    norm_aff.state = norm_state
                    norm_aff.i_country = norm_country_code
                    norm_aff.country = norm_country_name
        return (norm_aff, found_institutions)
