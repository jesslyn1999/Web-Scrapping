import spacy
from spacy.symbols import ORTH
nlp = spacy.load("en_core_web_sm", vectors=False, parser=False, entity=False)

#nlp.tokenizer.add_special_case(u'<i>', [{ORTH: u'<i>'}])
#nlp.tokenizer.add_special_case(u'</i>', [{ORTH: u'</i>'}])

doc = nlp('Hello, <i>world</i> !')

print([e.text for e in doc])