# top_hit_widget.py
#
# Copyright 2023 Nokse
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from tidalapi.page import PageItem
from tidalapi.mix import Mix, MixV2
from tidalapi.artist import Artist
from tidalapi.album import Album
from tidalapi.media import Track
from tidalapi.playlist import Playlist

from ..lib import utils
from ..lib import variables
from ..disconnectable_iface import IDisconnectable
import threading


@Gtk.Template(
    resource_path='/io/github/nokse22/HighTide/ui/widgets/top_hit_widget.ui')
class HTTopHitWidget(Gtk.Box, IDisconnectable):
    __gtype_name__ = 'HTTopHitWidget'

    """It is used to display the top hit when searching regardless
    of the type"""

    image = Gtk.Template.Child()
    primary_label = Gtk.Template.Child()
    secondary_label = Gtk.Template.Child()
    play_button = Gtk.Template.Child()
    shuffle_button = Gtk.Template.Child()
    artist_label = Gtk.Template.Child()
    click_gesture = Gtk.Template.Child()

    def __init__(self, _item):
        IDisconnectable.__init__(self)
        super().__init__()

        self.item = _item

        self.signals.append((
            self.track_artist_label,
            self.track_artist_label.connect(
                "activate-link", variables.open_uri)))

        if isinstance(_item, Mix):
            self.make_mix()
        elif isinstance(_item, Album):
            self.make_album()
        elif isinstance(_item, Playlist):
            self.make_playlist()
        if isinstance(_item, Artist):
            self.make_artist()
        elif isinstance(_item, Track):
            self.make_track()

        self.signals.append((
            self.click_gesture,
            self.click_gesture.connect("released", self.on_click)))

    def on_click(self, *args):
        if isinstance(self.item, Mix) or isinstance(self.item, MixV2):
            from ..pages import mixPage
            page = mixPage(self.item, f"{self.item.title}")
            page.load()
            variables.navigation_view.push(page)

        elif isinstance(self.item, Album):
            from ..pages import albumPage
            page = albumPage(self.item, f"{self.item.name}")
            page.load()
            variables.navigation_view.push(page)

        elif isinstance(self.item, Playlist):
            from ..pages import playlistPage
            page = playlistPage(self.item, f"{self.item.name}")
            page.load()
            variables.navigation_view.push(page)

        elif isinstance(self.item, Artist):
            from ..pages import artistPage
            page = artistPage(self.item, f"{self.item.name}")
            page.load()
            variables.navigation_view.push(page)

    def make_track(self):
        self.primary_label.set_label(self.item.name)
        self.secondary_label.set_label("Track")

        self.artist_label.set_visible(True)
        self.artist_label.set_artists(self.item.artists)

        self.shuffle_button.set_visible(False)

        self.signals.append((
            self.play_button,
            self.play_button.connect(
                "clicked",
                lambda *args: variables.player_object.play_track(self.item))))

        threading.Thread(
            target=utils.add_image,
            args=(self.image, self.item.album)).start()

    def make_mix(self):
        self.primary_label.set_label(self.item.title)
        self.secondary_label.set_label("Mix")

        self.artist_label.set_visible(True)
        self.artist_label.set_label(self.item.sub_title)

        self.signals.append((
            self.play_button,
            self.play_button.connect(
                "clicked",
                lambda *_: variables.player_object.play_this(self.item))))

        self.signals.append((
            self.play_button,
            self.play_button.connect(
                "clicked",
                lambda *_: variables.player_object.shuffle_this(self.item))))

        threading.Thread(
            target=utils.add_image,
            args=(self.image, self.item)).start()

    def make_album(self):
        self.primary_label.set_label(self.item.name)
        self.secondary_label.set_label("Album")

        self.artist_label.set_visible(True)
        self.artist_label.set_artists([self.item.artist])

        self.signals.append((
            self.play_button,
            self.play_button.connect(
                "clicked",
                lambda *_: variables.player_object.play_this(self.item))))

        self.signals.append((
            self.play_button,
            self.play_button.connect(
                "clicked",
                lambda *_: variables.player_object.shuffle_this(self.item))))

        threading.Thread(
            target=utils.add_image,
            args=(self.image, self.item)).start()

    def make_playlist(self):
        self.primary_label.set_label(self.item.name)
        self.secondary_label.set_visible(False)

        creator = self.item.creator
        if creator:
            creator = creator.name
        else:
            creator = "TIDAL"
        # self.detail_label.set_label(f"by {creator}")

        self.signals.append((
            self.play_button,
            self.play_button.connect(
                "clicked",
                lambda *_: variables.player_object.play_this(self.item))))

        self.signals.append((
            self.play_button,
            self.play_button.connect(
                "clicked",
                lambda *_: variables.player_object.shuffle_this(self.item))))

        threading.Thread(
            target=utils.add_image,
            args=(self.image, self.item)).start()

    def make_artist(self):
        self.primary_label.set_label(self.item.name)
        self.secondary_label.set_label("Artist")

        self.play_button.set_visible(False)
        self.shuffle_button.set_visible(False)

        threading.Thread(
            target=utils.add_image,
            args=(self.image, self.item)).start()

    def __repr__(self, *args):
        return "<HTCardWidget>"
