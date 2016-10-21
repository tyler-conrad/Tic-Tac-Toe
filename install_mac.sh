mkdir temp
cd temp
curl "http://pygame.org/ftp/pygame-1.9.2pre-py2.7-macosx10.7.mpkg.zip" -o "pygame.zip"
unzip pygame.zip
installer -package pygame-1.9.2pre-py2.7-macosx10.7.mpkg -target "/Volumes/Macintosh HD"

easy_install -U setuptools
easy_install pip
pip install cython
pip install kivy
pip install twisted
pip install pytest
pip install pydoctor