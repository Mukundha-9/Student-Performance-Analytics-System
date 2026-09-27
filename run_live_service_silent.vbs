Set WshShell = CreateObject("WScript.Shell")
strPath = WshShell.CurrentDirectory
WshShell.Run "py -3.13 """ & strPath & "\live_service.py""", 0, False
