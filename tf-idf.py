from math import exp, expm1
import re

def escape(document):
    return re.sub(r'([^\s\w]|_)+', '', document)

def freq(term, document):
    return document.count(term) / len(document.split(" "))

# Assuming your document is special-chars escaped
def tf(term, document):
    max_freq = 0
    
    for doc_term in document.split(" "):
        if(f(doc_term, document) > max_freq):
            max_freq = f(doc_term, document)
        
    return ((0.5 * f(term, document)) / max_freq) + 0.5

# Assuming every documents are special-chars escaped
def idf(term, documents):
    card_D = len(documents)
    card_D_C = 0

    for document in documents:
        if term in document.split(" "):
            card_D_C = card_D_C + 1

    return math.log( (card_D / card_D_C), 10 )


def fetch_docs(endpoint):
    return 0
            
