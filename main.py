# -*- coding: utf-8 -*-
import re


def parse_email(email):
    ar = email.split('@')
    if len(ar) == 2 and 2 < len(ar[1]) < 257 and len(ar[0]) < 129:
        if re.match(r'((^(?!-)[a-z0-9_-]*(?!-)[a-z0-9_-])([.]((?!-)[a-z0-9_-]*(?!-)[a-z0-9_]))+)+$', ar[1]) is not None\
                and re.match(r'(?:(?:"(?:[a-z0-9_!:,-]|(?:\.(?!\.)))*")|(?:[a-z0-9_-])|(?:\.(?!\.)))+$', ar[0]) is not None:
            return True
        return False
    return False


from random import randint
import unittest

class ParseTests(unittest.TestCase):
    # examples
    host = r'nikita_end'
    domain = r'edu.hse.com'

    def make_str(self, length):
        return ''.join([chr(randint(97, 122)) for i in xrange(length)])

    def test_length_host(self):
        #incorrect string
        for length in [0, 129]:
            string_incorrect = self.make_str(length) + '@' + self.domain
            self.assertFalse(parse_email(string_incorrect))

        #correct string
        string_correct = self.make_str(randint(1, 128)) + '@' + self.domain
        self.assertTrue(parse_email(string_correct))

    def test_length_domain(self):
        # incorrect string
        length = randint(257, 1000)
        string_incorrect = self.host + '@' + self.make_str(int(length / 2)) + '.' + self.make_str(int(length / 2))
        self.assertFalse(parse_email(string_incorrect))

        self.assertFalse(parse_email(self.host + '@' + '.' + self.make_str(1)))
        self.assertFalse(parse_email(self.host + '@' + self.make_str(1) + '.'))

        #correct string
        length = randint(3, 256)
        string_correct = self.host + '@' + self.make_str(int(length / 2)) + '.' + self.make_str(int(length / 2)+1)
        self.assertTrue(parse_email(string_correct))

    def test_dash(self):
        # all of variants of dash position
        string_parts = [self.make_str(randint(1, 120)), '.', self.make_str(randint(1, 120)), '']
        for i in xrange(len(string_parts)):
            string = self.host + '@'
            for j, part in enumerate(string_parts):
                if j == i:
                    string += '-'
                string += part
            self.assertFalse(parse_email(string))

        string_correct = self.host + '@' + self.make_str(20) + '-' + self.make_str(10) + '.' + self.make_str(20)
        self.assertTrue(parse_email(string_correct))

    def test_symbols_in_quotes(self):
        start = 'nikita_'
        end = 'end'
        quotes = ['"', '"']
        symbols = ['!', ',', ':']

        for symbol in symbols:
            string_correct = start + quotes[0] + symbol + quotes[1] + end + '@' + self.domain
            self.assertTrue(parse_email(string_correct))

        for symbol in symbols:
            string_incorrect = start + symbol + end + '@' + self.domain
            self.assertFalse(parse_email(string_incorrect))


    def test_full_stops(self):
        string_incorrect = '"' + self.make_str(randint(0, 64)) + '..' + '"' +\
                           self.make_str(randint(0, 64)) + '@' + self.domain
        self.assertFalse(parse_email(string_incorrect))

        string_incorrect = self.host + '@' + self.make_str(randint(1, 100)) + '..' + self.make_str(randint(0, 120))
        self.assertFalse(parse_email(string_incorrect))



if __name__ == '__main__':
    unittest.main()