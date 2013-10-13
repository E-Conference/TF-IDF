# -*- coding: cp1252 -*-
from math import exp, expm1
from stemming.porter2 import stem
import re

class Term:
    def __init__(self, content, tf):
        self.content = content
        self.tf = tf

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
            if(self.tf < other.tf):
                return True
        else:
            return False

    def __le__(self, other):
        if(other != None):
            if(self.tf <= other.tf):
                return True
        else:
            return False

    def __gt__(self, other):
        if(other != None):
            if(self.tf > other.tf):
                return True
        else:
            return False

    def __ge__(self, other):
        if(other != None):
            if(self.tf >= other.tf):
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

    return math.log( (card_D / card_D_C), 10 )


def fetch_docs(endpoint):
    return 0

doc = escape("Lookup algorithms[edit] A simple stemmer looks up the inflected form in a lookup table. The advantages of this approach is that it is simple, fast, and easily handles exceptions. The disadvantages are that all inflected forms must be explicitly listed in the table: new or unfamiliar words are not handled, even if they are perfectly regular (e.g. iPads ~ iPad), and the table may be large. For languages with simple morphology, like English, table sizes are modest, but highly inflected languages like Turkish may have hundreds of potential inflected forms for each root. A lookup approach may use preliminary part-of-speech tagging to avoid overstemming.[2] The production technique[edit] The lookup table used by a stemmer is generally produced semi-automatically. For example, if the word is run, then the inverted algorithm might automatically generate the forms running, runs, runned, and runly. The last two forms are valid constructions, but they are unlikely to appear in a normal English-language text. Suffix-stripping algorithms[edit] Suffix stripping algorithms do not rely on a lookup table that consists of inflected forms and root form relations. Instead, a typically smaller list of rules is stored which provides a path for the algorithm, given an input word form, to find its root form. Some examples of the rules include: if the word ends in 'ed', remove the 'ed' if the word ends in 'ing', remove the 'ing' if the word ends in 'ly', remove the 'ly' Suffix stripping approaches enjoy the benefit of being much simpler to maintain than brute force algorithms, assuming the maintainer is sufficiently knowledgeable in the challenges of linguistics and morphology and encoding suffix stripping rules. Suffix stripping algorithms are sometimes regarded as crude given the poor performance when dealing with exceptional relations (like 'ran' and 'run'). The solutions produced by suffix stripping algorithms are limited to those lexical categories which have well known suffixes with few exceptions. This, however, is a problem, as not all parts of speech have such a well formulated set of rules. Lemmatisation attempts to improve upon this challenge. Prefix stripping may also be implemented. Of course, not all languages use prefixing or suffixing. Additional algorithm criteria[edit] Suffix stripping algorithms may differ in results for a variety of reasons. One such reason is whether the algorithm constrains whether the output word must be a real word in the given language. Some approaches do not require the word to actually exist in the language lexicon (the set of all words in the language). Alternatively, some suffix stripping approaches maintain a database (a large list) of all known morphological word roots that exist as real words. These approaches check the list for the existence of the term prior to making a decision. Typically, if the term does not exist, alternate action is taken. This alternate action may involve several other criteria. The non-existence of an output term may serve to cause the algorithm to try alternate suffix stripping rules. It can be the case that two or more suffix stripping rules apply to the same input term, which creates an ambiguity as to which rule to apply. The algorithm may assign (by human hand or stochastically) a priority to one rule or another. Or the algorithm may reject one rule application because it results in a non-existent term whereas the other overlapping rule does not. For example, given the English term friendlies, the algorithm may identify the ies suffix and apply the appropriate rule and achieve the result of friendl. friendl is likely not found in the lexicon, and therefore the rule is rejected. One improvement upon basic suffix stripping is the use of suffix substitution. Similar to a stripping rule, a substitution rule replaces a suffix with an alternate suffix. For example, there could exist a rule that replaces ies with y. How this affects the algorithm varies on the algorithm's design. To illustrate, the algorithm may identify that both the ies suffix stripping rule as well as the suffix substitution rule apply. Since the stripping rule results in a non-existent term in the lexicon, but the substitution rule does not, the substitution rule is applied instead. In this example, friendlies becomes friendly instead of friendl. Diving further into the details, a common technique is to apply rules in a cyclical fashion (recursively, as computer scientists would say). After applying the suffix substitution rule in this example scenario, a second pass is made to identify matching rules on the term friendly, where the ly stripping rule is likely identified and accepted. In summary, friendlies becomes (via substitution) friendly which becomes (via stripping) friend. This example also helps illustrate the difference between a rule-based approach and a brute force approach. In a brute force approach, the algorithm would search for friendlies in the set of hundreds of thousands of inflected word forms and ideally find the corresponding root form friend. In the rule-based approach, the three rules mentioned above would be applied in succession to converge on the same solution. Chances are that the rule-based approach would be faster.")
#doc = escape("Python fully supports mixed arithmetic: when a binary arithmetic operator has operands of different numeric types, the operand with the “narrower” type is widened to that of the other, where plain integer is narrower than long integer is narrower than floating point is narrower than complex. Comparisons between numbers of mixed type use the same rule. [2] The constructors int(), long(), float(), and complex() can be used to produce numbers of a specific type.")
tc = TermCollection(len(doc.split(" ")))

for term in doc.split(" "):
    if(len(term) > 3):
        tf_ = tf(term, doc)
        clTerm = Term(term, tf_)
        tc.insert(clTerm)

print(str(len(tc.terms)) + " potential keywords extracted.")

for term in tc.retrieve(5):
    print(term.content + " | " + str(term.tf))
