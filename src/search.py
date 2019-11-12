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

        doc_vectors = {}
        num_tokens = len(query_tokens)
        current_token_number = 0
        
        # Vectorize query
        query_tf = {}
        for token in query_tokens:
            query_tf[token] = query_tf.get(token, 0) + 1
        
        query_normalizer = norm(np.fromiter(query_tf.values(), dtype=float))

        for token in query_tokens:
            query_tf[token] = query_tf[token]/query_normalizer
        
        query_vector = np.zeros(num_tokens)

        # Vectorize the docs
        for token in query_tokens:
            
            # Calculate idf
            docs_with_token_query = {"word": token}
            docs_with_token = self.index.find(docs_with_token_query)

            if docs_with_token.count() == 0:
                continue
            
            docs_with_token = docs_with_token[0]
            num_docs_with_token = len(docs_with_token["doc_list"])
            
            idf = num_docs / num_docs_with_token
            
            # Get query tf-idf vector Vectorize query
            query_vector[current_token_number] = query_tf[token] * math.log(idf)

            for doc in docs_with_token["doc_list"]:
                tf = doc["frequency_normalized"]
                tf_idf = tf * math.log(idf) # The final tf-idf score
                doc_id = doc["doc_id"]

                # Get doc tf-idf vector
                v = doc_vectors.get(doc_id, np.zeros(num_tokens))
                v[current_token_number] = tf_idf
                doc_vectors[doc_id] = v

            current_token_number += 1
        
        doc_ranks = []

        for i in doc_vectors:
            doc_vector = doc_vectors[i]
            doc_ranks.append((self._angle_between_vectors(query_vector, doc_vector), i))

        s = sorted(doc_ranks, key=lambda x: x[0])[:30]

        for i in s:
            print (i)
            print (query_vector)
            print (doc_vectors[i[1]])

if __name__ == "__main__":
    s = Search()
    
    q = "admission requirement in master of applied computing"
    q_processed = s._get_words_from_query(q)
    # print (q_processed)

    s.search(q)