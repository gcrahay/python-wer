from __future__ import unicode_literals

import wer


def test_main():
    assert wer


def test_windows_unix_timestam():
    from wer import helpers
    assert 1205218919 == helpers.windows_to_unix_timestamp(128496925196486378)


def test_unix_windows_timestamp():
    from wer import helpers
    assert 128496925190000000 == helpers.unix_to_windows_timestamp(1205218919)


def test_loading_from_string():
    xml_string = b"""<?xml version="1.0" encoding="UTF-8"?>
        <WERREPORT xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <MACHINEINFO machinename="client-machine.corp.cliendomain.com" os="6.1.6561.2.0.0.256.1"
        lcid="1033"/>
        <USERINFO username="Username"/>
        <APPLICATIONINFO appname="WER GPF Test Utility" apppath="E:\tools\GPFMe.exe" appcompany="Test
        Corporation"/>
        <EVENTINFO reporttype="2" eventtime="128496925196486378" eventtype="APPCRASH"
        friendlyeventname="Stopped working"/>
        <SIGNATURE>
        <PARAMETER id="0" name="Application Name" value="GPFMe.exe"/>
        <PARAMETER id="1" name="Application Version" value="6.0.4082.0"/>
        <PARAMETER id="2" name="Application Timestamp" value="40ce670d"/>
        <PARAMETER id="3" name="Fault Module Name" value="GPFMe.exe"/>
        <PARAMETER id="4" name="Fault Module Version" value="6.0.4082.0"/>
        <PARAMETER id="5" name="Fault Module Timestamp" value="40ce670d"/>
        <PARAMETER id="6" name="Exception Code" value="c0000005"/>
        <PARAMETER id="7" name="Exception Offset" value="000031de"/>
        </SIGNATURE>
        <FILES>
        <FILE filetype="5" filename="Version.txt"/>
        </FILES>
        </WERREPORT>
        """
    report = wer.Report.from_string(xml_string)
    assert isinstance(report, wer.Report)


def test_loading_from_files():
    from os import path
    from glob import glob
    examples_path = path.join(path.basename(__file__), 'data', 'examples')
    signature = None
    for f in glob(path.join(examples_path, '*.wer')):
        report = wer.Report.from_file(f)
        assert isinstance(report, wer.Report)
        assert signature != report.id
        signature = report.id


def test_metadata():
    from os import path
    from glob import glob
    examples_path = path.join(path.basename(__file__), 'data', 'examples')
    signature = None
    for f in glob(path.join(examples_path, 'WERInternalMetadata_*.xml')):
        meta = wer.ReportMetadata.from_file(f)
        assert isinstance(meta, wer.ReportMetadata)
