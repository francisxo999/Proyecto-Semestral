[Setup]
AppName=VETTsafe
AppVersion=1.0
DefaultDirName={commonpf}\VETTsafe
DefaultGroupName=VETTsafe
OutputDir=output
OutputBaseFilename=VETTsafe_Installer
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
;; No incluyas la base de datos (se creará automáticamente)

[Icons]
Name: "{commondesktop}\VETTsafe"; Filename: "{app}\main.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\VETTsafe"; Filename: "{app}\main.exe"