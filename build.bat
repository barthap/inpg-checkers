@echo off
cd /D "%~dp0"
Title Build checkers
set "MISSING_PYINSTALLER=true"
where python > NUL 2>&1 && set "MISSING_PYINSTALLER=false"

IF "%MISSING_PYINSTALLER%"=="true" (
  echo You need to install PyInstaller first! Closing
  exit /b
)

echo Do you want to build one big EXE file including all dependencies (including Python 3.6)
echo Or directory with separate library files?
@echo off
set /P choice= "Type 'file' or 'dir': "

IF "%choice%"=="file" (
    python -O -m PyInstaller --onefile --noconfirm --name checkers^
     --hidden-import menu --hidden-import pause^
     --hidden-import intro --hidden-import game^
     --hidden-import endgame^
     --windowed -i icon.ico src/main.py

    echo Copying resource files
    copy config.ini dist
    copy locale.ini dist
    robocopy resources dist\resources /e
) ELSE (
    python -O -m PyInstaller --onedir --noconfirm --name checkers^
     --hidden-import menu --hidden-import pause^
     --hidden-import intro --hidden-import game^
     --hidden-import endgame^
     --add-data ./config.ini;.^
     --add-data ./locale.ini;.^
     --add-data ./resources;./resources^
     --windowed -i icon.ico src/main.py
)

echo Finished building game! Your executable is in 'dist' directory
pause