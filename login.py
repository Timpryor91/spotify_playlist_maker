# -*- coding: utf-8 -*-
"""

@author: timpr
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def spotify_login():
    """
    Logs in to user's spotify acccount
    
    Returns:
        sp (Authorization): authorization object to allow writing to user's playlist
        
    """
    ##### Update these to include your own client ID and client secret
    SPOTIPY_CLIENT_ID = "ENTER YOUR CLIENT ID HERE"
    SPOTIPY_CLIENT_SECRET= "ENTER YOUR CLIENT SECRET HERE"
    SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
    
    SCOPE = 'playlist-modify-public'
    CACHE = '.spotipyoauthcache'
    
    sp = spotipy.Spotify(auth_manager = SpotifyOAuth(SPOTIPY_CLIENT_ID, 
                                                     SPOTIPY_CLIENT_SECRET,
                                                     SPOTIPY_REDIRECT_URI,
                                                     scope=SCOPE,
                                                     cache_path=CACHE))         
    return(sp)