# Clipboard to File 0.0.9
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
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    def get_file_items(self, window, items):
        """Click on a file"""
        # Checks
        if len(items) != 1:
            return
        
        if items[0].is_directory():
            return

        file_name = unquote(items[0].get_uri()[7:])
        if file_name[-4:].lower() != ".txt" and file_name[-4:].lower() != ".png":
            return

        # Menu
        menu_item_file = Nautilus.MenuItem(name="click_file", label=_("Clipboard to File"))
        menu_item_file.connect("activate", self.menu_file, file_name)
        return menu_item_file,

    def get_background_items(self, window, directory):
        """Click on directory"""
        dir = directory.get_uri()[7:]
        
        menu_item_dir = Nautilus.MenuItem(name="click_dir", label=_("Clipboard to File"))
        menu_item_dir.connect("activate", self.menu_dir, dir)
        return menu_item_dir,

    def menu_file(self, menu, filename):
        self.menu_clipboard(True, filename)

    def menu_dir(self, menu, dir):
        self.menu_clipboard(False, dir)

    def menu_clipboard(self, is_file, filename):
        """Clicked menu"""
        clipboard_has_content = False

        # Text
        text = self.clipboard.wait_for_text()
        if text is not None:
            clipboard_has_content = self.save("text/plain", is_file, filename, text)
        # Image
        else:
            image = self.clipboard.wait_for_image()
            if image is not None:
                clipboard_has_content = self.save("image/png", is_file, filename, image)
        # Nothing
        if not clipboard_has_content:
            self.show_error(_("The clipboard does not have content"))
            
    def save(self, mimetype, is_file, filename, content):
        file = self.compose_filename(mimetype, is_file, filename)

        if mimetypes.guess_type(file)[0] != mimetype:
            self.show_error(_("%(filename)s isn't a %(mimetype)s file") % ({'filename': os.path.basename(file), 'mimetype': mimetype}))
        else:
            overwrite = Gtk.ResponseType.ACCEPT
            if os.path.isfile(file):
                overwrite = self.ask_overwrite(mimetype, os.path.basename(file))
            # Text
            if mimetype == "text/plain":
                if overwrite == Gtk.ResponseType.ACCEPT:
                    try:
                        with open(file, "w") as f:
                            f.write(content)
                    except Exception as e:
                        self.show_error(str(e))
                if overwrite == Gtk.ResponseType.APPLY:
                    try:
                        with open(file, "a") as f:
                            f.write("\n" + content)
                    except Exception as e:
                        self.show_error(str(e))
            # Image
            if mimetype == "image/png" and overwrite == Gtk.ResponseType.ACCEPT:
                try:
                    content.savev(file, "png", ["quality"], ["100"])
                except Exception as e:
                    self.show_error(str(e))

        return True

    def compose_filename(self, mimetype, is_file, filename):
        """Compose the filename"""
        # File
        if is_file:
            return filename
        
        # Directory
        i = 1
        i18n_filename = _("Clipboard")
        while os.path.exists((filename + "/" + i18n_filename + "-%s.txt") % i) or os.path.exists((filename + "/" + i18n_filename + "-%s.png") % i):
            i += 1

        if mimetype == "text/plain":
            return (filename + "/" + i18n_filename + "-%s.txt") % i
        else:
            return (filename + "/" + i18n_filename + "-%s.png") % i

    def show_error(self, msg):
        dialog = Gtk.MessageDialog(
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=msg,
        )
        response = dialog.run()
        dialog.destroy()

    def ask_overwrite(self, mimetype, file_name):
        dialog = Gtk.MessageDialog(
            message_type=Gtk.MessageType.WARNING,
            text=_("File %s exists.") % (file_name)
        )
        if mimetype == "text/plain":
            dialog.add_buttons(_("Append"), Gtk.ResponseType.APPLY)
        dialog.add_buttons(_("Overwrite"), Gtk.ResponseType.ACCEPT)
        dialog.add_buttons(_("Cancel"), Gtk.ResponseType.CANCEL)
        response = dialog.run()
        dialog.destroy()
        return response
