# -*- coding: utf8 -*-
from __future__ import unicode_literals

from eulxml import xmlmap
from datetime import datetime
import time

REPORT_TYPES = (
    (0, 'Non Critical'),
    (1, 'Critical'),
    (2, 'Application Crash'),
    (3, 'Application Hang'),
    (4, 'Kernel Error')
)

FILE_TYPES = (
    (1, 'User Document'),
    (2, 'Other')
)


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
                manager = xmlmap.fields.SingleNodeManager(),
                mapper = DateMapper())


class MachineInfo(xmlmap.XmlObject):
    """ MachineInfo complex type
    """
    ROOT_NAME = 'MACHINEINFO'
    name = xmlmap.StringField('@machinneame')
    os = xmlmap.StringField('@os')
    lcid = xmlmap.IntegerField('@lcid')
    oem = xmlmap.StringField('@oem', required=False)


class ApplicationInfo(xmlmap.XmlObject):
    """ ApplicationInfo complex type
    """
    ROOT_NAME = 'APPLICATIONINFO'
    name = xmlmap.StringField('@apppath')
    path = xmlmap.StringField('@appname')
    company = xmlmap.StringField('@appcompany', required=False)


class EventInfo(xmlmap.XmlObject):
    """ EventInfo complex type
    """
    ROOT_NAME = 'EVENTINFO'
    report_type = xmlmap.IntegerField('@reporttype')
    type = xmlmap.StringField('@eventtype')
    time = DateField('@eventtime')
    name = xmlmap.StringField('@friendlyeventname', required=False)
    description = xmlmap.StringField('@eventdescription', required=False)


class Parameter(xmlmap.XmlObject):
    """ Parameter complex type
    """
    ROOT_NAME = 'PARAMETER'
    id = xmlmap.IntegerField('@id')
    name = xmlmap.StringField('@name', required=False)
    value = xmlmap.StringField('@value')


class SecondaryParameter(xmlmap.XmlObject):
    """ Secondary complex type
    """
    ROOT_NAME = 'SECONDARYPARAMETER'
    id = xmlmap.IntegerField('@id')
    value = xmlmap.StringField('@value')


class File(xmlmap.XmlObject):
    """ File complex type
    """
    ROOT_NAME = 'FILE'
    name = xmlmap.StringField('@filename')
    type = xmlmap.IntegerField('@filetype')


class Report(xmlmap.XmlObject):
    """ Windows Error Report
    """
    ROOT_NAME = 'WERREPORT'
    machine = xmlmap.NodeField('MACHINEINFO', MachineInfo)
    user = xmlmap.StringField('USERINFO/@username')
    application = xmlmap.NodeField('APPLICATIONINFO', ApplicationInfo, required=False)
    event = xmlmap.NodeField('EVENTINFO', EventInfo)
    parameters = xmlmap.NodeListField('SIGNATURE/PARAMETER', Parameter)
    secondary_parameters = xmlmap.NodeListField('SIGNATURE/SECONDARYPARAMETER', SecondaryParameter)
    files = xmlmap.NodeListField('FILES/FILE', File)
