# Clipboard to File 0.0.7
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
        self.from_clicked_file = False # Nautilus calls get_file_items and after that, get_background_items. Check from where is coming
        self.item = ""

    def get_file_items(self, window, items):
        """Clicked on a file (1st pass)"""
        self.from_clicked_file = False
        self.item = ""

        # Checks
        if len(items) != 1:
            return False
        
        if items[0].is_directory():
            return False

        file_name = unquote(items[0].get_uri()[7:])
        if file_name[-4:].lower() != ".txt" and file_name[-4:].lower() != ".png":
            return False

        # Values for event trigger
        self.from_clicked_file = True
        self.item = file_name

        # Menu
        menu_item = Nautilus.MenuItem(name="clipboard-to-file", label=_("Clipboard to File"))
        menu_item.connect("activate", self._menu_activate_paste)
        return menu_item,

    def get_background_items(self, window, directory):
        """Clicked on empty area (2nd pass)"""
        if not self.from_clicked_file:
            self.item = directory.get_uri()[7:]
        
        menu_item = Nautilus.MenuItem(name="clipboard-to-file", label=_("Clipboard to File"))
        menu_item.connect("activate", self._menu_activate_paste)
        return menu_item,

    def _menu_activate_paste(self, menu):
        """Clicked menu"""
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard_has_content = False

        # Text
        text = clipboard.wait_for_text()
        if text is not None:
            clipboard_has_content = True
            # Compose file
            filename = self._compose_filename("txt")
            if self.from_clicked_file and not mimetypes.guess_type(filename)[0] == 'text/plain':
                self._popup(_("%s isn't a text file") % (os.path.basename(filename)))
            else:
                overwrite = Gtk.ResponseType.YES
                if os.path.isfile(filename):
                    overwrite = self._ask_overwrite(os.path.basename(filename))
                if overwrite == Gtk.ResponseType.YES:
                    try:
                        with open(filename, "w") as f:
                            f.write(text)
                    except Exception as e:
                        self._popup(str(e))
        
        # Image
        else:
            image = clipboard.wait_for_image()
            if image is not None:
                clipboard_has_content = True
                # Compose file
                filename = self._compose_filename("png")
                if self.from_clicked_file and not mimetypes.guess_type(filename)[0] == 'image/png':
                    self._popup(_("%s isn't a PNG file") % (os.path.basename(filename)))
                else:
                    overwrite = Gtk.ResponseType.YES
                    if os.path.isfile(filename):
                        overwrite = self._ask_overwrite(os.path.basename(filename))
                    if overwrite == Gtk.ResponseType.YES:
                        try:
                            image.savev(filename, "png", ["quality"], ["100"])
                        except Exception as e:
                            self._popup(str(e))
                            
        self.item = ""
        self.from_clicked_file = False

        # Nothing
        if not clipboard_has_content:
            self._popup(_("The clipboard does not have content"))
            
    def _compose_filename(self, file_extension):
        """Compose the filename"""
        if self.from_clicked_file:
            return self.item
        else:
            extension = "." + file_extension
            
            # Incremental filename
            i = 1
            i18n_filename = _("Clipboard")
            while os.path.exists((self.item + "/" + i18n_filename + "-%s.txt") % i) or os.path.exists((self.item + "/" + i18n_filename + "-%s.png") % i):
                i += 1

            return (self.item + "/" + i18n_filename + "-%s" + extension) % i

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
        return response
