# coding=utf-8


class ArticleISIS(object):

    def __init__(self, article, section_code, text_or_article, files_info):
        self.text_or_article = text_or_article
        self.article = article
        self.section_code = section_code
        self.files_info = files_info
        
    def metadata(self):
        rec_f = {}
        rec_f['120'] = self.article.dtd_version
        rec_f['71'] = self.article.article_type
        rec_f['40'] = self.article.language

        rec_f['241'] = []
        for item in self.article.related_objects:
            new = {}
            new['k'] = item['id']
            new['r'] = item.get('link-type')
            new['i'] = item.get('document-id', item.get('object-id', item.get('source-id')))
            new['n'] = item.get('document-id-type', item.get('object-id-type', item.get('source-id-type')))
            new['t'] = item.get('document-type', item.get('object-type', item.get('source-type')))
            rec_f['241'].append(new)

        for item in self.article.related_objects:
            new = {}
            new['k'] = item['id']
            new['i'] = item.get('{http://www.w3.org/1999/xlink}href')
            new['n'] = item.get('ext-link-type')
            new['t'] = 'pr' if item.get('related-article-type') == 'press-release' else 'article'
            rec_f['241'].append(new)
        if self.article.is_article_press_release or self.article.is_issue_press_release:
            rec_f['41'] = 'pr'

        if self.article.is_article_press_release or self.article.is_issue_press_release:
            rec_f['241'] = 'pr'

        #rec_f['100'] = self.article.journal_title
        rec_f['30'] = self.article.abbrev_journal_title
        #rec_f['62'] = self.article.publisher_name
        #rec_f['421'] = self.article.journal_id_nlm_ta
        #rec_f['930'] = self.article.journal_id_nlm_ta
        #rec_f['935'] = self.article.journal_issns

        rec_f['85'] = self.article.keywords
        #rec_f['49'] = issue.section_code(self.article.toc_section)
        rec_f['49'] = self.section_code

        rec_f['10'] = []
        for item in self.article.contrib_names:
            new = {}
            new['n'] = item['given-names']
            new['s'] = item['surname']
            new['z'] = item['suffix']
            new['p'] = item['prefix']
            new['r'] = item['contrib-type']
            new['1'] = item['xref']
            new['k'] = item['contrib-id']
            rec_f['10'].append(new)

        rec_f['11'] = self.contrib_collab
        rec_f['12'] = []
        for item in self.article.title:
            new = {}
            new['_'] = item['article-title']
            new['s'] = item['subtitle']
            new['l'] = item['language']
            rec_f['12'].append(new)
        for item in self.article.trans_titles:
            new = {}
            new['_'] = item['trans-title']
            new['s'] = item['trans-subtitle']
            new['l'] = item['language']
            rec_f['12'].append(new)

        rec_f['601'] = self.article.trans_languages
        rec_f['237'] = self.article.doi

        rec_f['121'] = self.article.order if self.article.order is not None else self.article.fpage

        if self.article.is_ahead:
            rec_f['32'] = 'ahead'
            rec_f['223'] = self.article.ahpdate
        else:
            rec_f['31'] = self.article.volume
            rec_f['32'] = self.article.number
            rec_f['131'] = self.article.volume_suppl
            rec_f['132'] = self.article.number_suppl
            rec_f['223'] = self.article.article_pub_date

        rec_f['58'] = self.article.funding_source
        rec_f['591'] = [{'_': item for item in self.article.principal_award_recipient}]
        rec_f['591'] = [{'n': item for item in self.article.principal_investigator}]
        rec_f['60'] = self.article.award_id
        rec_f['102'] = self.article.funding_statement

        rec_f['65'] = format_dateiso(self.article.issue_pub_date)
        rec_f['223'] = format_dateiso(self.article.article_pub_date)

        rec_f['14'] = {}
        rec_f['14']['f'] = self.article.fpage
        rec_f['14']['l'] = self.article.lpage
        rec_f['14']['e'] = self.article.elocation_id

        rec_f['70'] = []
        for item in self.article.affiliations:
            a = {}
            a['l'] = item['label']
            a['i'] = item['id']
            a['p'] = item['country']
            a['e'] = item['email']
            a['c'] = item['city']
            a['s'] = item['state']
            a['3'] = item['orgdiv3']
            a['2'] = item['orgdiv2']
            a['1'] = item['orgdiv1']
            a['_'] = item['orgname']
            #a['9'] = item['original']
            #rec_f['170'].append(item['xml'])
            rec_f['70'].append(item)
        #FIXME nao existe clinical trial
        rec_f['770'] = self.article.clinical_trial
        rec_f['72'] = self.article.total_of_references
        rec_f['901'] = self.article.total_of_tables
        rec_f['902'] = self.article.total_of_figures

        rec_f['83'] = []
        for item in self.article.abstracts:
            rec_f['83'].append({'l': item['language'], '_': item['text']})

        _h = self.article.history
        rec_f['111'] = format_dateiso(_h['received'])
        rec_f['113'] = format_dateiso(_h['accepted'])

        return rec_f

    def references(self):

        records_c = []
        for item in self.article.references:
            rec_c = {}
            rec_c['71'] = item.publication_type

            if item.article_title or item.chapter_title:
                rec_c['12'] = {'_': item.article_title if item.article_title else item.chapter_title, 'l': item.language}
            if item.article_title:
                rec_c['30'] = item.source
            else:
                rec_c['18'] = item.source
            rec_c['71'] = item.publication_type

            rec_c['10'] = []
            rec_c['11'] = []
            rec_c['16'] = []
            rec_c['17'] = []
            for person_group_id, person_group in item.person_groups.items():

                for person in person_group:
                    field = self.author_tag(person_group_id, 'given-names' in person)
                    if 'collab' in person:
                        a = person['collab']
                    else:
                        a = {}
                        a['n'] = person['given-names']
                        a['s'] = person['surname']
                        a['z'] = person['suffix']
                        a['r'] = self.author_role(person_group_id)

                    rec_c[field].append(a)
            rec_c['31'] = item.volume
            rec_c['32'] = {}
            rec_c['32']['_'] = item.issue
            rec_c['32']['s'] = item.supplement
            rec_c['63'] = item.edition
            rec_c['65'] = item.year + '0000'
            rec_c['66'] = item.publisher_loc
            rec_c['62'] = item.publisher_name
            rec_c['514'] = {'f': item.fpage, 'l': item.lpage, 'r': item.page_range}
            rec_c['14'] = item.fpage + '-' + item.lpage
            if item.size:
                rec_c['20']['_'] = item.size['size']
                rec_c['20']['u'] = item.size['units']
            rec_c['118'] = item.label
            rec_c['810'] = item.etal
            rec_c['109'] = item.cited_date
            rec_c['61'] = item.notes if item.notes else item.comment
            rec_c['237'] = item.doi
            rec_c['238'] = item.pmid
            rec_c['239'] = item.pmcid
            rec_c['53'] = item.conference_name
            rec_c['56'] = item.conference_location
            rec_c['54'] = item.conference_date
        records_c.append(rec_c)
        return records_c

    def author_role(self, person_group_id):
        if person_group_id == 'editor':
            return 'ed'
        if person_group_id == 'author':
            return 'nd'
        if person_group_id == 'translator':
            return 'tr'
        if person_group_id == 'compiler':
            return 'org'
        return person_group_id

    def author_tag(self, person_group_id, is_person):
        other = ['transed', 'translator']
        monographic = ['compiler', 'director', 'editor', 'guest-editor', ]
        analytical = ['allauthors', 'assignee', 'author', 'inventor', ]
        if person_group_id in analytical:
            return '10' if is_person else '11'
        if person_group_id in monographic:
            return '16' if is_person else '17'
        return '10' if is_person else '11'

    def outline(self, total_of_records):
        rec_o = {}
        rec_o['91'] = datetime.now().isoformat()[0:10].replace('-', '')
        rec_o['92'] = datetime.now().isoformat()[11:19].replace(':', '')
        rec_o['703'] = total_of_records
        return rec_o

    @property
    def records(self):
        r = []

        rec = self.outline(str(4 + len(self.references)))
        rec.update(self.common_data)
        rec.update(self.record_info('1', 'o', '1', '1'))
        r.append(rec)

        rec = self.metadata(article)
        rec.update(self.common_data)
        rec.update(self.record_info('2', 'h', '1', '1'))
        r.append(rec)

        #metadata = self.metadata(article)
        rec = self.metadata(article)
        rec.update(self.common_data)
        rec.update(self.record_info('3', 'f', '1', '1'))
        r.append(rec)

        rec = self.metadata(article)
        rec.update(self.common_data)
        rec.update(self.record_info('4', 'l', '1', '1'))
        r.append(rec)

        c_total = str(len(self.references))
        c_index = 0
        k = 4
        for rec in self.references:
            c_index += 1
            k += 1
            rec.update(self.common_data)
            rec.update(self.record_info(str(k), 'c', str(c_index), c_total))
            r.append(rec)
        return r

    @property
    def common_data(self):
        r = {}
        r['2'] = self.files_locator.id_filename
        r['4'] = self.files_locator.issue_label
        r['702'] = self.files_locator.xml_filename
        r['705'] = 'S'
        r['709'] = self.text_or_article
        return r

    def record_info(self, record_index, record_name, record_name_index, record_name_total):
        r = {}
        r['706'] = record_name
        r['700'] = record_index # starts with 0
        r['701'] = record_name_index # starts with 1
        r['708'] = record_name_total
        # r.update(dict)
        return r
