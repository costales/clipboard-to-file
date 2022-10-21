#!/bin/bash

# setup
sed -i 's/nautilus-python/caja-python/' ../setup.py
sed -i 's/nautilus-extension/caja-extension/' ../setup.py
sed -i 's/clipboard-to-file/clipboard-to-file-caja/g' ../setup.py

# extension
mv ../nautilus-extension/ ../caja-extension
sed -i 's/nautilus/caja/g' ../caja-extension/clipboard-to-file.py
sed -i 's/Nautilus/Caja/g' ../caja-extension/clipboard-to-file.py

# po
sed -i 's/clipboard2file/clipboard-to-file-caja/' ../caja-extension/clipboard-to-file.py
sed -i 's/clipboard2file/clipboard-to-file-caja/' ../po/POTFILES.in
sed -i 's/folder_path/caja-extension/' ../po/POTFILES.in

# debian
sed -i 's/nautilus/caja/g' ../debian/install

sed -i 's/Upstream-Name: clipboard-to-file/Upstream-Name: clipboard-to-file-caja/' ../debian/copyright

sed -i 's/Source: clipboard-to-file/Source: clipboard-to-file-caja/' ../debian/control
sed -i 's/Package: clipboard-to-file/Package: clipboard-to-file-caja/' ../debian/control
sed -i 's/python3-nautilus, nautilus, /python-caja, caja, /' ../debian/control

sed -i 's/clipboard-to-file/clipboard-to-file-caja/' ../debian/changelog

# myself
rm -r ../install_scripts

