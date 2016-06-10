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
                if obj is None:
                    result[field_name] = None
                elif not hasattr(obj, 'to_dict'):
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


class LoaderMixin(object):
    """ Loading XML into object mixin

    """
    @classmethod
    def from_file(cls, file_path, validate=True):
        """ Creates a Python object from a XML file

        :param file_path: Path to the XML file
        :param validate: XML should be validated against the embedded XSD definition
        :type validate: Boolean
        :returns: the Python object
        """
        return xmlmap.load_xmlobject_from_file(file_path, xmlclass=cls, validate=validate)

    @classmethod
    def from_string(cls, xml_string, validate=True):
        """ Creates a Python object from a XML string

        :param xml_string: XML string
        :param validate: XML should be validated against the embedded XSD definition
        :type validate: Boolean
        :returns: the Python object
        """
        return xmlmap.load_xmlobject_from_string(xml_string, xmlclass=cls, validate=validate)


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


class Report(LoaderMixin, XmlObject):
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


class ProcessVmInformation(XmlObject):
    ROOT_NAME = 'ProcessVmInformation'
    peak_virtual_size = xmlmap.IntegerField('PeakVirtualSize')
    virtual_size = xmlmap.IntegerField('VirtualSize')
    pagefault_count = xmlmap.IntegerField('PageFaultCount')
    peak_workingset_size = xmlmap.IntegerField('PeakWorkingSetSize')
    workingset_size = xmlmap.IntegerField('WorkingSetSize')
    quota_peak_paged_pool_usage = xmlmap.IntegerField('QuotaPeakPagedPoolUsage')
    quota_paged_pool_usage = xmlmap.IntegerField('QuotaPagedPoolUsage')
    quota_peak_nonpaged_pool_usage = xmlmap.IntegerField('QuotaPeakNonPagedPoolUsage')
    quota_nonpaged_pool_usage = xmlmap.IntegerField('QuotaPagedNonPoolUsage')
    pagefile_usage = xmlmap.IntegerField('PagefileUsage')
    peak_pagefile_usage = xmlmap.IntegerField('PeakPagefileUsage')
    private_usage = xmlmap.IntegerField('PrivateUsage')


class ProcessInformation(XmlObject):
    ROOT_NAME = 'ProcessInformation'
    XSD_SCHEMA = path.join(path.dirname(__file__), 'wer-metadata.xsd')
    pid = xmlmap.IntegerField('Pid')
    image = xmlmap.StringField('ImageName')
    # Must generate more samples : bytes, string or integer ?
    cmd_line_signature = xmlmap.StringField('CmdLineSignature')
    uptime = xmlmap.IntegerField('Uptime')
    vm = xmlmap.NodeField('ProcessVmInformation', ProcessVmInformation)
    parent = xmlmap.NodeField('ParentProcess/ProcessInformation', 'self', required=False)


class OSVersionInformation(XmlObject):
    ROOT_NAME = 'OSVersionInformation'
    version = xmlmap.StringField('WindowsNTVersion')
    build = xmlmap.IntegerField('Build')
    product = xmlmap.StringField('Product')
    edition = xmlmap.StringField('Edition')
    build_info = xmlmap.StringField('BuildString')
    revision = xmlmap.IntegerField('Revision')
    flavor = xmlmap.StringField('Flavor')
    architecture = xmlmap.StringField('Architecture')
    lcid = xmlmap.IntegerField('LCID')


class SystemInformation(XmlObject):
    ROOT_NAME = 'SystemInformation'
    id = xmlmap.StringField('MID')
    manufacturer = xmlmap.StringField('SystemManufacturer')
    product = xmlmap.StringField('SystemProductName')
    bios_version = xmlmap.StringField('BIOSVersion')
    # TODO: Parse to date with timezone bias
    install_date = xmlmap.IntegerField('OSInstallDate')


class SecureBootState(XmlObject):
    # TODO: generate more samples with secure boot enabled machines
    ROOT_NAME = 'SecureBootState'
    uefi_state = xmlmap.StringField('UEFISecureBootEnabled', required=False)


class MetaParameter(XmlObject):
    id = xmlmap.IntegerField('substring(name(), 10)')
    value = xmlmap.StringField('text()')


class ReportMetadata(LoaderMixin, XmlObject):
    ROOT_NAME = 'WERReportMetadata'
    os = xmlmap.NodeField('OSVersionInformation', OSVersionInformation)
    process = xmlmap.NodeField('ProcessInformation', ProcessInformation)
    system = xmlmap.NodeField('SystemInformation', SystemInformation)
    secure_boot = xmlmap.NodeField('SecureBootState', SecureBootState, required=False)
    parameters = xmlmap.NodeListField('ProblemSignatures/*[starts-with(name(), "Parameter")]', MetaParameter)
    dynamic_parameters = xmlmap.NodeListField('DynamicSignatures/*[starts-with(name(), "Parameter")]', MetaParameter)
    id = xmlmap.StringField('ReportInformation/Guid')
    created_on = xmlmap.StringField('ReportInformation/CreationTime')
