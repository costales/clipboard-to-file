#!/bin/bash

# setup
sed -i 's/nautilus-python/nemo-python/' ../setup.py
sed -i 's/nautilus-extension/nemo-extension/' ../setup.py
sed -i 's/"clipboard-to-file"/"clipboard-to-file-nemo"/' ../setup.py

# extension
mv ../nautilus-extension/ ../nemo-extension
sed -i 's/nautilus/nemo/g' ../nemo-extension/clipboard-to-file.py
sed -i 's/Nautilus/Nemo/g' ../nemo-extension/clipboard-to-file.py

# po
sed -i 's/clipboard2file/clipboard-to-file-nemo/' ../nemo-extension/clipboard-to-file.py
sed -i 's/clipboard2file/clipboard-to-file-nemo/' ../po/POTFILES.in
sed -i 's/folder_path/nemo-extension/' ../po/POTFILES.in

# debian
sed -i 's/nautilus/nemo/g' ../debian/install

sed -i 's/Upstream-Name: clipboard-to-file/Upstream-Name: clipboard-to-file-nemo/' ../debian/copyright

sed -i 's/Source: clipboard-to-file/Source: clipboard-to-file-nemo/' ../debian/control
sed -i 's/Package: clipboard-to-file/Package: clipboard-to-file-nemo/' ../debian/control
sed -i 's/python3-nautilus, nautilus, /python-nemo, nemo, /' ../debian/control

sed -i 's/clipboard-to-file/clipboard-to-file-nemo/' ../debian/changelog

# myself
rm -r ../install_scripts

