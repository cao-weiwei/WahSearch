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


@app.route('/suggestion', methods=['GET', 'POST'])
def suggested_keywords():
    if request.method == 'GET':
        regex_word = r"[\w]+"
        # get the original string
        raw_string = request.args.get("keywords")
        # checking spell and give suggestions
        raw_words = re.findall(regex_word, raw_string)  # remove non-letter chars

        # first step is doing spell check
        words_after_spell_check = spell_suggestions.spell_checker(" ".join(raw_words))
        # then for the last word doing auto complete
        last_word_auto_complete = spell_suggestions.auto_completer(words_after_spell_check.split(" ")[-1])
        print("words_after_spell_check={}, last_word_auto_complete={}".format(words_after_spell_check, last_word_auto_complete))
        # combine the results
        words_spell_suggestions = []
        for item in last_word_auto_complete:
            tmp = words_after_spell_check.split(" ")
            tmp[-1] = item
            words_spell_suggestions.append(" ".join(tmp))
        return json.dumps(words_spell_suggestions) if words_spell_suggestions else "No results!"
        
    return 'Nothing Happened!'


if __name__ == '__main__':
    app.run(debug=True)
