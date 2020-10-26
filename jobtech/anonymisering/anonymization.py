# simple anonymization
# - removes entire sentences which contain phone numbers, email adresses, names or other manually defined keywords
# - uses nltk for Swedish tokenization
# - files with most common Swedish names in 'names' directory
import os
import re
import csv
import nltk.data

class anonymize_swe:

    currentdir = os.path.dirname(os.path.realpath(__file__))


    def initialize(self, firstnames=None, lastnames=None):
        '''
        :param firstnames: Optional list with firstnames to find. Will override the default firstnames list.
        :param lastnames: Optional list with lastnames to find. Will override the default lastnames list.
        '''
        self._all_names = []

        if firstnames is None:
            # load default firstnames
            names_m = self._load_terms_from_file(self.currentdir + '/resources/names/names_m_minus_common_terms.csv')
            names_f = self._load_terms_from_file(self.currentdir + '/resources/names/names_f_minus_common_terms.csv')
            self._all_names.extend(names_m)
            self._all_names.extend(names_f)

        else:
            self._all_names.extend(firstnames)

        if lastnames is None:
            # load default lastnames
            names_efternamn = self._load_terms_from_file(self.currentdir + '/resources/names/names_efternamn100_minus_common_terms.csv')
            self._all_names.extend(names_efternamn)
        else:
            self._all_names.extend(lastnames)

        self._tokenizer = nltk.data.load('nltk:tokenizers/punkt/swedish.pickle')

        # by default not using advanced regex for phone numbers - only removing any long numbers
        self._regexpPhoneNumberComplex = re.compile(r'^([+]46)\s*(7[0236])\s*(\d{4})\s*(\d{3})$')
        self._regexpPhoneNumberSimple = re.compile(r'[0-9]{6,7}')


    def __containsPhoneNumber(self,s, useSimpleVersion = True):

        if useSimpleVersion:
            if self._regexpPhoneNumberSimple.search(s.replace(' ','')) is not None:
                return True
        else:
            if self._regexpPhoneNumberComplex.search(s.replace(' ','')) is not None:
                return True
        
        return False

    def _load_terms_from_file(self, filepath):
        with open(filepath) as file:
            termer = file.readlines()
        termer = [x.strip() for x in termer]
        return termer

    def checkWord(self,word):
        
        # check if contains any keyword (default this only checks for names)
        if word in self._all_names:
            return { 'data':'NAME', 'index':1 }
        elif '@' in word:
            return { 'data':'EMAIL', 'index':2 }
        elif self.__containsPhoneNumber(word):
            return { 'data':'PHONE', 'index':3 }
        
        return { 'data': word, 'index': 0 }


    def _is_matching_sentencefilter(self, has_sentencefilters, is_found_sentencefilter, is_sentencefilter_rows):
        return has_sentencefilters and (is_found_sentencefilter or is_sentencefilter_rows)


    def _is_matching_rule(self, contains_pattern, has_sentencefilters, is_found_sentencefilter, is_sentencefilter_rows):
        is_matching_rule = False

        if (not has_sentencefilters and contains_pattern) or (has_sentencefilters and (is_found_sentencefilter or is_sentencefilter_rows) and contains_pattern):
            is_matching_rule = True
        return is_matching_rule

    def textRemoveSentences(self,text,keywords,ignored, sentencefilters, checkSentencefilterHeadlines):
        keywords = set(keywords)

        # returns new text and removed sentences
        removedSentences = []

        sentencefilters_lower = [filter.lower() for filter in sentencefilters]
        has_sentencefilters = len(sentencefilters) > 0

        # counts
        removedTypes = { 'Name&Email&Phone': 0, 'Name&Email': 0, 'Name&Phone':0,'Name':0,'Email&Phone':0,'Email':0,'Phone':0 }

        finalText = ''

        #newText = text.replace('   ','\n') # special case
        sections = text.split('\n')

        # Flag for: if the current sentence is after a headline that contains a sentence filter.
        is_sentencefilter_headline_rows = False

        for i, section in enumerate(sections):
            sentences = self._tokenizer.tokenize(section)
            sentences_count = len(sentences)


            for j, sentence in enumerate(sentences):
                sentence_lower = sentence.lower()
                containsEmail = False
                containsPhone = False
                containsName = False

                sentencepadding = ' ' if j < sentences_count - 1 else ''

                if sentence not in ignored:
                    words = sentence.split()
                    doNotUse = False

                    is_found_sentencefilter = any(sentencefilter in sentence_lower for sentencefilter in sentencefilters_lower)
                    is_sentencefilter_headline_rows = checkSentencefilterHeadlines and (is_found_sentencefilter or is_sentencefilter_headline_rows)

                    if not has_sentencefilters or (has_sentencefilters and (is_found_sentencefilter or is_sentencefilter_headline_rows)):
                        # check if contains any keyword (default this only checks for names)
                        for k in keywords:
                            if k in words or (len(k.split(' ')) > 1 and k in sentence):
                                doNotUse = True
                                containsName = True

                    # check if contains e-mail
                    contains_email = '@' in sentence
                    if self._is_matching_rule(contains_email, has_sentencefilters, is_found_sentencefilter, is_sentencefilter_headline_rows):
                        doNotUse = True
                        containsEmail = True

                    # check if contains phone number
                    contains_phonenumber = self.__containsPhoneNumber(sentence)
                    if self._is_matching_rule(contains_phonenumber, has_sentencefilters, is_found_sentencefilter, is_sentencefilter_headline_rows):
                        doNotUse = True
                        containsPhone = True

                    # update counts
                    if doNotUse == True:
                        removedSentences.append(sentence)
                        if containsEmail == True and containsPhone == True and containsName == True:
                            removedTypes['Name&Email&Phone'] = removedTypes['Name&Email&Phone'] + 1
                        elif containsName == True and containsEmail == True:
                            removedTypes['Name&Email'] = removedTypes['Name&Email'] + 1
                        elif containsName == True and containsPhone == True:
                            removedTypes['Name&Phone'] = removedTypes['Name&Phone'] + 1
                        elif containsName == True:
                            removedTypes['Name'] = removedTypes['Name'] + 1
                        elif containsEmail == True and containsPhone == True:
                            removedTypes['Email&Phone'] = removedTypes['Email&Phone'] + 1
                        elif containsEmail == True:
                            removedTypes['Email'] = removedTypes['Email'] + 1
                        elif containsPhone == True:
                            removedTypes['Phone'] = removedTypes['Phone'] + 1
                    else:
                        if not is_found_sentencefilter and j < sentences_count - 1:
                            is_sentencefilter_headline_rows = False
                        finalText = finalText + sentence + sentencepadding
                else: # do not check this sentence
                    if j < sentences_count - 1:
                        is_sentencefilter_headline_rows = False
                    finalText = finalText + sentence + sentencepadding

            if i < len(sections) - 1:
                finalText = finalText + '\n'

        return [finalText, removedSentences, removedTypes]

    def check_keywords(self, keywords, words, s, containsName, doNotUse):
        # check if contains any keyword (default this only checks for names)
        for k in keywords:
            if k in words or (len(k.split(' ')) > 1 and k in s):
                doNotUse = True
                containsName = True

                # but skip if the word is first in sentence ('Dina kompetenser ar...') - this will still get found by second word ('Dina Svensson är ...')
                if words[0] == k:
                    doNotUse = False
        return containsName, doNotUse

    def anonymizeText(self, s, extraKeywords=None, ignoredSentences=None, sentencefilters=None, checkSentencefilterHeadlines=False):
        '''
        :param s: Text to anonymize. One to many sentences.
        :param extraKeywords: Optional list with additional keywords, besides person names, to trigger anonymization
        :param ignoredSentences: Optional list with complete sentences to ignore.
        :param sentencefilters: Optional list with phrases that must be present in the sentences to remove.
        Only sentences with the found phrase, in combination with other personal data, will be removed.
        With the filter "facklig", the sentence "Du kan nå facklig företrädare på telefon 08-123456" will be removed,
        but not the sentence "Ring oss på telefon 08-123456".
        :param checkSentencefilterHeadlines: True if a check for sentencefilter should be done in the previous sentence
        with a following linefeed.
        :return:
        '''
        if extraKeywords is None:
            extraKeywords = []
        if ignoredSentences is None:
            ignoredSentences = []
        if sentencefilters is None:
            sentencefilters = []

        allKeywords = []
        allKeywords.extend(self._all_names) # names by default
        allKeywords.extend(extraKeywords)

        res = self.textRemoveSentences(s, allKeywords, ignoredSentences, sentencefilters, checkSentencefilterHeadlines)
        #print(res)

        return res

