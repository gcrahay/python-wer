# -*- coding: utf8 -*-
from __future__ import unicode_literals

import time
from datetime import datetime

from eulxml import xmlmap


def windows_to_unix_timestamp(windows_timestamp):
    """ Converts a Windows timestamp to Unix one

    :param windows_timestamp: Windows timestamp
    :type windows_timestamp: int

    :return: Unix timestamp
    :rtype: int
    """
    magic_number = 11644473600
    return int((windows_timestamp / 10000000) - magic_number)


def unix_to_windows_timestamp(unix_timestamp):
    """ Converts a Windows timestamp to Unix one

    :param unix_timestamp: Unix timestamp
    :type unix_timestamp: int

    :return: Windows timestamp
    :rtype: int
    """
    magic_number = 116444736000000000
    return (unix_timestamp * 10000000) + magic_number


class DateMapper(xmlmap.fields.DateTimeMapper):
    """ Custom mapper for WER date

    Converts XML timestamp to python :class:`datetime.datetime`
    """

    def to_python(self, node):
        """ Converts internal Windows timestamp to Python :class:`datetime.datetime`

        :param node: XML node value
        :type node: basestring
        :return: Python datetime
        :rtype: :class:`datetime.datetime`
        """
        return datetime.utcfromtimestamp(windows_to_unix_timestamp(int(node)))

    def to_xml(self, dt):
        """ Converts Windows timestamp

        :param dt: date and time to convert
        :return: Windows timestamp
        :rtype: int
        """
        return unix_to_windows_timestamp(time.mktime(dt.timetuple()))


class DateField(xmlmap.fields.Field):
    """ Custom date field

    Uses the custom date mapper
    """

    def __init__(self, xpath):
        super(DateField, self).__init__(xpath,
                                        manager=xmlmap.fields.SingleNodeManager(),
                                        mapper=DateMapper())
