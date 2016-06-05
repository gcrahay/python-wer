# -*- coding: utf8 -*-
from __future__ import unicode_literals

import time
from datetime import datetime

from eulxml import xmlmap


class DateMapper(xmlmap.fields.DateTimeMapper):
    """ Custom mapper for WER date

    Converts XML timestamp to python `datetime.datetime`
    """

    def to_python(self, node):
        rep = self.XPATH(node)
        return datetime.utcfromtimestamp(int(rep))

    def to_xml(self, dt):
        return time.mktime(dt.timetuple())


class DateField(xmlmap.fields.Field):
    """ Custom date field

    Uses the custom date mapper
    """

    def __init__(self, xpath):
        super(DateField, self).__init__(xpath,
                                        manager=xmlmap.fields.SingleNodeManager(),
                                        mapper=DateMapper())
