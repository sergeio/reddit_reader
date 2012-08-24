from deterministic_dingus import DingusWhitelistTestCase
import StringIO
import sys
#from json import JSONDecoder as JD

import reddit as mod
from reddit import Reddit
from reddit import Controller
import constants

class BaseTestCase(DingusWhitelistTestCase):

    module = mod
    mock_list = [
            'urllib2',
            'JSONDecoder',
            'sys',
            'webbrowser',
    ]

    def setup(self):
        super(BaseTestCase, self).setup()
        mod.urllib2.urlopen().read.return_value = constants.mock_http_json
        mod.JSONDecoder().decode().return_value = constants.mock_json


class TestReddit(BaseTestCase):

    def setup(self):
        super(TestReddit, self).setup()
        self.redd = Reddit('')

    def test_call_urlopen(self):
        assert mod.urllib2.calls('urlopen', 'http://reddit.com//.json')

    def test_call_decode(self):
        assert mod.JSONDecoder().calls('decode').once()

    def test_process_json_dict(self):
        assert len(self.redd.list_of_entries) == 25

class TestController(BaseTestCase):

    def setup(self):
        super(TestController, self).setup()
        self.controller = Controller()

        self.saved_stdout = sys.stdout
        self.mock_stdout = StringIO.StringIO()
        sys.stdout = self.mock_stdout

    def teardown(self):
        sys.stdout = self.saved_stdout

    def test_parse_input_two_nums(self):
        self.controller.parse_input('23-33bar')
        assert self.controller.lower_num == 23
        assert self.controller.upper_num == 33
        assert self.controller.cmd == 'bar'

    def test_parse_input_one_num(self):
        self.controller.parse_input('3bar')
        assert self.controller.lower_num == 3
        assert self.controller.upper_num == 4
        assert self.controller.cmd == 'bar'

    def test_parse_input_one_num_to_end(self):
        self.controller.parse_input('3-bar')
        assert self.controller.lower_num == 3
        assert self.controller.upper_num == 25
        assert self.controller.cmd == 'bar'

    def test_parse_input_no_num(self):
        self.controller.parse_input('o')
        assert self.controller.lower_num == 0
        assert self.controller.upper_num == 1
        assert self.controller.cmd == 'o'

    def test_extract_commands(self):
        self.controller.parse_input('1-2aoxr')
        assert self.controller.extract_commands() == {'o': [], 'r': []}

    def test_process_commands_change_subreddit(self):
        self.controller.act_on_input('r(pics)')
        assert self.controller.subreddit == '/r/pics'

    def test_extract_commands_with_arguments(self):
        self.controller.parse_input('3g(arg1, arg2)')
        assert self.controller.extract_commands() == {'g': ['arg1', 'arg2']}

    def test_extract_commands_when_multiple_with_arguments(self):
        self.controller.parse_input('1-23og(arg1, arg2)c(arg3)')
        assert self.controller.extract_commands() == {
                'o': [], 'g': ['arg1', 'arg2'], 'c': ['arg3']}

    def test_open_url_in_browser(self):
        self.controller.act_on_input('1o')
        assert mod.webbrowser.calls('open_new_tab').once()

    def test_open_url_in_browser_range_one_link(self):
        self.controller.act_on_input('1-2o')
        assert mod.webbrowser.calls('open_new_tab').once()

    def test_open_url_in_browser_range_two_links(self):
        self.controller.act_on_input('1-3o')
        assert not mod.webbrowser.calls('open_new_tab').once()
        assert mod.webbrowser.calls('open_new_tab')
        assert len(mod.webbrowser.calls) == 2

    def test_open_comments_in_browser(self):
        self.controller.act_on_input('1h')
        assert mod.webbrowser.calls('open_new_tab').once()

    def test_printing_names(self):
        self.controller.act_on_input('1-n')
        printed = self.mock_stdout.getvalue()
        sys.stdout = self.saved_stdout
        assert 'Canada' in printed

    def test_view_helper(self):
        self.controller.view_helper(['ignored'])
        printed = self.mock_stdout.getvalue()
        sys.stdout = self.saved_stdout
        assert 'Canada' in printed

    def test_view(self):
        # TODO:
        self.controller.view()
        printed = self.mock_stdout.getvalue()
        sys.stdout = self.saved_stdout
        assert 'Canada' in printed

    def test_load_comments(self):
        assert self.controller.reddit.comment_page == None
        self.controller.act_on_input('.hi')
        assert self.controller.reddit.comment_page

    def test_default_number_range_setting(self):
        self.controller.act_on_input('o')
        sys.stdout = self.saved_stdout
        print mod.webbrowser.calls
        assert mod.webbrowser.calls('open_new_tab')


class TestComment(BaseTestCase):

    def setup(self):
        super(TestComment, self).setup()
        self.controller = Comment('')

        self.saved_stdout = sys.stdout
        self.mock_stdout = StringIO.StringIO()
        sys.stdout = self.mock_stdout

    def teardown(self):
        sys.stdout = self.saved_stdout

