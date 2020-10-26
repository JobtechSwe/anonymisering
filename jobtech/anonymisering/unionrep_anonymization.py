from jobtech.anonymisering.anonymization import anonymize_swe


class unionrep_anonymize_swe(anonymize_swe):




    def initialize(self, **kwargs):
        names_m_extended = self._load_terms_from_file(self.currentdir + '/resources/names/names_m_extended_minus_common_terms_2019.csv')
        names_f_extended = self._load_terms_from_file(self.currentdir + '/resources/names/names_f_extended_minus_common_terms_2019.csv')

        firstnames = list(set(names_m_extended + names_f_extended))

        lastnames = self._load_terms_from_file(self.currentdir + '/resources/names/lastnames_extended_minus_common_terms_2019.csv')
        self.sentencefilters = ['facklig företrädare', 'fackliga företrädare',
                                'facklig representant', 'facklig representant',
                                'facklig kontaktperson', 'fackliga kontaktpersoner']

        super().initialize(firstnames=firstnames, lastnames=lastnames)


    def anonymizeText(self, s, extraKeywords=None, ignoredSentences=None, **kwargs):
        return super().anonymizeText(s, extraKeywords, ignoredSentences, sentencefilters=self.sentencefilters, checkSentencefilterHeadlines=True)