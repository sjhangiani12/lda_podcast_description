## file that contains the pre-trained lda model + the respective components associted with it
import gensim

ldamodel = gensim.models.ldamulticore.LdaMulticore.load('trained_lda.txt')

import nltk
nltk.download('wordnet')
nltk.download('stopwords')

import re
import html
import nltk

from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora
from nltk.corpus import reuters as rt
from nltk.corpus import stopwords as st
from stop_words import get_stop_words
from string import punctuation, whitespace

class LDAModel(object):

  LOT_OF_STOPWORDS = frozenset(list(STOPWORDS) + get_stop_words('en') + st.words('english'))
  lemma = nltk.wordnet.WordNetLemmatizer()

  WHITE_PUNC_REGEX = re.compile(r"[%s]+" % re.escape(whitespace + punctuation), re.UNICODE)

  def preprocess_document(self, document_text):
      """
          1.) Lowercase it all
          2.) Remove HTML Entities
          3.) Split by punctuations to remove them.
          4.) Stem / Lemmaize
          5.) Remove stop words
          6.) Remove unit length words
          7.) Remove numbers
      """
      def is_num(x):
          return not (x.isdigit() or (x[0] == '-' and x[1:].isdigit()))

      return list(
          filter(
              is_num,
              filter(
                  lambda x: len(x) > 1,
                  filter(
                      lambda x: x not in self.LOT_OF_STOPWORDS,
                      map(
                          lambda x: self.lemma.lemmatize(x),
                          re.split(
                              self.WHITE_PUNC_REGEX,
                              html.unescape(
                                  document_text.lower()
                              )
                          )
                      )
                  )
              )
          )
      )

  def getLDAPreds(self, temp):
    # takes in file, opens, and spits out the return value

    temp = [self.preprocess_document(temp)]
    temp
    dictionary = corpora.Dictionary(temp)
    corpus = [dictionary.doc2bow(text) for text in temp]
    topics = sorted(ldamodel[corpus],key=lambda x:x[1],reverse=True)
    text_topics = []
    top_pred = -1
    top_pred_prob = -1
    for i in topics[0]:
      print(i[1])
      print(ldamodel.print_topic(i[0]))
      if i[1] > top_pred_prob:
        top_pred = i[0]
        top_pred_prob = i[1]
    return(ldamodel.print_topic(top_pred))


