import webbrowser

from shell import Shell
from page import Page
from comments import Comments
from helpers import *

DEFAULT_SUBREDDIT = 'r/TrueReddit'


class Links(Shell):

    def __init__(self, subreddit=DEFAULT_SUBREDDIT, prompt='>>> '):
        super(Links, self).__init__(prompt=prompt)
        self.reddit = Page(subreddit)
        self.subreddit = subreddit

        self.action_list = {
            'o': self.open_link,
            'n': self.name,
            'c': self.expando,
            'h': self.open_comments,
            'r': self.load_subreddit,
            'g': self.custom_getter,
            'p': self.view_helper,
            '>': self.load_comments,
            '.': self.load_comments,
        }

    def print_attribute_from_key(self, key):
        if not(self.lower_num, self.upper_num) or \
                not key in self.reddit.list_of_entries[self.lower_num]:
            return
        x, _ = get_window_dimensions()
        for i in xrange(self.lower_num, self.upper_num):
            wrap_print(self.reddit.list_of_entries[i][key], x, i)

    def open_in_webbrowser_from_key(self, key):
        if not (self.lower_num != None and self.upper_num != None):
            return
        for site in self.reddit.list_of_entries[self.lower_num:self.upper_num]:
            url = site[key]
            if url[0] == '/':
                url = 'http://reddit.com' + url
            webbrowser.open_new_tab(url)

    def name(self, arg_list):
        self.print_attribute_from_key('title')

    def expando(self, arg_list):
        self.print_attribute_from_key('selftext')

    def open_comments(self, arg_list):
        self.open_in_webbrowser_from_key('permalink')
        self.view()

    def open_link(self, arg_list):
        self.open_in_webbrowser_from_key('url')
        self.view()

    def load_subreddit(self, arg_list):
        if arg_list:
            self.subreddit = ''
            if arg_list[0]:
                self.subreddit = '/r/' + arg_list[0]
        self.reddit.list_of_entries = Page(self.subreddit).list_of_entries
        self.view()

    def load_comments(self, arg_list):
        entry = self.reddit.list_of_entries[self.lower_num]
        self.reddit.fetch_comment_page(entry['permalink'])
        c = Comments(self.reddit.comment_page[1]['data']['children'],
                self, entry['title'])
        c.mainloop()
        self.view()

    def custom_getter(self, arg_list):
        for key in arg_list:
            try:
                self.print_attribute_from_key(key)
            except:
                pass

    def view_helper(self, junk_args):
        self.view()

    def view(self):
        i = 0
        x, y = get_window_dimensions()
        output = self.generate_output_to_print(i, x)
        print '\n'.join(output[:y - 1])
        self.print_blank_lines_after_titles(y, output)

    def generate_output_to_print(self, i, x):
        output = []
        for i, entry in enumerate(self.reddit.list_of_entries):
            title = unescape_html(entry['title'])
            title = title.replace('\n', '')
            if entry['selftext']:
                title = '+ ' + title
            elif entry['is_self']:
                title = '. ' + title
            output.append(u'{0:2} {1}'.format(i, title[:x - 3]))
        return output

    def print_blank_lines_after_titles(self, y, titles):
        num_blank_lines_needed = y - len(titles) - 2
        print '\n' * (num_blank_lines_needed - 1)
        if num_blank_lines_needed > 0:
            if self.lower_num:
                print u'%s %s%s' % (self.lower_num, self.upper_num, self.cmd)
            else:
                print self.input

