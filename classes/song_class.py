# -*- coding: utf-8 -*-
"""

@author: timpr
"""
from datetime import datetime

class Song(object):
    """
    A spotify song object.

    """
    def __init__(self, song_name, song_uri, sp):
        """
        Initialize a song object
        
        Parameters:
            song_name (string): the name of the song
            album_name (string): the name of the album the song is on
            song_uri (string): the Spotify uri of the song
            sp (Authorization token object): an authorization that allows user to write playlists to Spotify
            
        """
        self.song_name = song_name
        self.song_uri = song_uri
        self.sp = sp
        
        # Look up song release date and popularity score upon initialization of song object
        self.track_details = self.sp.track(self.song_uri)
        self.popularity = self.track_details["popularity"]
        self.release_date_precision = self.track_details["album"]["release_date_precision"]
        if self.release_date_precision == "year":
            self.date_format = "%Y"
        elif self.release_date_precision =="month":
            self.date_format = "%m/%Y"
        elif self.release_date_precision == "day":
            self.date_format = "%Y-%m-%d"
        else:
            raise Exception("release date precision format differs from expected values")
        
        self.release_date = datetime.strptime(self.track_details["album"]["release_date"], self.date_format)

        
    def get_song_name(self):
        return (self.song_name)
    
    def get_song_uri(self):
        return (self.song_uri)

    def get_release_date(self):
        return (self.release_date)
    
    def get_popularity(self):
        return (self.popularity)