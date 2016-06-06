# -*- coding: utf8 -*-
from __future__ import unicode_literals

import time
from datetime import datetime

from eulxml import xmlmap


def windows_to_unix_timestamp(windows_timestamp):
    magic_number = 11644473600
    return (windows_timestamp / 10000000) - magic_number


def unix_to_windows_timestamp(unix_timestamp):
    magic_number = 116444736000000000
    return (unix_timestamp * 10000000) + magic_number


class DateMapper(xmlmap.fields.DateTimeMapper):
    """ Custom mapper for WER date

    Converts XML timestamp to python `datetime.datetime`
    """

    def to_python(self, node):
        return datetime.utcfromtimestamp(windows_to_unix_timestamp(int(node)))

    def to_xml(self, dt):
        return unix_to_windows_timestamp(time.mktime(dt.timetuple()))


class DateField(xmlmap.fields.Field):
    """ Custom date field

    Uses the custom date mapper
    """

    def __init__(self, xpath):
        super(DateField, self).__init__(xpath,
                                        manager=xmlmap.fields.SingleNodeManager(),
                                        mapper=DateMapper())
