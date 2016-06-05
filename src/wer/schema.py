# -*- coding: utf8 -*-
from __future__ import unicode_literals

from eulxml import xmlmap
from wer.helpers import DateField

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


class MachineInfo(xmlmap.XmlObject):
    """ MachineInfo complex type
    """
    ROOT_NAME = 'MACHINEINFO'
    name = xmlmap.StringField('@machinneame')
    """ Machine name :type `string` """
    os = xmlmap.StringField('@os')
    """ Machine operating system version :type `string` """
    lcid = xmlmap.IntegerField('@lcid')
    """ Machine language identifier :type `int` """
    oem = xmlmap.StringField('@oem', required=False)
    """ Optional machine OEM name :type `string` """


class ApplicationInfo(xmlmap.XmlObject):
    """ ApplicationInfo complex type
    """
    ROOT_NAME = 'APPLICATIONINFO'
    name = xmlmap.StringField('@appname')
    """ Application name :type `string` """
    path = xmlmap.StringField('@apppath')
    """ Application executable path :type `string` """
    company = xmlmap.StringField('@appcompany', required=False)
    """ Optional application company :type `string` """


class EventInfo(xmlmap.XmlObject):
    """ EventInfo complex type
    """
    ROOT_NAME = 'EVENTINFO'
    report_type = xmlmap.IntegerField('@reporttype')
    """ Report type :type `int` """
    type = xmlmap.StringField('@eventtype')
    """ Event type :type `string` """
    time = DateField('@eventtime')
    """ Event date :type :class:`datetime.datetime`"""
    name = xmlmap.StringField('@friendlyeventname', required=False)
    """ Friendly event name :type `string` """
    description = xmlmap.StringField('@eventdescription', required=False)
    """ Event description :type `string` """


class Parameter(xmlmap.XmlObject):
    """ Parameter complex type
    """
    ROOT_NAME = 'PARAMETER'
    id = xmlmap.IntegerField('@id')
    """ Parameter ID :type `int`"""
    name = xmlmap.StringField('@name', required=False)
    """ Optional paramneter name :type `string`"""
    value = xmlmap.StringField('@value')
    """ Paramneter value :type `string`"""


class SecondaryParameter(xmlmap.XmlObject):
    """ Secondary parameter complex type
    """
    ROOT_NAME = 'SECONDARYPARAMETER'
    id = xmlmap.IntegerField('@id')
    """ Parameter ID :type `int` """
    value = xmlmap.StringField('@value')
    """ Paramneter value :type `string` """


class File(xmlmap.XmlObject):
    """ File complex type
    """
    ROOT_NAME = 'FILE'
    name = xmlmap.StringField('@filename')
    """ File name :type `string` """
    type = xmlmap.IntegerField('@filetype')
    """ File type :type `int` """


class Report(xmlmap.XmlObject):
    """ Windows Error Report
    """
    ROOT_NAME = 'WERREPORT'
    machine = xmlmap.NodeField('MACHINEINFO', MachineInfo)
    """ Machine informations :type :class:`wer.schema.MachineInfo` """
    user = xmlmap.StringField('USERINFO/@username')
    """ User informations :type :class:`wer.schema.UserInfo` """
    application = xmlmap.NodeField('APPLICATIONINFO', ApplicationInfo, required=False)
    """ Application informations :type :class:`wer.schema.ApplicationInfo` """
    event = xmlmap.NodeField('EVENTINFO', EventInfo)
    """ Event informations :type :class:`wer.schema.EventInfo` """
    parameters = xmlmap.NodeListField('SIGNATURE/PARAMETER', Parameter)
    """ Event parameters :type list of :class:`wer.schema.Parameter` """
    secondary_parameters = xmlmap.NodeListField('SIGNATURE/SECONDARYPARAMETER', SecondaryParameter)
    """ Event secondary parameters :type list of :class:`wer.schema.SecondaryParameter` """
    files = xmlmap.NodeListField('FILES/FILE', File)
    """ Event attached files :type list of :class:`wer.schema.File` """

    @classmethod
    def from_file(cls, file_path):
        """ Creates a Report from a XML file """
        return xmlmap.load_xmlobject_from_file(file_path, xmlclass=cls)

    @classmethod
    def from_string(cls, xml_string):
        """ Creates a Report from a XML string """
        return xmlmap.load_xmlobject_from_string(xml_string, xmlclass=cls)
