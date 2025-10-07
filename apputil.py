# apputil.py
import requests
import pandas as pd

class Genius:
    """Simple wrapper around the Genius API."""

    def __init__(self, access_token: str):
        if not isinstance(access_token, str) or not access_token.strip():
            raise ValueError("Access token must be a non-empty string")
        self.access_token = access_token.strip()
        self.base_url = "https://api.genius.com"

    def _get_headers(self):
        """Return authorization headers for Genius API requests."""
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_artist(self, search_term: str) -> dict:
        """Search Genius for an artist and return their information."""
        search_url = f"{self.base_url}/search"
        response = requests.get(search_url, headers=self._get_headers(), params={"q": search_term}, timeout=20)
        data = response.json()

        try:
            artist_id = data["response"]["hits"][0]["result"]["primary_artist"]["id"]
        except (KeyError, IndexError):
            raise ValueError(f"No artist found for search term '{search_term}'")

        artist_url = f"{self.base_url}/artists/{artist_id}"
        artist_response = requests.get(artist_url, headers=self._get_headers(), timeout=20)
        return artist_response.json()

    def get_artists(self, search_terms: list) -> pd.DataFrame:
        """Return a DataFrame with artist info for multiple search terms."""
        records = []
        for term in search_terms:
            try:
                data = self.get_artist(term)
                artist = data["response"]["artist"]
                records.append({
                    "search_term": term,
                    "artist_name": artist.get("name"),
                    "artist_id": artist.get("id"),
                    "followers_count": artist.get("followers_count")
                })
            except Exception:
                records.append({
                    "search_term": term,
                    "artist_name": None,
                    "artist_id": None,
                    "followers_count": None
                })
        return pd.DataFrame(records)
