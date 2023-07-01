import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import dotenv_values

config = dotenv_values("../.env")


def get_artist_id(spotify, artist_name, market="US"):
    results = spotify.search(
        artist_name, limit=1, offset=0, type="artist", market=market
    )

    for artist in results["artists"]["items"]:
        artist_id = artist["id"]
        break

    return artist_id


def get_artist_top_tracks_ids(spotify, artist_id):
    top_tracks = spotify.artist_top_tracks(artist_id)

    return [track["id"] for track in top_tracks["tracks"]]


def add_tracks_to_playlist(spotify, playlist_id, track_ids):
    return spotify.playlist_add_items(playlist_id, track_ids)


if __name__ == "__main__":
    spotify_client_id = config["SPOTIFY_CLIENT_ID"]
    spotify_client_secret = config["SPOTIFY_CLIENT_SECRET"]
    callback_url = config["SPOTIFY_CALLBACK_URL"]
    scope = "playlist-modify-public"
    playlist_id = config["SPOTIFY_PLAYLIST_ID"]

    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri=callback_url,
        )
    )

    # get list of artists from file
    with open("../artists.json", "r") as f:
        artists = json.load(f)["artists"]

    for artist in artists:
        add_tracks_to_playlist(
            spotify,
            playlist_id,
            get_artist_top_tracks_ids(spotify, get_artist_id(spotify, artist)),
        )
