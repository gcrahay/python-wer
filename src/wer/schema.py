# -*- coding: utf8 -*-
from __future__ import unicode_literals

import hashlib
from os import path

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


class DictMixin(object):
    """ Mixin class in order to export :class:`eulxml.xmlmap.XmlObject values to a Python dict"""

    def to_dict(self):
        """
        Recusively exports object values to a dict

        :return: `dict`of values
        """
        if not hasattr(self, '_fields'):
            return self.__dict__
        result = dict()
        for field_name, field in self._fields.items():
            if isinstance(field, xmlmap.NodeField):
                obj = getattr(self, field_name)
                if not hasattr(obj, 'to_dict'):
                    result[field_name] = obj.__dict__
                else:
                    result[field_name] = obj.to_dict()
            elif isinstance(field, xmlmap.NodeListField):
                objs = getattr(self, field_name)
                result[field_name] = list()
                for obj in objs:
                    if not hasattr(obj, 'to_dict'):
                        result[field_name].append(obj.__dict__)
                    else:
                        result[field_name].append(obj.to_dict())
            else:
                result[field_name] = getattr(self, field_name)
        return result


class XmlObject(DictMixin, xmlmap.XmlObject):
    pass


class MachineInfo(XmlObject):
    """ MachineInfo complex type
    """
    ROOT_NAME = 'MACHINEINFO'
    name = xmlmap.StringField('@machinename')
    """ Machine name :type `string` """
    os = xmlmap.StringField('@os')
    """ Machine operating system version :type `string` """
    lcid = xmlmap.IntegerField('@lcid')
    """ Machine language identifier :type `int` """
    oem = xmlmap.StringField('@oem', required=False)
    """ Optional machine OEM name :type `string` """


class ApplicationInfo(XmlObject):
    """ ApplicationInfo complex type
    """
    ROOT_NAME = 'APPLICATIONINFO'
    name = xmlmap.StringField('@appname')
    """ Application name :type `string` """
    path = xmlmap.StringField('@apppath')
    """ Application executable path :type `string` """
    company = xmlmap.StringField('@appcompany', required=False)
    """ Optional application company :type `string` """


class EventInfo(XmlObject):
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


class Parameter(XmlObject):
    """ Parameter complex type
    """
    ROOT_NAME = 'PARAMETER'
    id = xmlmap.IntegerField('@id')
    """ Parameter ID :type `int`"""
    name = xmlmap.StringField('@name', required=False)
    """ Optional paramneter name :type `string`"""
    value = xmlmap.StringField('@value')
    """ Paramneter value :type `string`"""


class SecondaryParameter(XmlObject):
    """ Secondary parameter complex type
    """
    ROOT_NAME = 'SECONDARYPARAMETER'
    id = xmlmap.IntegerField('@id')
    """ Parameter ID :type `int` """
    value = xmlmap.StringField('@value')
    """ Paramneter value :type `string` """


class File(XmlObject):
    """ File complex type
    """
    ROOT_NAME = 'FILE'
    name = xmlmap.StringField('@filename')
    """ File name :type `string` """
    type = xmlmap.IntegerField('@filetype')
    """ File type :type `int` """


class Report(XmlObject):
    """ Windows Error Report
    """
    ROOT_NAME = 'WERREPORT'
    XSD_SCHEMA = path.join(path.dirname(__file__), 'ms-cer2.xsd')
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
    def from_file(cls, file_path, validate=True):
        """ Creates a Report from a XML file

        :param file_path: Path to the XML WER file
        :param validate: XML should be validated against the embedded XSD definition
        :type validate: Boolean
        :returns: :class:`wer.schema.Report`
        """
        return xmlmap.load_xmlobject_from_file(file_path, xmlclass=cls, validate=validate)

    @classmethod
    def from_string(cls, xml_string, validate=True):
        """ Creates a Report from a XML string

        :param xml_string: XML WER string
        :param validate: XML should be validated against the embedded XSD definition
        :type validate: Boolean
        :returns: :class:`wer.schema.Report`
        """
        return xmlmap.load_xmlobject_from_string(xml_string, xmlclass=cls, validate=validate)

    @property
    def id(self):
        """
        Computes the signature of the record, a SHA-512 of significant values

        :return: SHa-512 Hex string
        """
        h = hashlib.new('sha512')
        h.update(
            "|{}|{}|{}|{}|{}|{}|{}|{}|".format(self.machine.name, self.machine.os, self.user, self.application.name,
                                               self.application.path, self.event.report_type, self.event.type,
                                               self.event.time.isoformat()))
        for parameter in sorted(self.parameters, key=lambda k: getattr(k, 'id')):
            h.update(parameter.value)
        return h.hexdigest()
