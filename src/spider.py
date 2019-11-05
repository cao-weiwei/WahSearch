"""
The engine to carry out searching through the web and indexing webpages

Author: Harsh Sodiwala
"""

import urllib.request
import urllib.error
import urllib.parse
import urllib.robotparser

from bs4 import BeautifulSoup

class Spider:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    The spider that will crawl the web
    Use the given seeds and crawl through them
    Collect webpages on the way and store/index them
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    def __init__(self):
        """ 
        Constructor 
        """
        
        self.seeds = ["https://www.uwindsor.ca"] # Crawling starts from here
        self.urls = []

    def get_http_response(self, url):
        """
        Send an HTTP request and return the response for given URL

        url     -- The URL of the webpage to get HTTP Response of
        return  -- HTTPRespone object
        """

        try:
            http_response = urllib.request.urlopen(url)    
            print("Get_url: ", http_response.geturl())
            return http_response
        except Exception:
            print("Error while fetching ", url)
            return None

    def get_links(self, url, html_text):
        """
        Fetch links in the source code of the given page

        url         -- The url of the webpage
        html_text   -- The source code of the webpage

        return      -- String: List of links
        """

        parser = BeautifulSoup(html_text, 'html.parser') # Initialize parser
        links = parser.find_all('a') # Fetch anchor tags

        hrefs = []

        for link in links:
            href = link.get('href')
            abs_href = urllib.parse.urljoin(url, href) # Handle relative links
            # abs_href = abs_href.split('?')[0]
            abs_href = abs_href.split('#')[0] # Remove fragment identifier
            hrefs.append(abs_href)

        return hrefs

    def index_page(self, url, html_text):
        """
        Index the retrieved webpage

        url         -- URL of the webpage to index
        html_text   -- The source code of the page
        """
        
        # TODO - Write the indexing logic 
        self.urls.append(url)

    def run(self):
        """
        The entry point
        """

        max_depth = 20000 #fetch only max_dept number of webpages
        depth = 0 #initial depth
        visited = {} #keep track of visited links to avoid cycle
        
        # BFS from each seed
        q = [_ for _ in self.seeds]

        while len(q) and depth < max_depth:
            
            print ("At depth ", depth)
            
            url = q.pop(0)

            # get html response and index the page
            http_response = self.get_http_response(url)
            visited[url] = True

            if not http_response: # Skip if page not retrieved
                continue

            html_text = http_response.read()
            response_url = http_response.geturl()
            
            if url != response_url and visited.get(response_url):
                continue

            visited[response_url] = True  # mark visited links to avoid cycles in BFS
            self.index_page(url, html_text) # Index the retrieved webpage
            links = self.get_links(url, html_text) # Get links from the current page

            # Push the new found links to ToCrawl list [BFS]
            for link in links:
                if not visited.get(link):
                    q.append(link)
        
            depth += 1
        
        for i in self.urls:
            print(i)

s = Spider()
s.run()