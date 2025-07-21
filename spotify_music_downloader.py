import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import yt_dlp
import json
import os, sys
from pathlib import Path
from pprint import pprint


client_id = "42092746c07640b8a02ec0080a39fdd8"
client_secret = "0bfd04cde7624ecd8ce3634c9cb2b596"
playlist_id = "14EEcrqWlztbH4hKn9c635"

# Authorize with Spotify
auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Get the Playlist

tracks = []
filtered_tracks = []
yt_queries = []
urls = []


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
    artist = obj["artists"][0]
    return f"{track} by {artist} audio"


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
def download_track(query):
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
        "outtmpl": "/home/matrix/music/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])


def filter_tracks(track):
    return None


# Playlist Objects keys/properties returned from `playlist_items` method
# href
# items
# limit
# next
# offset
# previous
# total
# playlists = sp.playlist_items(playlist_id=playlist_id, limit=100, offset=100)

# Filter Tracks
tracks = get_all_tracks(playlist_id, sp)
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

for track in filtered_tracks:
    yt_queries.append(build_yt_query(track))


for i, query in enumerate(yt_queries):
    download_track(query)
    print(f"#{i} | {query} has downloaded successfully ✅")
