from json import JSONDecoder
import urllib2

from helpers import *


class Page:

    jd = JSONDecoder()

    def __init__(self, subreddit):
        self.subreddit = subreddit
        self.comment_page = None

        page = self._fetch_subreddit()
        self.raw_json_dict = Page.jd.decode(page.read())
        self.list_of_entries = self.extract_list_of_entries(self.raw_json_dict)

    def _fetch_subreddit(self):
        print 'Loading...'
        return self._fetch_page(self.subreddit)

    def fetch_comment_page(self, url):
        print 'Loading...'
        page = self._fetch_page(url)
        self.comment_page = Page.jd.decode(page.read())
        for e in self.comment_page:
            unescape_html_in_whole_dictionary(e)

    def _fetch_page(self, url):
        print ('http://www.reddit.com/%s.json/' % url)
        return urllib2.urlopen('http://www.reddit.com/%s.json' % url)

    def extract_list_of_entries(self, raw_json_dict):
        entries = [entry['data'] for entry in raw_json_dict['data']['children']]
        for e in entries:
            unescape_html_in_whole_dictionary(e)
        return entries

