#-*- coding: utf-8 -*-
__author__ = u'Никита'

from pprint import pprint
import numpy as np
import math

from nltk.stem.snowball import RussianStemmer
# ----------------------------------------- use only once --------------------------------------------------------------
stemmer = RussianStemmer()
#-----------------------------------------------------------------------------------------------------------------------

class BaseDict(object):
    def __init__(self, docs, ignore=''',:'!'''):
        if not isinstance(docs, list):
            raise Exception("type of documents must be a list")

        self.ignore = ignore
        self.base = {}
        self.len_docs = len(docs)
        for i, document in enumerate(docs):
            if isinstance(document, (str, unicode)):
                self.add_document(i, document)

    def normalise(self, number, word, add=True):
        if isinstance(word, unicode):
            word = word.encode('utf-8')

        word = word.lower().translate(None, self.ignore)
        word = word.decode('utf-8')
        word = stemmer.stem(word)

        if word in self.base:
            self.base[word][number] += 1
        else:
            if add:
                word_info = np.zeros(self.len_docs)
                word_info[number] += 1
                self.base[word] = word_info

    def add_document(self, number, document):
        for word in document.split(' '):
            self.normalise(number, word, add=True)

    def delete_waste(self, count_ignore):
        if not isinstance(count_ignore, int):
            raise Exception("count of w words must be integer number")
        return [key for key in self.base.keys() if sum(self.base[key]) > count_ignore]

    def __str__(self):
        for key, value in self.base.iteritems():
            (10 - len(key))*' '
            print key, (13 - len(key))*' ', '-> ', value

    def __json_read__(self, filename):
        import json
        self.dictionary = {}
        try:
            with open(filename, 'r') as f:
                text = f.read()
                self.dictionary = json.loads(text)
                return self.dictionary
        except IOError:
            raise Exception("problem with file")
        except:
            raise Exception(ValueError)

    def __json_write__(self, filename):
        import json
        try:
            with open(filename, 'w') as f:
                f.write(json.dumps(self.base))
            print 'file saved'
        except IOError:
            raise Exception("problem with file")
        except:
            raise ValueError

class SVDMatrixCreator(BaseDict):
    def __init__(self, docs, count_ignore):
        super(SVDMatrixCreator, self).__init__(docs)
        self.keys = self.delete_waste(count_ignore)

    def create_matrix(self):
        self.matrix = np.zeros([len(self.keys), self.len_docs])
        for i, word in enumerate(self.keys):
            for j in self.base[word]:
                self.matrix[i, j] += 1

    def svd_creator(self):
        from numpy.linalg.linalg import svd
        self.U, self.S, self.Vt = svd(self.matrix)

    def __str_U__(self):
        pprint(self.U)

    def __str_S__(self):
        pprint(self.S)

    def __str_Vt__(self):
        pprint(self.Vt)

class LSI(object):
    '''
    enter_data = dictionary with word : number_of_word_in_doc
    base_dict = {word: [1, 0, 3], ...} dictionary of words with their counts in different docs
    '''
    def __init__(self, svd_matrix):
        if isinstance(svd_matrix, SVDMatrixCreator):
            self.svd = svd_matrix
            self.svd.create_matrix()
            self.matrix = self.svd.matrix

    @classmethod
    def from_raw_data(cls, docs, count_ignore=None):
        svd_matrix = SVDMatrixCreator(docs=docs, count_ignore=count_ignore)
        return cls(svd_matrix)


    def tf_idf(self):
        word_on_doc = np.sum(self.matrix, axis=0)
        docs_on_word = np.sum(np.asarray(self.matrix > 0, 'i'), axis=1)
        rows, cols = self.matrix.shape
        for i in xrange(rows):
            for j in xrange(cols):
                self.matrix[i, j] = (self.matrix[i, j] / word_on_doc[j]) * math.log(float(cols) / docs_on_word[i])

class Approximate:
    ''' We have words with docs in 3D (svd matrix) - our base .
        Also we want to know theme/tag/class ... of enter document
        from enter document we will try get U, S, Vt - svd
        and find nearest tag/class/theme ...
     '''

    def __init__(self, base_matrix, enter_matrix):
        self.base = base_matrix
        self.enter = enter_matrix

    @classmethod
    def enter_from_SVDClass(cls, base_matrix, svd_matrix):
        return cls(base_matrix, svd_matrix.matrix)

    @classmethod
    def enter_from_file(cls, base_matrix, filename):
        docs = []
        with open(filename, 'r') as f:
            line = f.readline()
            while line != "":
                docs.append(line)
                line = f.readline()

        if len(docs) == 0:
            raise Exception("empty enter file")

        svd_matrix = SVDMatrixCreator(docs, 1)
        return cls(base_matrix, svd_matrix.matrix)

    def __str__(self):
        pass

    def approximate(self):
        pass
'''
    def find(self, word):
        self.prepare()
        idx = self.dic(word)
        if not idx:
            print 'слово невстерчается'
            return []
        if not idx in self.keys:
            print 'слово отброшено как не имеющее значения которое через stopwords'
            return []
        idx = self.keys.index(idx)
        print 'word --- ', word, '=', self.dictionary[self.keys[idx]], '.\n'
        # получаем координаты слова
        wx, wy = (-1 * self.U[:, 1:3])[idx]
        print 'word {}\t{:0.2f}\t{:0.2f}\t{}\n'.format(idx, wx, wy, word)
        arts = []
        xx, yy = -1 * self.Vt[1:3, :]
        for k, v in enumerate(self.docs):
            ax, ay = xx[k], yy[k]
            dx, dy = float(wx - ax), float(wy - ay)
            arts.append((k, v, ax, ay, sqrt(dx * dx + dy * dy)))
        return sorted(arts, key = lambda a: a[4])
'''


docs =[
    "Британская полиция знает о местонахождении основателя WikiLeaks",
    "В суде США США начинается процесс против россиянина, рассылавшего спам",
    "Церемонию вручения Нобелевской премии мира бойкотируют 19 стран",
    "В Великобритании арестован основатель сайта Wikileaks Джулиан Ассандж",
    "Украина игнорирует церемонию вручения Нобелевской премии",
    "Шведский суд отказался рассматривать апелляцию основателя Wikileaks",
    "НАТО и США разработали планы обороны стран Балтии против России",
    "Полиция Великобритании нашла основателя WikiLeaks, но, не арестовала",
    "В Стокгольме и Осло сегодня состоится вручение Нобелевских премий",
    "В Париже Кожемякин Александр обосрался на вручении Нобелевской премии",
    "В Пекине Александр Кожемякин насрал на китайца, при попытке сходить в туалет",
    "НАТО и США объединяют свои усилия в борьбе против Александра и его другей"

]

base = BaseDict(docs)
base.__str__()

lsi = LSI.from_raw_data(docs, 1)
lsi.svd.svd_creator()
lsi.svd.__str_S__()
lsi.svd.__str_U__()
lsi.svd.__str_Vt__()