#define MyAppName "RepoDumper"
#define MyAppVersion "1.2.1"
#define MyAppPublisher "Chetan M"
#define MyAppExeName "RepoDumper.exe"

[Setup]
AppId=c44891f3-3b81-443c-a268-0b09967c8cb3
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer
OutputBaseFilename=RepoDumper_Setup
SetupIconFile=assets\repo_dumper.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "dist\RepoDumper.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\RepoDumper"; Filename: "{app}\RepoDumper.exe"
Name: "{commondesktop}\RepoDumper"; Filename: "{app}\RepoDumper.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\RepoDumper.exe"; Description: "Launch RepoDumper"; Flags: nowait postinstall skipifsilent
