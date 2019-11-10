"""
To handle the indexing of the pages/documents

Author: Harsh Sodiwala
"""

import re
import nltk
import utils
import math

from bs4 import BeautifulSoup

class Indexer:

    def __init__(self):
        """
        Constructor
        """

        self.load_mongo_client()

    def load_mongo_client(self):
        """
        Load the mongoDB handler
        """

        import pymongo
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["wah_search"]
        self.index = mydb["index"]
        self.docs = mydb["docs"]

    def index_words(self, words, doc_name):

        # Generate table with word frequence
        word_dict = {}

        # Populate word dictionary
        all_words = words
        for word in utils.get_processed_words_list(all_words):
            word_dict[word] = word_dict.get(word,0) + 1
        
        # Calculate normalizing factor: Root of sum of squares of word frequencies
        normalizing_factor = 0.0
        for word in word_dict:
            normalizing_factor += math.pow(word_dict[word], 2)
        normalizing_factor = math.sqrt(normalizing_factor)

        print ("Normalizer: ", normalizing_factor)

        for word in word_dict:
            cnt = word_dict[word]
            # print ("Normalized frequency: ", word, cnt/normalizing_factor)
            query = dict()
            query[word] = {"$exists": True}
            
            # upd = {"$push": {word: {docId: count}}}
            upd = dict()
            upd["$push"] = dict()
            upd["$push"][word] = {
                "doc_id": doc_name,
                "frequency": cnt,
                "frequency_normalized": cnt / normalizing_factor
            }

            # Append the page with count to the word->doc list
            update_status = self.index.update(query, upd)
            updated = update_status.get('updatedExisting')

            # If the word is seen first time
            if not updated:
                upd = dict()
                upd[word] = [{"doc_id": doc_name, "frequency": cnt, "frequency_normalized": cnt / normalizing_factor}]
                self.index.insert(upd)

    def update_doc_list(self, doc_name):
        q = {"pages.lst": {"$exists": True}}
        if self.docs.find(q).count():
            if not self.docs.find({"pages.lst": doc_name}).count():
                self.docs.update({}, {"$inc": {"pages.cnt": 1}})
                self.docs.update({}, {"$addToSet": {"pages.lst": doc_name}})

        else:
            self.docs.insert({
                "pages": {
                    "cnt":1,
                    "lst": [doc_name]
                }
            })

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
        title_words = title.strip().split() * 3 # Title words are more important than body words
        body_words = body.strip().split()
        all_words = title_words + body_words

        # Insert in the inverted index
        self.index_words(all_words, doc_name)
        self.update_doc_list(doc_name)

if __name__ == "__main__":
    #test
    sample_file_path = '../../sample_data/Accessible Rich Internet Applications (WAI-ARIA) 1.0.htm'

    file = open(sample_file_path, 'r')
    data = file.read()
    file.close()

    indexer = Indexer()
    indexer.index_html_page("www.example1.com", data)