#!/bin/bash
pyv=$( python -c 'import sys; print(sys.version_info[0])' )

install_command = -O -m PyInstaller --onefile --noconfirm --onefile --name checkers \
 --hidden-import menu --hidden-import pause \
 --hidden-import intro --hidden-import game \
 --windowed --distpath ./ -i icon.ico src/main.py

if [ $pyv = '3' ]
then
	echo "Running python game: python src/main.py"
	python "$install_command"
else
	echo "Python version not valid. Trying python3"
	py3=$( python3 -c 'import sys; print(sys.version_info[0])' )
	if [ $py3 = '3' ]
	then
		echo "Running python3 src/main.py"
		python3 "$install_command"
	else
		echo $py3
		echo "No valid python found. Exiting..."
	fi
fi

