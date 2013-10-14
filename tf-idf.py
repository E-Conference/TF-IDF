# -*- coding: cp1252 -*-
import MySQLdb
import math
from stemming.porter2 import stem
import re
import sys

class Term:
    def __init__(self, content, tf, itf):
        self.content = content
        self.tf = tf
        self.itf = itf

    def tfitf(self):
        try:
            return self.tf*self.itf
        except TypeError:
            print(">> Extraction failed -- Either tf or itf is NoneType \n @tf[" + str(self.tf)+ "];@itf[" + str(self.itf) + "] --\nSee the following stacktrace for further information.")
            sys.exit(0)

    def __eq__(self, other):
        if(other != None):
            if(self.content == other.content):
                return True
        else:
            return False

    def __ne__(self, other):
        if(other != None):
            if(self.content == other.content):
                return False
        else:
            return True

    def __lt__(self, other):
        if(other != None):
            if(self.tfitf() < other.tfitf()):
                return True
        else:
            return False

    def __le__(self, other):
        if(other != None):
            if(self.tfitf() <= other.tfitf()):
                return True
        else:
            return False

    def __gt__(self, other):
        if(other != None):
            if(self.tfitf() > other.tfitf()):
                return True
        else:
            return False

    def __ge__(self, other):
        if(other != None):
            if(self.tfitf() >= other.tfitf()):
                return True
        else:
            return False

class TermCollection:
    def __init__(self, max_size):
        self.terms = [None] * max_size
        self.length = 0

    def insert(self, term):
        if term not in self.terms:
            self.terms[self.length] = term
            self.length = self.length+1
        self.terms = sorted(self.terms)

    def retrieve(self, max_kw):
        arr = [None] * max_kw
        for x in range(1, max_kw+1):            
            arr[x-1] = self.terms[self.length-x]
        return arr

def escape(document):
    return re.sub(r'([^\s\w]|_)+', '', document)

def freq(term, document):
    return float(document.count(term)) / float(len(document.split(" ")))

# Assuming your document is special-chars escaped
def tf(term, document):
    max_freq = 0
    
    for doc_term in document.split(" "):
        if(freq(doc_term, document) > max_freq):
            max_freq = freq(doc_term, document)

    if(freq(term, document) == 0):
        return 0.5
    else:
        return ((0.5 * freq(term, document)) / max_freq) + 0.5

# Assuming every documents are special-chars escaped
def idf(term, documents):
    card_D = len(documents)
    card_D_C = 0

    for document in documents:
        if term in document.split(" "):
            card_D_C = card_D_C + 1

    try:
        return math.log1p(card_D / card_D_C)
    except ZeroDivisionError:
        print(">> Divided By Zero -- trace: @cardDocuments[" + str(len(documents)) + "] @cardDC is zero --") 

def fetch_docs(endpoint):
    return 0

def get_keywords(document_id, host, username, password, dbname, tbl_name, col_name, kw_nb, char_limit):
    db = MySQLdb.connect(host=host, user=username, passwd=password, db=dbname)
    cur = db.cursor()
    document = ""

    cur.execute("SELECT COUNT(*) FROM " + tbl_name + " WHERE length(x_key) > " + str(char_limit))
    for row in cur.fetchall():
        max_size = int(row[0])

    documents = [None] * max_size

    cur.execute("SELECT " + col_name + " FROM " + tbl_name + " WHERE length(x_key) > " + str(char_limit))

    i = 0
    for row in cur.fetchall() :
        documents[i] = escape(row[0])
        i = i+1

    cur.execute("SELECT " + col_name + " FROM " + tbl_name + " WHERE id = " + str(document_id))
    for row in cur.fetchall():
        document = escape(row[0])

    tc = TermCollection(len(document.split(" ")))

    for term in document.split(" "):
        if(len(term) > 3):
            tf_ = tf(term, document)
            idf_ = idf(term, documents)
            clTerm = Term(term, tf_, idf_)
            tc.insert(clTerm)
    
    return tc.retrieve(kw_nb)


kws = get_keywords(388, "localhost", "root", "", "wwwconference", "xproperty", "x_key", 5, 50)     

print("Extraction result:\n========")
for term in kws:
    try:
        print(term.content)
    except AttributeError:
        print(">> WARNING: Unexpected end of keywords!")
