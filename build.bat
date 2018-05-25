cd /D "%~dp0"
python -O -m PyInstaller --onefile --noconfirm --name checkers^
 --hidden-import menu --hidden-import pause^
 --hidden-import intro --hidden-import game^
 --hidden-import endgame^
 --windowed --distpath ./ -i icon.ico src/main.py