"""
The spell checking module
For a given word get 
"""

import json

class SpellChecker:

    def __init__(self):
        """
        Constructor
        """
        self.dict = None
        self._load_words()

    def _load_words(self):
        """
        Load the words in an appropriate data structure.
        Intuition: use something like { 1:["a", "b", ...], 2:["ab", "cd", ...] }
        """
        pass

    def get_correct_words(self, word):
        """
        word    -- The word to search similar words for
        return -- List of similar words
        """
    
        similar_words = ["abcde", "efghij", "klmno"]
        return json.dumps(similar_words)