import re
import nltk
import utils

class Search:

    def __init__(self):
        """
        Constructor
        """
        self.stemmer = nltk.SnowballStemmer("english")

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

    def search(self, query):
        """
        Search the database for given query and return relevent pages

        query   - The search keywords
        """
        
        """
        Breakdown the query
        remove stopwords
        Stem keywords

        Get all the pages with at least one matching word
        Rank the pages
        """

        query_tokens = self._get_words_from_query(query)

if __name__ == "__main__":
    s = Search()
    
    q = "How t[o learn: guitar playing ?"
    q_processed = s._get_words_from_query(q)
    # print (q_processed)

    s.search(q)