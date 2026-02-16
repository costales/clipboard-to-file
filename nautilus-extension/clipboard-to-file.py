# Clipboard to File 0.1.0
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

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Nautilus, Gtk, GObject, Gdk, GLib, Gio

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
    RESPONSE_CANCEL = 0
    RESPONSE_APPEND = 1
    RESPONSE_OVERWRITE = 2
    RESPONSE_OK = 3

    def __init__(self):
        GObject.Object.__init__(self)
        display = Gdk.Display.get_default()
        self.clipboard = display.get_clipboard() if display is not None else None
        self.parent_window = None

    def get_file_items(self, *args):
        """Click on a file"""
        if len(args) == 2:
            window, items = args
            self.parent_window = window
        elif len(args) == 1:
            (items,) = args
        else:
            return

        # Checks
        if len(items) != 1:
            return

        if items[0].is_directory():
            return

        file_name = self.uri_to_path(items[0].get_uri())
        if file_name[-4:].lower() != ".txt" and file_name[-4:].lower() != ".png":
            return

        # Menu
        menu_item_file = Nautilus.MenuItem(
            name="click_file", label=_("Clipboard to File")
        )
        menu_item_file.connect("activate", self.menu_file, file_name)
        return (menu_item_file,)

    def get_background_items(self, *args):
        """Click on directory"""
        if len(args) == 2:
            window, directory = args
            self.parent_window = window
        elif len(args) == 1:
            (directory,) = args
        else:
            return

        dir = self.uri_to_path(directory.get_uri())

        menu_item_dir = Nautilus.MenuItem(
            name="click_dir", label=_("Clipboard to File")
        )
        menu_item_dir.connect("activate", self.menu_dir, dir)
        return (menu_item_dir,)

    def menu_file(self, menu, filename):
        GLib.idle_add(self.menu_clipboard, True, filename)

    def menu_dir(self, menu, dir):
        GLib.idle_add(self.menu_clipboard, False, dir)

    def menu_clipboard(self, is_file, filename):
        """Clicked menu"""
        clipboard_has_content = False
        if self.clipboard is None:
            self.show_error(_("Cannot access the clipboard"))
            return False

        # Text
        text = self.read_clipboard_text()
        if text is not None:
            clipboard_has_content = self.save("text/plain", is_file, filename, text)
        # Image
        else:
            image = self.read_clipboard_texture()
            if image is not None:
                clipboard_has_content = self.save("image/png", is_file, filename, image)
        # Nothing
        if not clipboard_has_content:
            self.show_error(_("The clipboard does not have content"))
        return False

    def save(self, mimetype, is_file, filename, content):
        file = self.compose_filename(mimetype, is_file, filename)

        if mimetypes.guess_type(file)[0] != mimetype:
            self.show_error(
                _("%(filename)s isn't a %(mimetype)s file")
                % ({"filename": os.path.basename(file), "mimetype": mimetype})
            )
        else:
            overwrite = self.RESPONSE_OVERWRITE
            if os.path.isfile(file):
                overwrite = self.ask_overwrite(mimetype, os.path.basename(file))
            # Text
            if mimetype == "text/plain":
                if overwrite == self.RESPONSE_OVERWRITE:
                    try:
                        with open(file, "w") as f:
                            f.write(content)
                    except Exception as e:
                        self.show_error(str(e))
                if overwrite == self.RESPONSE_APPEND:
                    try:
                        with open(file, "a") as f:
                            f.write("\n" + content)
                    except Exception as e:
                        self.show_error(str(e))
            # Image
            if mimetype == "image/png" and overwrite == self.RESPONSE_OVERWRITE:
                try:
                    content.save_to_png(file)
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
        while os.path.exists(
            (filename + "/" + i18n_filename + "-%s.txt") % i
        ) or os.path.exists((filename + "/" + i18n_filename + "-%s.png") % i):
            i += 1

        if mimetype == "text/plain":
            return (filename + "/" + i18n_filename + "-%s.txt") % i
        else:
            return (filename + "/" + i18n_filename + "-%s.png") % i

    def show_error(self, msg):
        self.run_alert_dialog(msg, [_("OK")])

    def ask_overwrite(self, mimetype, file_name):
        message = _("File %s exists.") % (file_name)
        if mimetype == "text/plain":
            choice = self.run_alert_dialog(
                message, [_("Append"), _("Overwrite"), _("Cancel")]
            )
            if choice == 0:
                return self.RESPONSE_APPEND
            if choice == 1:
                return self.RESPONSE_OVERWRITE
            return self.RESPONSE_CANCEL

        choice = self.run_alert_dialog(message, [_("Overwrite"), _("Cancel")])
        if choice == 0:
            return self.RESPONSE_OVERWRITE
        return self.RESPONSE_CANCEL

    def read_clipboard_text(self):
        """Read text from clipboard using Gtk4 async API."""
        text = {"value": None}
        loop = GLib.MainLoop()

        def on_text_ready(clipboard, result):
            try:
                text["value"] = clipboard.read_text_finish(result)
            except GLib.Error:
                text["value"] = None
            loop.quit()

        self.clipboard.read_text_async(None, on_text_ready)
        loop.run()
        return text["value"]

    def read_clipboard_texture(self):
        """Read image texture from clipboard using Gtk4 async API."""
        texture = {"value": None}
        loop = GLib.MainLoop()

        def on_texture_ready(clipboard, result):
            try:
                texture["value"] = clipboard.read_texture_finish(result)
            except GLib.Error:
                texture["value"] = None
            loop.quit()

        self.clipboard.read_texture_async(None, on_texture_ready)
        loop.run()
        return texture["value"]

    def get_parent_window(self):
        """Get a Nautilus window to use as transient parent for dialogs."""
        if isinstance(self.parent_window, Gtk.Window):
            return self.parent_window
        try:
            app = Gio.Application.get_default()
            if isinstance(app, Gtk.Application):
                window = app.get_active_window()
                if isinstance(window, Gtk.Window):
                    return window
        except Exception:
            pass
        try:
            toplevels = Gtk.Window.get_toplevels()
            for i in range(toplevels.get_n_items()):
                window = toplevels.get_item(i)
                if isinstance(window, Gtk.Window) and window.is_active():
                    return window
        except Exception:
            return None
        return None

    def run_alert_dialog(self, message, buttons):
        """Run a Gtk.AlertDialog and return selected button index."""
        response = {"id": len(buttons) - 1}
        loop = GLib.MainLoop()
        dialog = Gtk.AlertDialog()
        dialog.set_message(message)
        dialog.set_buttons(buttons)
        dialog.set_cancel_button(len(buttons) - 1)
        if len(buttons) > 1:
            dialog.set_default_button(0)

        def on_choose_done(_dialog, result):
            try:
                response["id"] = int(_dialog.choose_finish(result))
            except Exception:
                response["id"] = len(buttons) - 1
            loop.quit()

        parent = self.get_parent_window()
        dialog.choose(parent, None, on_choose_done)
        loop.run()
        return response["id"]

    def uri_to_path(self, uri):
        """Convert file:// URI to local path safely."""
        try:
            path, _hostname = GLib.filename_from_uri(uri)
            if path:
                return path
        except Exception:
            pass
        if uri.startswith("file://"):
            return unquote(uri[7:])
        return unquote(uri)
