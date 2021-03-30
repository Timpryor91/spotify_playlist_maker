# -*- coding: utf-8 -*-
"""

@author: timpr
"""

from classes.song_class import Song
from datetime import datetime
from datetime import timedelta
import random as rand

class Artist(object):
    """
    A spotify artist object.

    """
    def __init__(self, artist_name, artist_uri, artist_id_num, last_played, sp, played_songs_df):
        """
        Initialize a playlist object
        
        Parameters:
            artist_name (string): the name of the artist
            artist_uri (string): the Spotify uri of the artist
            artist_id_num (int): the id number of the artist from the artist dataframe
            last_played (datetime): the last time a song from the artist was included in a playlist
            sp (Authorization token object): an authorization that allows user to write playlists to Spotify
            played_song_df (Pandas DataFrame):a dataframe with details of songs that have been included in playlists previously
            
        """
        self.artist_name = artist_name
        self.artist_uri = artist_uri
        self.artist_id_num = artist_id_num
        self.last_played = last_played
        self.sp = sp
        self.played_songs_df = played_songs_df
        
    def get_artist_name(self):
        return (self.artist_name)
    
    def get_artist_uri(self):
        return (self.artist_uri)

    def get_artist_id_num(self):
        return (self.artist_id_num)
    
    def get_last_played(self):
        return (self.last_played)
    
    def update_last_played(self, last_played):
        self.last_played = last_played
        return
    
    def get_artist_songs(self):
        """
        Gets a list of all the songs created by the artist
        
        Parameters:
            None
            
        Returns:
            artist_songs (List<Song>): a list of song objects, created by the artist
            
        """ 
        
        self.artist_albums = self.sp.artist_albums(self.artist_uri, album_type = "album")
        self.album_uris = []
    
        for i in range(len(self.artist_albums["items"])):
            self.album_uris.append(self.artist_albums["items"][i]["uri"])
        
        self.artist_songs = []
                
        for uri in self.album_uris:
            self.album_tracks = self.sp.album_tracks(uri)
            
            for i in range(len(self.album_tracks["items"])):
                self.track_name = self.album_tracks["items"][i]["name"]
                self.track_uri = self.album_tracks["items"][i]["uri"]
                self.artist_songs.append(Song(self.track_name,
                                              self.track_uri,
                                              self.sp))
        return (self.artist_songs)

    def pick_artist_song(self):
        """
        Picks a song by the artist to include in the playlist
        
        Parameters:
            None
            
        Returns:
            artist_playlist_song (Song): a song by the artist to be added to the playlist
            
        """ 
        self.artist_songs = self.get_artist_songs()
        self.artist_playlist_song = 0
        
        # Check if there are any new releases by the artist (music from the past 12 weeks)
        self.new_release_songs = []
        self.song_popularity_dict = {}
        
        # Copy song list for iteration purposes
        self.artist_songs_copy = self.artist_songs.copy()
        for song in self.artist_songs.copy():
            # Check to see if song has already been included in a playlist before
            self.played_song = self.played_songs_df["played_song_uri"].str.\
                                   contains(song.get_song_uri()).any()
            if self.played_song == True:
                self.artist_songs.remove(song)
                continue
            
            self.song_popularity_dict[song] = song.get_popularity()
            if song.get_release_date() > (datetime.today() - timedelta(weeks=12)):
                self.new_release_songs.append(song)
        
        # If there are, choose the most popular new release song
        if len(self.new_release_songs) > 0:            
            self.most_popular_score = 0
            for song in self.new_release_songs:
                if self.song_popularity_dict[song] > self.most_popular_score:
                    self.most_popular_score = self.song_popularity_dict[song]
                    self.artist_playlist_song = song
            return(self.artist_playlist_song)
        
        # If there are no new release songs, create shortlist of top 10% most popular songs
        self.sorted_popularity_list = sorted(self.song_popularity_dict.items(), 
                                             key=lambda item: item[1], reverse = True)
        self.cutoff_index = max(int(0.1*len(self.sorted_popularity_list)),1)
        self.sorted_popularity_list = self.sorted_popularity_list[:self.cutoff_index]
        
        # Randomly select a song from the shortlist
        self.artist_playlist_song = rand.choice(self.sorted_popularity_list)[0]

        return(self.artist_playlist_song)            
