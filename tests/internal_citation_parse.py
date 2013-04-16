#vim: set encoding=utf-8
from unittest import TestCase
import internal_citations

class ParseTest(TestCase):

    def test_multiple_paragraphs(self):
        """ Ensure that offsets work correctly in a simple multiple paragraph scenario. """

        parser = internal_citations.InternalCitationParser()
        text = u"the requirements of paragraphs (c)(3), (d)(2), (e)(1), (e)(3), and (f) of this section"
        citations = parser.parse(text, parts = ['1005', '6'])

        self.assertEqual(len(citations), 5)

        for c in citations:
            if c['citation'] == ['1005', '6', u'c', u'3']:
                self.assertEqual(text[c['offsets'][0][0]], '(')
                self.assertEquals(c['offsets'], [(31, 37)])
                self.assertEquals(text[c['offsets'][0][0] + 1], 'c')
            if c['citation'] == ['1005', '6', u'd', u'2']:
                self.assertEquals(text[c['offsets'][0][0] + 1], 'd')

    def test_multiple_paragraph_or(self):
        """ Ensure that an 'or' between internal citations is matched correctly. """
        parser = internal_citations.InternalCitationParser()
        text = u"set forth in paragraphs (b)(1) or (b)(2)" 
        citations = parser.parse(text, parts = ['1005', '6'])
        self.assertEquals(2, len(citations))

    def test_single_paragraph(self):
        """ Ensure that offsets work correctly in a simple single paragraph citation. """
        parser = internal_citations.InternalCitationParser()
        text = 'The requirements in paragraph (a)(4)(iii) of'
        citations = parser.parse(text, parts = ['1005', '6'])
        c = citations[0]
        self.assertEquals(text[c['offsets'][0][0]:c['offsets'][0][1]], 
                u'(a)(4)(iii)')
        self.assertEquals(['1005', '6', 'a', '4', 'iii'], c['citation'])

    def test_single_labeled_paragraph(self):
        """ Ensure the parser doesn't pick up unecessary elements, such as the 
        (a) in the text below. """
        parser = internal_citations.InternalCitationParser()
        text = '(a) Solicited issuance. Except as provided in paragraph (b) of this section'
        citations = parser.parse(text, parts = ['1005', '6'])
        self.assertEqual(1, len(citations))

    def test_multiple_section_citation(self):
        """ Ensure that offsets work correctly in a simple multiple section citation case. """
        parser = internal_citations.InternalCitationParser()
        text = u"set forth in §§ 1005.6(b)(3) and 1005.11 (b)(1)(i) from 60 days"
        citations = parser.parse(text, parts = ['1005', '6'])

        self.assertEqual(len(citations), 2)
        occurrences = 0
        for c in citations:
            if c['citation'] == [u'1005', u'6', u'b', u'3']:
                occurrences += 1
                self.assertEquals(text[c['offsets'][0][0]:c['offsets'][0][1]], u'1005.6(b)(3)')
            if c['citation'] == [u'1005', u'11', u'b', u'1', u'i']:
                occurrences += 1
                self.assertEquals(text[c['offsets'][0][0]:c['offsets'][0][1]], u'1005.11 (b)(1)(i)')
        self.assertEquals(occurrences, 2)

    def test_single_section_citation(self):
        """ Ensure that offsets work correctly in a simple single section citation case. """
        parser = internal_citations.InternalCitationParser()
        text = u"date in § 1005.20(h)(1) must disclose"
        citations = parser.parse(text, parts = ['1005', '6'])
        c =  citations[0]
        self.assertEquals(text[c['offsets'][0][0]:c['offsets'][0][1]], u'1005.20(h)(1)')

    def test_multiple_paragraph_single_section(self):
        text = u'§ 1005.10(a) and (d)'
        parser = internal_citations.InternalCitationParser()
        result = parser.parse(text, parts = ['1005', '6'])
        self.assertEqual(2, len(result))
        self.assertEqual(['1005', '10', 'a'], result[0]['citation'])
        self.assertEqual(['1005', '10', 'd'], result[1]['citation'])
        start, end = result[0]['offsets'][0]
        self.assertEqual(u'1005.10(a)', text[start:end])
        start, end = result[1]['offsets'][0]
        self.assertEqual(u'(d)', text[start:end])

    def test_multiple_paragraph_single_section2(self):
        text = u'§ 1005.7(b)(1), (2) and (3)'
        parser = internal_citations.InternalCitationParser()
        result = parser.parse(text, parts = ['1005', '6'])
        self.assertEqual(3, len(result))
        self.assertEqual(['1005', '7', 'b', '1'], result[0]['citation'])
        self.assertEqual(['1005', '7', 'b', '2'], result[1]['citation'])
        self.assertEqual(['1005', '7', 'b', '3'], result[2]['citation'])
        start, end = result[0]['offsets'][0]
        self.assertEqual(u'1005.7(b)(1)', text[start:end])
        start, end = result[1]['offsets'][0]
        self.assertEqual(u'(2)', text[start:end])
        start, end = result[2]['offsets'][0]
        self.assertEqual(u'(3)', text[start:end])

    def test_multiple_paragraphs_this_section(self):
        text = u'paragraphs (c)(1) and (2) of this section'
        parser = internal_citations.InternalCitationParser()
        result = parser.parse(text, parts = ['1005', '6'])
        self.assertEqual(2, len(result))
        self.assertEqual(['1005', '6', 'c', '1'], result[0]['citation'])
        self.assertEqual(['1005', '6', 'c', '2'], result[1]['citation'])
        start, end = result[0]['offsets'][0]
        self.assertEqual(u'(c)(1)', text[start:end])
        start, end = result[1]['offsets'][0]
        self.assertEqual(u'(2)', text[start:end])

    def test_abc(self):
        text = "(d) Procedures in paragraph (c) of this section, the financial in this paragraph (d) if it"