import nltk

try:
    stop_words_file = open("./stop_words.dat")
    stop_word_data = stop_words_file.read()
    stop_words_list = stop_word_data.split('\n')
    stop_words = dict.fromkeys(stop_words_list, True)

    stemmer = nltk.SnowballStemmer("english")
except Exception:
    print ("Error while loading processing engine. WIll index useless stuff along with useful ones.")

def get_processed_words_list(words):

    """
    Process words list and return a searchable words list
    remove stop words
    stem remaining words
    """

    processed_list = []

    for word in words:
        if not stop_words.get(word):
            word = stemmer.stem(word)
            processed_list.append(word)

    return processed_list