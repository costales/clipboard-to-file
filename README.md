Clipboard to File © 2022 Marcos Alvarez Costales
================================================

## WHAT IS IT?

Paste clipboard (text/image) into a file.

Available for Nautilus, Nemo & Caja file browsers.

## HOW DOES IT WORK?

Copy a text or image into your clipboard.

Then, go to your file browser and right click into:

 * Empty area / Clipboard to file: Will create or overwrite the file clipboard.txt or clipboard.png (depends clipboard content).
 * File / Clipboard to file: Will overwrite that file with the clipboard content.
 

## HOW DO I INSTALL?

Nautilus:

```
sudo add-apt-repository ppa:costales/clipboard-to-file
sudo apt-get install clipboard-to-file
nautilus -q
```

Nemo:

```
sudo add-apt-repository ppa:costales/clipboard-to-file
sudo apt-get install clipboard-to-file-nemo
nemo -q
```

Caja:

```
sudo add-apt-repository ppa:costales/clipboard-to-file
sudo apt-get install clipboard-to-file-caja
caja -q
```


## LICENSES

Clipboard to File code is licensed under the GPL v3.
http://www.gnu.org/licenses
