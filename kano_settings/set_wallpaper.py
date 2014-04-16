#!/usr/bin/env python

# set_wallpaper.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#

from gi.repository import Gtk, GdkPixbuf
#import kano_settings.config_file as config_file
import kano_settings.components.fixed_size_box as fixed_size_box
import os

wallpaper_path = "/usr/share/kano-desktop/wallpapers/"


class Wallpaper():

    def __init__(self):
        NUMBER_OF_ROWS = 2
        NUMBER_OF_COLUMNS = 5
        COLUMN_PADDING = 0
        ROW_PADDING = 0
        ICON_WIDTH = 90
        ICON_HEIGHT = 90

        #self.dict = {"Icon-Audio": False, "Icon-Display": False, "Icon-Overclocking": False, "Icon-Keyboard": False, "Icon-Email": False, "Icon-Mouse": False, "Icon-Wallpaper": False, "Icon-Account": False}
        self.dict = {"kanux-background": False}
        self.images = {}
        self.table = Gtk.Table(NUMBER_OF_ROWS, NUMBER_OF_COLUMNS, True)
        self.table.set_row_spacings(ROW_PADDING)
        self.table.set_col_spacings(COLUMN_PADDING)
        buttons = []

        for name in self.dict:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(wallpaper_path + name + "-4-3.png", 120, 90)
            cropped_pixbuf = pixbuf.new_subpixbuf(15, 0, ICON_WIDTH, ICON_HEIGHT)
            #pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(constants.media + "/Icons/" + name + ".png", ICON_WIDTH, ICON_HEIGHT)
            image = Gtk.Image()
            image.get_style_context().add_class('wallpaper_box')
            image.set_from_pixbuf(cropped_pixbuf)
            self.images[name] = image
            backgroundbox = Gtk.Button()
            backgroundbox.add(image)
            backgroundbox.connect('button_press_event', self.select_wallpaper, name)
            buttons.append(backgroundbox)

        # Attach to table
        index = 0
        row = 0

        while index < len(self.dict):
            for j in range(NUMBER_OF_COLUMNS):
                if index < len(self.dict):
                    self.table.attach(buttons[index], j, j + 1, row, row + 1,
                                      Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.EXPAND, 0, 0)
                    index += 1
                else:
                    grey_box = Gtk.Button()
                    grey_box.set_size_request(ICON_WIDTH, ICON_HEIGHT)
                    grey_box.get_style_context().add_class('grey_box')
                    grey_box.connect('button_press_event', self.add_wallpaper)
                    self.table.attach(grey_box, j, j + 1, row, row + 1,
                                      Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.EXPAND, 0, 0)
                    index += 1
            row += 1

    # Add class to wallpaper picture which displays border even when mouse is moved
    def select_wallpaper(self, widget=None, event=None, image_name=""):

        print "self.get_selected() = " + str(self.get_selected())

        for x in self.images:
            style = self.images[x].get_style_context()
            style.remove_class("wallpaper_box_active")
            style.add_class("wallpaper_box")

        image_style = self.images[image_name].get_style_context()
        image_style.remove_class("wallpaper_box")
        image_style.add_class("wallpaper_box_active")
        self.set_selected(image_name)

        print self.images[image_name]
        print image_style.list_classes()

        print "self.get_selected() = " + str(self.get_selected())

    def add_wallpaper(self, widget=None, event=None):
        print "grey_box"

    # Get the current selected wallpaper
    # Handles global variable wallpaper_array
    def get_selected(self):

        for x in self.dict:
            if self.dict[x]:
                return x

    # Set the currents elected wallpaper
    # Handles global variable wallpaper_array
    def set_selected(self, image_name):

        for x in self.dict:
            self.dict[x] = False

        self.dict[image_name] = True

    def change_wallpaper(self):
        image_name = self.get_selected

        # home directory
        USER = os.environ['SUDO_USER']
        deskrc_path = "/home/%s/.kdeskrc" % (USER)
        if not os.path.isfile(deskrc_path):
            return 1

         # Change wallpaper in deskrc
        image_169 = "%s%s-16-9.png" % (wallpaper_path, image_name)
        image_43 = "%s%s-4-3.png" % (wallpaper_path, image_name)
        image_1024 = "%s%s-1024.png" % (wallpaper_path, image_name)
        # Read deskrc config file
        f = file(deskrc_path)
        newlines = []
        for line in f:
            if "Background.File-medium: " in line:
                line = "  Background.File-medium: %s\n" % (image_1024)
            if "Background.File-4-3: " in line:
                line = "  Background.File-4-3: %s\n" % (image_43)
            if "Background.File-16-9: " in line:
                line = "  Background.File-16-9: %s\n" % (image_169)
            newlines.append(line)
        # Overwrite config file with new lines
        outfile = file(deskrc_path, 'w')
        outfile.writelines(newlines)

        # Refresh the wallpaper
        os.system('pkill kdesk && kdesk &')
        # TODO: can we use ksdek -w for previewing the wallpaper?

        return 0


wallpaper = None


def activate(_win, box, update):
    global wallpaper

    title = Gtk.Label("Choose your background")
    title.get_style_context().add_class('title')

    wallpaper = Wallpaper()
    settings = fixed_size_box.Fixed()
    settings.box.pack_start(wallpaper.table, False, False, 10)

    # Add apply changes button under the main settings content
    box.pack_start(title, False, False, 0)
    box.pack_start(settings.box, False, False, 0)
    box.pack_start(update.box, False, False, 0)
    update.enable()


def apply_changes(button):
    global wallpaper

    wallpaper.change_wallpaper()
