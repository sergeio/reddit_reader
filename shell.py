import re

from helpers import *


class Shell(object):

    def __init__(self, prompt=u'? '):
        self.prompt = prompt
        self.cmd = None
        self.lower_num = 0
        self.upper_num = 1
        self.input = ''
        self.action_list = {}

    def view(self):
        pass

    def mainloop(self):
        self.view()
        while not '<' in self.input and \
                not 'q' in self.input and \
                not ',' == self.input:
            self.input = raw_input(self.prompt)
            self.act_on_input(self.input)

    def act_on_input(self, input):
        """Parses input and acts on it.
        """
        if not input:
            return
        self.parse_input(input)
        commands = self.extract_commands()
        self.execute_commands(commands)

    def execute_commands(self, commands):
        """Executes all commands passed as an argument.
        """
        for cmd in commands:
            self.action_list[cmd](commands[cmd])
            if cmd == 'r':
                break

    def extract_commands(self):
        """Pulls valid commands out of the input, and returns them as a list.
        """
        # import pdb; pdb.set_trace()
        left_i = 0
        right_i = 1
        commands = {}
        cmd = self.cmd

        if not cmd:
            return
        while left_i < len(cmd):
            sub_cmd = cmd[left_i:right_i]
            if sub_cmd in self.action_list:
                arg_len, arguments = self.extract_command_arguments(right_i)
                commands[sub_cmd] = arguments
                left_i = right_i + arg_len
                right_i = left_i + 1
            else:
                left_i, right_i = self.update_i(left_i, right_i)
        return commands

    def update_i(self, left_i, right_i):
        if right_i == len(self.cmd):
            left_i += 1
            right_i = left_i + 1
        else:
            right_i += 1
        return left_i, right_i

    def extract_command_arguments(self, right_i):
        """Extract optional arguments passed to commands in parentheses.
        """
        cmd = self.cmd
        arg_len = 0
        if right_i + 1 < len(cmd) and \
            cmd[right_i] == '(' and ')' in cmd[right_i + 1:]:
            r = re.match('\((.*?)\)', cmd[right_i:])
            arguments = r.group(1).split(', ')
            arg_len = len(r.group(1))
        else:
            arguments = []
        return arg_len, arguments

    def parse_input(self, input):
        """Takes input and parses it. Expects 1-23cmd, or 3cmd, or cmd.
        """
        r = re.match('(\d+)?(-\d*)?(\D.*)', input)
        if not r:
            return
        lower_num = r.group(1)
        upper_num = r.group(2)
        command = r.group(3)
        if lower_num:
            self.lower_num = int(lower_num)
            if upper_num:
                # Want to be able to say 3-o to open all links from 3 to end
                if upper_num == '-':
                    self.upper_num = len(self.reddit.list_of_entries)
                else:
                    self.upper_num = int(upper_num[1:])
            else:
                self.upper_num = self.lower_num + 1
        self.cmd = command

