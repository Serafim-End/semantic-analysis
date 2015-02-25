# -*- coding: utf-8 -*-
__author__ = u'Никита'

from nltk.stem.snowball import RussianStemmer

# ----------------------------------------- use only once --------------------------------------------------------------
stemmer = RussianStemmer()
#------------------------------------------- stemming ------------------------------------------------------------------

class Dictionary(object):
    def __init__(self, dictionary=None):
        if dictionary is None:
            self.__dictionary__ = {}
        else:
            self.__dictionary__ = dictionary

    def __add__(self, other):
        '''transform and add normal word to dictionary'''
        if isinstance(other, unicode):
            other = stemmer.stem(other.lower())
            if other not in self.__dictionary__:
                self.__dictionary__[other] = 1
            else:
                self.__dictionary__[other] += 1
        else:
            raise Exception('Dictionary: incorrect type')

    def __str__(self):
        ''' print dictionary '''
        for key, value in self.__dictionary__.iteritems():
            print key, ' -> ', value

    def __len__(self):
        return len(self.__dictionary__)

class Stemming:
    def __init__(self, lines=None, ignore_stop=False, dictionary=None):
        self.dictionary = Dictionary(dictionary=dictionary)
        if isinstance(lines, unicode) or isinstance(lines, str):
            line_array = lines.split(' ')
            if len(line_array) > 1:
                self.stem_array(line_array)
            else:
                self.dictionary.__add__(line_array[0])
        elif isinstance(lines, list):
            self.stem_array(lines)
        else:
            raise Exception('Stemming: incorrect type')

    @classmethod
    def stream_stem(cls, stream, ignore_stopwords=False, dictionary=None):
        '''transform file data to dictionary with normal words '''
        if not isinstance(stream, file):
            raise TypeError('type of stream is not file')
        try:
            words = []
            line = stream.readline()
            while line is not '':
                for word in line.split(' '):
                    words.append(word)
                line = stream.readline()
            return cls(words, ignore_stopwords, dictionary)
        except IOError:
            raise Exception('cannot read from file')
        except ValueError:
            raise Exception('incorrect data in file')

    def stem_array(self, array):
        ''' transform array to normal array '''
        for word in array:
            if isinstance(word, str) or isinstance(word, unicode):
                self.dictionary.__add__(word)
            else:
                raise Exception('incorrect type of word')

    def __str__(self):
        """ print normal dictionary"""
        if self.dictionary is not None:
            self.dictionary.__str__()

    def __len__(self):
        """ number of normal dictionary pairs """
        return len(self.dictionary)