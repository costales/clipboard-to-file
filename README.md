Clipboard to File
=================

## WHAT IS IT?

Paste Linux clipboard (text/image) into a file.

![logo](https://user-images.githubusercontent.com/5886786/197257960-3ec9192e-cd53-4494-99ef-1ce1758eafa3.png)


## HOW DOES IT WORK?

### TEXT

Copy a text into your clipboard.

Go to your file browser and do a right click:

 * Into empty area / "Clipboard to file" menu: Will create the file clipboard-X.txt.
 * Into file / "Clipboard to file" menu: Will ask to overwrite that file content with the clipboard text.
 
### IMAGE

Copy an image into your clipboard.

Go to your file browser and do a right click:

 * Into empty area / "Clipboard to file" menu: Will create the file clipboard-X.png.
 * Into file / "Clipboard to file" menu: Will ask to overwrite that file content with the clipboard image.

![image](https://user-images.githubusercontent.com/5886786/197329936-f365c30b-e6c3-42a8-9106-bc0f94aacb09.png)


## REQUIREMENTS

Ubuntu 20.04 or 22.04.

## HOW TO INSTALL?

### Nautilus

```
sudo add-apt-repository ppa:costales/clipboard-to-file
sudo apt-get update
sudo apt-get install clipboard-to-file
nautilus -q
```

### Nemo

```
sudo add-apt-repository ppa:costales/clipboard-to-file
sudo apt-get update
sudo apt-get install clipboard-to-file-nemo
nemo -q
```

### Caja

```
sudo add-apt-repository ppa:costales/clipboard-to-file
sudo apt-get update
sudo apt-get install clipboard-to-file-caja
caja -q
```

## TRANSLATIONS

https://translations.launchpad.net/clipboard-to-file/trunk

## LICENSES

Clipboard to File code is licensed under the GPL v3.
http://www.gnu.org/licenses

## AUTHOR

© 2022 Marcos Alvarez Costales
