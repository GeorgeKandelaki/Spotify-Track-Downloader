import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import yt_dlp
import os, sys
from pathlib import Path
from pprint import pprint
import sys

# Playlist Objects keys/properties returned from `playlist_items` method
# href
# items
# limit
# next
# offset
# previous
# total
# playlists = sp.playlist_items(playlist_id=playlist_id, limit=100, offset=100)

client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"

# Authorize with Spotify
auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(auth_manager=auth_manager)

tracks = []
filtered_tracks = []
yt_queries = []
urls = []
path = []


# Function for filtering objects
def filter_obj(obj, keys_to_add):
    buffer_obj = {}

    for key, value in obj.items():
        if key in keys_to_add:
            buffer_obj[key] = value

    return buffer_obj


# Function For building youtube search queries
def build_yt_query(obj):
    track = obj["track"]
    artists = ""
    i = 0
    for artist in obj["artists"]:
        i += 1
        if i > 3:
            break
        artists += f"{artist}, "

    return f"{track} by {artists} audio"


# Function to get data of ONE track
def get_track(id, sp):
    track = sp.track(id=id)
    return None


# iterating/looping till we get all the tracks from the playlist because 100 is the max amount of tracks we can fetch/request
def get_all_tracks(playlist_id, sp):
    all_tracks = []
    offset = 0
    limit = 100

    while True:
        res = sp.playlist_items(playlist_id=playlist_id, offset=offset, limit=limit)
        items = res["items"]
        all_tracks.extend(items)

        if len(items) < limit:
            break

        offset += limit

    return all_tracks


# Download tracks with yt_dlp
def download_track(query, path):
    # yt_dlp Options
    ydl_opts = {
        "format": "bestaudio/best",
        "cookiesfrombrowser": ("chrome", "Default"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": f"{path}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])


# Filter Tracks
def filter_tracks(tracks):
    # Specific to only track Object
    filtered_tracks = []

    for item in tracks:
        track = item["track"]
        if not track:
            continue

        buffer_obj = {"track": "", "artists": []}
        name = filter_obj(track, ["name"]).get("name")
        if name:
            buffer_obj["track"] = name

        for artist in track["artists"]:
            name = filter_obj(artist, ["name"]).get("name")
            if name:
                buffer_obj["artists"].append(name)

        filtered_tracks.append(buffer_obj)

    return filtered_tracks


def loop_over_tracks_to_build_query(tracks):
    yt_queries = []
    for track in tracks:
        yt_queries.append(build_yt_query(track))

    return yt_queries


def loop_over_queries_and_download_tracks(yt_queries, path):
    for i, query in enumerate(yt_queries):
        download_track(query, path)
        print(f"#{i} | {query} has downloaded successfully ✅")


def determine_option_and_execute(option, id=""):
    if option == "--help":
        print(
            """
Free and Easy to use tool, Spotify Downloader is a tool for downloading tracks and playlists from spotify without any complications or inconveniences.

Usage: spotidownload <?options>

Informative options:
    --help                                          Display this help message and the options

General Options:
    --track <?track_id>                             Download one singular track
    --playlist <?playlist_id>                       Download all the track from the playlist

"""
        )
        return None
    elif option == "--track":
        # Feature would be added in later releases
        return None
    elif option == "--playlist":
        tracks = get_all_tracks(id, sp)
        print("Fetching all tracks... ✅")

        filtered_tracks = filter_tracks(tracks)
        print("Filtering the Data for it to be readable... ✅")

        yt_queries = loop_over_tracks_to_build_query(filtered_tracks)
        print("Building the Youtube Queries... ✅")

        print("Downloading Tracks... ✅")
        loop_over_queries_and_download_tracks(yt_queries, path)

        return None
    else:
        raise ValueError("This option wasn't found!")


def main():
    option = sys.argv[1]
    track_playlist_id = ""

    if option != "--help":
        if len(sys.argv) < 4:
            raise ValueError(
                "Playlist/Track URL or Output Path wasn't specified or is invalid!"
            )
        track_playlist_id = sys.argv[2]
        path = sys.argv[3]
    else:
        determine_option_and_execute(option)
        return None

    determine_option_and_execute(option, track_playlist_id)
    return None


if __name__ == "__main__":
    main()
