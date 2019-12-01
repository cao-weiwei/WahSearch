import re

from flask import Flask, request, render_template
import json 

from SpellSuggestion import SpellSuggestion
from search import Search


app = Flask(__name__, template_folder='templates')
spell_suggestions = SpellSuggestion()

@app.route('/')
def hello_world():
    return 'Hello World!'
    
@app.route('/search', methods=['GET', 'POST'])
def search_keywords():
    if request.method == 'GET':
        keywords = request.args.get("keywords")
        page_number_query = int(request.args.get("page_number"))
        links_per_page = int(request.args.get("per_page"))

        s = Search()
        search_results = []
        page_indexer = 1
        
        ans = s.search(keywords, links_per_page, page_number=page_number_query)
    
        return json.dumps(ans)

@app.route('/suggestion', methods=['GET', 'POST'])
def suggested_keywords():
    if request.method == 'GET':
        regex_word = r"[\w]+"
        # get the original string
        raw_string = request.args.get("keywords")
        # checking spell and give suggestions
        raw_words = re.findall(regex_word, raw_string)  # remove non-letter chars
        query = re.sub('[^0-9a-zA-Z]', ' ', raw_string)

        print (query)
        print (query.split())

        query = query.split(" ")

        to_spell_check = query[: -1]
        to_autocomp = query[-1]
        
        corrections = [spell_suggestions.correct_word(x) for x in to_spell_check]
        autocompletes = spell_suggestions.auto_completer(to_autocomp)

        ans = [corrections + [x] for x in autocompletes]
        ans = [" ".join(x) for x in ans]

        return json.dumps(ans)
        
    return 'Nothing Happened!'


if __name__ == '__main__':
    app.run(debug=True)
