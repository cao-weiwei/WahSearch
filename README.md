# WahSearch
Our little search engine :)

## Introduction
- It's based on Flask framework which is written in Python. 
- We implement three main servers, they get requests from front-end, calling corresponding methods to handle with requests. After each transaction, the server will return the data in JSON and to the front-end.

## Data Collection
- A spider that will crawl the webpages using Breadth First-Search strategy.
- For each webpage, a Parser will extract links from html tag.
- To support full text search over a set of documents, Inverted Index is used here.

## Main Features
1. Searching
2. Auto-complete
- The algorithm for query checking it’s the non-word errors correction based on Edit Distance.
3. Spelling checking
- It will give spell suggestions, it will correct spelling and show suggestions when typing the keywords
- By using Trie, put all the words from the dictionary in terms of chars. Then we get the sufﬁx according to the given preﬁx.
