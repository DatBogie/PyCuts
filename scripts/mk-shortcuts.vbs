Set oWS = WScript.CreateObject("WScript.Shell") 
sLinkFile = oWS.ExpandEnvironmentStrings("%APPDATA%\Microsoft\Windows\Start Menu\Programs\PyCuts.lnk")
sLinkFileC = oWS.ExpandEnvironmentStrings("%APPDATA%\Microsoft\Windows\Start Menu\Programs\PyCuts Config.lnk")
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = oWS.ExpandEnvironmentStrings("%LOCALAPPDATA%\PyCuts\PyCuts.exe")
oLink.Save
Set oLinkC = oWS.CreateShortcut(sLinkFileC)
oLinkC.TargetPath = oWS.ExpandEnvironmentStrings("%LOCALAPPDATA%\PyCuts\PyCuts Config.exe")
oLinkC.Save
