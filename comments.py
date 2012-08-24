import webbrowser
import re

from shell import Shell
from helpers import *


class Comments(Shell):

    def __init__(self, comment_page, Links,
            page_name='', prompt='C>> ', depth = 1):
        super(Comments, self).__init__(prompt=prompt)
        self.comment_page = comment_page
        self.links = []
        self.Links = Links
        self.page_name = page_name
        self.depth = depth

        self.action_list = {
            '>': self.go_deeper,
            '.': self.go_deeper,
            'p': self.view_helper,
            'o': self.open_story_link,
            'h': self.open_comments,
            'c': self.Links.expando,
            'f': self.follow_link,
        }


    def go_deeper(self, dummy):
        replies = self.comment_page[self.lower_num]['data']['replies']
        if replies == '':
            print 'You shall not pass.'
            return
        c = Comments(
                replies['data']['children'],
                self.Links,
                page_name=self.page_name,
                prompt=('C%d> ' % (self.depth + 1)),
                depth=(self.depth + 1),
                )
        c.mainloop()
        self.view()

    def view_helper(self, arg_list):
        self.view()

    def open_story_link(self, arg_list):
        """Opens the story corresponding to the current Comments page in the
        browser
        """
        self.Links.open_link(arg_list)
        self.view()

    def open_comments(self, arg_list):
        self.Links.open_comments(arg_list)
        self.view()

    def follow_link(self, arg_list):
        if not arg_list:
            arg_list = [0]
        for i in arg_list:
            try:
                webbrowser.open_new_tab(self.links[self.lower_num][int(i)])
            except Exception as x:
                print 'Failed opening link "%s"' % i
                print x


    def view(self):
        x, y = get_window_dimensions()
        lines_printed = 0
        numspaces = 3

        lines_printed = wrap_print(self.page_name, x, '', numspaces=2)
        self._parse_links()
        for i, entry in enumerate(self.comment_page):
            if self._is_a_loser(entry):
                continue
            entry['data']['body'] = unescape_html(entry['data']['body'])
            text = self._format_comment_lines(entry, x, i)
            if len(text) + lines_printed > y - 2:
                break
            lines_printed += wrap_print(entry['data']['body'], x, i)
            # for line in text:
                # wrap_print(line, 
        print '\n' * (y - lines_printed - 3)

    def _parse_links(self):
        """Look through all the comments for something that looks like a link,
        add those links to self.links, and format the links inside of the
        Comments body to look nice.
        """

        for entry in self.comment_page:
            entry_links = []
            if self._is_a_loser(entry):
                continue
            reddit_link_pattern = '\[([^\]]+)\]\(([^\)]+)\)|(http://\S+)'
            r_links = re.findall(reddit_link_pattern, entry['data']['body'])
            for link_i, group in enumerate(r_links):
                url = group[1] if group[1] else group[2]
                entry_links.append(url)
                self._make_link(entry, link_i, group, url)
            self.links.append(entry_links)

    def _make_link(self, entry, link_i, group, url):
        """Change links from reddit's format into somehing shorter/simpler,
        and most importantly 'clickable'.

        This updates the entry[data][body] directly.

        Bug/Feature: If multiple links in the comment point to the same site,
        the link-making will replace all instances of the link with the index
        of the first occurance of that link.
        ie: if you have 3 of the same link, the same index '0->' will prepend
        all three links, letting you know that all those links are the same

        The above bug/feature can be fixed by appending count=1 to the
        parameters of re.sub.

        """
        text = group[0] if group[0] else get_domain(group[2])
        entry['data']['body'] = re.sub(
                u'\[{0}\]\({1}\)|{2}'.format(
                    escape_regex_chars(text),
                    escape_regex_chars(url),
                    escape_regex_chars(url)),
                u'{0}->{1}'.format(link_i, text.replace(' ', '_')),
                entry['data']['body'])

    def _format_comment_lines(self, entry, x, i):
        """Wraps lines and adds entry numbers to the first line of each
        Comments.
        """
        # TODO: Indent quoted text (starting with '>')
        numspaces = 3
        if self._is_a_loser(entry):
            return []
        text = wraplines(entry['data']['body'], x)
        text[0] = u'{0:2} {1}'.format(str(i), text[0])
        return text

    def _is_a_loser(self, entry):
        """Returns True if Comments doesn't exist or has a bad score
        """
        if not 'body' in entry['data']:
            return True
        up = int(entry['data']['ups'])
        down = int(entry['data']['downs'])
        if up - down < -3:
            return True
        return False

