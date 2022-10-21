#!/usr/bin/env python3

# Clipboard to File 0.0.2 - https://github.com/costales/clipboard-to-file
# Copyright (C) 2022 Marcos Alvarez Costales - https://costales.github.io/
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


import os, sys, glob, DistUtilsExtra.auto

# Create data files
data = [ ('/usr/share/nautilus-python/extensions',      ['nautilus-extension/clipboard-to-file.py']) ]

# Setup stage
DistUtilsExtra.auto.setup(
    name         = "clipboard-to-file",
    version      = "0.0.2",
    description  = "Save your clipboard content to a file",
    author       = "Marcos Alvarez Costales",
    author_email = "marcos.costales@gmail.com",
    url          = "https://github.com/costales/clipboard-to-file",
    license      = "GPL3",
    data_files   = data
)

