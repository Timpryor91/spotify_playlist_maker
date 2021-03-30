# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import pandas as pd
from datetime import date
from classes.playlist_class import Playlist
from login import spotify_login

if __name__ == "__main__":
    
    # Obtain authentication token for user's Spotify account
    sp = spotify_login()
    
    # Read in dataframe of recently played artists and songs that have been
    # included in playlists previously
    artists_df = pd.read_csv("artist_data.csv")
    played_songs_df = pd.read_csv("played_songs.csv")
    
    # Playlist parameters, can be modified to suit user preferences
    playlist_name = "Tim's Playlist " + date.today().strftime("%d/%m/%Y")
    playlist_length = 10
    
    # Initiate new playlist object
    playlist = Playlist(artists_df, playlist_name, playlist_length, sp, played_songs_df)
    
    # Randomly select artists to include in the weekly playlist, and add one song per artist
    playlist_songs = playlist.add_playlist_songs()
    
    # Update the played songs register
    playlist.update_played_songs_df(playlist_songs)
    
    # Send playlist link email
    playlist.send_playlist_email("jackiehwang92@gmail.com")