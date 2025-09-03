import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import os, sys
from pathlib import Path
from pprint import pprint
import sys


from utils import filter_obj, filtering_track_process, convert_arr_into_obj

# Playlist Objects keys/properties returned from `playlist_items` method
# href
# items
# limit
# next
# offset
# previous
# total


client_id = ""
client_secret = ""
sp = {}


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
def get_track(track_id, sp):
    track = sp.track(track_id)

    return track


# iterating/looping till we get all the tracks from the playlist because 100 is the max amount of tracks we can fetch/request
def get_all_tracks(
    playlist_id,
    sp,
    offset=0,
):
    all_tracks = []
    limit = 100
    total = 0

    while True:
        res = sp.playlist_items(playlist_id=playlist_id, offset=offset, limit=limit)

        items = res["items"]
        all_tracks.extend(items)

        if len(items) < limit:
            break

        offset += limit

    return {"tracks": all_tracks, "total_tracks": res["total"]}


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
def filter_tracks(tracks, download_type="playlist"):
    # Specific to only track Object
    filtered_tracks = []

    if download_type == "playlist":
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

    if download_type == "track":
        track = tracks[0]
        buffer_obj = {"track": "", "artists": []}
        name = filter_obj(track, ["name"]).get("name")

        if name:
            buffer_obj["track"] = name

        for artist in track["artists"]:
            name = filter_obj(artist, ["name"]).get("name")
            if name:
                buffer_obj["artists"].append(name)

        return buffer_obj

    return None


def loop_over_tracks_to_build_query(tracks):
    yt_queries = []
    for track in tracks:
        yt_queries.append(build_yt_query(track))

    return yt_queries


def loop_over_queries_and_download_tracks(yt_queries, path="./"):
    for i, query in enumerate(yt_queries):
        download_track(query, path)
        print(f"#{i} | {query} has downloaded successfully ✅")


def determine_option_and_execute(options):
    path = "./"
    offset = 0

    if "--help" in options:
        print(
            """
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

"""
        )

        return None

    if "--client_id" not in options and "--client_secret" not in options:
        raise ValueError("You have to specify client secret and id to download tracks!")
    else:
        client_id = options["--client_id"]
        client_secret = options["--client_secret"]

        # Authorize with Spotify
        auth_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret
        )

        sp = spotipy.Spotify(auth_manager=auth_manager)

    if "--path" in options:
        path = options["--path"]

    if "--offset" in options:
        offset = int(options["--offset"])

    if "--track" in options:
        track_id = options["--track"]

        track = get_track(track_id, sp)

        if not track:
            raise ValueError("We couldn't find the track :(")

        print("Fetching the track... ✅")

        filtered_track = filter_tracks([track], "track")
        print("Filtering the Data for it to be readable... ✅")
        print(filtered_track)

        yt_query = build_yt_query(filtered_track)
        print("Building the Youtube Query... ✅")

        print("Downloading Track... ✅")
        download_track(yt_query, path)

        return None

    if "--playlist" in options:
        playlist_id = options["--playlist"]

        tracks_obj = get_all_tracks(playlist_id, sp, offset)

        if tracks_obj["total_tracks"]:
            raise ValueError(
                "".join(
                    [
                        "Total songs were ",
                        str(tracks_obj["total_tracks"]),
                        ", lower the offset option.",
                    ]
                )
            )

        else:
            raise ValueError("Playlist couldn't be found :(")

        print("Fetching all tracks... ✅")

        filtered_tracks = filter_tracks(tracks_obj["tracks"])
        print("Filtering the Data for it to be readable... ✅")

        yt_queries = loop_over_tracks_to_build_query(filtered_tracks)
        print("Building the Youtube Queries... ✅")

        print("Downloading Tracks... ✅")
        loop_over_queries_and_download_tracks(yt_queries, path)

        return None

    raise ValueError("This option wasn't found!")


def main():
    namespace, *options_arr = sys.argv
    # print(namespace, "\n", options_arr)

    options = convert_arr_into_obj(options_arr)
    # print(options)

    if len(options_arr) == 1:
        options["--help"] = None

    # print(sys.argv) OUTPUT <- ['spotidownload.py', '--playlist', '17kf5gMvi1Pm5A0B6NO0t1', './musics']

    determine_option_and_execute(options)
    return None


if __name__ == "__main__":
    main()
