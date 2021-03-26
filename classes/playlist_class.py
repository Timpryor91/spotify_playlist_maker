# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import random as rand
from classes.artist_class import Artist
from datetime import datetime, timedelta
import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText

class Playlist(object):
    """
    A spotify playlist, created once a week, containing 10 songs by different artists

    """
    def __init__(self, artist_df, playlist_name, playlist_length, sp, played_songs_df):
        """
        Initialize a playlist object
        
        Parameters:
            artist_df (Pandas DataFrame): a dataframe with details of artists that playlist will be constructed from
            playlist_name (string): the name of the playlist, which will appear in Spotify
            playlist_length (int): the number of songs to be populated into the playlist
            sp (Authorization token object): an authorization that allows user to write playlists to Spotify
            played_song_df (Pandas DataFrame):a dataframe with details of songs that have been included in playlists previously
        
        """
        self.artist_df = artist_df
        self.playlist_name = playlist_name
        self.playlist_length = playlist_length
        self.sp = sp
        self.played_songs_df = played_songs_df
        self.user_id = self.sp.me()["id"]
        
        # Extract a list of played songs from the played songs dataframe
        self.played_songs_df = played_songs_df
        self.played_song_uri_list = []
        #TO DO
        
        # Create a new playlist in user's spotify account
        self.playlist_json = self.sp.user_playlist_create(self.user_id, self.playlist_name)
        self.playlist_uri = self.playlist_json["uri"]
        
    def get_playlist_artists(self):
        """
        Chooses the unique artists to include in the playlist
        
        Parameters:
            None
        
        Return:
            playlist_artists (List<Artist>): A list of artists, equal in length to the playlist_length
        """
        self.num_artists = len(self.artist_df.index)
        self.playlist_artists = []
        self.playlist_artist_ids = []
        
        while len(self.playlist_artists) < self.playlist_length:
            self.artist_id = rand.randint(0, self.num_artists-1)
            
            self.artist = Artist(self.artist_df.iloc[self.artist_id]["artist_name"],
                                 self.artist_df.iloc[self.artist_id]["artist_uri"],
                                 self.artist_id,
                                 datetime.strptime(self.artist_df.iloc[self.artist_id]["last_played_date"],"%d/%m/%Y"),
                                 self.sp,
                                 self.played_songs_df)
            
            # Check to ensure proposed artist isn't already in this week's playlist
            # and hasn't been included in a recent playlist
            if self.artist.get_artist_id_num() not in self.playlist_artist_ids:
                if self.artist.get_last_played() < (datetime.today() - timedelta(weeks=12)):
                    self.playlist_artists.append(self.artist)
                    self.playlist_artist_ids.append(self.artist_id)
                
        return(self.playlist_artists)

    def add_playlist_songs(self):
        """
        Adds a song to the Spotify playlist for each of the chosen artists
        
        Parameters:
            None
        
        Return:
            playlist_songs (List<Songs>): a list of songs that are included in the playlist
        """
        self.artists = self.get_playlist_artists()
        self.playlist_songs = []
        
        for artist in self.artists:
            # Add artist song to Spotify playlist
            self.artist_song = artist.pick_artist_song()
            self.sp.playlist_add_items(self.playlist_uri, [self.artist_song.get_song_uri()])
            self.playlist_songs.append(self.artist_song)

        return(self.playlist_songs)        
    
    def update_played_songs_df(self, playlist_songs):
        """
        Adds the current playlists songs to the playlist songs dataframe
        
        Parameters:
            playlist_songs (List<Songs>): a list of songs that are included in the playlist
        
        Return:
            None
        """
        for song in playlist_songs:
            self.song_df = pd.DataFrame({"played_song_name": [song.get_song_name()], 
                                         "played_song_uri": [song.get_song_uri()]}) 
            
            self.song_df.to_csv("played_songs.csv", mode = "a", header = False)
        
        return
    
    def send_playlist_email(self, email_address):
        """
        Sends a link for the new playlist to nominated email addresses
        
        Parameters:
            email_address (string): an email addresses that playlist info will be sent to
        
        Return:
            None
        """
        self.port = 587
        self.smtp_server = 'smtp.gmail.com'
        self.sender_email ="ENTER SENDER EMAIL ADDRESS HERE"
        self.receiver_email = email_address
        self.password ="ENTER SENDER EMAIL PASSWORD HERE"
        
        # Email content to send to Tim
        self.text = "\
        Hi Jackie\n\
        Here is a uri for this week's playlist:\n\
        " + self.playlist_uri
                
        self.message = MIMEText(self.text, "plain")
        self.message["Subject"] = "Weekly Spotify Playlist"
        self.message["From"] = self.sender_email
        self.message["To"] = self.receiver_email
        
        # Create secure connection with server and send email
        self.context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, 465, context=self.context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, self.message.as_string())
       
        return