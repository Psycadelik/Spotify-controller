import os
import json
from unittest import mock, TestCase
from src.controller import (
    get_artist_id,
    get_artist_top_tracks_ids,
    add_tracks_to_playlist,
)


class ControllerTest(TestCase):
    def setUp(self):
        self.spotify = mock.Mock()

        with open(
            os.path.join(os.path.dirname(__file__), "artist_top_tracks.json")
        ) as fp:
            self.top_tracks = json.load(fp)
            self.top_tracks_ids = [track["id"] for track in self.top_tracks["tracks"]]

    def test_get_artist_id(self):
        self.spotify.search.return_value = {
            "artists": {
                "href": "https://api.spotify.com/v1/search?query=weezer&type=artist&market=US&offset=0&limit=1",
                "items": [
                    {
                        "external_urls": {
                            "spotify": "https://open.spotify.com/artist/3jOstUTkEu2JkjvRdBA5Gu"
                        },
                        "followers": {"href": None, "total": 3120448},
                        "genres": [
                            "alternative rock",
                            "modern power pop",
                            "modern rock",
                            "permanent wave",
                            "rock",
                        ],
                        "href": "https://api.spotify.com/v1/artists/3jOstUTkEu2JkjvRdBA5Gu",
                        "id": "3jOstUTkEu2JkjvRdBA5Gu",
                        "images": [
                            {
                                "height": 640,
                                "url": "https://i.scdn.co/image/ab6761610000e5eb878154b813440af37fb3d64d",
                                "width": 640,
                            },
                            {
                                "height": 320,
                                "url": "https://i.scdn.co/image/ab67616100005174878154b813440af37fb3d64d",
                                "width": 320,
                            },
                            {
                                "height": 160,
                                "url": "https://i.scdn.co/image/ab6761610000f178878154b813440af37fb3d64d",
                                "width": 160,
                            },
                        ],
                        "name": "Weezer",
                        "popularity": 73,
                        "type": "artist",
                        "uri": "spotify:artist:3jOstUTkEu2JkjvRdBA5Gu",
                    }
                ],
                "limit": 1,
                "next": "https://api.spotify.com/v1/search?query=weezer&type=artist&market=US&offset=1&limit=1",
                "offset": 0,
                "previous": None,
                "total": 199,
            }
        }

        for item in self.spotify.search()["artists"]["items"]:
            artist_id = item["id"]

        actual = get_artist_id(self.spotify, "weezer")
        self.assertEqual(actual, artist_id)

    def test_get_artist_top_tracks_ids(self):
        self.spotify.artist_top_tracks.return_value = self.top_tracks

        artist_id = "some-random-artist-id"
        actual = get_artist_top_tracks_ids(self.spotify, artist_id)
        self.assertEqual(actual, self.top_tracks_ids)

    def test_add_tracks_to_playlist(self):
        self.spotify.playlist_add_items.return_value = {
            "snapshot_id": "NCw5N2RjZWIzYmJmY2RiMDRmNDUxN2RkNDBjZDIwYzcxYzYxZDNjN2Vi"
        }
        playlist_id = "some-random-playlist-id"
        actual = add_tracks_to_playlist(self.spotify, playlist_id, self.top_tracks_ids)
        self.assertEqual(
            actual,
            {"snapshot_id": "NCw5N2RjZWIzYmJmY2RiMDRmNDUxN2RkNDBjZDIwYzcxYzYxZDNjN2Vi"},
        )
