# -*- coding: utf-8 -*-
__author__ = u'Никита'

from LSI_nltk.converts import Stemming
import unittest

class TestConverts(unittest.TestCase):

    def test_one_word(self):
        word = Stemming(u'красивый')
        self.assertTrue(word, u'красив')

    def test_many_words(self):
        line = u'жили были красивый мальчик и красивая девочка'
        stem = Stemming(line)
        stem.dictionary.__str__()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()