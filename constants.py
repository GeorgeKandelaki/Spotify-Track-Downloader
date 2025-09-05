import os

HELP_STR = """
Free and Easy to use tool, Spotify Downloader is a tool for downloading tracks and playlists from spotify without any complications or inconveniences.

Usage: spotidownload <?options> <?path>

Informative options:
    --help                                          Display this help message and the options

General Options:
    --track <?track_id>                             Download one singular track
    --playlist <?playlist_id>                       Download all the track from the playlist
    --path <?download_dir>                          Specifying Path/Dir/Route for storing/saving tracks | DEFAULT CURRENT DIR
    --offset <?index>                               From which index of the playlist to download | DEFAULT 0
    --client_id <?client_id>                        Spotify's client ID | NECESSARY 
    --client_secret <?client_secret>                Spotify's client secret | NECESSARY
    --save_credentials                              Save the client secret and id 
"""
USER_HOME = os.path.expanduser("~")
CONFIG_FILE_NAME = "spotidownload"
BASE_CONFIG_PATH = f"{USER_HOME}/.config"
CONFIG_DIR = f"{USER_HOME}/spotidownload"
CONFIG_PATH = f"{BASE_CONFIG_PATH}/spotidownload/{CONFIG_FILE_NAME}.py"
