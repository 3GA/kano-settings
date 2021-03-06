#
# boot_config_parser.py
#
# Copyright (C) 2016 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#
# Parse and manipulate the boot config file for ease of modification
#

import re

from kano_settings.system.boot_config.boot_config_filter import Filter
from kano_settings.system.boot_config.boot_config_line import BootConfigLine


class BootConfigParser(object):
    CONFIG_FILTER_PATTERN = r'^\[(\w*)=?([\w\-]*)\]$'
    CONFIG_FILTER_RE = re.compile(CONFIG_FILTER_PATTERN)

    def __init__(self, conf_file_lines, debug=False):
        if not conf_file_lines:
            conf_file_lines = []

        if isinstance(conf_file_lines, basestring):
            conf_file_lines = conf_file_lines.splitlines()

        self.current_filter = 'all'
        self.debug = debug
        self.config = []

        for line in conf_file_lines:
            self.add(line)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.config)

    def add(self, line):
        if self.is_filter(line):
            return

        line = BootConfigLine(line, self.current_filter, debug=self.debug)
        self.config.append(line)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, item, value):
        self.set(item, value)

    def __iter__(self):
        for line in self.config:
            yield line

    def __len__(self):
        return len(self.config)

    def is_filter(self, line):
        if isinstance(line, BootConfigLine):
            self.current_filter = line.filter
            return False

        if not isinstance(line, basestring):
            return False

        filter_match = self.CONFIG_FILTER_RE.match(line)

        if not filter_match:
            return False

        filter_groups = filter_match.groups()
        new_filter = filter_groups[0]

        if filter_groups[1]:
            new_filter += '=' + filter_groups[1]

        self.current_filter = new_filter

        return True

    def get_line(self, setting, config_filter=Filter.ALL, fallback=False, ignore_comments=False):
        search = {
            'setting': setting,
            'filter': config_filter
        }

        for line in reversed(self.config):
            if line == search and not (ignore_comments and line.is_comment):
                return line

        if fallback and config_filter != Filter.ALL:
            return self.get_line(setting, config_filter=Filter.ALL, ignore_comments=ignore_comments)

        return BootConfigLine({
            'setting': setting,
            'filter': config_filter
        })

    def get(self, setting, config_filter=Filter.ALL, fallback=False, ignore_comments=False):
        return self.get_line(
            setting,
            config_filter=config_filter,
            fallback=fallback,
            ignore_comments=ignore_comments
        ).value

    def set(self, setting, value, config_filter=Filter.ALL):
        # NB if value is None, we comment out the setting
        # If the value is not None, we uncomment the setting and set it to the value
        search = {
            'setting': setting,
            'filter': config_filter
        }

        for line in reversed(self.config):
            if line == search:
                line.value = value or 0
                line.is_comment = value is None
                line.is_commented_out = value is None
                line.is_manual_comment = False
                return

        new_line = BootConfigLine({
            'setting': setting,
            'filter': config_filter,
            'value': value or 0,
            'is_comment': value is None,
            'is_commented_out': value is None
        })

        self.add(new_line)

    def dump(self):
        current_filter = Filter.ALL
        output = ''

        for line in self.config:
            if line.filter != current_filter:
                current_filter = line.filter
                output += self.construct_filter_entry(current_filter)

            output += '{}\n'.format(line)

        return output

    @staticmethod
    def sanitise_filter(config_filter):
        return config_filter.strip(' [').rstrip(' ]')

    @staticmethod
    def construct_filter_entry(config_filter):
        # This module doesn't understand overlapping filters, so always
        # terminate previous filter.
        terminate_filter = ''
        if config_filter != Filter.ALL:
            terminate_filter = '[all]\n'
        return '{}[{config_filter}]\n'.format(terminate_filter,
                                              config_filter=config_filter)
