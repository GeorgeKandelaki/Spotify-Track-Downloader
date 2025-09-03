# 🎵 Spotidownload — Spotify Playlist Downloader CLI Tool

Spotidownload is a free, easy-to-use CLI tool for downloading Spotify playlists. It pulls track metadata from Spotify and downloads high-quality MP3 audio from YouTube using yt-dlp. Fast, no bloat, no BS.

## 🚀 Features

- 🔥 Download any track from spotify (public)
- 🔥 Download all tracks from any Spotify playlist (public)
- 🎧 High-quality MP3 audio (192 kbps)
- 🔎 Automatically builds YouTube search queries using track name and artists
- 🧠 Simple CLI interface — --playlist or --help
- 🔒 Uses Spotify Web API with client credentials (no user login needed)

## 📦 Requirements

- Python 3.7+
- yt-dlp
- Google Chrome installed (used for cookies in yt-dlp)
- Spotify Developer credentials (Client ID & Secret)

## 🔧 Setup

### Install dependencies:

```bash
pip install spotipy yt-dlp
```

### Get Spotify API credentials:

- Go to the Spotify Developer Dashboard and create an app.
- Copy your Client ID and Client Secret and paste them into the script:

```python
client_id = "YOUR_SPOTIFY_CLIENT_ID"
client_secret = "YOUR_SPOTIFY_CLIENT_SECRET"
```

### Run the script:

```bash
python spotidownload.py --playlist <PLAYLIST_ID> <OUTPUT_PATH>
```

### For example:

```bash
python spotidownload.py --playlist 37i9dQZF1DXcBWIGoYBM5M ./downloads
```

## 🛠️ Command-Line Options

```bash
spotidownload.py <?option> <playlist_id> <output_path>

Available Options:
  Option	Descriptions
  --help	Displays help/instructions
  --playlist	Downloads all tracks from a Spotify playlist
  --track	(Coming soon) Downloads a single track from ID
```

## 📁 Output

- Downloads MP3 files to the specified output folder.
- Filenames follow YouTube video titles (cleaned up by yt-dlp).
- Tracks are searched with the format:
  - <track name> by <artist(s)> audio

## ⚙️ How It Works (High-Level)

- Spotify Web API is used to fetch playlist data (max 100 tracks per request, looped until all fetched).
- Tracks are filtered to extract only name and artist(s).
- A YouTube query is built from this info.
- yt-dlp searches YouTube and downloads the best audio match.
- Audio is extracted into MP3 using FFmpeg postprocessing.

## ✅ Example Output

```bash
Fetching all tracks... ✅
Filtering the Data for it to be readable... ✅
Building the Youtube Queries... ✅
Downloading Tracks... ✅
#0 | Blinding Lights by The Weeknd audio has downloaded successfully ✅
#1 | Starboy by The Weeknd, Daft Punk audio has downloaded successfully ✅
```

## 🧠 Notes

- Currently only supports public Spotify playlists.
- YouTube matches aren't 100% accurate, but close in most cases.

## 🔓 License

This project is free and open-source. Use responsibly — this is for educational purposes only.

## 💡 TODO

- Improve filename handling
- Add album support
- GUI version?

## Improvements (Release 1.2.0.0)

- In this updated version we have added support to download single track. Now --track option works.
- Some Code improvements. Improved DRY Principle, made Code more reusable, encapsulated some filtering processes in functions, Code is cleaner and more readable
- A lot of buggy and bad Code has been removed and rewritten with better, clean and safe Code.
- Improved Error Handling.
- Added features to specify offset.
- Also added options for users to specify their own client secret and id.
