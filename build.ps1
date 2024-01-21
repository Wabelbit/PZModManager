pyinstaller.exe --windowed --icon NONE --noupx --noconfirm .\src\PzModManager.py
signtool.exe sign /n wabelbit.github.io /du "https://github.com/Wabelbit/PZModManager" .\dist\PzModManager\PzModManager.exe
