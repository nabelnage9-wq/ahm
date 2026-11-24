; Inno Setup Script for SMART GRADES Windows Installer
[Setup]
AppName=SMART GRADES
AppVersion=1.0.0
DefaultDirName={autopf}\SMART GRADES
DefaultGroupName=SMART GRADES
OutputBaseFilename=SMART_GRADES_Setup_v1.0
Compression=lzma
SolidCompression=yes

[Files]
Source: "..\desktop-tauri\src-tauri\target\release\smart-grades.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\SMART GRADES"; Filename: "{app}\smart-grades.exe"
Name: "{autodesktop}\SMART GRADES"; Filename: "{app}\smart-grades.exe"

[Run]
Filename: "{app}\smart-grades.exe"; Description: "Launch SMART GRADES"; Flags: nowait postinstall skipifsilent
