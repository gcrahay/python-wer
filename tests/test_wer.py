from __future__ import unicode_literals

import wer


def test_main():
    assert wer


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
