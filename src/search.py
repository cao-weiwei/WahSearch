import re
import nltk
import utils
import math
import numpy as np
import pymongo

from numpy.linalg import norm

class Search:

    def __init__(self):
        """
        Constructor
        """
        self.stemmer = nltk.SnowballStemmer("english")

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["wah_search"]
        self.index = mydb["index"]
        self.docs = mydb["docs"]

        self.doc_vectors = {}
        self.words = []
        self.set_doc_vectors()

    def set_doc_vectors(self):
        # Load the whole index
        index = self.index.find({})
        n_words = index.count()

        current_word_num = 0
        self.word_index = {}
        for i in index: # For each word in index
            word = i["word"]
            doc_list = i["doc_list"]

            for doc in doc_list:
                doc_id = doc["doc_id"]
                if self.doc_vectors.get(doc_id):
                    self.doc_vectors[doc_id]["d"][current_word_num] = doc["frequency_normalized"]
                else:
                    v = np.zeros(n_words)
                    v[current_word_num] = doc["frequency_normalized"]
                    self.doc_vectors[doc_id] = {"d": v}

            self.word_index[word] = current_word_num
            current_word_num += 1

        self.num_word_in_corpus = len(self.word_index.keys())

    def _get_words_from_query(self, query_raw):
        """
        Process the given search query
        Return a list of proper tokens
        Alphanumeric non-stopping stemmed
        Example: "How t[o learn: guitar playing ?" => ['how', 'learn', 'guitar', 'play'] 
        """

        query_alphanum = re.sub(r'[^a-zA-Z\s]', '', query_raw.strip())
        query_processed = utils.get_processed_words_list(query_alphanum.split())

        return query_processed

    def _angle_between_vectors(self, u, v):
        c = np.dot(u,v)/norm(u)/norm(v) # -> cosine of the angle
        angle = np.arccos(c) # if you really want the angle
        return angle

    def search(self, query):
        """
        Search the database for given query and return relevent pages

        query   - The search keywords
        """
        
        query_tokens = self._get_words_from_query(query.lower())
        
        print (query_tokens)

        # Get nuimber of docs
        docs_data = self.docs.find({})
        num_docs = docs_data[0]["cnt"]

        # Vectorize query
        query_tf = {}
        for token in query_tokens:
            query_tf[token] = query_tf.get(token, 0) + 1
        
        query_normalizer = norm(np.fromiter(query_tf.values(), dtype=float))

        for token in query_tokens:
            query_tf[token] = query_tf[token]/query_normalizer
        
        query_vector = np.zeros(self.num_word_in_corpus)

        # Vectorize the docs
        current_token_number = 0
        doc_vectors = {}
        for token in query_tokens:
            
            # Fetch doc numbers to use for IDF calculation
            docs_with_token_query = {"word": token}
            docs_with_token = self.index.find(docs_with_token_query)

            # If the search token is irrelevant, skip it
            if docs_with_token.count() == 0:
                continue
            
            # Calculate IDF
            docs_with_token = docs_with_token[0]
            num_docs_with_token = len(docs_with_token["doc_list"])
            idf = num_docs / num_docs_with_token
            
            # Get query tf-idf vector Vectorize query
            query_vector[self.word_index[token]] = query_tf[token] * math.log(idf)

            # Update the doc vector by multiplying the TF with IDF
            for doc in docs_with_token["doc_list"]:
                tf = doc["frequency_normalized"]
                tf_idf = tf * math.log(idf) # The final tf-idf score
                doc_id = doc["doc_id"]

                # Get doc tf-idf vector
                if doc_vectors.get(doc_id) == None:
                    doc_vectors[doc_id] = {"d": self.doc_vectors[doc_id]}

                doc_vectors[doc_id]["d"][self.word_index[token]] = tf_idf

            current_token_number += 1
        
        doc_ranks = []

        # Calculate cosine angles and create doc list with ranks
        for i in doc_vectors:
            doc_vector = doc_vectors[i]["d"]["d"]
            doc_ranks.append((self._angle_between_vectors(query_vector, doc_vector), i))

        # s = sorted(doc_ranks, key=lambda x: x[0])[:30]
        s = utils.quick_select(doc_ranks, 20, lambda x,y: x[0] <= y[0])

        for i in s:
            print (i)

if __name__ == "__main__":
    s = Search()
    
    q = "master of applied computing"
    q_processed = s._get_words_from_query(q)

    s.search(q)