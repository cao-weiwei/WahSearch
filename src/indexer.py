"""
To handle the indexing of the pages/documents

Author: Harsh Sodiwala
"""

import re
import nltk

from bs4 import BeautifulSoup

class Indexer:

    def __init__(self):
        """
        Constructor
        """

        self.stemmer = nltk.SnowballStemmer("english")
        self._load_stop_words()
        self.load_mongo_client()

    def load_mongo_client(self):
        """
        Load the mongoDB handler
        """

        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["wah_search"]
        self.mycol = mydb["index"]

    def _load_stop_words(self):
        """
        Load stop words in memory
        """
        
        stop_words_file = open("./stop_words.dat")
        stop_word_data = stop_words_file.read()
        stop_words_list = stop_word_data.split('\n')

        self.stop_words = dict.fromkeys(stop_words_list, True)

    def _index_word(self):
        pass

    def index_html_page(self, doc_name, doc_content):
        """
        Parse the HTML page, fetch keywords and index them

        doc_name    - The reference (URL) to the page
        doc_content - THe HTML content of the page
        """

        parser = BeautifulSoup(doc_content, 'html.parser') # Initialize parser

        # Get title
        title = ""
        title_tag = parser.find('title')
        if title_tag:
            title = title_tag.text.lower()

        # Keep title and body words separate for now
        # TODO - Implementing word weightage in future

        # Get whole body part in text
        body = ""
        body_tag = parser.find('body')
        if title_tag:
            body = body_tag.text.lower()

        non_alpha_num_exp = r'[^a-z0-9 ]' # Regex: Everything except aplhanumeric characters

        title = re.sub(non_alpha_num_exp,' ', title)
        body = re.sub(non_alpha_num_exp,' ', body) # Replace non alphanumeric characters with space
        # TODO - Take care of words that become like randomword34 after replacement

        # Get list of words from both
        title_words = [self.stemmer.stem(word) for word in title.strip().split() if not self.stop_words.get(word)]
        body_words = [self.stemmer.stem(word) for word in body.strip().split() if not self.stop_words.get(word)]

        # Get word table with frequence
        word_dict = {}

        # Process title words
        for title_word in title_words:
            if not self.stop_words.get(title_word):
                word = self.stemmer.stem(title_word)
                # TODO: Decide on title's weught
                word_dict[word] = word_dict.get(word,0) + 1

        # Process body words
        for body_word in body_words:
            if not self.stop_words.get(body_word):
                word = self.stemmer.stem(body_word)
                word_dict[word] = word_dict.get(word,0) + 1
        
        for word in word_dict:
            cnt = word_dict[word]
            query = dict()
            query[word] = {"$exists": True}
            
            # upd = {"$push": {word: {docId: count}}}
            upd = dict()
            upd["$push"] = dict()
            upd["$push"][word] = {
                "doc_id": doc_name,
                "cnt": cnt
            }

            # Append the page with count to the word->doc list
            update_status = self.mycol.update(query, upd)
            updated = update_status.get('updatedExisting')

            # If the word is seen first time
            if not updated:
                upd = dict()
                upd[word] = [{"doc_id": doc_name, "cnt": cnt}]
                self.mycol.insert(upd)

if __name__ == "__main__":
    #test
    sample_file_path = '../../sample_data/Accessible Rich Internet Applications (WAI-ARIA) 1.0.htm'

    file = open(sample_file_path, 'r')
    data = file.read()
    file.close()

    indexer = Indexer()
    indexer.index_html_page("www.example2.com", data)