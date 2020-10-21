import os
import sys
import pytest
# import requests
import unionrep_anonymization


@pytest.fixture(scope="module")
def unionrep_anonymize():
    anonymizer = unionrep_anonymization.unionrep_anonymize_swe()
    anonymizer.initialize()
    return anonymizer

# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_name_true_positive(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan namn. Kontakta vår fackliga företrädare Bosse Bengtsson. En sista mening utan namn.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    # output = res[0]
    # print(output)
    removedSentences = res[1]

    assert len(removedSentences) == 1

# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_name_true_negative(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan namn. Hos oss arbetar Bosse Bengtsson.\nEn sista mening utan namn.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    # output = res[0]
    # print(output)
    removedSentences = res[1]
    #
    assert len(removedSentences) == 0


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_no_personal_true_negative(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan personuppgifter. En andra mening utan personuppgifter.\nEn sista mening utan personuppgifter.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    # output = res[0]
    # print(output)
    removedSentences = res[1]
    #
    assert len(removedSentences) == 0


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_no_personal_true_negative2(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan personuppgifter. För Fackliga kontaktpersoner se https://www.justatest.com/sv/karriar/kontakta-oss/facklig-kontakt/\nEn sista mening utan personuppgifter.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    # output = res[0]
    # print(output)
    removedSentences = res[1]
    #
    assert len(removedSentences) == 0


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_phonenumber_true_positive(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan telefon. Kontakta vår fackliga företrädare på telefon 08-123123123. En sista mening utan telefon.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    # output = res[0]
    # print(output)
    removedSentences = res[1]

    assert len(removedSentences) == 1

# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_phonenumber_true_negative(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan telefon. Ring oss på telefon 08-123123123.\nEn sista mening utan telefon.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    # output = res[0]
    # print(output)
    removedSentences = res[1]
    #
    assert len(removedSentences) == 0


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_email_true_positive(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan email. Kontakta vår fackliga företrädare genom att skriva till adam@svensson.se. En sista mening utan email.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    # output = res[0]
    # print(output)
    removedSentences = res[1]

    assert len(removedSentences) == 1


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_email_true_negative(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan email. Skriv till adam@svensson.se. En sista mening utan email.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    # output = res[0]
    # print(output)
    removedSentences = res[1]
    #
    assert len(removedSentences) == 0



# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_filter_no_name_true_negative(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan personuppgifter. Vi är stolta över vår fackliga företrädare och denna mening ska inte tas bort. En sista mening utan personuppgifter.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    # output = res[0]
    # print(output)
    removedSentences = res[1]
    #
    assert len(removedSentences) == 0


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_unionrep_anonymize_with_extra_keywords_without_sentencefilters(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan extra keywords.
                    En andra mening med extra keywords, ta bort mig, men kommer ändå att behållas eftersom det saknas sentencefilters.
                    En tredje mening med extra keywords, radera bort mig, men kommer ändå att behållas eftersom det saknas sentencefilters.
                    En sista mening utan extra keywords.'''

    extraKeywords = ['ta bort mig', 'radera mig']
    ignoredSentences = []

    res = unionrep_anonymize.anonymizeText(input_text, extraKeywords, ignoredSentences)

    removedSentences = res[1]

    assert len(removedSentences) == 0

# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_unionrep_anonymize_with_extra_keywords_with_sentencefilters(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan extra keywords.
                    En andra mening med extra keywords, facklig företrädare med keywords ta bort mig, ska raderas.
                    En tredje mening med extra keywords, facklig företrädare med keywords radera mig, ska raderas.
                    En sista mening utan extra keywords.'''

    extraKeywords = ['ta bort mig', 'radera mig']
    ignoredSentences = []

    res = unionrep_anonymize.anonymizeText(input_text, extraKeywords, ignoredSentences)

    removedSentences = res[1]

    assert len(removedSentences) == 2
    assert extraKeywords[0] in removedSentences[0]
    assert extraKeywords[1] in removedSentences[1]


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_linefeed_true_positive(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''En första mening utan personuppgifter. 
Fackliga företrädare: 
Bosse Bengtsson tel: 08 123 4567  
En sista mening utan personuppgifter.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    output = res[0]
    # print(output)
    removedSentences = res[1]
    # print(removedSentences)

    assert len(removedSentences) == 1


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_multiple_linefeeds_true_positive(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''
Upplysningar om tjänsten lämnas av:
Centrumchef, Karin Testsson, 010-123 12 34, karin@testsson.se
Lokala fackliga företrädare:
Läkarförbundet är överläkare reumatologiska kliniken, Bosse Bengtsson, bosse@bengtsson.se, 
Fackliga företrädare för:
Vårdförbundet är Kalle Karlsson, kalle@karlsson.se
Vision är Maja majasson, maja@majasson.se
Kommunal är Frida Frid, frida@frid.se
Ansökan
Sista ansökningsdag är 2 november 2020.
'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    output = res[0]
    # print(output)
    removedSentences = res[1]
    # print(removedSentences)

    assert len(removedSentences) == 4



# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_multiple_linefeeds_true_positive2(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''Vill du veta mer?
Karin Testsson Rektor, tfn. 036-123456
Kalle Karlsson bitr.rektor, tfn. 036-234567
Maja majasson bitr.rektor  tfn, 036- 345678
Fackliga företrädare lärarförbundet. Frida Frid, tfn. 036-456789 och Lars Larsson, tfn. 036-4567890
Facklig företrädare kommunal. Mattis Mattiasson, tfn. 036-5678901'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    output = res[0]
    # print(output)
    removedSentences = res[1]
    # print(removedSentences)
    removedSentencesJoined = ' '.join(removedSentences)

    assert len(removedSentences) > 0

    assert 'Frida Frid' in removedSentencesJoined and '036-456789' in removedSentencesJoined
    assert 'Lars Larsson' in removedSentencesJoined and '036-4567890' in removedSentencesJoined
    assert 'Mattis Mattiasson' in removedSentencesJoined and '036-5678901' in removedSentencesJoined

    assert 'Karin Testsson' not in removedSentencesJoined
    assert 'Kalle Karlsson' not in removedSentencesJoined
    assert 'Maja majasson' not in removedSentencesJoined


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_multiple_linefeeds_true_positive3(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''Fackliga företrädare:
 Facklig representant, Kalle Persson
 Tel: 070-123 45 56'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    output = res[0]
    # print(output)
    removedSentences = res[1]
    # print(removedSentences)
    removedSentencesJoined = ' '.join(removedSentences)

    assert len(removedSentences) > 0

    assert 'Kalle Persson' in removedSentencesJoined and '070-123 45 56' in removedSentencesJoined


# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_multiple_linefeeds_true_negative(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''Fackliga kontaktpersoner
Information om fackliga kontaktpersoner, se Hjälp för sökande.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    output = res[0]
    # print(output)
    removedSentences = res[1]
    # print(removedSentences)
    removedSentencesJoined = ' '.join(removedSentences)

    assert len(removedSentences) == 0



# @pytest.mark.skip(reason="Temporarily disabled")
@pytest.mark.unit
def test_anonymize_unionrep_multiple_linefeeds_true_negative2(unionrep_anonymize):
    print('\n============================', sys._getframe().f_code.co_name, '============================')
    input_text = '''Fackliga kontaktpersoner
Information om fackliga kontaktpersoner, se Hjälp för sökande.'''
    res = unionrep_anonymize.anonymizeText(input_text, [], [])
    output = res[0]
    # print(output)
    removedSentences = res[1]
    # print(removedSentences)
    removedSentencesJoined = ' '.join(removedSentences)

    assert len(removedSentences) == 0






if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__), '-svv', '-ra', '-m unit'])
