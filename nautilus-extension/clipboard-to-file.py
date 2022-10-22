# Clipboard to File 0.0.5
# Copyright (C) 2022 Marcos Alvarez Costales https://costales.github.io/about/
#
# Clipboard to File is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# Clipboard to File is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Clipboard to File; if not, see http://www.gnu.org/licenses
# for more information.

import os, gettext, mimetypes

from gi.repository import Nautilus, Gtk, GObject, Gdk

# Python 2 or 3
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

# i18n
gettext.textdomain("clipboard2file")
_ = gettext.gettext

class PasteIntoFile(GObject.GObject, Nautilus.MenuProvider):
    """File Browser Menu"""
    def __init__(self):
        GObject.Object.__init__(self)
        self.clipboard = Gtk.Clipboard()

    def get_file_items(self, window, items):
        """Create menu when click on a file"""
        # Checks
        if items[0].is_gone():
            return False
        
        if len(items) != 1:
            return False
        
        if items[0].is_directory():
            return False

        file_name = unquote(items[0].get_uri()[7:])
        if file_name[-4:].lower() != ".txt" and file_name[-4:].lower() != ".png":
            return False

        # Menu
        menu_item = Nautilus.MenuItem(name="clipboard-to-file", label=_("Clipboard to File"))
        menu_item.connect("activate", self._menu_activate_paste, "file", file_name)
        return menu_item,

    def get_background_items(self, window, file):
        """Create menu when click on empty area"""
        file_name = file.get_uri()[7:]
        menu_item = Nautilus.MenuItem(name="clipboard-to-file", label=_("Clipboard to File"))
        menu_item.connect("activate", self._menu_activate_paste, "empty", file_name)
        return menu_item,

    def _compose_filename(self, from_menu, clipboard_type, file_name):
        """Compose the filename"""
        if from_menu == "file":
            return file_name
        
        if from_menu == "empty":
            if clipboard_type == "text":
                extension = ".txt"
            if clipboard_type == "image":
                extension = ".png"
            
            # Incremental filename
            i = 1
            while os.path.exists((file_name + "/clipboard-%s" + extension) % i):
                i += 1

            return (file_name + "/clipboard-%s" + extension) % i

    def _popup(self, msg):
        dialog = Gtk.MessageDialog(
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=msg,
        )
        response = dialog.run()
        dialog.destroy()

    def _ask_overwrite(self, file_name):
        dialog = Gtk.MessageDialog(
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=_("File %s exists. Overwrite?") % (file_name)
        )
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            return True
        else:
            return False


    def _menu_activate_paste(self, menu, from_menu, file_name):
        """Menu: Clipboard to File clicked"""
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        text = clipboard.wait_for_text()

        # Text
        if text is not None:
            # Compose file
            filename = self._compose_filename(from_menu, "text", file_name)
            if from_menu == "file" and not mimetypes.guess_type(file_name)[0] == 'text/plain':
                self._popup(_("%s isn't a text file") % (os.path.basename(filename)))
            else:
                overwrite = True
                if os.path.isfile(filename):
                    overwrite = self._ask_overwrite(os.path.basename(filename))
                if overwrite:
                    try:
                        with open(filename, "w") as f:
                            f.write(text)
                    except Exception as e:
                        self._popup(str(e))
        
        # Image
        else:
            image = clipboard.wait_for_image()
            if image is not None:
                # Compose file
                filename = self._compose_filename(from_menu, "image", file_name)
                if from_menu == "file" and not mimetypes.guess_type(file_name)[0] == 'image/png':
                    self._popup(_("%s isn't a PNG file") % (os.path.basename(filename)))
                else:
                    overwrite = True
                    if os.path.isfile(filename):
                        overwrite = self._ask_overwrite(os.path.basename(filename))
                    if overwrite:
                        try:
                            image.savev(filename, "png", ["quality"], ["100"])
                        except Exception as e:
                            self._popup(str(e))
