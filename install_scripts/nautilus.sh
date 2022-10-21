#!/bin/bash
rm ../README.md

# po
sed -i 's/clipboard2file/clipboard-to-file/' ../nautilus-extension/clipboard-to-file.py
sed -i 's/clipboard2file/clipboard-to-file/' ../po/POTFILES.in
sed -i 's/folder_path/nautilus-extension/' ../po/POTFILES.in

# myself
rm -r ../install_scripts
