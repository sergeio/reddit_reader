import os
import re

def has_body(entry):
    if not 'data' in entry:
        return False
    if not 'body' in entry['data']:
        return False
    return True

def unescape_html(text):
    replace_dict = {
            u'%27': u'\'', # Not sure about this one
            u'&lt;': u'<',
            u'&gt;': u'>',
            # This has to be last
            u'&amp;': u'&',
            }
    for key in replace_dict:
        text = text.replace(key, replace_dict[key])
    return text

def unescape_html_in_whole_dictionary(dictionary):
    for key in dictionary:
        if type(dictionary[key]) == str:
            dictionary[key] = unescape_html(dictionary[key])
        elif type(dictionary[key]) == dict:
            unescape_html_in_whole_dictionary(dictionary[key])

def wrap_print(string, max_width, prepending, numspaces=3):
    """Wraps the string to not wrap in the middle of a word, using max_width as
    the maximum width of the line.

    Then, prints out the wrapped string, prepending the passed in argument to
    the first line.

    numspaces is the amount of spaces to prepend to every line (except maybe
    the first line).

    Returns the amount of lines printed.
    """
    # TODO: Use this for all printing
    text = wraplines(string, max_width - numspaces)
    if numspaces == 0:
        print u'{{0:{0}}} {{1}}'.format(numspaces - 1).format(prepending, text[0])
    print u'{{0:{0}}} {{1}}'.format(numspaces - 1).format(prepending, text[0])
    for line in text[1:]:
        print u'{0}{1}'.format(' ' * numspaces, line)
    return len(text)

def escape_regex_chars(text):
    # '\\' has to be first
    regex = ['\\', '?', '*', '+', '[', ']', '(',
             ')', '.', '^', '$', '{', '}', '|']
    for char in regex:
        text = text.replace(char, '\\' + char)

    return text

def get_domain(url, default='link'):
    domain = default
    result = re.search('(http://|www\.)([^/ ]+)', url)
    if result:
        domain = result.group(2)
    return domain

def get_window_dimensions():
    y, x =  os.popen('stty size', 'r').read().split()
    return int(x), int(y)

def wraplines(string, max_width):
    return_list = []

    for line in string.split(u'\n'):
        line_width = 0
        split_line = line.split(' ')
        aggregate_string = []
        for word in split_line:
            # Truncate very long words (TODO: split them across multiple lines)
            if len(word) > max_width:
                word = word[0:max_width]
            if line_width + 1 + len(word) > max_width:
                return_list.append(' '.join(aggregate_string))
                aggregate_string = [word]
                line_width = len(word)
            else:
                line_width += len(word) + 1
                aggregate_string.append(word)
        return_list.append(' '.join(aggregate_string))

    return return_list
